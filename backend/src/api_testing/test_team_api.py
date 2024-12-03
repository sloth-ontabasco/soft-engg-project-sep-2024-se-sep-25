import pytest
import json
from bson import ObjectId
from flask_jwt_extended import create_access_token
from unittest.mock import patch
from src.models.user import User
from src.models.project import Project
from src.models.team import Team


@pytest.fixture
def user():
    user = User(username="testuser", email="testuser@example.com", role="admin")
    user.save()
    return user

@pytest.fixture
def project():
    project = Project(title="Test Project")
    project.save()
    return project

@pytest.fixture
def team(project, user):
    team = Team(team_name="Test Team", project=project, members=[user])
    team.save()
    return team


@pytest.fixture
def auth_header(user):
    access_token = create_access_token(identity=user.email)
    return {'Authorization': f'Bearer {access_token}'}


@pytest.fixture
def client(app):
    return app.test_client()


def test_get_teams_as_admin(client, project, user, auth_header):
    user.role = "admin"
    user.save()

    another_team = Team(team_name="Another Team", project=project, members=[user])
    another_team.save()

    # Create an additional team to ensure there are two teams
    additional_team = Team(team_name="Additional Team", project=project, members=[user])
    additional_team.save()

    with patch('src.lib.auth.get_current_user', return_value=user):
        response = client.get(f'/api/{project.id}/teams', headers=auth_header)
        print("Actual response:", response.json)  # Print actual response
        assert response.status_code == 200
        data = response.json
        assert isinstance(data['teams'], list)
        assert len(data['teams']) == 2
        assert data['message'] == "Teams found"


def test_get_team_as_student(client, project, user, auth_header):
    user.role = "student"
    user.save()

    team = Team(team_name="Student's Team", project=project, members=[user])
    team.save()

    with patch('src.lib.auth.get_current_user', return_value=user):
        response = client.get(f'/api/{project.id}/teams', headers=auth_header)
        print("Actual response:", response.json)  # Print actual response
        assert response.status_code == 200
        data = response.json
        assert data['team']['team_name'] == "Student's Team"
        assert data['message'] == "Team found"


def test_create_team(client, project, user):
    user.role = "admin"
    user.save()

    payload = {
        "team_name": "New Team",
        "members": [user.email]
    }

    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=user):
            response = client.post(
                f'/api/{project.id}/teams',
                data=json.dumps(payload),
                content_type="application/json"
            )
            print("Actual response:", response.json)  # Print actual response
            assert response.status_code == 201
            data = response.json
            assert data['team']['team_name'] == "New Team"
            assert data['message'] == "Team created successfully"


def test_update_team(client, project, team, user):
    user.role = "admin"
    user.save()

    payload = {
        "team_name": "Updated Team",
        "members": [user.email]
    }

    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=user):
            response = client.put(
                f'/api/{project.id}/teams/{team.id}',
                data=json.dumps(payload),
                content_type="application/json"
            )
            print("Actual response:", response.json)  # Print actual response
            assert response.status_code == 200
            data = response.json
            assert data['team']['team_name'] == "Updated Team"
            assert data['message'] == "Team updated successfully"


def test_delete_team(client, project, team, user):
    user.role = "admin"
    user.save()

    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=user):
            response = client.delete(f'/api/{project.id}/teams/{team.id}')
            print("Actual response:", response.json)  # Print actual response
            assert response.status_code == 200
            assert response.json['message'] == "Team deleted successfully"


def test_create_team_missing_fields(client, project, user):
    user.role = "admin"
    user.save()

    payload = {
        # Missing "team_name" and "members"
    }

    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=user):
            response = client.post(
                f'/api/{project.id}/teams',
                data=json.dumps(payload),
                content_type="application/json"
            )
            print("Actual response:", response.json)  # Print actual response
            assert response.status_code == 400
            assert response.json['message'] == "Missing required fields: team_name, members"


def test_get_teams_invalid_project(client, user):
    user.role = "admin"
    user.save()

    invalid_project_id = ObjectId()

    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=user):
            response = client.get(f'/api/{invalid_project_id}/teams')
            print("Actual response:", response.json)  # Print actual response
            assert response.status_code == 404
            assert response.json['message'] == "Project not found"
