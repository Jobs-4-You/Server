import os

from dotenv import dotenv_values, load_dotenv

from j4u_api.utils.print import to_pretty_string


class Config:
    def __init__(self, keys):
        for k in keys:
            setattr(self, k, os.environ[k])

    def __repr__(self):
        res = {}
        for key in sorted(dir(self)):
            if not key.startswith("_"):
                res[key] = getattr(self, key)
        return to_pretty_string(res)

    @property
    def DB_URL(self):
        return (
            f"postgres://{self.POSTGRES_USER}:{self.POSTGRES_PW}@"
            f"{self.POSTGRES_IP}/{self.POSTGRES_DB}"
        )


env_dict = dotenv_values("../.dotenv")
load_dotenv("../.dotenv")
config = Config(env_dict.keys())

print(config)
exit()
