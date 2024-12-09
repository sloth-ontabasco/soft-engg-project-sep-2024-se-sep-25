import datetime
from io import BytesIO
import os
from flask import request, send_file
from flask_jwt_extended import get_current_user
from flask_restful import Resource

from ..models.response import Response
from ..models.milestone import Milestone
from ..models.team import Team
from ..models.milestone_submission import MilestoneSubmission
from ..lib.auth import check_any_role
from .ai_summary_gemini_final import process_files
class MilestoneSubmissionAPI(Resource):

    @check_any_role(roles=['instructor', 'ta', 'admin', 'student'])
    def post(self):
        """
        Route: POST /api/submission
        Description: Creates a new milestone submission.
        Requires JWT authentication.
        """
        data = request.form
        file = request.files.get('submission')

        # Validate required fields
        required_fields = ['milestone_id', 'team_id']
        for field in required_fields:
            if field not in data:
                return Response.error(code=400, message=f"Missing required field: {field}")

        # Check if Milestone exists
        milestone = Milestone.objects(id=data['milestone_id']).first()
        if not milestone:
            return Response.error(code=404, message="Milestone not found")

        # Check if Team exists
        team = Team.objects(id=data['team_id']).first()
        if not team:
            return Response.error(code=404, message="Team not found")

        # Create MilestoneSubmission
        milestone_submission = MilestoneSubmission(
            milestone=milestone,
            team=team,
            status=0  # Set status to 0 (Not Yet Started) by default
        )

        if file:
            try:
                milestone_submission.submission.put(file, content_type="application/x-rar-compressed")
                milestone_submission.file_name = file.filename
                print("File stored successfully in MongoDB")
            except Exception as e:
                print(f"Error storing file: {e}")
                return Response.error(code=500, message="Error storing file")
            if milestone.due_date > datetime.datetime.utcnow():
                milestone_submission.status = 2  # Complete
            else:
                milestone_submission.status = 3  # Late Submission

        milestone_submission.save()

        return Response.success(data=milestone_submission.to_dict(), message="Milestone submission created successfully")

    @check_any_role(roles=['instructor', 'ta', 'admin', 'student'])
    def get(self):
        """
        Route: GET /api/submission
        Description: Retrieves a milestone submission by team_id and milestone_id from query params.
        Requires JWT authentication.
        """
        team_id = request.args.get('team_id')
        milestone_id = request.args.get('milestone_id')

        if not team_id or not milestone_id:
            return Response.error(code=400, message="Missing required query parameters: team_id and milestone_id")

        milestone_submission = MilestoneSubmission.objects(team=team_id, milestone=milestone_id).first()
        if not milestone_submission:
            return Response.error(code=404, message="Milestone submission not found")

        submission_data = milestone_submission.to_dict()
        return Response.success(data=submission_data)

    @check_any_role(roles=['instructor', 'ta', 'admin'])
    def delete(self, submission_id):
        """
        Route: DELETE /api/submission/<submission_id>
        Description: Deletes a milestone submission by its ID.
        Requires JWT authentication.
        """
        milestone_submission = MilestoneSubmission.objects(id=submission_id).first()
        if not milestone_submission:
            return Response.error(code=404, message="Milestone submission not found")

        if milestone_submission.submission:
            milestone_submission.submission.delete()
        milestone_submission.delete()

        return Response.success(message="Milestone submission deleted successfully")

    @check_any_role(roles=['student', 'instructor', 'admin', 'ta'])
    def put(self):
        """
        Route: PUT /api/submission
        Description: Updates a milestone submission.
        Students can upload a file, and instructors or TAs can update the grade field.
        Requires JWT authentication.
        """
        team_id = request.args.get('team_id')
        milestone_id = request.args.get('milestone_id')

        if not team_id or not milestone_id:
            return Response.error(code=400, message="Missing required query parameters: team_id and milestone_id")

        milestone_submission = MilestoneSubmission.objects(team=team_id, milestone=milestone_id).first()
        if not milestone_submission:
            return Response.error(code=404, message="Milestone submission not found")

        data = request.form
        file = request.files.get('submission')
        grade = data.get('grade')

        current_user = get_current_user()

        # Student may upload or delete a file from current MilestoneSubmission
        # but, may not update the grade field
        if 'student' in current_user.role or 'admin' in current_user.role:
            if file:
                milestone_submission.submission.put(file, content_type="application/zip")
                milestone_submission.file_name = file.filename
                if milestone_submission.milestone.due_date > datetime.datetime.utcnow():
                    milestone_submission.status = 2  # Complete
                else:
                    milestone_submission.status = 3  # Late Submission
            elif milestone_submission.submission:
                milestone_submission.submission.delete()

            if grade and 'student' in current_user.role:
                return Response.error(code=403, message="Students are not allowed to update the grade field")

        # Instructors and TAs may update the grade field, 
        # but may not upload or delete a submission file
        if 'instructor' in current_user.role or 'ta' in current_user.role \
            or 'admin' in current_user.role:
            if grade:
                if grade.upper() in ['A', 'B', 'C', 'D', 'F']:
                    milestone_submission.grade = grade.upper()
                else:
                    return Response.error(code=400, message="Invalid grade value")
                
            if file and not 'admin' in current_user.role:
                return Response.error(code=403, message="Instructors and TAs are not allowed to edit submissions")

        milestone_submission.updated_at = datetime.datetime.utcnow()
        milestone_submission.save()

        return Response.success(data=milestone_submission.to_dict(), message="Milestone submission updated successfully")
