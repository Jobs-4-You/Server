import os
from functools import lru_cache

import click
import graphene

from j4u_api.database import engine
from j4u_api.database.seed import seed_testing

graphene.Enum.from_enum = lru_cache(maxsize=None)(graphene.Enum.from_enum)


@click.group()
def database_operations():
    pass


@database_operations.command()
def fresh_start():
    """database operations: restart the project from scratch"""
    engine.execute("DROP SCHEMA public CASCADE")
    engine.execute("CREATE SCHEMA public")
    os.system("rm ./alembic/versions/* -rf")
    os.system("alembic revision --autogenerate")
    os.system("alembic upgrade head")


@database_operations.command()
def fresh_start_and_seed():
    """database operations: restart the project from scratch"""
    engine.execute("DROP SCHEMA public CASCADE")
    engine.execute("CREATE SCHEMA public")
    os.system("rm ./alembic/versions/* -rf")
    os.system("alembic revision --autogenerate")
    os.system("alembic upgrade head")
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
