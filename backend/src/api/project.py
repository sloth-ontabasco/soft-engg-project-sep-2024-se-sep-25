from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, Api
from datetime import datetime

from ..models.response import Response
from ..models.project import Project
from ..models.user import User
from ..models.team import Team  
from ..lib.auth import check_any_role

class ProjectAPI(Resource):
    """
    API Resource for project management.
    - Provides endpoints to retrieve, update and delete project information.
    - Requires JWT authentication for access.
    """

    @jwt_required()
    def get(self):
        """
        Route: GET /api/project
        Description: Retrieves the project details.
        Requires JWT authentication.
        """
        projects = Project.objects()
        return Response.success(data=[project.to_dict() for project in projects])
    

    @check_any_role(roles=['instructor', 'admin'])
    def post(self):
        """
        Route: POST /api/project
        Description: Creates a new project.
        Requires JWT authentication.
        """
        data = request.get_json()

        # Validate required fields
        required_fields = ['title', 'description', 'deadline', 'mentors']
        for field in required_fields:
            if field not in data:
                return Response.error(code=400, message=f"Missing required field: {field}")

        # Convert mentors to a list of User objects
        mentors = [User.objects(id=mentor_id).first() for mentor_id in data['mentors']]
        if None in mentors:
            return Response.error(code=400, message="One or more mentors not found")

        # Parse deadline string to datetime object
        deadline_str = str(data['deadline'])
        deadline = datetime.strptime(deadline_str, '%m/%d/%y %H:%M:%S')

        # Create new project
        project = Project(
            title=data['title'],
            description=data['description'],
            deadline=deadline,
            mentors=mentors
        )

        project.save()
        return Response.success(data=project.to_dict(), message="Project created successfully")
    
class ProjectsByUserAPI(Resource):
    
    @check_any_role(roles=['instructor', 'admin','student'])
    def get(self, user_id):
        """
        Route: GET /api/projects/user/<user_id>
        Description: Retrieves all projects assigned to a specific user.
        Requires JWT authentication.
        """
        user = User.objects(id=user_id).first()
        if not user:
            return Response.error(code=404, message="User not found")
        
        projects = Project.objects(mentors=user)
        return Response.success(data=[project.to_dict() for project in projects])
    
class ProjectByStudentAPI(Resource):
    def get(self, user_id):
        """
        Route: GET /api/projects/student/<user_id>
        Description: Retrieves all projects assigned to a specific user.
        Requires JWT authentication.
        """
        user = User.objects(id=user_id).first()
        if not user:
            return Response.error(code=404, message="User not found")
        
        # get all the teams that user is part of 
        # return all the projects that the teams are part of
        teams = Team.objects(members__in=[user])
        projects = [team.project for team in teams]
        return Response.success(data=[project.to_dict() for project in projects])

class ProjectByIdAPI(Resource):
    
    @check_any_role(roles=['instructor', 'admin','student'])
    def get(self, project_id):
        """
        Route: GET /api/project/<project_id>
        Description: Retrieves a specific project by its ID.
        Requires JWT authentication.
        """
        project = Project.objects(id=project_id).first()
        if not project:
            return Response.error(code=404, message="Project not found")
        
        return Response.success(data=project.to_dict())
    
    @check_any_role(roles=['instructor', 'admin'])
    def put(self, project_id):
        """
        Route: PUT /api/project/<project_id>
        Description: Edits a project.
        Requires JWT authentication.
        """
        project = Project.objects(id=project_id).first()
        if not project:
            return Response.error(code=404, message="Project not found")
        
        data = request.get_json()

        deadline_str = str(data['deadline'])
        deadline = datetime.strptime(deadline_str, '%m/%d/%y %H:%M:%S')

        # Update project fields
        project.title = data.get('title', project.title)
        project.description = data.get('description', project.description)
        project.deadline = deadline
        project.mentors = [User.objects(id=mentor_id).first() for mentor_id in data.get('mentors', [mentor.id for mentor in project.mentors])]
        project.updated_at = datetime.utcnow()

        project.save()
        return Response.success(data=project.to_dict(), message="Project updated successfully")
    
    @check_any_role(roles=['instructor', 'admin'])
    def delete(self, project_id):
        """
        Route: DELETE /api/project/<project_id>
        Description: Deletes a specific project by its ID.
        Requires JWT authentication.
        """
        project = Project.objects(id=project_id).first()
        if not project:
            return Response.error(code=404, message="Project not found")
        
        project.delete()
        return Response.success(message="Project deleted successfully")

