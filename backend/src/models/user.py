from ..db import db
import datetime
from flask_login import UserMixin

# User model
class User(db.Document, UserMixin):
    username = db.StringField(max_length=64, required=True)
    email = db.StringField(max_length=120, unique=True, required=True)
    github_id = db.StringField()
    picture = db.URLField()
    role = db.StringField(required=True, choices=["student", "admin", "instructor", "ta"])
    status = db.IntField(default=0, choices=[(0, 'Pending'), (1, 'Approved')])
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username}>"

    def to_dict(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "email": self.email,
            "github_id": self.github_id,
            "role": self.role,
            "status": self.status,
        }