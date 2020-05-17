import os

from elasticsearch_dsl import Index

from j4u_api.database import engine


def reset_db():
    engine.execute("DROP SCHEMA public CASCADE")
    engine.execute("CREATE SCHEMA public")


def reset_migrations():
    os.system("rm ./alembic/versions/* -rf")


def reset_elastic_db():
    try:
        Index(name="jobs").delete()
        Index(name="events").delete()
        print("INDEXES DELETED")
    except Exception as err:
        print("NO INDEX DELETED")


def migrate():
    os.system("alembic revision --autogenerate")
    os.system("alembic upgrade head")
