from ..db import db
import datetime

# Team model
class Team(db.Document):
    team_id = db.IntField(primary_key=True)
    team_name = db.StringField(max_length=64, required=True)
    project_status = db.IntField(choices=[(0, 'Not Yet Started'), (1, 'In Progress'), (2, 'Complete'), (3, 'Late Submission')])
    grade = db.StringField()
    project = db.ReferenceField('Project')
    members = db.ListField(db.ReferenceField('User'))
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Team {self.team_name}>"
    
    def to_dict(self):
        return {
            "team_id": self.team_id,
            "team_name": self.team_name,
            "project_status": self.project_status,
            "grade": self.grade,
            "project": self.project,
            "members": self.members,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }