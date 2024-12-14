from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.milestone import Milestone
from ..models.team import Team
from ..models.project import Project
from ..models.user import User
from flask_restful import Response  # Utility for consistent API responses

milestone_api = Blueprint('milestone_api', __name__)

@milestone_api.route('/api/milestones', methods=['GET'])
@jwt_required()
def get_milestones():
    """
    Fetch milestones for the authenticated user.
    """
    current_user_id = get_jwt_identity()
    user = User.objects(id=current_user_id).first()
    if not user:
        return Response.error(404, "User not found")

    team = Team.objects(members=user).first()
    if not team:
        return Response.error(404, "Team not found")

    project = team.project
    if not project:
        return Response.error(404, "Project not found")

    milestones = Milestone.objects(project=project)
    return Response.success(
        data=[milestone.to_dict() for milestone in milestones],
        message="Milestones retrieved successfully"
    )
