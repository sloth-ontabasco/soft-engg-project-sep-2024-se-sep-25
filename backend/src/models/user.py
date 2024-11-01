from ..db import db
import datetime
from flask_login import UserMixin


class User(db.Document, UserMixin):
    name = db.StringField(max_length=64, required=True)
    role = db.StringField(required=True)
    email = db.StringField(max_length=120, unique=True, required=True)
    # utc to keep it universal
    created = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % (self.email)
