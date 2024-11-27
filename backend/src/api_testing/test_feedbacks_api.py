import pytest
import json
from unittest.mock import patch
from src.models.feedback import Feedback
from src.models.milestone_submission import MilestoneSubmission
from src.models.milestone import Milestone
from src.models.project import Project
from src.models.team import Team
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
def team(project):
    team = Team(team_name="Test Team", project=project)
    team.save()
    return team

@pytest.fixture
def milestone(project):
    milestone = Milestone(title="Test Milestone", description="Test Description", project=project)
    milestone.save()
    return milestone

@pytest.fixture
def milestone_submission(milestone, team):
    milestone_submission = MilestoneSubmission(milestone=milestone, team=team)
    milestone_submission.save()
    return milestone_submission

@pytest.fixture
def auth_header(instructor):
    access_token = create_access_token(identity=instructor.email)
    return {'Authorization': f'Bearer {access_token}'}

def test_instructor_create_feedback(client, instructor, project, milestone_submission, auth_header):
    payload = {
        "content": "This is a new feedback."
    }
    with patch('src.lib.auth.get_current_user', return_value=instructor):
        response = client.post(
            f"/api/projects/{project.id}/milestones/{milestone_submission.milestone.id}" + 
            f"/submissions/{milestone_submission.id}/feedbacks",
            data=json.dumps(payload),
            content_type="application/json",
            headers=auth_header
        )
        assert response.status_code == 201
        data = response.json
        assert data['feedback']["content"] == "This is a new feedback."

def test_instructor_get_feedback(client, instructor, project, milestone_submission):
    feedback = Feedback(content="Test Feedback", milestone_submission=milestone_submission, 
                        team=milestone_submission.team, posted_by=instructor)
    feedback.save()
    feedback_id = feedback.id
    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=instructor):
            response = client.get(f"/api/projects/{project.id}/milestones/" +
                                  f"{milestone_submission.milestone.id}/submissions/" +
                                  f"{milestone_submission.id}/feedbacks/{feedback_id}")
            assert response.status_code == 200
            data = response.json
            assert data['feedback']["content"] == "Test Feedback"

def test_instructor_update_feedback(client, instructor, project, milestone_submission):
    feedback = Feedback(content="Test Feedback", milestone_submission=milestone_submission, 
                        team=milestone_submission.team, posted_by=instructor)
    feedback.save()
    feedback_id = feedback.id
    update_payload = {
        "content": "This is an updated feedback."
    }
    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=instructor):
            response = client.put(
                f"/api/projects/{project.id}/milestones/{milestone_submission.milestone.id}"
                + f"/submissions/{milestone_submission.id}/feedbacks/{feedback_id}",
                data=json.dumps(update_payload),
                content_type="application/json"
            )
            assert response.status_code == 200
            
def test_instructor_delete_feedback(client, instructor, project, milestone_submission):
    feedback = Feedback(content="Test Feedback", milestone_submission=milestone_submission, 
                        team=milestone_submission.team, posted_by=instructor)
    feedback.save()
    feedback_id = feedback.id
    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=instructor):
            response = client.delete(f"/api/projects/{project.id}/milestones/"
                                     + f"{milestone_submission.milestone.id}/submissions/"
                                     + f"{milestone_submission.id}/feedbacks/{feedback_id}")
            assert response.status_code == 200

def test_student_get_feedback(client, student, project, milestone_submission):
    feedback = Feedback(content="Test Feedback", milestone_submission=milestone_submission, 
                        team=milestone_submission.team, posted_by=student)
    feedback.save()
    feedback_id = feedback.id
    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=student):
            response = client.get(f"/api/projects/{project.id}/milestones/"
                                  + f"{milestone_submission.milestone.id}/submissions/"
                                  + f"{milestone_submission.id}/feedbacks/{feedback_id}")
            assert response.status_code == 200
            data = response.json
            assert data['feedback']["content"] == "Test Feedback"

def test_student_create_feedback(client, student, project, milestone_submission):
    payload = {
        "content": "This is a new feedback."
    }
    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=student):
            response = client.post(
                f"/api/projects/{project.id}/milestones/{milestone_submission.milestone.id}"
                + f"/submissions/{milestone_submission.id}/feedbacks",
                data=json.dumps(payload),
                content_type="application/json"
            )
            assert response.status_code == 401

def test_student_update_feedback(client, student, project, milestone_submission):
    feedback = Feedback(content="Test Feedback", milestone_submission=milestone_submission, 
                        team=milestone_submission.team, posted_by=student)
    feedback.save()
    feedback_id = feedback.id
    update_payload = {
        "content": "This is an updated feedback."
    }
    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=student):
            response = client.put(
                f"/api/projects/{project.id}/milestones/{milestone_submission.milestone.id}"
                + f"/submissions/{milestone_submission.id}/feedbacks/{feedback_id}",
                data=json.dumps(update_payload),
                content_type="application/json"
            )
            assert response.status_code == 401

def test_student_delete_feedback(client, student, project, milestone_submission):
    feedback = Feedback(content="Test Feedback", milestone_submission=milestone_submission, 
                        team=milestone_submission.team, posted_by=student)
    feedback.save()
    feedback_id = feedback.id
    with patch('src.lib.auth.verify_jwt_in_request'):
        with patch('src.lib.auth.get_current_user', return_value=student):
            response = client.delete(f"/api/projects/{project.id}/milestones/"
                                     + f"{milestone_submission.milestone.id}/submissions/"
                                     + f"{milestone_submission.id}/feedbacks/{feedback_id}")
            assert response.status_code == 401
