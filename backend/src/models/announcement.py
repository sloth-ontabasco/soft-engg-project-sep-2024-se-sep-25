from ..db import db
import datetime

# Announcement model
class Announcement(db.Document):
    project = db.ReferenceField('Project', required=True, reverse_delete_rule=db.CASCADE)
    title = db.StringField(max_length=128, required=True)
    content = db.StringField(required=True)
    posted_by = db.ReferenceField('User', reverse_delete_rule=db.CASCADE, required=True)
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Announcement for Project {self.project.title}>"
    
    def to_dict(self):
        print(f"Converting Announcement {self.id} to dict")
        return {
            "id": str(self.id),
            "title": self.title,
            "content": self.content,
            "posted_by": str(self.posted_by.username),
            "project_id": str(self.project.id),
            "project_title": self.project.title,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }