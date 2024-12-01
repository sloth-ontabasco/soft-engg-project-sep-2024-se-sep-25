import pytest
import json
from unittest.mock import patch
from src.models.resource import Resource
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

def test_get_resources(client, user, project):
    resource = Resource(title="Test Resource", url="http://example.com", description="Test Description", project=project)
    resource.save()
    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=user):
            response = client.get(f'/api/resource/{project.id}')
            print("response:", response.status_code)
            assert response.status_code == 200
            data = response.json
            assert isinstance(data['data'], list)
            assert data['data'][0]['title'] == "Test Resource"

def test_create_resource(client, user, project):
    payload = {
        "title": "New Resource",
        "url": "http://example.com",
        "description": "This is a description of the new resource."
    }
    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=user):
            response = client.post(
                f"/api/resource/{project.id}",
                data=json.dumps(payload),
                content_type="application/json"
            )
            print("response:", response.status_code)
            assert response.status_code == 200
            data = response.json
            assert data['data']["title"] == "New Resource"
            assert data['data']["description"] == "This is a description of the new resource."

def test_update_resource(client, user, project):
    resource = Resource(title="Test Resource", url="http://example.com", description="Test Description", project=project)
    resource.save()
    payload = {
        "title": "Updated Resource",
        "url": "http://example.com/updated",
        "description": "This is an updated description of the resource."
    }
    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=user):
            response = client.put(
                f'/api/resource/{project.id}/{resource.id}',
                data=json.dumps(payload),
                content_type="application/json"
            )
            print("response:", response.status_code)
            assert response.status_code == 200
            data = response.json
            assert data['data']["title"] == "Updated Resource"
            assert data['data']["description"] == "This is an updated description of the resource."

def test_delete_resource(client, user, project):
    resource = Resource(title="Test Resource", url="http://example.com", description="Test Description", project=project)
    resource.save()
    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=user):
            response = client.delete(f'/api/resource/{project.id}/{resource.id}')
            print("response:", response.status_code)
            assert response.status_code == 200
            assert response.json['message'] == "Resource deleted successfully"