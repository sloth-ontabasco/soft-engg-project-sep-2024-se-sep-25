from ..db import db
import datetime

# Feedback model
class Feedback(db.Document):
    milestone_submission = db.ReferenceField("MilestoneSubmission", required=True, reverse_delete_rule=db.CASCADE)  # Delete feedback if submission is deleted
    team = db.ReferenceField('Team', reverse_delete_rule=db.CASCADE)  # Delete feedback if team is deleted
    content = db.StringField()
    posted_by = db.ReferenceField('User', reverse_delete_rule=db.CASCADE)  # Delete feedback if User who posted it is deleted
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Feedback by {self.posted_by.username}>"
    
    def to_dict(self):
        return {
            "milestone_submission": self.milestone_submission,
            "team": self.team,
            "content": self.content,
            "posted_by": self.posted_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }