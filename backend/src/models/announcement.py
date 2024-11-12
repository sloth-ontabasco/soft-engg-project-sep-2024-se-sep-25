from ..db import db
import datetime

class Announcement(db.Document):
    announcementId = db.IntField(primary_key=True)
    project = db.ReferenceField('Project')
    content = db.StringField(required=True)
    postedBy = db.StringField(choices=['Instructor', 'TA'], required=True)
    created = db.DateTimeField(default=datetime.datetime.utcnow)
    updated = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<Announcement {self.announcementId}>'

    def to_dict(self):
        return {
            "announcementId": self.announcementId,
            "project": str(self.project),
            "content": self.content,
            "postedBy": self.postedBy
        }