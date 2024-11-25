from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_current_user
from datetime import datetime

from ..lib.auth import check_any_role

from ..models.announcement import Announcement
from ..models.team import Team
from ..models.project import Project
from ..models.milestone import Milestone
from ..models.milestone_submission import MilestoneSubmission
from ..models.response import Response

"""
API for project analytics
"""
class ProjectAnalyticsAPI(Resource):
    """
    Route: GET /api/<string:project_id>/analytics
    Description: Fetch analytics data for a specific project.
    """

    # @check_any_role(['admin', 'instructor', 'ta'])
    def get(self, project_id):
        try:
            # Fetch the project by ID
            project = Project.objects(id=project_id).first()
            if not project:
                return Response.error(404, message="Project not found")

            # Total students and TAs in the project
            teams = Team.objects(project=project)
            total_students = sum(len(team.members) for team in teams)
            total_tas = len(project.mentors)

            # Fetch all milestones for the project
            milestones = Milestone.objects(project=project).order_by('due_date')
            if not milestones:
                return Response.error(404, message="No milestones found for this project")

            # Get the current milestone and the previous one
            current_date = datetime.utcnow()
            current_milestone = (
                Milestone.objects(project=project, due_date__gte=current_date).order_by('due_date').first()
            )
            previous_milestone = (
                Milestone.objects(project=project, due_date__lt=current_date).order_by('-due_date').first()
            )

            def get_submission_stats(milestone):
                """Helper function to fetch late and on-time submission counts for a milestone."""
                submissions = MilestoneSubmission.objects(milestone=milestone)
                late = submissions.filter(status=3).count()  # Late Submission
                on_time = submissions.filter(status=2).count()  # Complete (On-time)
                return late, on_time

            # Calculate late submission percentage change
            if previous_milestone:
                latest_late, latest_on_time = get_submission_stats(current_milestone)
                prev_late, prev_on_time = get_submission_stats(previous_milestone)
                prev_total = prev_late + prev_on_time
                late_submission_change = (
                    ((latest_late - prev_late) / prev_total) * 100 if prev_total > 0 else None
                )
            else:
                latest_late, latest_on_time = get_submission_stats(current_milestone)
                late_submission_change = None

            # Prepare submissions grouped by milestone
            submissions_by_milestone = {}
            for milestone in milestones:
                late, on_time = get_submission_stats(milestone)
                submissions_by_milestone[str(milestone.id)] = {
                    "milestone_name": milestone.title,
                    "late": late,
                    "on_time": on_time,
                }

            # Prepare the analytics response
            analytics = {
                "total_students": total_students,
                "total_tas": total_tas,
                "late_submission_change": late_submission_change,
                "submissions_by_milestone": submissions_by_milestone,
            }

            return Response.success(data=analytics)
        except Exception as e:
            print(f"Error occurred: {e}")
            return Response.error(500, message="Internal Server Error")
