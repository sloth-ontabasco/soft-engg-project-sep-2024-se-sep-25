from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_current_user
from src.models.announcement import Announcement
from src.models.project import Project
from src.lib.auth import check_any_role
from src.models.response import Response

"""
API for handling CRUD operations for Announcements
"""
class AnnouncementAPI(Resource):

    """
    Route: /api/<string:project_id>/announcements,
           /api/<string:project_id>/announcements/<string:id>
    Description: Get all (or a specific) announcement(s) under a project
    """
    @jwt_required()
    def get(self, project_id, id=None):
        project = Project.objects(id=project_id).first()
        if not project:
            return Response.error(404, message="Project not found")
        if id:
            print(f"Fetching announcement with id: {id} for project: {project_id}")
            announcement = Announcement.objects(id=id, project=project).first()
            if not announcement:
                print(f"Announcement with id {id} not found for project {project_id}")
                return Response.error(404, message="Announcement not found")
            print(f"Announcement found: {announcement.title}")
            return Response.success(200, announcement=announcement.to_dict())
        print(f"Fetching all announcements for project: {project_id}")
        announcements = Announcement.objects(project=project)
        print(f"Found {announcements.count()} announcements")
        response = Response.success(200, announcements=[announcement.to_dict() for announcement in announcements])
        return response

    """
    Route: /api/<string:project_id>/announcements
    Description: Post a new announcement under a project
    Body: title(required), content(required)
    """
    @jwt_required()
    @check_any_role(['instructor', 'ta', 'admin'])
    def post(self, project_id):
        project = Project.objects(id=project_id).first()
        if not project:
            return Response.error(404, message="Project not found")
        data = request.get_json()
        user = get_current_user()
        announcement = Announcement(
            project=project,
            title=data['title'],
            content=data['content'],
            posted_by=user.role
        )
        announcement.save()
        return Response.success(code=201, announcement=announcement.to_dict())

    """
    Route: /api/<string:project_id>/announcements/<string:id>
    Description: Update an announcement
    Body: title(optional), content(optional)
    """
    @jwt_required()
    @check_any_role(['instructor', 'ta', 'admin'])
    def put(self, project_id, id):
        project = Project.objects(id=project_id).first()
        if not project:
            return Response.error(404, message="Project not found")
        data = request.get_json()
        announcement = Announcement.objects(id=id, project=project).first()
        if not announcement:
            return Response.error(404, message="Announcement not found")
        announcement.update(**data)
        print(f"Announcement with id: {announcement.id} updated")
        return Response.success(200, announcement=announcement.to_dict())

    """
    Route: /api/<string:project_id>/announcements/<string:id>
    Description: Delete an announcement
    """
    @jwt_required()
    @check_any_role(['instructor', 'ta', 'admin'])
    def delete(self, project_id, id):
        project = Project.objects(id=project_id).first()
        if not project:
            return Response.error(404, message="Project not found")
        announcement = Announcement.objects(id=id, project=project).first()
        if not announcement:
            return Response.error(404, message="Announcement not found")
        print(f"Announcement with id: {announcement.id} deleted")
        announcement.delete()
        return Response.success(200, message="Announcement deleted")