from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_current_user 
from flask_jwt_extended.exceptions import NoAuthorizationError
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
from src.lib.jwt_handler import token_required
>>>>>>> 97ecc0e (backend)
from src.models.response import Response
from src.models.user import User
>>>>>>> f19afa2 (backend)

def check_any_role(roles):
    def decorator(f):
        @wraps(f)
        def decorator_function(*args, **kwargs):
            verify_jwt_in_request()
            current_user = get_current_user()
            print('current user roles',current_user.get_roles())
            if not set(current_user.get_roles()).intersection(roles):
                print('erroring here')
                raise NoAuthorizationError("Role is not allowed.")
            return f(*args, **kwargs)
        return decorator_function
    return decorator
