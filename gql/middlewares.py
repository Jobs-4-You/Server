import jwt
from database.models import User
from utils.token import extract_from_token
from gql.errors.token_errors import SessionExpired


def auth_middleware(next, root, info, **args):
    user = None
    token = info.context.headers.get("accessToken")
    if token:
        try:
            user_id = extract_from_token(token)["user_id"]
            user = User.query.filter(User.id == user_id).first()
        except jwt.DecodeError as err:
            print("DcodeError")
            print(err)
        except jwt.ExpiredSignatureError as err:
            raise SessionExpired().error

    info.context.user = user
    return next(root, info, **args)
