import pytest
import json
from flask_jwt_extended import create_access_token
from unittest.mock import patch
from src.models.user import User
from src.lib.auth import get_current_user

@pytest.fixture
def user():
    user = User(username="testuser", email="testuser@example.com", role="admin")
    user.save()
    return user

@pytest.fixture
def auth_header(user):
    access_token = create_access_token(identity=user.email)
    return {'Authorization': f'Bearer {access_token}'}

@pytest.fixture
def client(app):
    return app.test_client()


def test_get_user_by_id(client, user, auth_header):
    user.role = "student"
    user.save()

    with patch('src.lib.auth.get_current_user', return_value=user):
        response = client.get(f'/api/users/{user.id}', headers=auth_header)
        print("Actual response:", response.json)  # Print actual response
        assert response.status_code == 200
        data = response.json
        assert data['user']['username'] == user.username
        assert data['message'] == "User found"


def test_get_all_users_as_admin(client, user, auth_header):
    with patch('src.lib.auth.get_current_user', return_value=user):
        response = client.get('/api/users', headers=auth_header)
        print("Actual response:", response.json)  # Print actual response
        assert response.status_code == 200
        data = response.json
        assert isinstance(data['users'], list)
        assert data['message'] == "Users found"


def test_get_all_users_as_non_admin(client, user, auth_header):
    user.role = "student"
    user.save()

    with patch('src.lib.auth.get_current_user', return_value=user):
        response = client.get('/api/users', headers=auth_header)
        print("Actual response:", response.json)  # Print actual response
        assert response.status_code == 403
        assert response.json['message'] == "Unauthorized access"


def test_update_user(client, user, auth_header):
    payload = {
        "username": "updateduser",
        "github_id": "newgithubid123"
    }
    with patch('src.lib.auth.get_current_user', return_value=user):
        response = client.put(
            f'/api/users/{user.id}',
            data=json.dumps(payload),
            content_type="application/json",
            headers=auth_header
        )
        print("Actual response:", response.json)  # Print actual response
        assert response.status_code == 200
        data = response.json
        assert data['user']['username'] == "updateduser"
        assert data['user']['github_id'] == "newgithubid123"
        assert data['message'] == "User updated successfully"


def test_delete_user_as_admin(client, user):
    another_user = User(username="testdelete", email="delete@example.com", role="student")  
    another_user.save()
    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=user):
            response = client.delete(f'/api/users/{another_user.id}')
            print("Actual response:", response.json)  # Print actual response
            assert response.status_code == 200
            assert response.json['message'] == "User deleted successfully"


def test_delete_user_as_non_admin(client, user):
    user.role = "student"
    user.save()

    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=user):
            response = client.delete(f'/api/users/{user.id}')
            print("Actual response:", response.json)  # Print actual response
            assert response.status_code == 401
            assert response.json['msg'] == "Role is not allowed."