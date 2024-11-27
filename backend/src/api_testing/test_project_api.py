
import pytest
import json
from unittest.mock import patch
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

def test_get_projects(client, user):
    """Test the GET /api/projects endpoint."""
    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=user):
            response = client.get("/api/project")
            print("response:", response.status_code)
            assert response.status_code == 200
            data = response.json
            assert isinstance(data['data'], list)

def test_create_project(client, user):
    """Test the POST /api/projects endpoint."""
    payload = {
        "title": "Test Project",
        "description": "A test project description",
        "deadline": "12/31/24 23:59:59",
        "mentors": [str(user.id)]
    }
    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=user):
            response = client.post(
                "/api/project",
                data=json.dumps(payload),
                content_type="application/json"
            )
            print("response:", response.status_code)
            assert response.status_code == 200
            data = response.json
            assert data['data']["title"] == "Test Project"
            assert data['data']["description"] == "A test project description"

def test_invalid_project_creation(client, user):
    """Test creating a project with invalid data."""
    payload = {
        "description": "Missing required title field",
    }
    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=user):
            response = client.post(
                "/api/project",
                data=json.dumps(payload),
                content_type="application/json"
            )
            print("response:", response.status_code)
            assert response.status_code == 400
            data = response.json
            assert "message" in data

def test_get_project_by_id(client, user):
    project = Project(title="Test Project", description="Test Description", mentors=[user])
    project.save()
    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=user):
            response = client.get(f'/api/project/{project.id}')
            print("response:", response.status_code)
            assert response.status_code == 200
            assert response.json['data']['title'] == "Test Project"

def test_delete_project(client, user):
    project = Project(title="Test Project", description="Test Description", mentors=[user])
    project.save()
    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=user):
            response = client.delete(f'/api/project/{project.id}')
            print("response:", response.status_code)
            assert response.status_code == 200
            assert response.json['message'] == "Project deleted successfully"

def test_get_projects_by_user(client, user):
    project = Project(title="Test Project", description="Test Description", mentors=[user])
    project.save()
    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=user):
            response = client.get(f'/api/project/user/{user.id}')
            print("response:", response.status_code)
            assert response.status_code == 200
            assert isinstance(response.json['data'], list)
            assert response.json['data'][0]['title'] == "Test Project"

def test_update_project(client, user):
    """Test the PUT /api/project/<project_id> endpoint."""
    project = Project(title="Test Project", description="Test Description", mentors=[user])
    project.save()
    payload = {
        "title": "Updated Project",
        "description": "An updated project description",
        "deadline": "01/01/25 23:59:59",
        "mentors": [str(user.id)]
    }
    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=user):
            response = client.put(
                f'/api/project/{project.id}',
                data=json.dumps(payload),
                content_type="application/json"
            )
            print("response:", response.status_code)
            assert response.status_code == 200
            data = response.json
            assert data['data']["title"] == "Updated Project"
            assert data['data']["description"] == "An updated project description"