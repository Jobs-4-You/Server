import os
from utils.print import to_pretty_string


class ConfigCommon:
    COMMON = "COMMON"
    EMAIL_USER = os.environ.get("MAIL_USER")
    EMAIL_PWD = os.environ.get("MAIL_PWD")
    APP_KEY = os.environ.get("APP_KEY")
    SALT = os.environ.get("SALT")
    JWT_KEY = os.environ.get("JWT_KEY")
    ADMIN_PWORD = os.environ.get("ADMIN_PWORD")
    MYSQL_USER = os.environ.get("MYSQL_USER")
    MYSQL_PWD = os.environ.get("MYSQL_PWD")
    MONGO_USER = os.environ.get("MONGO_USER")
    MONGO_PWD = os.environ.get("MONGO_PWD")
    UPDATE_PWD = os.environ.get("UPDATE_PWD")

    def __repr__(self):
        res = {}
        for key in sorted(dir(self)):
            if not key.startswith("_"):
                res[key] = getattr(self, key)
        return to_pretty_string(res)


class ConfigDev(ConfigCommon):
    MODE = "dev"
    URL = "http://127.0.0.1:5000"
    APP_URL = "http://127.0.0.1:8080"
    HOST = "0.0.0.0"
    PORT = 5000
    MYSQL_DB = "j4u-test"


class ConfigProd(ConfigCommon):
    MODE = "prod"
    URL = "https://j4u.unil.ch:5000"
    APP_URL = "https://j4u.unil.ch"
    HOST = "127.0.0.1"
    PORT = 3000
    MYSQL_DB = "j4u"


if os.environ.get("ENV") == "prod":
    config = ConfigProd()
elif os.environ.get("ENV") == "dev":
    config = ConfigDev()
else:
    raise Exception("Config environment not set")
