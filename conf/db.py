from importlib import import_module

from shared.connection_handler import get_db_handler as _get_db_handler
from shared.models import TimeStampedBaseModel

from .settings import APPS, DATABASE_URL


def get_db_handler():
    return _get_db_handler(connection_string=DATABASE_URL)


def get_metadata():
    [import_module(f"{app}.models") for app in APPS]
    return TimeStampedBaseModel.metadata
