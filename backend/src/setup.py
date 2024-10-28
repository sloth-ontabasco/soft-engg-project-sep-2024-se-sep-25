from datetime import datetime
from urllib.parse import unquote

from flask import Flask, request
from flask_limiter import RateLimitExceeded
from flask_login import LoginManager

from src.api.auth import *


def setup_auth(app: Flask):
    login_manager = LoginManager(app=app)
    login_manager.session_protection = "strong"

    # @app.before_request
    # def request_interceptor():
    #     try:
    #         if request.path not in [
    #             "/api/hello",
    #             "/api/auth/login",
    #             "/api/auth/login/callbacks",
    #         ]:
    #             user = User.get_user_from_request(request)
    #             if user:
    #                 app.logger.debug(f"{datetime.utcnow()} - {request.path} - {user.id}:{user.username}")
    #         else:
    #             app.logger.debug(f"{datetime.utcnow()} - {request.path}")

    #     except Exception as e:
    #         app.logger.error(e.__str__())
    #         pass

    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, RateLimitExceeded):
            return Response.error(code=429, message="Rate Limit Exceeded.")
        app.log_exception(e)
        return Response.error()

    @app.get("/api/hello")
    def hello_world():
        """
        This function serves two purpose:
        1. To check if API server is working. (kind of like a ping command)
        2. Template for how all API endpoints should be made.
        """
        try:
            app.logger.info("Ping!!!")
            return Response.success(200, "Hello World")
        except Exception as e:
            raise e

    @login_manager.user_loader
    def load_user(email_id):
        """
        Loading user into session from DB. (For admin API endpoints)
        """
        u = User(email=email_id) 
        if not u:
            return None
        return u

    @app.errorhandler(404)
    def page_not_found(error):
        return Response.error(404, message="Not Found")


def setup_api(app, api):
    api.add_resource(LoginAPI, "/api/auth/<string:provider>/login")
    api.add_resource(CallbackAPI, "/api/auth/login/<string:provider>/callback",endpoint='oauth2_callback')
    api.add_resource(LogoutAPI, "/api/auth/logout")


def list_routes(app: Flask):

    output = []
    for rule in app.url_map.iter_rules():
        assert rule.methods
        methods = ",".join(rule.methods)
        line = unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, rule))
        output.append(line)

    for line in sorted(output):
        app.logger.warning(line)
