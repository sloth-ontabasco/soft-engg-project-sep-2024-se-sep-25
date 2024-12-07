from flask import request
from flask_jwt_extended import jwt_required, current_user
from flask_restful import Resource

from ..lib.auth import check_any_role

from ..models.response import Response
from ..models.user import User


"""
API for handling CRUD operations for Users
"""
class UserAPI(Resource):

    """
    Route: GET /api/users/<string:user_id>
           GET /api/users
    Description: Retrieve the details of all users or a specific user.
    """
    @check_any_role(['admin', 'student', 'instructor', 'ta'])
    def get(self, user_id=None):

        try:
            # If user_id is provided and matches the current user's ID
            if user_id:
                if str(current_user.id) == user_id:
                    print(f"Returning current user data for userId: {user_id}")
                    return Response.success(200,user=current_user.to_dict(), message="User found")

                print(f"Fetching user with id: {user_id}")
                user = User.objects(id=user_id).first()
                if not user:
                    print(f"User with id {user_id} not found")
                    return Response.error(404, message="User not found")
                print(f"User found: {user.username}")
                return Response.success(200, user=user.to_dict(), message="User found")

            # If no user_id is provided, check admin privileges before fetching all users
            if current_user.role not in ['admin','instructor','ta']:
                print("Unauthorized access attempt by non-admin user")
                return Response.error(403, message="Unauthorized access")

            print("Fetching all users")
            users = User.objects()
            print(f"Found {users.count()} users")
            users_list = [user.to_dict() for user in users]
            return Response.success(200, users=users_list, message="Users found")
        except Exception as e:
            print(f"Error occurred: {e}")
            return Response.error(500, message="Internal Server Error")
        
    """
    Route: PUT /api/users/<string:user_id>
    Description: Update the details of a user.
    Body: username, github_id
    """
    @check_any_role(['admin', 'student', 'instructor', 'ta'])
    def put(self, user_id):
        try:
            # Check if the user is modifying their own data
            if str(current_user.id) != user_id:
                print(f"Unauthorized access attempt by user: {current_user.username}")
                return Response.error(403, message="Unauthorized access")

            # Update the user data
            data = request.get_json()
            current_user.update(
                username=data.get('username', current_user.username),
                github_id=data.get('github_id', current_user.github_id),
            )
            print(f"User with id {user_id} updated successfully")
            return Response.success(200, user=current_user.reload().to_dict(), message="User updated successfully")

        except Exception as e:
            print(f"Error occurred: {e}")
            return Response.error(500, message="Internal Server Error")
        
    """
    Route: DELETE /api/users/<string:user_id>
    Description: Delete a user.
    """
    @check_any_role(['admin'])
    def delete(self, user_id):

        try:
            user = User.objects(id=user_id).first()
            if not user:
                print(f"User with id {user_id} not found")
                return Response.error(404, message="User not found")

            user.delete()
            print(f"User with id {user_id} deleted successfully")
            return Response.success(200, message="User deleted successfully")

        except Exception as e:
            print(f"Error occurred: {e}")
            return Response.error(500, message="Internal Server Error")