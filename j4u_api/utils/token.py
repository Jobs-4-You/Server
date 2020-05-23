from datetime import datetime, timedelta

import jwt

from j4u_api.config import config


def extract_from_token(token):
    return jwt.decode(token, config.JWT_KEY, algorithm="HS256")


def create_auth_token(user_id, exp_time):
    exp = datetime.utcnow() + timedelta(seconds=exp_time)
    return jwt.encode(
        {"user_id": user_id, "exp": exp}, config.JWT_KEY, algorithm="HS256"
    ).decode()


def create_signup_token(group_id, expire_at):
    return jwt.encode(
        {"group_id": group_id, "exp": expire_at}, config.JWT_KEY, algorithm="HS256"
    ).decode()
