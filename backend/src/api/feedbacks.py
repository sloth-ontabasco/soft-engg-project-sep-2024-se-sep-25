from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_current_user
from src.models.feedback import Feedback
from src.models.milestone_submission import MilestoneSubmission
from src.lib.auth import check_any_role
from src.models.response import Response

"""
API for handling CRUD operations for Feedbacks
"""
class FeedbackAPI(Resource):

    """
    Route: /api/projects/<string:project_id>/milestones/<string:milestone_id>/submissions/<string:milestone_submission_id>/feedbacks,
           /api/projects/<string:project_id>/milestones/<string:milestone_id>/submissions/<string:milestone_submission_id>/feedbacks/<string:id>
    Description: Get feedback(s) under a milestone submission
    """
    # @jwt_required()
    @check_any_role(['instructor', 'student', 'admin'])
    def get(self, project_id, milestone_id, milestone_submission_id, id=None):
        milestone_submission = MilestoneSubmission.objects(id=milestone_submission_id).first()
        if not milestone_submission:
            print(f"Could not locate milestone submission with id: {milestone_submission_id}")
            return Response.error(404, message="Milestone Submission not found")
        
        if id:
            feedback = Feedback.objects(id=id, milestone_submission=milestone_submission).first()
            if not feedback:
                return Response.error(404, message="Feedback not found")
            return Response.success(200, feedback=feedback.to_dict())
        
        print(f"Fetching all feedbacks for milestone submission with id: {milestone_submission_id}")
        feedbacks = Feedback.objects(milestone_submission=milestone_submission)
        print(f"Found {len(feedbacks)} feedbacks")
        response = Response.success(200, feedbacks=[feedback.to_dict() for feedback in feedbacks])
        return response

    """
    Route: /api/projects/<string:project_id>/milestones/<string:milestone_id>/submissions/<string:milestone_submission_id>/feedbacks
    Description: Post a new feedback under a milestone submission
    Body: content(required)
    """
    @check_any_role(['instructor', 'admin'])
    def post(self, project_id, milestone_id, milestone_submission_id):
        milestone_submission = MilestoneSubmission.objects(id=milestone_submission_id).first()
        if not milestone_submission:
            return Response.error(404, message="Milestone Submission not found")
        data = request.get_json()
        user = get_current_user()
        feedback = Feedback(
            milestone_submission=milestone_submission,
            team=milestone_submission.team,
            content=data['content'],
            posted_by=user
        )
        feedback.save()
        return Response.success(code=201, feedback=feedback.to_dict())

    """
    Route: /api/projects/<string:project_id>/milestones/<string:milestone_id>/submissions/<string:milestone_submission_id>/feedbacks/<string:id>
    Description: Update a feedback
    Body: content(optional)
    """
    @check_any_role(['instructor', 'admin'])
    # @jwt_required()
    def put(self, project_id, milestone_id, milestone_submission_id, id):
        milestone_submission = MilestoneSubmission.objects(id=milestone_submission_id).first()
        if not milestone_submission:
            return Response.error(404, message="Milestone Submission not found")
        data = request.get_json()
        feedback = Feedback.objects(id=id, milestone_submission=milestone_submission).first()
        if not feedback:
            return Response.error(404, message="Feedback not found")
        feedback.update(**data)
        return Response.success(200, feedback=feedback.to_dict())

    """
    Route: /api/projects/<string:project_id>/milestones/<string:milestone_id>/submissions/<string:milestone_submission_id>/feedbacks/<string:id>
    Description: Delete a feedback
    """
    @check_any_role(['instructor', 'admin'])
    def delete(self, project_id, milestone_id, milestone_submission_id, id):
        milestone_submission = MilestoneSubmission.objects(id=milestone_submission_id).first()
        if not milestone_submission:
            return Response.error(404, message="Milestone Submission not found")
        feedback = Feedback.objects(id=id, milestone_submission=milestone_submission).first()
        if not feedback:
            return Response.error(404, message="Feedback not found")
        feedback.delete()
        return Response.success(200, message="Feedback deleted")