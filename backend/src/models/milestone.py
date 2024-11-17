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
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "project_title": self.project.title,
            "project_id": str(self.project.id),
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }