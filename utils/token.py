import jwt
from datetime import datetime, timedelta
from config import config


def extract_from_token(token):
    return jwt.decode(token, config.JWT_KEY, algorithm="HS256")


def create_auth_token(user_id, exp_time=3600):
    exp = datetime.utcnow() + timedelta(seconds=exp_time)
    return jwt.encode(
        {"user_id": user_id, "exp": exp}, config.JWT_KEY, algorithm="HS256"
    ).decode()


def create_signup_token(group, expire_at):
    return jwt.encode(
        {"group": group, "exp": expire_at}, config.JWT_KEY, algorithm="HS256"
    ).decode()
