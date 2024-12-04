import pytest
from unittest.mock import patch
from datetime import datetime, timedelta
from bson import ObjectId
from src.models.project import Project
from src.models.milestone import Milestone
from src.models.team import Team
from src.models.milestone_submission import MilestoneSubmission 
from src.models.user import User

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
def milestones(project):
    milestone1 = Milestone(
        title="Milestone 1",
        project=project,
        due_date=datetime.utcnow() - timedelta(days=10)
    )
    milestone1.save()

    milestone2 = Milestone(
        title="Milestone 2",
        project=project,
        due_date=datetime.utcnow() + timedelta(days=5)
    )
    milestone2.save()

    return [milestone1, milestone2]


@pytest.fixture
def team(project, user):
    team = Team(team_name="Test Team", project=project, members=[user])
    team.save()
    return team


@pytest.fixture
def milestone_submissions(milestones, team):
    milestone1, milestone2 = milestones

    # Previous milestone submissions
    submission1 = MilestoneSubmission(milestone=milestone1, team=team, status=3)  # Late
    submission2 = MilestoneSubmission(milestone=milestone1, team=team, status=2)  # On-time
    submission1.save()
    submission2.save()

    # Current milestone submissions
    submission3 = MilestoneSubmission(milestone=milestone2, team=team, status=3)  # Late
    submission4 = MilestoneSubmission(milestone=milestone2, team=team, status=2)  # On-time
    submission3.save()
    submission4.save()

    return [submission1, submission2, submission3, submission4]


@pytest.fixture
def client(app):
    return app.test_client()


def test_get_analytics_success(client, project, team, milestones, milestone_submissions, user):
    user.role = "admin"
    user.save()

    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=user):
            response = client.get(f'/api/{project.id}/analytics')
            print("Actual response:", response.json)  # Print actual response
            assert response.status_code == 200
            data = response.json['data']
            assert data['total_students'] == len(team.members)
            assert 'late_submission_change' in data
            assert 'days_till_due' in data
            assert 'submissions_by_milestone' in data
            assert len(data['submissions_by_milestone']) == len(milestones)


def test_get_analytics_no_milestones(client, project, user):
    user.role = "admin"
    user.save()

    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=user):
            response = client.get(f'/api/{project.id}/analytics')
            print("Actual response:", response.json)  # Print actual response
            assert response.status_code == 404
            assert response.json['message'] == "No milestones found for this project"


def test_get_analytics_invalid_project(client, user):
    user.role = "admin"
    user.save()

    invalid_project_id = str(ObjectId())

    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=user):
            response = client.get(f'/api/{invalid_project_id}/analytics')
            print("Actual response:", response.json)  # Print actual response
            assert response.status_code == 404
            assert response.json['message'] == "Project not found"


def test_get_analytics_non_admin_user(client, project, user):
    user.role = "student"
    user.save()

    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=user):
            response = client.get(f'/api/{project.id}/analytics')
            print("Actual response:", response.json)  # Print actual response
            assert response.status_code == 401
            assert response.json['msg'] == "Role is not allowed."


def test_get_analytics_no_submissions(client, project, milestones, user):
    user.role = "admin"
    user.save()

    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=user):
            response = client.get(f'/api/{project.id}/analytics')
            print("Actual response:", response.json)  # Print actual response
            assert response.status_code == 200
            data = response.json['data']
            assert data['total_students'] == 0  # No teams created
            assert data['late_submission_change'] is None
            assert 'submissions_by_milestone' in data
            assert len(data['submissions_by_milestone']) == len(milestones)


def test_get_analytics_late_submission_change(client, project, team, milestones, milestone_submissions, user):
    user.role = "admin"
    user.save()

    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=user):
            response = client.get(f'/api/{project.id}/analytics')
            print("Actual response:", response.json)  # Print actual response
            assert response.status_code == 200
            data = response.json['data']
            assert data['late_submission_change'] is not None
            assert isinstance(data['late_submission_change'], float)