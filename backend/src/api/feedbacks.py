from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_current_user
from src.models.feedback import Feedback
from src.models.milestone_submission import MilestoneSubmission
from src.models.team import Team
from src.lib.auth import check_any_role
from src.models.response import Response
from datetime import datetime

"""
API for handling CRUD operations for Feedbacks
"""
class FeedbackAPI(Resource):

    """
    Route: /api/projects/<string:project_id>/milestones/<string:milestone_id>/teams/<string:team_id>/feedbacks,
           /api/projects/<string:project_id>/milestones/<string:milestone_id>/teams/<string:team_id>/feedbacks/<string:id>
    Description: Get feedback(s) under a milestone for a team
    """
    @check_any_role(['instructor', 'student', 'admin'])
    def get(self, project_id, milestone_id, team_id, id=None):
        team = Team.objects(id=team_id).first()
        if not team:
            print(f"Could not locate team with id: {team_id}")
            return Response.error(404, message="Team not found")
        
        if id:
            feedback = Feedback.objects(id=id, team=team).first()
            if not feedback:
                return Response.error(404, message="Feedback not found")
            return Response.success(200, feedback=feedback.to_dict())
        
        print(f"Fetching all feedbacks for team with id: {team_id} and milestone with id: {milestone_id}")
        milestone_submissions = MilestoneSubmission.objects(team=team, milestone=milestone_id)
        feedbacks = Feedback.objects(milestone_submission__in=milestone_submissions)
        print(f"Found {len(feedbacks)} feedbacks")
        response = Response.success(200, feedbacks=[feedback.to_dict() for feedback in feedbacks])
        return response

    """
    Route: /api/projects/<string:project_id>/milestones/<string:milestone_id>/teams/<string:team_id>/feedbacks
    Description: Post a new feedback under a milestone for a team
    Body: content(required)
    """
    @check_any_role(['instructor', 'admin'])
    def post(self, project_id, milestone_id, team_id):
        team = Team.objects(id=team_id).first()
        if not team:
            return Response.error(404, message="Team not found")
        
        milestone_submission = MilestoneSubmission.objects(team=team, milestone=milestone_id).first()
        if not milestone_submission:
            print(f"Could not locate milestone submission for team with id: {team_id} and milestone with id: {milestone_id}")
            return Response.error(404, message="Milestone Submission not found for the team")
        
        data = request.get_json()
        user = get_current_user()
        feedback = Feedback(
            milestone_submission=milestone_submission,
            team=team,
            content=data['content'],
            posted_by=user
        )
        feedback.save()
        return Response.success(code=201, feedback=feedback.to_dict())

    """
    Route: /api/projects/<string:project_id>/milestones/<string:milestone_id>/teams/<string:team_id>/feedbacks/<string:id>
    Description: Update a feedback
    Body: content(optional)
    """
    @check_any_role(['instructor', 'admin'])
    def put(self, project_id, milestone_id, team_id, id):
        team = Team.objects(id=team_id).first()
        if not team:
            return Response.error(404, message="Team not found")
        
        milestone_submission = MilestoneSubmission.objects(team=team, milestone=milestone_id).first()
        if not milestone_submission:
            print(f"Could not locate milestone submission for team with id: {team_id} and milestone with id: {milestone_id}")
            return Response.error(404, message="Milestone Submission not found for the team")
        
        data = request.get_json()
        feedback = Feedback.objects(id=id, team=team).first()
        if not feedback:
            return Response.error(404, message="Feedback not found")
        
        modified = False
        if 'content' in data and data['content'] != feedback.content:
            feedback.content = data['content']
            modified = True
        
        if modified:
            feedback.updated_at = datetime.utcnow()
            feedback.save()
            return Response.success(200, feedback=feedback.to_dict())
        
        return Response.success(200, feedback=feedback.to_dict(), message="No changes detected")

    """
    Route: /api/projects/<string:project_id>/milestones/<string:milestone_id>/teams/<string:team_id>/feedbacks/<string:id>
    Description: Delete a feedback
    """
    @check_any_role(['instructor', 'admin'])
    def delete(self, project_id, milestone_id, team_id, id):
        team = Team.objects(id=team_id).first()
        if not team:
            return Response.error(404, message="Team not found")
        
        milestone_submission = MilestoneSubmission.objects(team=team, milestone=milestone_id).first()
        if not milestone_submission:
            print(f"Could not locate milestone submission for team with id: {team_id} and milestone with id: {milestone_id}")
            return Response.error(404, message="Milestone Submission not found for the team")
        
        feedback = Feedback.objects(id=id, team=team).first()
        if not feedback:
            return Response.error(404, message="Feedback not found")
        feedback.delete()
        return Response.success(200, message="Feedback deleted")