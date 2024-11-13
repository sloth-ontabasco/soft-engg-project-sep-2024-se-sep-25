from ..db import db
import datetime

# GitHubIntegration model
class GitHubIntegration(db.Document):
    githubintegration_id = db.IntField(primary_key=True)
    team = db.ReferenceField("Team", required=True)
    repo_url = db.URLField()
    last_commit = db.DateTimeField()

    def __repr__(self):
        return f"<GitHubIntegration for Team {self.team.team_name}>"
    
    def to_dict(self):
        return {
            "team": self.team,
            "repo_url": self.repo_url,
            "last_commit": self.last_commit
        }