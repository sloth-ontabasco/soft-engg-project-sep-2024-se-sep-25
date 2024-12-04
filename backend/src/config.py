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

#GEMINI API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

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
    },

    # github oauth documentation:
    # https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/creating-an-oauth-app

    'github' : {
        'client_id': os.environ.get('GITHUB_CLIENT_ID'),
        'client_secret': os.environ.get('GITHUB_CLIENT_SECRET'),
        'authorize_url': 'https://github.com/login/oauth/authorize',
        'token_url': 'https://github.com/login/oauth/access_token',
        'userinfo':{
            'url': 'https://api.github.com/user',
            'email': lambda json: json['login'],
            'repos_url': lambda json: json['reops_url']
        },
        # 'scopes': ['user:email','repo','user']
        'scopes': ['user','repo','user:email']
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
