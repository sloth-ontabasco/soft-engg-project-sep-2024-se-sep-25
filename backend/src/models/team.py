from ..db import db
import datetime

class Team(db.Document):
    teamId = db.IntField(primary_key=True)
    teamName = db.StringField(max_length=100, required=True)
    grade = db.StringField()
    created = db.DateTimeField(default=datetime.datetime.utcnow)
    updated = db.DateTimeField(default=datetime.datetime.utcnow)
    project = db.ReferenceField('Project')

    def __repr__(self):
        return f'<Team {self.teamName}>'

    def to_dict(self):
        return {
            "teamId": self.teamId,
            "teamName": self.teamName,
            "grade": self.grade,
            "project": str(self.project)
        }