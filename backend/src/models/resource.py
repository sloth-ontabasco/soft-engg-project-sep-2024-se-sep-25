from ..db import db
import datetime

# Resource model
class Resource(db.Document):
    resource_id = db.IntField(primary_key=True)
    project = db.ReferenceField("Project", required=True)
    title = db.StringField(max_length=128, required=True)
    url = db.URLField()
    description = db.StringField()
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Resource {self.title}>"
    
    def to_dict(self):
        return {
            "resource_id": self.resource_id,
            "project": self.project,
            "title": self.title,
            "url": self.url,
            "description": self.description,
            "created_at": self.created_at
        }