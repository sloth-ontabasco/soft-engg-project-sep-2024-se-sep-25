from ..db import db
import datetime
from flask_login import UserMixin


class User(db.Document, UserMixin):
    userId = db.IntField(primary_key=True)
    username = db.StringField(max_length=64, required=True)
    email = db.StringField(max_length=120, unique=True, required=True)
    picture = db.StringField(required=True)
    role = db.ReferenceField('Role', required=True)
    created = db.DateTimeField(default=datetime.datetime.utcnow)
    updated = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            "userId": self.userId,
            "username": self.username,
            "email": self.email,
            "role": self.role.to_dict() if self.role else None,
			"picture":self.picture
        }