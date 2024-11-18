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
    updated_at = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<MilestoneSubmission for Milestone {self.milestone.title}>"
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "project_title": self.milestone.project.title,
            "project_id": str(self.milestone.project.id),
            "milestone_title": self.milestone.title,
            "milestone_id": str(self.milestone.id),
            "team_name": self.team.team_name,
            "team_id": str(self.team.id),
            "status": self.status,
            "submission_id": str(self.submission.id) if self.submission else None,
            "grade": self.grade,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }