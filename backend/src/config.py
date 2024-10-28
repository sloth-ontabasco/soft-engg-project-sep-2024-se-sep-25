import logging
import os
from datetime import timedelta

from dotenv import load_dotenv

logger = logging.getLogger("Config")
load_dotenv()

# CI
CI = True if os.environ.get("CI") == "true" else False
PORT = os.getenv("FLASK_PORT")

# MONGO
MONGO_URI = os.getenv("MONGO_URI")

# FRONTEND
FRONTEND_URI = os.getenv("FRONTEND_URI")

# JWT
JWT_KEY = os.getenv("JWT_KEY")


OAUTH2_PROVIDERS = {
    # Google OAuth 2.0 documentation:
    # https://developers.google.com/identity/protocols/oauth2/web-server#httprest
    'google': {
        'client_id': os.environ.get('GOOGLE_CLIENT_ID'),
        'client_secret': os.environ.get('GOOGLE_CLIENT_SECRET'),
        'authorize_url': 'https://accounts.google.com/o/oauth2/auth',
        'token_url': 'https://accounts.google.com/o/oauth2/token',
        'userinfo': {
            'url': 'https://www.googleapis.com/oauth2/v3/userinfo',
            'email': lambda json: json['email'],
        },
        'scopes': ['https://www.googleapis.com/auth/userinfo.email'],
    }
}


class Config:
    DEBUG = False
    WTF_CSRF_ENABLED = False
    MONGO_URI = MONGO_URI
    PORT = PORT
    SECRET_KEY = os.getenv("FLASK_SECRET")
    MAX_CONTENT_LENGTH = 25 * 1024 * 1024
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)


class LocalDevConfig(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = False
