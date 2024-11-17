from ..db import db
import datetime

# MilestoneSubmission model
class MilestoneSubmission(db.Document):
    milestone = db.ReferenceField("Milestone", required=True, reverse_delete_rule=db.CASCADE)
    team = db.ReferenceField('Team', reverse_delete_rule=db.CASCADE)
    status = db.IntField(choices=[(0, 'Not Yet Started'), (1, 'In Progress'), (2, 'Complete'), (3, 'Late Submission')])
    submission = db.FileField()
    grade = db.StringField()
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<MilestoneSubmission for Milestone {self.milestone.title}>"
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "project": str(self.milestone.project.title),
            "milestone": str(self.milestone.title),
            "team": str(self.team.team_name),
            "status": self.status,
            "submission": str(self.submission.id) if self.submission else None,
            "grade": self.grade,
            "created_at": self.created_at.isoformat()
        }

    def upload_file(self, file):
        self.submission.put(file)
        self.save()

    def download_file(self):
        return self.submission.read()

    def delete_file(self):
        self.submission.delete()
        self.save()