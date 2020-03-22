import os
from utils.print import to_pretty_string


class ConfigCommon:
    COMMON = "COMMON"
    EMAIL_USER = os.environ.get("MAIL_USER")
    EMAIL_PWD = os.environ.get("MAIL_PWD")
    APP_KEY = os.environ.get("APP_KEY")
    SALT = os.environ.get("SALT")
    JWT_KEY = os.environ.get("JWT_KEY")
    POSTGRES_USER = os.environ["POSTGRES_USER"]
    POSTGRES_PW = os.environ["POSTGRES_PW"]
    POSTGRES_DB = os.environ["POSTGRES_DB"]
    POSTGRES_IP="127.0.0.1"
    ELASTIC_USER = os.environ["ELASTIC_USER"]
    ELASTIC_PW = os.environ["ELASTIC_PW"]


    def __repr__(self):
        res = {}
        for key in sorted(dir(self)):
            if not key.startswith("_"):
                res[key] = getattr(self, key)
        return to_pretty_string(res)

    @property
    def DB_URL(self):
        return f"postgres://{self.POSTGRES_USER}:{self.POSTGRES_PW}@{self.POSTGRES_IP}/{self.POSTGRES_DB}"



class ConfigDev(ConfigCommon):
    MODE = "dev"
    URL = "http://127.0.0.1:5000"
    APP_URL = "http://127.0.0.1:8080"
    HOST = "0.0.0.0"
    PORT = 5000


class ConfigProd(ConfigCommon):
    MODE = "prod"
    URL = "https://j4u.unil.ch:5000"
    APP_URL = "https://j4u.unil.ch"
    HOST = "127.0.0.1"
    PORT = 3000


if os.environ.get("ENV") == "prod":
    config = ConfigProd()
elif os.environ.get("ENV") == "dev":
    config = ConfigDev()
else:
    raise Exception("Config environment not set")
