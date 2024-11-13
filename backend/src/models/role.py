from ..db import db
import datetime
from flask_login import RoleMixin

# Role model
class Role(db.Document, RoleMixin):
    name = db.StringField(required=True, choices=['Admin', 'Instructor', 'TA', 'Student'])
    description = db.StringField()
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Role {self.name}>"
    
    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }