from ..db import db
import datetime

# GitHubIntegration model
class GithubIntegration(db.Document):
    team = db.ReferenceField("Team", required=True, reverse_delete_rule=db.CASCADE)  # Delete integration if team is deleted
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