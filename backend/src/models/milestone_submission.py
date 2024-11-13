
from ..db import db
import datetime

# MilestoneSubmission model
class MilestoneSubmission(db.Document):
    milestone_submission_id = db.IntField(primary_key=True)
    milestone = db.ReferenceField("Milestone", required=True)
    team = db.ReferenceField("Team", required=True)
    status = db.IntField(choices=[(0, 'Not Yet Started'), (1, 'In Progress'), (2, 'Complete'), (3, 'Late Submission')])
    submission = db.URLField()
    grade = db.StringField()
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<MilestoneSubmission for Milestone {self.milestone.title}>"
    
    def to_dict(self):
        return {
            "milestone_submission_id": self.milestone_submission_id,
            "milestone": self.milestone,
            "team": self.team,
            "status": self.status,
            "submission": self.submission,
            "grade": self.grade,
            "created_at": self.created_at
        }