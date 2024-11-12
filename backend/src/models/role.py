from ..db import db
import datetime
from flask_login import RoleMixin

class Role(db.Document, RoleMixin):
    roleId = db.IntField(primary_key=True)
    name = db.StringField(choices=['Admin', 'Instructor', 'TA', 'Student'], required=True)
    description = db.StringField()
    created = db.DateTimeField(default=datetime.datetime.utcnow)
    updated = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<Role {self.name}>'

    def to_dict(self):
        return {
            "roleId": self.roleId,
            "name": self.name,
            "description": self.description
        }