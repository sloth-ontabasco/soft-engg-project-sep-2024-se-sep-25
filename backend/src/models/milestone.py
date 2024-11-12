
from ..db import db
import datetime

class Milestone(db.Document):
    milestoneId = db.IntField(primary_key=True)
    title = db.StringField(required=True)
    description = db.StringField()
    dueDate = db.DateTimeField()
    project = db.ReferenceField('Project')
    created = db.DateTimeField(default=datetime.datetime.utcnow)
    updated = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<Milestone {self.title}>'

    def to_dict(self):
        return {
            "milestoneId": self.milestoneId,
            "title": self.title,
            "description": self.description,
            "dueDate": self.dueDate,
            "project": str(self.project)
        }