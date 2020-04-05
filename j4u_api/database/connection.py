from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from j4u_api.config import config

engine = create_engine(config.DB_URL)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
