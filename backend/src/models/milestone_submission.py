
from ..db import db
import datetime

class MilestoneSubmission(db.Document):
    milestoneSubmitId = db.IntField(primary_key=True)
    milestone = db.ReferenceField('Milestone')
    team = db.ReferenceField('Team')
    status = db.IntField(choices=[0, 1, 2, 3])  # 0: Not Yet Started, 1: In Progress, 2: Complete, 3: Late Submission
    submission = db.URLField()
    grade = db.StringField()
    created = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<MilestoneSubmission {self.milestoneSubmitId}>'

    def to_dict(self):
        return {
            "milestoneSubmitId": self.milestoneSubmitId,
            "milestone": str(self.milestone),
            "team": str(self.team),
            "status": self.status,
            "submission": self.submission,
            "grade": self.grade
        }