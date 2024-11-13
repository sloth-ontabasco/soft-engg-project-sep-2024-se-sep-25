from ..db import db
import datetime

# MilestoneSubmission model
class MilestoneSubmission(db.Document):
    milestone = db.ReferenceField("Milestone", required=True, reverse_delete_rule=db.CASCADE)  # Delete submission if milestone is deleted
    team = db.ReferenceField('Team', reverse_delete_rule=db.CASCADE)  # Delete submission if team is deleted
    status = db.IntField(choices=[(0, 'Not Yet Started'), (1, 'In Progress'), (2, 'Complete'), (3, 'Late Submission')])
    submission = db.FileField()
    grade = db.StringField()
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<MilestoneSubmission for Milestone {self.milestone.title}>"
    
    def to_dict(self):
        return {
            "milestone": self.milestone,
            "team": self.team,
            "status": self.status,
            "submission": self.submission,
            "grade": self.grade,
            "created_at": self.created_at
        }