from flask import request
from flask_jwt_extended import jwt_required, current_user
from flask_restful import Resource

from ..lib.auth import check_any_role

from ..models.response import Response
from ..models.project import Project
from ..models.team import Team
from ..models.user import User


"""
API for handling CRUD operations for Teams
"""
class TeamAPI(Resource):

    """
    Route: GET /api/<string:project_id>/teams
    Description:
        - For Admins, Instructors, and TAs: Retrieve all teams working on a specific project.
        - For Students: Retrieve the team they belong to for the specified project.
    """
    @jwt_required()
    def get(self, project_id):
        try:
            # Fetch the project
            project = Project.objects(id=project_id).first()
            if not project:
                return Response.error(404, message="Project not found")
            
            # Handle different roles
            if current_user.role in ['admin', 'instructor', 'ta']:
                # Retrieve all teams associated with the project
                teams = Team.objects(project=project)
                teams_list = [team.to_dict() for team in teams]
                return Response.success(200, teams=teams_list, message="Teams found")
            
            elif current_user.role == 'student':
                # Find the user's team for the project
                team = Team.objects(project=project, members=current_user).first()
                if not team:
                    return Response.error(404, message="You are not part of any team for this project")
                return Response.success(200, team=team.to_dict(), message="Team found")
            
            else:
                print(f"Unauthorized access attempt by user: {current_user.username}")
                return Response.error(403, message="Unauthorized access")
        
        except Exception as e:
            print(f"Error occurred: {e}")
            return Response.error(500, message="Internal Server Error")
        
    """
    Route: POST /api/<string:project_id>/teams
    Description: Create a new team for the specified project.
    Body: team_name, members(list of user emails)
    """
    @check_any_role(['admin', 'instructor'])
    def post(self, project_id):
        try:
            # Fetch the project
            project = Project.objects(id=project_id).first()
            if not project:
                return Response.error(404, message="Project not found")
            
            data = request.get_json()
            team_name = data.get('team_name')
            members = data.get('members')
            
            if not team_name or not members:
                return Response.error(400, message="Missing required fields: team_name, members")
            
            # Check if the team name is unique for the project
            if Team.objects(project=project, team_name=team_name).first():
                return Response.error(400, message="Team name already exists for this project")
            
            # Fetch the users associated with the provided emails
            team_members = []
            for email in members:
                user = User.objects(email=email).first()
                if not user:
                    return Response.error(404, message=f"User with email {email} not found")
                team_members.append(user)
            
            # Create the new team
            team = Team(
                team_name=team_name,
                project=project,
                members=team_members
            )
            team.save()
            return Response.success(201, team=team.to_dict(), message="Team created successfully")
        
        except Exception as e:
            print(f"Error occurred: {e}")
            return Response.error(500, message="Internal Server Error")
        
    """
    Route: PUT /api/<string:project_id>/teams/<string:team_id>
    Description: Update the details of a team.
    Body: team_name, members(list of user emails)
    """
    @check_any_role(['admin', 'instructor'])
    def put(self, project_id, team_id):
        try:
           # Fetch and validate the project
            project = Project.objects(id=project_id).first()
            if not project:
                return Response.error(404, message="Project not found")
            
            # Fetch and validate the team
            team = Team.objects(id=team_id, project=project).first()
            if not team:
                return Response.error(404, message="Team not found")
            
            # Parse the request body
            data = request.get_json()
            if not data:
                return Response.error(400, message="Request body is missing")
            team_name = data.get('team_name', team.team_name)
            members = data.get('members', [member.email for member in team.members])
            
            # Fetch the users associated with the provided emails
            team_members = []
            for email in members:
                user = User.objects(email=email).first()
                if not user:
                    return Response.error(404, message=f"User with email {email} not found")
                team_members.append(user)
            
            # Update the team data
            team.update(
                team_name=team_name,
                members=team_members
            )
            return Response.success(200, team=team.reload().to_dict(), message="Team updated successfully")
        
        except Exception as e:
            print(f"Error occurred: {e}")
            return Response.error(500, message="Internal Server Error")
        
    """
    Route: DELETE /api/<string:project_id>/teams/<string:team_id>
    Description: Delete a team.
    """
    @check_any_role(['admin', 'instructor'])
    def delete(self, project_id, team_id):
        try:
            # Fetch the project
            project = Project.objects(id=project_id).first()
            if not project:
                return Response.error(404, message="Project not found")
            
            # Fetch the team
            team = Team.objects(id=team_id, project=project).first()
            if not team:
                return Response.error(404, message="Team not found")
            
            team.delete()
            return Response.success(200, message="Team deleted successfully")
        
        except Exception as e:
            print(f"Error occurred: {e}")
            return Response.error(500, message="Internal Server Error")
