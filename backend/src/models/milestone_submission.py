from ..db import db
import datetime
import hashlib

# MilestoneSubmission model
class MilestoneSubmission(db.Document):
    milestone = db.ReferenceField("Milestone", required=True, reverse_delete_rule=db.CASCADE)  # Delete submission if milestone is deleted
    team = db.ReferenceField('Team', reverse_delete_rule=db.CASCADE)  # Delete submission if team is deleted
    status = db.IntField(choices=[(0, 'Not Yet Started'), (1, 'In Progress'), (2, 'Complete'), (3, 'Late Submission')])
    submission = db.FileField()
    grade = db.StringField(choices=['A', 'B', 'C', 'D', 'F'])
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<MilestoneSubmission for Milestone {self.milestone.title}>"
    
    def to_dict(self):
        submission_id = None
        # if self.submission:
        #     file_data = self.submission.read()
        #     sha256_hash = hashlib.sha256(file_data).hexdigest()
        #     submission_id = sha256_hash

        return {
            "id": str(self.id),
            "project_title": self.milestone.project.title,
            "project_id": str(self.milestone.project.id),
            "milestone_title": self.milestone.title,
            "milestone_description": self.milestone.description,
            "milestone_id": str(self.milestone.id),
            "team_name": self.team.team_name,
            "team_id": str(self.team.id),
            "status": self.status,
            "submission_id": submission_id,
            "grade": self.grade,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }