from ..db import db
import datetime
from flask_login import UserMixin


class User(db.Document, UserMixin):
	name = db.StringField(max_length=64, required=True)
	role = db.StringField(required=True, choices=['administrator','student','instructor','ta'])
	email = db.StringField(max_length=120, unique=True, required=True)
    # utc to keep it universal
	created = db.DateTimeField(default=datetime.datetime.utcnow)
	picture = db.StringField(required=True)

	def __repr__(self):
		return '<User %r>' % (self.email)

	def to_dict(self):
		return {
			"name":self.name,
			"role":self.role,
			"email":self.email,
			"picture":self.picture
		}
