import secrets
import time
from urllib.parse import urlencode

import requests
from flask_cors import cross_origin
from flask import make_response, redirect, request, session, url_for, jsonify
from flask_login import current_user
from datetime import datetime
from flask_restful import Resource, Api
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from ..config import *
from ..models.response import Response
from ..models.user import User
from ..models.team import Team
from ..models.github_integration import GithubIntegration


class CreateGithubIntegrationAPI(Resource):
    """
    Route: /api/github/integration
    """

    # @jwt_required()
    def post(self):
        """
        Create a new GitHub integration.
        """
        data = request.get_json()
        if not data:
            return Response.error(code=400, message="Missing JSON data")

        team_id = data.get('team_id')
        repo_url = data.get('repo_url')
        last_commit = data.get('last_commit')

        if not team_id or not repo_url or not last_commit:
            return Response.error(code=400, message="Missing required fields")

        team = Team.objects(id=team_id).first()
        if not team:
            return Response.error(code=404, message="Team not found")

        github_integration = GithubIntegration(
            team=team,
            repo_url=repo_url,
            last_commit=datetime.strptime(last_commit, '%m/%d/%y %H:%M:%S')
        )
        github_integration.save()

        return Response.success(data=github_integration.to_dict(), message="GitHub integration created successfully")
        

