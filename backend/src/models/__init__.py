from .user import User
from .milestone import Milestone
from .project import Project
from .team import Team
from .resource import Resource
from .announcement import Announcement
from .github_integration import GithubIntegration
from .milestone_submission import MilestoneSubmission
from .feedback import Feedback
from ..db import db

# Milestone.register_delete_rule(Project, "project", db.CASCADE)
Milestone.register_delete_rule(Project, "milestones", db.PULL)

