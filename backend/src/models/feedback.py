from ..db import db
import datetime

# Feedback model
class Feedback(db.Document):
    milestone_submission = db.ReferenceField("MilestoneSubmission", required=True, reverse_delete_rule=db.CASCADE)
    team = db.ReferenceField('Team', reverse_delete_rule=db.CASCADE, required=True)
    content = db.StringField(required=True)
    posted_by = db.ReferenceField('User', reverse_delete_rule=db.CASCADE, required=True)
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Feedback by {self.posted_by.username}>"
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "project_title": str(self.milestone_submission.milestone.project.title),
            "project_id": str(self.milestone_submission.milestone.project.id),
            "milestone_title": str(self.milestone_submission.milestone.title),
            "milestone_id": str(self.milestone_submission.milestone.id),
            "team_name": str(self.team.team_name),
            "team_id": str(self.team.id),
            "content": self.content,
            "posted_by": str(self.posted_by.username),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }