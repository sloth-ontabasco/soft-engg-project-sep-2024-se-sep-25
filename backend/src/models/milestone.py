
from ..db import db
import datetime

# Milestone model
class Milestone(db.Document):
    milestone_id = db.IntField(primary_key=True)
    title = db.StringField(max_length=128, required=True)
    description = db.StringField()
    due_date = db.DateTimeField()
    project = db.ReferenceField("Project", required=True)
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Milestone {self.title}>"
    
    def to_dict(self):
        return {
            "milestone_id": self.milestone_id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "project": self.project,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }