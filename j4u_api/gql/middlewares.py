import jwt

from j4u_api.database.models import User
from j4u_api.errors.token_errors import SessionExpired
from j4u_api.utils.token import extract_from_token


def auth_middleware(next, root, info, **args):
    user = None
    token = info.context.headers.get("accessToken")
    if token:
        try:
            user_id = extract_from_token(token)["user_id"]
            user = User.query.get(user_id)
        except jwt.DecodeError as err:
            raise err
        except jwt.ExpiredSignatureError:
            raise SessionExpired()

    info.context.user = user

    return next(root, info, **args)
