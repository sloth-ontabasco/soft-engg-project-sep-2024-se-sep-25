import os
from flask import Blueprint, request, send_file
from flask_restful import Resource, Api
from io import BytesIO

from ..models.response import Response
from ..models.milestone import Milestone
from ..models.team import Team
from ..models.milestone_submission import MilestoneSubmission
from ..lib.auth import check_any_role
from .ai_summary_gemini_final import process_files
class MilestoneSubmissionAPI(Resource):

    # @check_any_role(roles=['instructor', 'admin', 'student'])
    def post(self):
        """
        Route: POST /api/submission
        Description: Creates a new milestone submission.
        Requires JWT authentication.
        """
        data = request.form
        file = request.files.get('submission')

        # Validate required fields
        required_fields = ['milestone_id', 'team_id', 'status']
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
            status=int(data['status']),
            grade=data.get('grade')  # Make grade optional
        )

        # Store the file in the submission field
        if file:
            milestone_submission.submission.put(file, content_type="application/zip")

        milestone_submission.save()

        return Response.success(data=milestone_submission.to_dict(), message="Milestone submission created successfully")

    # @check_any_role(roles=['instructor', 'admin', 'student'])
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
            output_pdf_path = os.path.join(os.getcwd(), "backend", "src", "api", "reports", "summary_report.pdf")

            process_files(zip_file_data, rubrix_file_path, milestone_title, milestone_description, output_pdf_path)
        else:
            return Response.error(code=404, message="Milestone submission file not found")

        # Return the generated PDF file as a downloadable response
        return send_file(output_pdf_path, as_attachment=True, download_name="summary_report.pdf")
        # return Response.success(data=submission_data, message="Milestone submission retrieved successfully")