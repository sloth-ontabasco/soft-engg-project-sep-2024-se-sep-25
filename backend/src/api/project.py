from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, Api
from datetime import datetime

from ..models.response import Response
from ..models.project import Project
from ..models.user import User
from ..models.role import Role
from ..models.milestone import Milestone

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
        Description: Retrieves the project details of the currently authenticated user.
        Requires JWT authentication.
        """
        projects = Project.objects()
        return Response.success(data=[project.to_dict() for project in projects])
    
    @jwt_required()
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

        # Convert mentors to a list of User references
        mentor_ids = data['mentors']
        mentors = User.objects(id__in=mentor_ids)
        if len(mentors) != len(mentor_ids):
            return Response.error(code=400, message="One or more mentors not found")

        # Parse the deadline
        try:
            deadline = datetime.strptime(data['deadline'], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return Response.error(code=400, message="Invalid date format for deadline. Use 'YYYY-MM-DD HH:MM:SS'.")

        # Create the project
        project = Project(
            title=data['title'],
            description=data['description'],
            deadline=deadline,
            mentors=mentors
        )
        project.save()

        return Response.success(data=project.to_dict(), message="Project created successfully.")

    
class ProjectsByMentorAPI(Resource):
    
    @jwt_required()
    def get(self, mentor_id):
        """
        Route: GET /api/projects/instructor/<mentor_id>
        Description: Retrieves all projects assigned to a specific mentor.
        Requires JWT authentication.
        """
        mentor = User.objects(id=mentor_id).first()
        if not mentor:
            return Response.error(code=404, message="Mentor not found")
        
        projects = Project.objects(mentors=mentor)
        return Response.success(data=[project.to_dict() for project in projects])
    
class ProjectByIdAPI(Resource):
    
    @jwt_required()
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
    
    @jwt_required()
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

        # Update project fields
        project.title = data.get('title', project.title)
        project.description = data.get('description', project.description)
        project.deadline = data.get('deadline', project.deadline)
        project.mentors = [User.objects(id=mentor_id).first() for mentor_id in data.get('mentors', [mentor.id for mentor in project.mentors])]
        project.updated_at = datetime.datetime.utcnow()

        project.save()
        return Response.success(data=project.to_dict(), message="Project updated successfully")

