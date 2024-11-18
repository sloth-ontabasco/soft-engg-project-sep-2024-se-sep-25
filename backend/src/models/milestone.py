from ..db import db
import datetime

# Milestone model
class Milestone(db.Document):
    title = db.StringField(max_length=128, required=True)
    description = db.StringField()
    due_date = db.DateTimeField()
    project = db.ReferenceField("Project", required=True, reverse_delete_rule=db.CASCADE)  # Delete milestone if project is deleted
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Milestone {self.title}>"
    
    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "project": str(self.project.id) if self.project else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }