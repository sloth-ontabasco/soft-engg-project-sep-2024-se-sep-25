import pytest
import json
from unittest.mock import patch
from src.models.milestone import Milestone
from src.models.project import Project
from src.models.user import User
from src.lib.auth import get_current_user

@pytest.fixture
def user():
    user = User(username="testuser", email="testuser@example.com", role="admin")
    user.save()
    return user

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def project(user):
    project = Project(title="Test Project", description="Test Description", mentors=[user])
    project.save()
    return project

def test_get_milestone(client, user, project):
    milestone = Milestone(title="Test Milestone", description="Test Description", project=project)
    milestone.save()
    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=user):
            response = client.get(f'/api/milestones/{milestone.id}')
            print("response:", response.status_code)
            assert response.status_code == 200
            data = response.json
            assert data['data']['title'] == "Test Milestone"

def test_create_milestone(client, user, project):
    payload = {
        "title": "New Milestone",
        "description": "This is a description of the new milestone.",
        "due_date": "12/31/24 23:59:59"
    }
    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=user):
            response = client.post(
                f"/api/project/milestones/{project.id}",
                data=json.dumps(payload),
                content_type="application/json"
            )
            print("response:", response.status_code)
            assert response.status_code == 200
            data = response.json
            assert data['data']["title"] == "New Milestone"
            assert data['data']["description"] == "This is a description of the new milestone."

def test_update_milestone(client, user, project):
    milestone = Milestone(title="Test Milestone", description="Test Description", project=project)
    milestone.save()
    payload = {
        "title": "Updated Milestone",
        "description": "This is an updated description of the milestone.",
        "due_date": "01/01/25 23:59:59"
    }
    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=user):
            response = client.put(
                f'/api/milestones/{project.id}/{milestone.id}',
                data=json.dumps(payload),
                content_type="application/json"
            )
            print("response:", response.status_code)
            assert response.status_code == 200
            data = response.json
            assert data['data']["title"] == "Updated Milestone"
            assert data['data']["description"] == "This is an updated description of the milestone."

def test_delete_milestone(client, user, project):
    milestone = Milestone(title="Test Milestone", description="Test Description", project=project)
    milestone.save()
    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=user):
            response = client.delete(f'/api/milestones/{project.id}/{milestone.id}')
            print("response:", response.status_code)
            assert response.status_code == 200
            assert response.json['message'] == "Milestone deleted successfully"

def test_get_milestones_by_project(client, user, project):
    milestone = Milestone(title="Test Milestone", description="Test Description", project=project)
    milestone.save()
    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=user):
            response = client.get(f'/api/project/milestones/{project.id}')
            print("response:", response.status_code)
            assert response.status_code == 200
            data = response.json
            assert isinstance(data['data'], list)
            assert data['data'][0]['title'] == "Test Milestone"