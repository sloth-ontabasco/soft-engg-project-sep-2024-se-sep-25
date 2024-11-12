from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, Api

from ..models.user import User

class UserAPI(Resource):

    @jwt_required()
    def get(self):
        current_user_email = get_jwt_identity()
        user = User.objects(email=current_user_email).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify(user.to_dict()), 200