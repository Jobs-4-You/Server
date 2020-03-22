import graphene
from functools import lru_cache

graphene.Enum.from_enum = lru_cache(maxsize=None)(graphene.Enum.from_enum)
from app import app
from config import config


if __name__ == "__main__":

    app.run()
