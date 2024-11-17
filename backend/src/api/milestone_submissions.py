
from flask import request, send_file
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from src.models.milestone_submission import MilestoneSubmission
from src.models.response import Response
import io

class MilestoneSubmissionAPI(Resource):
    @jwt_required()
    def post(self, project_id, milestone_id):
        file = request.files['file']
        if not file:
            return Response.error(400, message="No file uploaded")
        
        milestone_submission = MilestoneSubmission(
            milestone=milestone_id,
            team=request.json.get('team_id'),
            status=1
        )
        milestone_submission.upload_file(file)
        return Response.success(201, message="File uploaded successfully")

    @jwt_required()
    def get(self, project_id, milestone_id, id):
        milestone_submission = MilestoneSubmission.objects(id=id).first()
        if not milestone_submission or not milestone_submission.submission:
            return Response.error(404, message="File not found")
        
        file_data = milestone_submission.download_file()
        return send_file(io.BytesIO(file_data), attachment_filename='submission.zip', as_attachment=True)

    @jwt_required()
    def delete(self, project_id, milestone_id, id):
        milestone_submission = MilestoneSubmission.objects(id=id).first()
        if not milestone_submission:
            return Response.error(404, message="Milestone Submission not found")
        
        milestone_submission.delete_file()
        return Response.success(200, message="File deleted successfully")