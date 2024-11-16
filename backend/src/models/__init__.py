from .user import User
from .project import Project
from .team import Team
from .resource import Resource
from .announcement import Announcement
from .github_integration import GithubIntegration
from .milestone import Milestone
from .milestone_submission import MilestoneSubmission
from .feedback import Feedback
from ..db import db

Project.register_delete_rule(Milestone, "milestones", db.CASCADE)
