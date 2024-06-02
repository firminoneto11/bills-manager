import subprocess
from os import listdir

from typer import Typer

from conf import Settings

cli = Typer()


@cli.command(name="makemigrations")
def makemigrations(message: str = "auto", autogenerate: bool = True):
    init_file = "__init__.py"
    versions_directory = Settings.BASE_DIR / "migrations" / "versions"

    versions = [el for el in listdir(versions_directory) if el != init_file]
    new_version = str(len(versions) + 1).zfill(4)

    command = f"alembic revision {'--autogenerate' if autogenerate else ''} -m"
    command = [*command.split(" "), f"{new_version}_{message}"]

    subprocess.run(command)


@cli.command(name="migrate")
def migrate():
    command = "alembic upgrade head"
    subprocess.run(command.split(" "))
