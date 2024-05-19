from functools import lru_cache
from importlib import import_module
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shared.connection_handler import DBConnectionHandler
from shared.models import TimeStampedBaseModel

from .settings import Settings


@lru_cache
def get_db_handler(connection_string: str = Settings.DATABASE_URL):
    return DBConnectionHandler(connection_string)


def get_metadata():
    for app in Settings.APPS:
        try:
            import_module(f"{app}.{Settings.MODELS_MODULE}")
        except ImportError:
            # TODO: Log the import error just in case
            continue

    return TimeStampedBaseModel.metadata


DbSessionDep = Annotated[AsyncSession, Depends(get_db_handler().get_session)]
