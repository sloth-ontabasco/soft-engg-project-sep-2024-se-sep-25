from ..db import db
import datetime

class TeamUser(db.Document):
    teamUserId = db.IntField(primary_key=True)
    team = db.ReferenceField('Team', required=True)
    user = db.ReferenceField('User', required=True)

    def __repr__(self):
        return f'<TeamUser Team: {self.team.teamName}, User: {self.user.username}>'

    def to_dict(self):
        return {
            "teamUserId": self.teamUserId,
            "team": str(self.team.teamId),
            "user": str(self.user.userId),
        }