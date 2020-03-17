from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from utils.print import to_pretty_string
from config import config

engine = create_engine(
    f"mysql+mysqldb://{config.MYSQL_USER}:{config.MYSQL_PWD}@127.0.0.1/{config.MYSQL_DB}"
)
mysql_session = scoped_session(
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
Base.query = mysql_session.query_property()


class Features(Base):
    __tablename__ = "features"
    id = Column(Integer, primary_key=True)
    userId = Column(ForeignKey("user.id"), nullable=False, unique=True)
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
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    civilite = Column(String(4))
    firstName = Column(String(50))
    lastName = Column(String(50))
    birthDate = Column(Date())
    email = Column(String(120), unique=True)
    phone = Column(String(16), unique=True)
    pwd_hash = Column(String(256))
    plastaId = Column(String(16), unique=False)
    formDone = Column(Boolean(), default=False)
    surveyId = Column(String(10))
    verified = Column(Boolean(), default=False)
    alpha = Column(Float, nullable=True, default=50)
    beta = Column(Float, nullable=True, default=50)
    oldJobValue = Column(Integer, nullable=True)
    oldJobLabel = Column(String(100), nullable=True)
    features = relationship(Features, uselist=False)
    blocked = Column(Boolean(), default=False)
    fixedOldJobValue = Column(Boolean(), default=False)
    fixedAlphaBeta = Column(Boolean(), default=False)
    group = Column(String(16))

    def __init__(self, **kwargs):
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
