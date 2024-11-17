from ..db import db
import datetime

# Announcement model
class Announcement(db.Document):
    project = db.ReferenceField('Project', required=True, reverse_delete_rule=db.CASCADE)
    title = db.StringField(max_length=128, required=True)
    content = db.StringField(required=True)
    posted_by = db.StringField(choices=['instructor', 'ta', 'admin'], required=True)
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Announcement for Project {self.project.title}>"
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "content": self.content,
            "posted_by": self.posted_by,
            "project": str(self.project.id),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }