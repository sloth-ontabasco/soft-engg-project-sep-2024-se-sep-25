from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.announcement import Announcement
from src.models.project import Project
from src.lib.auth import check_any_role
from src.models.response import Response

class AnnouncementAPI(Resource):
    @jwt_required()
    def get(self, project_id, id=None):
        project = Project.objects(id=project_id).first()
        if not project:
            return Response.error(404, message="Project not found")
        if id:
            announcement = Announcement.objects(project=project, id=id).first()
            if not announcement:
                return Response.error(404, message="Announcement not found")
            return Response.success(200, announcement=announcement.to_dict())
        announcements = Announcement.objects(project=project)
        return Response.success(200, announcements=[announcement.to_dict() for announcement in announcements])

    @jwt_required()
    @check_any_role(['instructor', 'ta', 'admin'])
    def post(self, project_id):
        data = request.get_json()
        project = Project.objects(id=project_id).first()
        if not project:
            return Response.error(404, message="Project not found")
        user = get_jwt_identity()
        announcement = Announcement(
            project=project,
            title=data['title'],
            content=data['content'],
            posted_by=user['role']
        )
        announcement.save()
        return Response.success(201, announcement=announcement.to_dict())

    @jwt_required()
    @check_any_role(['instructor', 'ta', 'admin'])
    def put(self, project_id, id):
        data = request.get_json()
        project = Project.objects(id=project_id).first()
        if not project:
            return Response.error(404, message="Project not found")
        announcement = Announcement.objects(project=project, id=id).first()
        if not announcement:
            return Response.error(404, message="Announcement not found")
        announcement.update(**data)
        return Response.success(200, announcement=announcement.to_dict())

    @jwt_required()
    @check_any_role(['instructor', 'ta', 'admin'])
    def delete(self, project_id, id):
        project = Project.objects(id=project_id).first()
        if not project:
            return Response.error(404, message="Project not found")
        announcement = Announcement.objects(project=project, id=id).first()
        if not announcement:
            return Response.error(404, message="Announcement not found")
        announcement.delete()
        return Response.success(200, message="Announcement deleted")