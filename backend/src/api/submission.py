import datetime
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

    @check_any_role(roles=['instructor', 'ta', 'admin'])
    def post(self):
        """
        Route: POST /api/submission
        Description: Creates a new milestone submission.
        Requires JWT authentication.
        """
        data = request.json

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

        milestone_submission.save()

        return Response.success(data=milestone_submission.to_dict(), message="Milestone submission created successfully")

    def get(self, submission_id):
        """
        Route: GET /api/submission/<submission_id>
        Description: Retrieves a milestone submission by its ID.
        Requires JWT authentication.
        """
        milestone_submission = MilestoneSubmission.objects(id=submission_id).first()
        if not milestone_submission:
            return Response.error(code=404, message="Milestone submission not found")

        submission_data = milestone_submission.to_dict()
        if milestone_submission.submission:
            file_data = milestone_submission.submission.read()
            submission_data['submission_file'] = file_data.decode('latin1')  # Convert binary to string for JSON
            
            zip_file_data = file_data
            rubrix_file_path = ""; # No rubrix file provided
            milestone_title = milestone_submission.milestone.title
            milestone_description = milestone_submission.milestone.description
            # output_pdf_path = os.path.join(os.getcwd(), "src", "api", "reports", "summary_report.pdf")

            process_files(zip_file_data, rubrix_file_path, milestone_title, milestone_description)
        else:
            return Response.error(code=404, message="Milestone submission file not found")

        # Return the generated PDF file as a downloadable response
        return send_file(os.path.join(os.getcwd(), "submission_evaluation.html"), as_attachment=True, download_name="submission_evaluation.html")
        # return Response.success(data=submission_data, message="Milestone submission retrieved successfully")

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
    def put(self, submission_id):
        """
        Route: PUT /api/submission/<submission_id>
        Description: Updates a milestone submission.
        Students can upload a file, and instructors or TAs can update the grade field.
        Requires JWT authentication.
        """
        milestone_submission = MilestoneSubmission.objects(id=submission_id).first()
        if not milestone_submission:
            return Response.error(code=404, message="Milestone submission not found")

        data = request.form
        file = request.files.get('submission')
        grade = data.get('grade')

        current_user = get_current_user()
        
        # Student may upload or delete a file from current MilestoneSubmission
        #but, may not update the grade field
        if 'student' in current_user.role or 'admin' in current_user.role:
            if file:
                milestone_submission.submission.put(file, content_type="application/zip")
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
