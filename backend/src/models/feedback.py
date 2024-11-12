from ..db import db
import datetime

class Feedback(db.Document):
    feedbackId = db.IntField(primary_key=True)
    milestone = db.ReferenceField('MilestoneSubmission')
    user = db.ReferenceField('User')
    content = db.StringField(required=True)
    postedBy = db.StringField(choices=['TA', 'Instructor'], required=True)
    created = db.DateTimeField(default=datetime.datetime.utcnow)
    updated = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<Feedback {self.feedbackId}>'

    def to_dict(self):
        return {
            "feedbackId": self.feedbackId,
            "milestone": str(self.milestone),
            "user": str(self.user),
            "content": self.content,
            "postedBy": self.postedBy
        }