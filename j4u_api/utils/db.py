import os

from j4u_api.database import engine


def reset_db():
    engine.execute("DROP SCHEMA public CASCADE")
    engine.execute("CREATE SCHEMA public")


def reset_migrations():
    os.system("rm ./alembic/versions/* -rf")


def migrate():
    os.system("alembic revision --autogenerate")
    os.system("alembic upgrade head")
