from ..db import db
import datetime

# Feedback model
class Feedback(db.Document):
    feedback_id = db.IntField(primary_key=True)
    milestone_submission = db.ReferenceField("MilestoneSubmission", required=True)
    team = db.ReferenceField("Team", required=True)
    content = db.StringField()
    posted_by = db.ReferenceField("User")
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Feedback by {self.posted_by.username}>"
    
    def to_dict(self):
        return {
            "feedback_id": self.feedback_id,
            "milestone_submission": self.milestone_submission,
            "team": self.team,
            "content": self.content,
            "posted_by": self.posted_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }