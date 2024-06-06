import subprocess
import sys
from os import listdir

from alembic.config import Config
from alembic.script import ScriptDirectory
from slugify import slugify
from typer import Exit, Typer

from conf import Settings

cli = Typer()


def log(msg: str):
    sys.stderr.write(msg)
    sys.stderr.flush()


@cli.command(name="makemigrations")
def makemigrations(message: str = "auto", autogenerate: bool = True):
    init_file = "__init__.py"
    versions_directory = Settings.BASE_DIR / "migrations" / "versions"

    versions = [el for el in listdir(versions_directory) if el != init_file]
    new_version = str(len(versions) + 1).zfill(4)

    message = slugify(text=message, separator="_")
    command = f"alembic revision {'--autogenerate' if autogenerate else ''} -m"

    log(f"Executing {command!r} command...\n")

    command = [*command.split(" "), f"{new_version}_{message}"]

    subprocess.run(command)

    raise Exit(0)


@cli.command(name="migrate")
def migrate(revision: str = ""):
    """
    Ensures that the database reflects the state defined in the inputted revision, and
    auto detects weather is a up or down operation.

    :param revision: Can be set to 'zero', a valid revision id or left blank. If set to
    'zero', it will downgrade everything and clean the entire database. If set to
    empty, it will ensure that the database reflects the state of the head
    revision. If a valid revision id is set, it will ensure that the database state
    reflects what is defined in that revision and it will automatically figure out
    if is weather an up or down migration.
    """
    alembic_cfg = Config("alembic.ini")
    script = ScriptDirectory.from_config(alembic_cfg)

    revisions = {
        revision.revision: None for revision in reversed(list(script.walk_revisions()))
    }
    revisions = {key: idx + 1 for (idx, key) in enumerate(revisions)}

    if not revision:
        command = "alembic upgrade head"
        log(f"Executing {command!r} command...\n")
        subprocess.run(command.split(" "))
        raise Exit(0)

    if revision == "zero":
        command = "alembic downgrade base"
        log(f"Executing {command!r} command...\n")
        subprocess.run(command.split(" "))
        raise Exit(0)

    if revision not in revisions:
        log(f"Could not find the {revision!r} revision in the versions directory\n")
        raise Exit(1)

    # NOTE: This means that the database doesn't have a migration applied atm. The only
    # possible direction is upwards
    output = subprocess.run(["alembic", "current"], capture_output=True).stdout.decode()
    if not (current := output.split(" ")[0].replace("\n", "")):
        command = f"alembic upgrade {revision}"
        log(f"Executing {command!r} command...\n")
        subprocess.run(command.split(" "))
        raise Exit(0)

    # TODO: There is a possibility of the current value not being in the versions dict.
    # Handle these cases

    if revisions[revision] > revisions[current]:
        direction = "up"
    elif revisions[revision] < revisions[current]:
        direction = "down"
    else:
        log(
            (
                "Skipping migration because the current revision applied in the "
                "database is already the desired one\n"
            )
        )
        raise Exit(0)

    command = f"alembic {'upgrade' if direction == 'up' else 'downgrade'} {revision}"

    log(f"Executing {command!r} command...\n")

    subprocess.run(command.split(" "))

    raise Exit(0)
