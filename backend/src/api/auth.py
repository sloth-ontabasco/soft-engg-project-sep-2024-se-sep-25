import secrets
import time
from urllib.parse import urlencode

import requests
from flask_cors import cross_origin
from flask import make_response, redirect, request, session, url_for
from flask_login import current_user
import datetime
from flask_restful import Resource, Api
from flask_jwt_extended import create_access_token, jwt_required, current_user

from ..config import *
from ..models.response import Response
from ..models.user import User


class LoginAPI(Resource):
    """
    Route: /api/<str:provider>/login
    """

    def get(self, provider):
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
    Route: /api/<str:provider>/callback
    """

    def get(self, provider):
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
                    return Response.error(code=400, message=f'{k}: {v}')
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
        
        # print(response.json())

        
        # use the access token to get the user's email address
        response = requests.get(provider_data['userinfo']['url'], headers={
            'Authorization': 'Bearer ' + oauth2_token,
            'Accept': 'application/json',
        })

        user_info = response.json()
        print(user_info)
        print("--------------------------------------------------------")

        if response.status_code != 200:
            return Response.error(401)
        
        # Fetch repositories
        if provider == 'github':
            repos_url = 'https://api.github.com/user/repos'
            repos_response = requests.get(repos_url, headers={
                'Authorization': f'token {oauth2_token}',
                'Accept': 'application/json'
            })

            print(repos_response.json())
            print("--------------------------------------------------------")

            if repos_response.status_code != 200:
                return Response.error(code=repos_response.status_code, message="Failed to fetch repositories")

            repos = repos_response.json()
            if not repos:
                return Response.error(code=404, message="No repositories found")

            # list of repos with url
            repo_list = [{repo['full_name']: repo['html_url']} for repo in repos]
            # endcoded repo list query string
            rqs = urlencode({"repos": repo_list})
            
            
            # Save the OAuth2 token
            session['oauth2_token'] = oauth2_token #save in db
            # return repo_list
            return redirect(FRONTEND_URI + '?' + rqs)
        
        email = provider_data['userinfo']['email'](response.json())
        picture = provider_data['userinfo']['picture'](response.json())

        # find or create the user in the database
        user = User.objects(email=email).first()
        if user is None:
            user = User(email=email, username=email.split('@')[0], picture=picture if provider=='google' else None, role='student') # TODO: make dynamic based on role
            user.save()

        token = create_access_token(
        identity=user.email, additional_claims={"transitive": True}, expires_delta=datetime.timedelta(minutes=5), fresh=True)
        # log the user in
        qs = urlencode({"jwt": token})
        return redirect(FRONTEND_URI + '?' + qs)
        


class GetRepoCommitsAPI(Resource):
    """
    Route: /api/github/commits
    """

    def get(self):
        """
        Fetch commits for a given repository.
        """
        repo_name = request.args.get('repo_name')
        if not repo_name:
            return Response.error(code=400, message="Missing repository name")

        oauth2_token = session.get('oauth2_token')
        if not oauth2_token:
            return Response.error(code=401, message="Missing OAuth2 token")

        # Fetch the repository details
        repo_url = f"https://api.github.com/repos/{repo_name}"
        repo_response = requests.get(repo_url, headers={
            'Authorization': f'token {oauth2_token}',
            'Accept': 'application/json'
        })

        if repo_response.status_code != 200:
            return Response.error(code=repo_response.status_code, message="Failed to fetch repository details")

        repo = repo_response.json()
        default_branch = repo['default_branch']

        # Fetch commits from the default branch
        commits_url = f"https://api.github.com/repos/{repo_name}/commits?sha={default_branch}"
        commits_response = requests.get(commits_url, headers={
            'Authorization': f'token {oauth2_token}',
            'Accept': 'application/json'
        })

        if commits_response.status_code != 200:
            return Response.error(code=commits_response.status_code, message="Failed to fetch commits")

        commits = commits_response.json()
        all_commit_comments = []

        # for commit in commits:
        #     commit_sha = commit['sha']
        #     commit_comments_url = f"https://api.github.com/repos/{repo_name}/commits/{commit_sha}/comments"
        #     comments_response = requests.get(commit_comments_url, headers={
        #         'Authorization': f'token {oauth2_token}',
        #         'Accept': 'application/json'
        #     })
        

            # if comments_response.status_code == 200:
            #     comments = comments_response.json()
            #     all_commit_comments.extend(comments)
        # repo_commit = {
        #     'repo_name': repo_name,
        #     'default_branch': default_branch,
        #     'commits': commits,
        #     'commit_comments': all_commit_comments
        # }
        for commit in commits:
            commit_data ={
                'sha': commit['sha'],
                'message': commit['commit']['message'],
                'author': commit['commit']['author']['name'],
                'date': commit['commit']['author']['date']
            }
            
            all_commit_comments.append(commit_data)
            
        repo_commit = {
            'repo_name': repo_name,
            'default_branch': default_branch,
            'commits': all_commit_comments
        }
        
        return repo_commit

        


class TokenAPI(Resource):
    """
    /api/token
    Endpoint to get JWT    
    """

    @jwt_required(fresh=True)
    def get(self):
        token = create_access_token(
            identity=current_user.email, additional_claims=current_user.to_dict(), expires_delta=datetime.timedelta(days=1))
        return {"token": token}
