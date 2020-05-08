import os
import pathlib

from dotenv import load_dotenv

from j4u_api.utils.print import to_pretty_string


class Config:
    # Mode
    MODE = None

    # Email
    EMAIL_USER = None
    EMAIL_PW = None

    # App secrets
    APP_KEY = None
    SALT = None
    JWT_KEY = None
    AUTH_TOKEN_EXPIRATION = None

    # Jobs config
    GET_FEATURES_JOB_INTERVAL = None

    # Postgres
    POSTGRES_USER = None
    POSTGRES_PW = None
    POSTGRES_DB = None
    POSTGRES_IP = None

    # Qualtrics
    QUALTRICS_TOKEN = None
    QUALTRICS_USER = None

    # App
    URL = None
    APP_URL = None
    APP_DOCKER_URL = None
    HOST = None
    PORT = None

    # Gunicorn
    GUNICORN_BIND = None
    GUNICORN_WORKER_CLASS = None
    GUNICORN_WORKERS = None

    def __init__(self):
        keys = [
            x
            for x in dir(self)
            if not x.startswith("_")
            and not isinstance(getattr(type(self), x), property)
        ]
        for k in keys:
            setattr(self, k, os.environ[k])
        # Root path
        self.ROOT_DIR = os.path.abspath(
            f"{pathlib.Path(__file__).parent.absolute()}/.."
        )
        self.LOGGING_CONF_PATH = os.path.abspath(
            os.path.join(self.ROOT_DIR, "loggin.ini")
        )

    def __repr__(self):
        res = {}
        for key in sorted(dir(self)):
            if not key.startswith("_"):
                res[key] = getattr(self, key)
        return to_pretty_string(res)

    @property
    def DB_URL(self):
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PW}@"
            f"{self.POSTGRES_IP}/{self.POSTGRES_DB}"
        )


current_folder = pathlib.Path(__file__).parent.absolute()
dotenv_path = f"{current_folder}/../../.dotenv"
load_dotenv(dotenv_path)
config = Config()
