from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, Api
from datetime import datetime

from ..models.response import Response
from ..models.project import Project
from ..models.user import User
from ..models.role import Role
from ..models.milestone import Milestone
from ..models.milestone_submission import MilestoneSubmission
from ..models.team import Team
from ..models.resource import Resource as ProjectResource
from ..lib.auth import check_any_role


class ProjectResourcesAPI(Resource):
    
    @check_any_role(roles=['instructor', 'admin','student'])
    def get(self, project_id):
        """
        Route: GET /api/resource/<project_id>
        Description: Retrieves all resources for a specific project.
        Requires JWT authentication.
        """
        project = Project.objects(id=project_id).first()
        if not project:
            return Response.error(code=404, message="Project not found")
        
        resources = ProjectResource.objects(project=project)
        return Response.success(data=[resource.to_dict() for resource in resources])
    
    @check_any_role(roles=['instructor', 'admin'])
    def post(self, project_id):
        """
        Route: POST /api/resource/<project_id>
        Description: Adds a resource to a specific project.
        Requires JWT authentication.
        """
        project = Project.objects(id=project_id).first()
        if not project:
            return Response.error(code=404, message="Project not found")
        
        data = request.get_json()

        # Validate required fields
        required_fields = ['title', 'url', 'description']
        for field in required_fields:
            if field not in data:
                return Response.error(code=400, message=f"Missing required field: {field}")

        # Create new resource
        resource = ProjectResource(
            project=project,
            title=data['title'],
            url=data['url'],
            description=data['description']
        )
        resource.save()
        return Response.success(data=resource.to_dict(), message="Resource added successfully")
    
    @check_any_role(roles=['instructor', 'admin'])
    def put(self, project_id, resource_id):
        """
        Route: PUT /api/resources/<project_id>/<resource_id>
        Description: Edits a resource for a specific project.
        Requires JWT authentication.
        """
        project = Project.objects(id=project_id).first()
        if not project:
            return Response.error(code=404, message="Project not found")
        
        resource = ProjectResource.objects(id=resource_id, project=project).first()
        if not resource:
            return Response.error(code=404, message="Resource not found")
        
        data = request.get_json()

        # Update resource fields
        resource.title = data.get('title', resource.title)
        resource.url = data.get('url', resource.url)
        resource.description = data.get('description', resource.description)
        resource.updated_at = datetime.utcnow()

        resource.save()
        return Response.success(data=resource.to_dict(), message="Resource updated successfully")
    
    @check_any_role(roles=['instructor', 'admin'])
    def delete(self, project_id, resource_id):
        """
        Route: DELETE /api/resources/<project_id>/<resource_id>
        Description: Deletes a resource for a specific project.
        Requires JWT authentication.
        """
        project = Project.objects(id=project_id).first()
        if not project:
            return Response.error(code=404, message="Project not found")
        
        resource = ProjectResource.objects(id=resource_id, project=project).first()
        if not resource:
            return Response.error(code=404, message="Resource not found")
        
        resource.delete()
        return Response.success(message="Resource deleted successfully")

