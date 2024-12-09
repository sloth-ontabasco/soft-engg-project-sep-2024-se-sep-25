import datetime
from io import BytesIO
from flask import request, send_file
from flask_restful import Resource
from ..models.response import Response
from ..models.milestone_submission import MilestoneSubmission
from ..lib.auth import check_any_role

class FileAPI(Resource):

    @check_any_role(roles=['instructor', 'ta', 'admin', 'student'])
    def get(self):
        """
        Route: GET /api/file
        Description: Retrieves the file of a milestone submission by team_id and milestone_id from query params.
        Requires JWT authentication.
        """
        team_id = request.args.get('team_id')
        milestone_id = request.args.get('milestone_id')
        print(f"Received team_id: {team_id}, milestone_id: {milestone_id}")

        if not team_id or not milestone_id:
            print("Missing required query parameters: team_id and milestone_id")
            return Response.error(code=400, message="Missing required query parameters: team_id and milestone_id")

        milestone_submission = MilestoneSubmission.objects(team=team_id, milestone=milestone_id).first()
        if not milestone_submission:
            print("Milestone submission not found")
            return Response.error(code=404, message="Milestone submission not found")
        
        if milestone_submission.submission:
            try:
                file_data = milestone_submission.submission.read()
            except Exception as e:
                print(f"Error retrieving file: {e}")
                return Response.error(code=500, message="Error retrieving file")

            if file_data[:2] != b'PK':
                print("File is not a valid ZIP archive")
                return Response.error(code=400, message="The file is not a valid ZIP archive")
            
            # Wrap the file data in a BytesIO object
            file_stream = BytesIO(file_data)
            file_stream.seek(0)  # Ensure the stream position is at the beginning
        else:
            print("Milestone submission file not found")
            return Response.error(code=404, message="Milestone submission file not found")

        # Return the milestone submission file
        return send_file(file_stream, as_attachment=True, download_name="submission.zip", mimetype='application/zip')
