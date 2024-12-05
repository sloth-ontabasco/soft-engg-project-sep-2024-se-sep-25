from datetime import datetime
from urllib.parse import unquote

from flask import Flask, request
from flask_limiter import RateLimitExceeded
from flask_jwt_extended import JWTManager
from src.api.auth import *
from src.api.users import *
from src.api.teams import *
from src.api.announcements import *
from src.api.feedbacks import *
from src.api.project import *
from src.api.milestone import *
from src.api.resource import *
from src.api.submission import MilestoneSubmissionAPI  # Import the API resource
from src.api.analytics import *
from src.api.github import *


def setup_auth(app: Flask):
 
    jwt = JWTManager(app)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        u = User.objects(email=identity).first()
        if not u:
            return None
        return u

    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, RateLimitExceeded):
            return Response.error(code=429, message="Rate Limit Exceeded.")
        app.log_exception(e)
        return Response.error()

    @app.get("/api/hello")
    def hello_world():
        """
        ping pong
        """
        try:
            app.logger.info("Ping!!!")
            return Response.success(200, "Hello World")
        except Exception as e:
            raise e

    @app.errorhandler(404)
    def page_not_found(error):
        return Response.error(404, message="Not Found")



def setup_api(app, api):
    # Authentication Routes
    api.add_resource(LoginAPI, "/api/<string:provider>/login")
    api.add_resource(CallbackAPI, "/api/<string:provider>/callback",endpoint='oauth2_callback')
    api.add_resource(TokenAPI,"/api/token")

    # User Routes
    api.add_resource(UserAPI,
                     "/api/users",
                     "/api/users/<string:user_id>")
    
    # Team Routes
    api.add_resource(TeamAPI, 
                     "/api/<string:project_id>/teams",
                     "/api/<string:project_id>/teams/<string:team_id>")

    # Announcement Routes
    api.add_resource(AnnouncementAPI, 
                     "/api/projects/<string:project_id>/announcements", 
                     "/api/projects/<string:project_id>/announcements/<string:id>")

    # Feedback Routes
    api.add_resource(FeedbackAPI, 
                     "/api/projects/<string:project_id>/milestones/<string:milestone_id>/submissions/<string:milestone_submission_id>/feedbacks",
                     "/api/projects/<string:project_id>/milestones/<string:milestone_id>/submissions/<string:milestone_submission_id>/feedbacks/<string:id>")

    # Project Routes
    api.add_resource(ProjectAPI,"/api/project")
    api.add_resource(ProjectsByUserAPI, '/api/project/user/<string:user_id>')
    api.add_resource(ProjectByIdAPI, '/api/project/<string:project_id>')


    # Milestone Routes 
    api.add_resource(MilestoneAPI, '/api/milestones/<string:milestone_id>')
    api.add_resource(ProjectMilestonesAPI,"/api/project/milestones/<project_id>")
    api.add_resource(EditDeleteMilestoneAPI, '/api/milestones/<string:project_id>/<string:milestone_id>')

    # Milestone Submission Routes
    api.add_resource(MilestoneSubmissionAPI, "/api/submission", "/api/submission/<string:submission_id>")
    
    # Resource Routes
    api.add_resource(ProjectResourcesAPI, '/api/resource/<string:project_id>','/api/resource/<string:project_id>/<string:resource_id>')

    # Analytics Routes
    api.add_resource(ProjectAnalyticsAPI, '/api/<string:project_id>/analytics')

    api.add_resource(CreateGithubIntegrationAPI, '/api/github/integration')
    api.add_resource(GetRepoCommitsAPI, '/api/github/commits')
    


def list_routes(app: Flask):

    output = []
    for rule in app.url_map.iter_rules():
        assert rule.methods
        methods = ",".join(rule.methods)
        line = unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, rule))
        output.append(line)

    for line in sorted(output):
        app.logger.warning(line)
