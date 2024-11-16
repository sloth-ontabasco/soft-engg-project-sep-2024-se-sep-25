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


class MilestoneAPI(Resource):
    
    @jwt_required()
    def get(self, milestone_id):
        """
        Route: GET /api/milestones/<milestone_id>
        Description: Retrieves a specific milestone by its ID.
        Requires JWT authentication.
        """
        milestone = Milestone.objects(id=milestone_id).first()
        if not milestone:
            return Response.error(code=404, message="Milestone not found")
        
        return Response.success(data=milestone.to_dict())
    
class MilestoneSubmissionsAPI(Resource):
    
    @jwt_required()
    def get(self, milestone_id):
        """
        Route: GET /api/milestones/<milestone_id>/submissions
        Description: Retrieves all submissions for a specific milestone.
        Requires JWT authentication.
        """
        milestone = Milestone.objects(id=milestone_id).first()
        if not milestone:
            return Response.error(code=404, message="Milestone not found")
        
        submissions = MilestoneSubmission.objects(milestone=milestone)
        return Response.success(data=[submission.to_dict() for submission in submissions])
    
class ProjectMilestonesAPI(Resource):
    
    @jwt_required()
    def get(self, project_id):
        """
        Route: GET /api/projects/<project_id>/milestones
        Description: Retrieves all milestones for a specific project.
        Requires JWT authentication.
        """
        project = Project.objects(id=project_id).first()
        if not project:
            return Response.error(code=404, message="Project not found")
        
        milestones = Milestone.objects(project=project)
        return Response.success(data=[milestone.to_dict() for milestone in milestones])
    
    @jwt_required()
    def post(self, project_id):
        """
        Route: POST /api/projects/<project_id>/milestones
        Description: Adds a milestone to a specific project.
        Requires JWT authentication.
        """
        project = Project.objects(id=project_id).first()
        if not project:
            return Response.error(code=404, message="Project not found")
        
        data = request.get_json()

        # Validate required fields
        required_fields = ['title', 'description', 'due_date']
        for field in required_fields:
            if field not in data:
                return Response.error(code=400, message=f"Missing required field: {field}")

        # Create new milestone
        milestone = Milestone(
            title=data['title'],
            description=data['description'],
            due_date=data['due_date'],
            project=project
        )
        milestone.save()
        return Response.success(data=milestone.to_dict(), message="Milestone added successfully")
    
class EditDeleteMilestoneAPI(Resource):
    
    @jwt_required()
    def put(self, project_id, milestone_id):
        """
        Route: PUT /api/milestones/<project_id>/<milestone_id>
        Description: Edits a milestone for a specific project.
        Requires JWT authentication.
        """
        project = Project.objects(id=project_id).first()
        if not project:
            return Response.error(code=404, message="Project not found")
        
        milestone = Milestone.objects(id=milestone_id, project=project).first()
        if not milestone:
            return Response.error(code=404, message="Milestone not found")
        
        data = request.get_json()

        # Update milestone fields
        milestone.title = data.get('title', milestone.title)
        milestone.description = data.get('description', milestone.description)
        milestone.due_date = data.get('due_date', milestone.due_date)
        milestone.updated_at = datetime.datetime.utcnow()

        milestone.save()
        return Response.success(data=milestone.to_dict(), message="Milestone updated successfully")
    
    @jwt_required()
    def delete(self, project_id, milestone_id):
        """
        Route: DELETE /api/milestones/<project_id>/<milestone_id>
        Description: Deletes a milestone for a specific project.
        Requires JWT authentication.
        """
        project = Project.objects(id=project_id).first()
        if not project:
            return Response.error(code=404, message="Project not found")
        
        milestone = Milestone.objects(id=milestone_id, project=project).first()
        if not milestone:
            return Response.error(code=404, message="Milestone not found")
        
        milestone.delete()
        return Response.success(message="Milestone deleted successfully")


    


    
# class AddMilestoneSubmissionAPI(Resource):
    
#     @jwt_required()
#     def post(self, milestone_id):
#         """
#         Route: POST /api/milestones/<milestone_id>/submissions
#         Description: Adds a submission to a specific milestone.
#         Requires JWT authentication.
#         """
#         milestone = Milestone.objects(id=milestone_id).first()
#         if not milestone:
#             return Response.error(code=404, message="Milestone not found")
        
#         data = request.get_json()

#         # Validate required fields
#         required_fields = ['team_id', 'status', 'submission', 'grade']
#         for field in required_fields:
#             if field not in data:
#                 return Response.error(code=400, message=f"Missing required field: {field}")

#         team = Team.objects(id=data['team_id']).first()
#         if not team:
#             return Response.error(code=404, message="Team not found")

#         # Create new milestone submission
#         milestone_submission = MilestoneSubmission(
#             milestone=milestone,
#             team=team,
#             status=data['status'],
#             submission=data['submission'],
#             grade=data['grade']
#         )
#         milestone_submission.save()
#         return Response.success(data=milestone_submission.to_dict(), message="Milestone submission added successfully")
    
# class DeleteMilestoneSubmissionAPI(Resource):
    
#     @jwt_required()
#     def delete(self, milestone_id, submission_id):
#         """
#         Route: DELETE /api/milestones/<milestone_id>/submissions/<submission_id>
#         Description: Deletes a specific submission from a milestone.
#         Requires JWT authentication.
#         """
#         milestone = Milestone.objects(id=milestone_id).first()
#         if not milestone:
#             return Response.error(code=404, message="Milestone not found")
        
#         submission = MilestoneSubmission.objects(id=submission_id, milestone=milestone).first()
#         if not submission:
#             return Response.error(code=404, message="Submission not found")
        
#         submission.delete()
#         return Response.success(message="Milestone submission deleted successfully")