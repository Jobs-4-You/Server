import random

import sqlalchemy as S
from sqlalchemy.ext.declarative import declarative_base
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


class Feature(Base):
    __tablename__ = "features"
    id = S.Column(S.Integer, primary_key=True)
    user = relationship("User", back_populates="features", uselist=False)
    var1 = S.Column(S.Float, nullable=False)
    var2 = S.Column(S.Float, nullable=False)
    var3 = S.Column(S.Float, nullable=False)
    var4 = S.Column(S.Float, nullable=False)
    var5 = S.Column(S.Float, nullable=False)
    var6 = S.Column(S.Float, nullable=False)
    var7 = S.Column(S.Float, nullable=False)
    var8 = S.Column(S.Float, nullable=False)
    var9 = S.Column(S.Float, nullable=False)
    var10 = S.Column(S.Float, nullable=False)
    var11 = S.Column(S.Float, nullable=False)
    var12 = S.Column(S.Float, nullable=False)


class Group(Base):
    __tablename__ = "groups"
    id = S.Column(S.Integer, primary_key=True)
    name = S.Column(S.String(64), nullable=False)
    users = relationship("User", back_populates="group")
    baseline_id = S.Column(S.String(64))
    cruiser_id = S.Column(S.String(64))


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
    form_done = S.Column(S.Boolean(), default=False)
    survey_id = S.Column(S.String(10), unique=True)
    verified = S.Column(S.Boolean(), default=False)
    alpha = S.Column(S.Float, nullable=True, default=50)
    beta = S.Column(S.Float, nullable=True, default=50)
    old_job_id = S.Column(S.Integer)
    features_id = S.Column(S.ForeignKey("features.id"), unique=True)
    features = relationship("Feature", back_populates="user", uselist=False)
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
