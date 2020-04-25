import random

import sqlalchemy as S
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from j4u_api.database.connection import db_session
from j4u_api.database.enums import CiviliteEnum, RoleEnum
from j4u_api.utils.print import to_pretty_string


class BaseExt(object):
    """Does much nicer repr/print of class instances
     from sqlalchemy list suggested by Michael Bayer
     """

    def __repr__(self):
        res = {}
        for key in sorted(self.__dict__.keys()):
            if not key.startswith("_"):
                res[key] = getattr(self, key)
        return self.__class__.__name__ + to_pretty_string(res)

    def to_dict(self):
        res = {}
        for key in sorted(self.__dict__.keys()):
            if not key.startswith("_"):
                res[key] = getattr(self, key)
        return res


Base = declarative_base(cls=BaseExt)
# We will need this for querying
Base.query = db_session.query_property()


class FeatureConfig(Base):
    __tablename__ = "feature_configs"
    id = S.Column(S.Integer, primary_key=True)
    qualtrics_name = S.Column(S.String(64), nullable=False, unique=True)
    engine_name = S.Column(S.String(64), nullable=False, unique=True)
    from_min = S.Column(S.Integer, nullable=False)
    from_max = S.Column(S.Integer, nullable=False)
    to_min = S.Column(S.Integer, nullable=False)
    to_max = S.Column(S.Integer, nullable=False)
    inverse = S.Column(S.Boolean, nullable=False)


class Feature(Base):
    __tablename__ = "features"
    id = S.Column(S.Integer, primary_key=True)
    user_id = S.Column(S.Integer, S.ForeignKey("users.id"))
    feature_config_id = S.Column(S.Integer, S.ForeignKey("feature_configs.id"))
    user = relationship("User", foreign_keys=[user_id])
    feature_config = relationship("FeatureConfig", foreign_keys=[feature_config_id])
    value = S.Column(S.Float, nullable=False)


class UIConfig(Base):
    __tablename__ = "ui_configs"
    id = S.Column(S.Integer, primary_key=True)
    search = S.Column(S.Boolean, default=False)
    group_id = S.Column(S.ForeignKey("groups.id"), nullable=False)


class Group(Base):
    __tablename__ = "groups"
    id = S.Column(S.Integer, primary_key=True)
    name = S.Column(S.String(64), nullable=False)
    users = relationship("User", back_populates="group")
    baseline_id = S.Column(S.String(64))
    cruiser_id = S.Column(S.String(64))
    ui_config = relationship("UIConfig")


class User(Base):
    __tablename__ = "users"
    id = S.Column(S.Integer, primary_key=True)
    role = S.Column(S.Enum(RoleEnum), default=RoleEnum.USER)
    civilite = S.Column(S.Enum(CiviliteEnum), nullable=False)
    first_name = S.Column(S.String(50), nullable=False)
    last_name = S.Column(S.String(50), nullable=False)
    birth_date = S.Column(S.Date(), nullable=False)
    email = S.Column(S.String(120), unique=True)
    phone = S.Column(S.String(16), unique=True)
    password_hash = S.Column(S.String(256), nullable=False)
    form_done = S.Column(S.Boolean, default=False)
    form_done_at = S.Column(S.Date)
    survey_id = S.Column(S.String(10), unique=True)
    verified = S.Column(S.Boolean(), default=False)
    alpha = S.Column(S.Float, nullable=True, default=50)
    beta = S.Column(S.Float, nullable=True, default=50)
    old_job_id = S.Column(S.Integer)
    features = relationship("Feature", back_populates="user")
    group_id = S.Column(S.ForeignKey("groups.id"), nullable=False)
    group = relationship(Group, back_populates="users", uselist=False)

    def __init__(self, **kwargs):
        kwargs["password_hash"] = self.hash_password(kwargs["password"])
        del kwargs["password"]
        if kwargs.get("survey_id") is None:
            unique_key = random.randint(10000000, 99999999)
            while self.query.filter(self.survey_id == unique_key).first() is not None:
                unique_key = random.randint(10000000, 99999999)
            kwargs["survey_id"] = unique_key
        super(User, self).__init__(**kwargs)

    def hash_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @hybrid_property
    def baseline_link(self):
        base_url = "https://fpse.qualtrics.com/jfe/form"
        return f"{base_url}/{self.group.baseline_id}?={self.survey_id}"
