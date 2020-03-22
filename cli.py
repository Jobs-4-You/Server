import graphene
from functools import lru_cache

graphene.Enum.from_enum = lru_cache(maxsize=None)(graphene.Enum.from_enum)
import click
import os
import subprocess
from database import Base, engine, db_session
from database.seed import seed_testing
from elastic import create_all_indices, delete_all_indices, import_jobs


@click.group()
def database_operations():
    pass


@database_operations.command()
def fresh_start():
    """database operations: restart the project from scratch"""
    Base.metadata.drop_all(bind=engine)
    engine.execute("DROP TABLE IF EXISTS alembic_version")
    os.system("rm ./alembic/versions/* -rf")
    os.system("alembic revision --autogenerate")
    os.system("alembic upgrade head")


@database_operations.command()
def fresh_start_and_seed():
    """database operations: restart the project from scratch"""
    Base.metadata.drop_all(bind=engine)
    engine.execute("DROP TABLE IF EXISTS alembic_version")
    os.system("rm ./alembic/versions/* -rf")
    os.system("alembic revision --autogenerate")
    os.system("alembic upgrade head")
    delete_all_indices()
    create_all_indices()
    import_jobs()
    seed_testing()


@click.group()
def other():
    pass


@other.command()
def cmd2():
    """other operations"""


cli = click.CommandCollection(sources=[database_operations, other])

if __name__ == "__main__":
    cli()

