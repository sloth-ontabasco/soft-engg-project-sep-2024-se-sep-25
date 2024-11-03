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
            'picture': lambda json: json['picture']
        },
        'scopes': ['https://www.googleapis.com/auth/userinfo.email'],
    }
}


class Config:
    DEBUG = False
    WTF_CSRF_ENABLED = True
    MONGO_URI = MONGO_URI
    PORT = PORT
    SECRET_KEY = os.getenv("FLASK_SECRET")
    MAX_CONTENT_LENGTH = 25 * 1024 * 1024
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=6)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=10)
    JWT_KEY = os.getenv("JWT_KEY")

class LocalDevConfig(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = False
