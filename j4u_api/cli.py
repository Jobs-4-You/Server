import subprocess

import click

from j4u_api.config import config
from j4u_api.database.seed import seed_testing
from j4u_api.utils.db import migrate, reset_db, reset_elastic_db, reset_migrations


@click.group()
def database_operations():
    pass


@database_operations.command()
@click.option("--seed-test", is_flag=True)
def fresh_start(seed_test):
    """database operations: restart the project from scratch"""
    reset_db()
    reset_migrations()
    migrate()
    if seed_test:
        seed_testing()


@click.group()
def serving():
    pass


@serving.command()
def wsgi_serve():
    """serving: serve the application in WSGi mode for production"""
    bind = f"--bind {config.GUNICORN_BIND}"
    worker_class = f"--worker-class {config.GUNICORN_WORKER_CLASS}"
    workers = f"--workers {config.GUNICORN_WORKERS}"
    call_list = ["gunicorn", bind, worker_class, workers, "wsgi:app"]
    call_string = " ".join(call_list)
    print(call_string)
    subprocess.call(call_string.split())


cli = click.CommandCollection(sources=[database_operations, serving])

if __name__ == "__main__":
    cli()
