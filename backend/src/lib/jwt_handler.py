import time
from functools import wraps

import jwt
from flask import request

from src.config import JWT_KEY

algorithm = "HS256"

def encode(data):
    """
    Encode data into JWT token.
    86400 => 24 hours
    """
    data["valid_until"] = int(time.time() + 86400)
    return jwt.encode(data, JWT_KEY, algorithm)


def decode(token):
    """
    Decode JWT token.
    """
    return jwt.decode(token, JWT_KEY, [algorithm])


def token_required(f):
    """
    Wrapper to validate a token.
    Use this for member validation.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        try:
            token = request.cookies.get("token")
        except ValueError as ve:
            return Response.error(401, "Authentication Token is missing.")

        if not token:
            return Response.error(401, "Authentication Token is missing.")

        try:
            data = decode(token)
            if data["valid_until"] < int(time.time()):
                return Response.error(401, "Authentication Token has expired.")

        except jwt.exceptions.InvalidTokenError:
            return Response.error(401, "Authentication Token is invalid.")

        if request.path not in ["/api/users/@me"]:
            user_data = User.get_from_token(DiscordOAuth(data))
            if not user_data.is_present_in_kurz_guild():
                return Response.error(403, "Please join Kurzgesagt Discord server.")

        return f(*args, **kwargs)

    return decorated
