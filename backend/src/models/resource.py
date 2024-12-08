from ..db import db
import datetime

# Resource model
class Resource(db.Document):
    project = db.ReferenceField("Project", required=True, reverse_delete_rule=db.CASCADE)  # Delete resource if project is deleted
    title = db.StringField(max_length=128, required=True)
    url = db.URLField()
    description = db.StringField()
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Resource {self.title}>"
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "project": str(self.project.id) if self.project else None,
            "title": self.title,
            "url": self.url,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,

        }