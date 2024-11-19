from ..db import db
import datetime

# Project model
class Project(db.Document):
    title = db.StringField(max_length=128, required=True)
    description = db.StringField()
    deadline = db.DateTimeField()
    mentors = db.ListField(db.ReferenceField('User'), reverse_delete_rule=db.PULL)
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.datetime.utcnow)
    milestones = db.ListField(db.ReferenceField('Milestone'))

    def __repr__(self):
        return f"<Project {self.title}>"
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "mentors": [str(mentor.id) for mentor in self.mentors],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "milestones": [str(milestone.id) for milestone in self.milestones]
        }