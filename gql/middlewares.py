from database.models import User
from utils.token import extract_from_token


def auth_middleware(next, root, info, **args):
    user = None
    token = info.context.headers.get("accessToken")
    if token:
        try:
            user_id = extract_from_token(token)["user_id"]
            user = User.query.filter(User.id == user_id).first()
        except Exception as err:
            print(err)
            pass
    info.context.user = user
    return next(root, info, **args)
