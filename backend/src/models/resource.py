from ..db import db
import datetime

class Resource(db.Document):
    resourceId = db.IntField(primary_key=True)
    project = db.ReferenceField('Project')
    title = db.StringField(required=True)
    url = db.URLField(required=True)
    description = db.StringField()
    created = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<Resource {self.title}>'

    def to_dict(self):
        return {
            "resourceId": self.resourceId,
            "project": str(self.project),
            "title": self.title,
            "url": self.url,
            "description": self.description
        }