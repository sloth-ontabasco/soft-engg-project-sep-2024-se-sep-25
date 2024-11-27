import pytest
import json
from unittest.mock import patch
from src.models.announcement import Announcement
from src.models.project import Project
from src.models.user import User
from src.lib.auth import get_current_user
from flask_jwt_extended import verify_jwt_in_request, create_access_token

@pytest.fixture
def instructor():
    user = User(username="instructor", email="instructor@example.com", role="instructor")
    user.save()
    return user

@pytest.fixture
def student():
    user = User(username="student", email="student@example.com", role="student")
    user.save()
    return user

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def project(instructor):
    project = Project(title="Test Project", description="Test Description", mentors=[instructor])
    project.save()
    return project

@pytest.fixture
def auth_header(instructor):
    access_token = create_access_token(identity=instructor.email)
    return {'Authorization': f'Bearer {access_token}'}

def test_instructor_create_announcement(client, instructor, project, auth_header):
    payload = {
        "title": "New Announcement",
        "content": "This is a new announcement."
    }
    with patch('src.lib.auth.get_current_user', return_value=instructor):
        response = client.post(
            f"/api/projects/{project.id}/announcements",
            data=json.dumps(payload),
            content_type="application/json",
            headers=auth_header
        )
        assert response.status_code == 201
        data = response.json
        assert data['announcement']["title"] == "New Announcement"
        assert data['announcement']["content"] == "This is a new announcement."

def test_instructor_get_announcement(client, instructor, project):
    announcement = Announcement(title="Test Announcement", content="Test Content", project=project, posted_by=instructor)
    announcement.save()
    announcement_id = announcement.id
    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=instructor):
            response = client.get(f"/api/projects/{project.id}/announcements/{announcement_id}")
            assert response.status_code == 200
            data = response.json
            assert data['announcement']["title"] == "Test Announcement"
            assert data['announcement']["content"] == "Test Content"

def test_instructor_update_announcement(client, instructor, project):
    announcement = Announcement(title="Test Announcement", content="Test Content", project=project, posted_by=instructor)
    announcement.save()
    announcement_id = announcement.id
    update_payload = {
        "title": "Updated Announcement",
        "content": "This is an updated announcement."
    }
    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=instructor):
            response = client.put(
                f"/api/projects/{project.id}/announcements/{announcement_id}",
                data=json.dumps(update_payload),
                content_type="application/json"
            )
            assert response.status_code == 200

def test_instructor_delete_announcement(client, instructor, project):
    announcement = Announcement(title="Test Announcement", content="Test Content", project=project, posted_by=instructor)
    announcement.save()
    announcement_id = announcement.id
    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=instructor):
            response = client.delete(f"/api/projects/{project.id}/announcements/{announcement_id}")
            assert response.status_code == 200

def test_student_get_announcement(client, student, project):
    announcement = Announcement(title="Test Announcement", content="Test Content", project=project, posted_by=student)
    announcement.save()
    announcement_id = announcement.id
    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=student):
            response = client.get(f"/api/projects/{project.id}/announcements/{announcement_id}")
            assert response.status_code == 200
            data = response.json
            assert data['announcement']["title"] == "Test Announcement"
            assert data['announcement']["content"] == "Test Content"

def test_student_create_announcement(client, student, project):
    payload = {
        "title": "New Announcement",
        "content": "This is a new announcement."
    }
    with patch('src.lib.auth.verify_jwt_in_request', return_value=True):
        with patch('src.lib.auth.get_current_user', return_value=student):
            response = client.post(
                f"/api/projects/{project.id}/announcements",
                data=json.dumps(payload),
                content_type="application/json"
            )
            assert response.status_code == 401

def test_student_update_announcement(client, student, project):
    announcement = Announcement(title="Test Announcement", content="Test Content", project=project, posted_by=student)
    announcement.save()
    announcement_id = announcement.id
    update_payload = {
        "title": "Updated Announcement",
        "content": "This is an updated announcement."
    }
    with patch('src.lib.auth.verify_jwt_in_request', return_value=True):
        with patch('src.lib.auth.get_current_user', return_value=student):
            response = client.put(
                f"/api/projects/{project.id}/announcements/{announcement_id}",
                data=json.dumps(update_payload),
                content_type="application/json"
            )
            assert response.status_code == 401

def test_student_delete_announcement(client, student, project):
    announcement = Announcement(title="Test Announcement", content="Test Content", project=project, posted_by=student)
    announcement.save()
    announcement_id = announcement.id
    with patch('src.lib.auth.verify_jwt_in_request', return_value=True):
        with patch('src.lib.auth.get_current_user', return_value=student):
            response = client.delete(f"/api/projects/{project.id}/announcements/{announcement_id}")
            assert response.status_code == 401