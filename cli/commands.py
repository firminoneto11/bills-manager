import asyncio as aio
from traceback import print_exc

from alembic import command
from alembic.config import Config
from alembic.runtime.environment import EnvironmentContext
from alembic.script import ScriptDirectory
from typer import Typer

cli = Typer()


def _makemigrations(msg: str):
    config = Config("alembic.ini")
    script = ScriptDirectory.from_config(config)

    try:
        with EnvironmentContext(config, script):
            command.revision(config, message=msg, autogenerate=True)
    except:
        print_exc()


@cli.command()
def makemigrations(message: str):
    return _makemigrations(message)


@cli.command()
def migrate():
    print("Migrating")
