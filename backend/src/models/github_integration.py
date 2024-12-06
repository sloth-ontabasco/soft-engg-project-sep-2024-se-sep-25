from ..db import db
import datetime

# GitHubIntegration model
class GithubIntegration(db.Document):
    team = db.ReferenceField("Team", required=True, reverse_delete_rule=db.CASCADE)  # Delete integration if team is deleted
    token = db.StringField()
    repo_url = db.URLField()
    last_commit = db.DateTimeField()
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<GitHubIntegration for Team {self.team.team_name}>"
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "team_name": self.team.team_name,
            "team_id": str(self.team.id),
            "token": self.token,
            "repo_url": self.repo_url,
            "last_commit": self.last_commit.isoformat(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
