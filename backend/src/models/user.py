from ..db import db
import datetime
from flask_login import UserMixin

# User model
class User(db.Document, UserMixin):
    username = db.StringField(max_length=64, required=True)
    email = db.StringField(max_length=120, unique=True, required=True)
    github_id = db.StringField()
    role = db.ReferenceField('Role', reverse_delete_rule=db.DENY) # Prevent deletion if still assigned to a User
    status = db.IntField(default=0, choices=[(0, 'Pending'), (1, 'Approved')])
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username}>"

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "github_id": self.github_id,
            "role": self.role.name if self.role else None,
            "status": self.status,
        }