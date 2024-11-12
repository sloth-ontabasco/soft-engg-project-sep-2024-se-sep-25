from ..db import db
import datetime

class GitHubIntegration(db.Document):
    repoId = db.IntField(primary_key=True)
    project = db.ReferenceField('Project')
    repoUrl = db.URLField(required=True)
    lastCommit = db.DateTimeField()
    commitHistory = db.StringField()

    def __repr__(self):
        return f'<GitHubIntegration {self.repoId}>'

    def to_dict(self):
        return {
            "repoId": self.repoId,
            "project": str(self.project),
            "repoUrl": self.repoUrl,
            "lastCommit": self.lastCommit,
            "commitHistory": self.commitHistory
        }