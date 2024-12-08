from ..db import db
import datetime

# Team model
class Team(db.Document):
    team_name = db.StringField(max_length=64, required=True)
    project_status = db.IntField(choices=[(0, 'Not Yet Started'), (1, 'In Progress'), (2, 'Complete'), (3, 'Late Submission')])
    grade = db.StringField()
    project = db.ReferenceField('Project', reverse_delete_rule=db.CASCADE) # Deletes related team if project is deleted
    members = db.ListField(db.ReferenceField('User'), reverse_delete_rule=db.PULL) # Removes User from team if User is deleted
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Team {self.team_name}>"
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "team_name": self.team_name,
            "project_status": self.project_status,
            "grade": self.grade,
            "project_id": str(self.project.id),
            "project_title": self.project.title,
            "members": [member.email for member in self.members],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.created_at else None,
        }