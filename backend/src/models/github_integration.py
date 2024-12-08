from ..db import db
import datetime
from mongoengine import *

class SaveCommitHistory(EmbeddedDocument):
    sha = StringField(required=True)
    message = StringField(required=True)
    author = StringField()
    date = DateTimeField()

# GitHubIntegration model
class GithubIntegration(db.Document):
    team = db.ReferenceField("Team", required=True, reverse_delete_rule=db.CASCADE)  # Delete integration if team is deleted
    token = db.StringField()
    repo_url = db.URLField()
    last_commit = db.ListField(EmbeddedDocumentField(SaveCommitHistory))
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
            "last_commit": [commit.to_mongo() for commit in self.last_commit],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    def save_commits(self, repo_commits):
        """
        Save or update commits for the repository.
        :param repo_commits: List of commits with keys `sha`, `message`, `author`, `date`.
        """
        if not isinstance(self.last_commit, list):
            self.last_commit = []

        for commit in repo_commits:
            existing_commit = next((c for c in self.last_commit if c.sha == commit['sha']), None)
            if not existing_commit:
                # Add new commit
                self.last_commit.append(
                    SaveCommitHistory(
                        sha=commit['sha'],
                        message=commit['message'],
                        author=commit['author'],
                        date=datetime.datetime.fromisoformat(commit['date']) if commit['date'] else None
                    )
                )
        self.updated_at = datetime.datetime.utcnow()
        self.save()