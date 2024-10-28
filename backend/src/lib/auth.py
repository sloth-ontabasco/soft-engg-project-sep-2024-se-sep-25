from functools import wraps

from flask import request
from flask_login import current_user
from flask_login import login_required as flask_login_required

from src.lib.jwt_handler import token_required
from src.models.response import Response
from src.models.user import User


def login_required(f):
    """
    Decorator for endpoints that can be accessed by both admin and user.
    It calls `token_required` wrapper for member, and Flask's `login_required` for admin.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        if request.cookies.get("token"):
            x = token_required(f)
            return x(*args, **kwargs)
        else:
            try:
                if isinstance(current_user, User) and current_user.id:
                    x = flask_login_required(f)
                    return x(*args, **kwargs)
            except AttributeError as ae:
                return Response.error(401, "Unauthorized.")

    return decorated
