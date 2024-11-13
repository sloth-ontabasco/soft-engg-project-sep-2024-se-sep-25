from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, Api

from ..models.response import Response
from ..models.user import User

class UserAPI(Resource):
    """
    API Resource for user profile management.
    - Provides endpoints to retrieve, update and delete user profile information.
    - Requires JWT authentication for access.
    """

    @jwt_required()
    def get(self):
        """
        Route: GET /api/user/profile
        Description: Retrieves the profile details of the currently authenticated user.
        Requires JWT authentication.
        """
        current_user_email = get_jwt_identity()
        user = User.objects(email=current_user_email).first()

        if not user:
            return Response.error(code=404, message="User not found")

        return Response.success(data=user.to_dict())