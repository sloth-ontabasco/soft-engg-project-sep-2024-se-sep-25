from ..db import db
import datetime

# Project model
class Project(db.Document):
    project_id = db.IntField(primary_key=True)
    title = db.StringField(max_length=128, required=True)
    description = db.StringField()
    deadline = db.DateTimeField()
    mentors = db.ListField(db.ReferenceField('User'))
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Project {self.title}>"
    
    def to_dict(self):
        return {
            "project_id": self.project_id,
            "title": self.title,
            "description": self.description,
            "deadline": self.deadline,
            "mentors": self.mentors,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }