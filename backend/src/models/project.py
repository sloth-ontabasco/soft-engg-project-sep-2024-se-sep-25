from ..db import db
import datetime

class Project(db.Document):
    projectId = db.IntField(primary_key=True)
    title = db.StringField(required=True)
    type = db.StringField(choices=['Team', 'Individual'], required=True)
    description = db.StringField()
    deadline = db.DateTimeField()
    status = db.IntField(choices=[0, 1, 2, 3])  # 0: Not Yet Started, 1: In Progress, 2: Complete, 3: Late Submission
    team = db.ReferenceField('Team')
    created = db.DateTimeField(default=datetime.datetime.utcnow)
    updated = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<Project {self.title}>'

    def to_dict(self):
        return {
            "projectId": self.projectId,
            "title": self.title,
            "type": self.type,
            "description": self.description,
            "deadline": self.deadline,
            "status": self.status,
            "team": str(self.team)
        }