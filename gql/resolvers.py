from utils.auth import jwt_auth_required, roles_required
from utils.token import create_signup_token
from .types import *
from database.enums import RoleEnum
from config import config


@roles_required([RoleEnum.ADMIN])
def resolve_all_users(parent, info, user_id):
    query = User.get_query(info)  # SQLAlchemy query
    return query.all()


@jwt_auth_required
def resolve_me(parent, info):
    return info.context.user


def resolve_get_signup_link(parent, info, group, expire_at):
    signup_token = create_signup_token(group, expire_at)
    url = f"{config.APP_URL}/?signup&token={signup_token}"
    return SignupUrl(url=url, token=signup_token)
