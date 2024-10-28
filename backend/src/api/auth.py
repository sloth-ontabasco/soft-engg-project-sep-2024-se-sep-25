import secrets
import time
from urllib.parse import urlencode

import requests
from flask import make_response, redirect, request, session, url_for
from flask_login import current_user, login_user, logout_user
from flask_restful import Resource, Api

from ..config import *
from ..models.response import Response
from ..models.user import User, UserType

from ..lib.auth import login_required
from ..lib.jwt_handler import decode, encode
from ..db import db 

class UserAPI(Resource):
    """
    Route: /api/users/@me
    """

    @login_required
    def get(self):
        try:
            user_data = User.get_user_from_request(request)
            return Response.success(user_data=user_data.to_dict())
        except Exception as e:
            raise e


class LoginAPI(Resource):
    """
    Route: /api/auth/<str:provider>/login
    """

    def get(self,provider):
        """
        Login endpoint, redirects to provider OAuth.
        """
        provider_data = OAUTH2_PROVIDERS.get(provider)
        if provider_data is None:
            return Response.error(404)

        # generate a random string for the state parameter
        session['oauth2_state'] = secrets.token_urlsafe(16)

        # create a query string with all the OAuth2 parameters
        qs = urlencode({
            'client_id': provider_data['client_id'],
            'redirect_uri': url_for('oauth2_callback', provider=provider,
                                    _external=True),
            'response_type': 'code',
            'scope': ' '.join(provider_data['scopes']),
            'state': session['oauth2_state'],
        })

        # redirect the user to the OAuth2 provider authorization URL
        return redirect(provider_data['authorize_url'] + '?' + qs)


class CallbackAPI(Resource):
    """
    Route: /api/auth/login/<str:provider>/callback
    """

    def get(self,provider):
        """
        Route: /api/auth/login/<str:provider>/callback
        Callback endpoint that gets hit after discord OAuth.
        """
        print('callback provider', provider)
        provider_data = OAUTH2_PROVIDERS.get(provider)
        if provider_data is None:
            return Response.error(404)

        # if there was an authentication error, flash the error messages and exit
        if 'error' in request.args:
            for k, v in request.args.items():
                if k.startswith('error'):
                    return Response.error(code=400,message=f'{k}: {v}')
            return redirect(FRONTEND_URI)

        # make sure that the state parameter matches the one we created in the
        # authorization request
        if request.args['state'] != session.get('oauth2_state'):
            return Response.error(401)

        # make sure that the authorization code is present
        if 'code' not in request.args:
            return Response.error(401)

        # exchange the authorization code for an access token
        response = requests.post(provider_data['token_url'], data={
            'client_id': provider_data['client_id'],
            'client_secret': provider_data['client_secret'],
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': url_for('oauth2_callback', provider=provider,
                                    _external=True),
        }, headers={'Accept': 'application/json'})

        if response.status_code != 200:
            return Response.error(401)
        oauth2_token = response.json().get('access_token')
        if not oauth2_token:
            return Response.error(401)

        # use the access token to get the user's email address
        response = requests.get(provider_data['userinfo']['url'], headers={
            'Authorization': 'Bearer ' + oauth2_token,
            'Accept': 'application/json',
        })
        if response.status_code != 200:
            return Response.error(401)
        email = provider_data['userinfo']['email'](response.json())

        # find or create the user in the database
        user =  User.objects(email=email, ).first()
        print(user)
        if user is None:
            user = User(email=email, nickname=email.split('@')[0])
            user.save()

        # log the user in
        login_user(user)
        return redirect('https://google.com')


class LogoutAPI(Resource):
    """
    Route: /api/auth/logout
    """

    @login_required
    def get(self):
        """
        Logout an user.
        """
        try:
            res = make_response(redirect(src.config.FRONTEND_URI))  # type: ignore
            try:
                if isinstance(current_user, User) and current_user.id:
                    logout_user()
                    res.status_code = 200
            except AttributeError as ae:
                if request.cookies.get("token"):
                    res.delete_cookie("token")
                    res.status_code = 200
            return res

        except Exception as e:
            raise e
