from ..db import db
import datetime

# Project model
class Project(db.Document):
    title = db.StringField(max_length=128, required=True)
    description = db.StringField()
    deadline = db.DateTimeField()
    mentors = db.ListField(db.ReferenceField('User'), reverse_delete_rule=db.PULL) # Removes User from Project if User is deleted
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.datetime.utcnow)
    milestones = db.ListField(db.ReferenceField('Milestone', reverse_delete_rule=db.CASCADE))  # Cascade deletes milestones when project is deleted

    def __repr__(self):
        return f"<Project {self.title}>"
    
    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "deadline": self.deadline,
            "mentors": self.mentors,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "milestones": self.milestones
        }