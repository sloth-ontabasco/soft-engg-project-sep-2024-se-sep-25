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
            "title": self.title,
            "description": self.description,
            "deadline": self.deadline.strftime("%m/%d/%y %H:%M:%S") if self.deadline else None,
            # "deadline": self.deadline.isoformat() if self.deadline else None,
            # "mentors": self.mentors,
            "mentors": [str(mentor.id) for mentor in self.mentors],
            "created_at": self.created_at.strftime("%m/%d/%y %H:%M:%S") if self.deadline else None,
            "updated_at": self.updated_at.strftime("%m/%d/%y %H:%M:%S") if self.deadline else None,
            "milestones": self.milestones
        }