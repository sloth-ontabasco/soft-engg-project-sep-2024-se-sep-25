from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_current_user
from flask_jwt_extended.exceptions import NoAuthorizationError
from src.models.response import Response
from src.models.user import User






def check_any_role(roles):
    def decorator(f):
        @wraps(f)
        def decorator_function(*args, **kwargs):
            print(f"Checking roles: {roles}")
            verify_jwt_in_request()
            current_user = get_current_user()
            print("Current user's roles:", current_user.role)
            if not current_user.role in roles:
                raise NoAuthorizationError("Role is not allowed.")
            return f(*args, **kwargs)
        return decorator_function
    return decorator
