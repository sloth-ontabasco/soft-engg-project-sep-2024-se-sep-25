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
class GenAISummaryAPI(Resource):

    def get(self, submission_id):
        """
        Route: GET /api/genai/summary/<submission_id>
        Description: Generates an AI summary based on the given milestone submission ID.
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
