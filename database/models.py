from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from utils.print import to_pretty_string
from config import config
from .enums import RoleEnum, CiviliteEnum, GroupEnum

engine = create_engine(config.DB_URL)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


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


Base = declarative_base(cls=BaseExt)
# We will need this for querying
Base.query = db_session.query_property()


class Feature(Base):
    __tablename__ = "features"
    id = Column(Integer, primary_key=True)
    userId = Column(ForeignKey("users.id"), nullable=False, unique=True)
    var1 = Column(Float, nullable=False)
    var2 = Column(Float, nullable=False)
    var3 = Column(Float, nullable=False)
    var4 = Column(Float, nullable=False)
    var5 = Column(Float, nullable=False)
    var6 = Column(Float, nullable=False)
    var7 = Column(Float, nullable=False)
    var8 = Column(Float, nullable=False)
    var9 = Column(Float, nullable=False)
    var10 = Column(Float, nullable=False)
    var11 = Column(Float, nullable=False)
    var12 = Column(Float, nullable=False)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    role = Column(Enum(RoleEnum), default=RoleEnum.USER)
    civilite = Column(Enum(CiviliteEnum), nullable=False)
    firstName = Column(String(50), nullable=False)
    lastName = Column(String(50), nullable=False)
    birthDate = Column(Date(), nullable=False)
    email = Column(String(120), unique=True)
    phone = Column(String(16), unique=True)
    pwd_hash = Column(String(256), nullable=False)
    formDone = Column(Boolean(), default=False)
    surveyId = Column(String(10))
    verified = Column(Boolean(), default=False)
    alpha = Column(Float, nullable=True, default=50)
    beta = Column(Float, nullable=True, default=50)
    oldJobValue = Column(Integer, nullable=True)
    oldJobLabel = Column(String(100), nullable=True)
    features = relationship(Feature, uselist=False)
    fixedOldJobValue = Column(Boolean(), default=False)
    fixedAlphaBeta = Column(Boolean(), default=False)
    group = Column(Enum(GroupEnum), nullable=False)

    def __init__(self, **kwargs):
        # TODO Change surveyId behaviour
        kwargs["pwd_hash"] = self.hash_password(kwargs["pwd"])
        del kwargs["pwd"]
        if kwargs["surveyId"] is None:
            kwargs["surveyId"] = randint(10000000, 99999999)
        else:
            kwargs["surveyId"] = kwargs["surveyId"]
        super(User, self).__init__(**kwargs)

    def hash_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwd_hash, password)
