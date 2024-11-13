from ..db import db
import datetime

# Announcement model
class Announcement(db.Document):
    project = db.ReferenceField("Project", required=True, reverse_delete_rule=db.CASCADE)  # Delete announcement if project is deleted
    title = db.StringField(max_length=128, required=True)
    content = db.StringField(required=True)
    posted_by = db.StringField(choices=['Instructor', 'TA'], required=True)
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Announcement for Project {self.project.title}>"
    
    def to_dict(self):
        return {
            "project": self.project,
            "content": self.content,
            "posted_by": self.posted_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }