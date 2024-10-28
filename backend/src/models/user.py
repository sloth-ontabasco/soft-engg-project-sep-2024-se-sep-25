from ..db import db
import datetime 
from enum import Enum
from flask_login import UserMixin

class User(db.Document, UserMixin):
	nickname = db.StringField( max_length=64 )
	email = db.StringField( max_length=120, unique=True, required=True )
	created = db.DateTimeField( default=datetime.datetime.utcnow ) # utc to keep it universal

	def __repr__(self):
		return '<User %r>' % ( self.nickname )


class UserType(Enum):
    ADMIN = "admin"
    MEMBER = "member"
    NONE = None
