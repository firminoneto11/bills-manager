from functools import lru_cache
from importlib import import_module
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shared.db_handler import DBHandler
from shared.models import TimeStampedBaseModel

from .settings import Settings


@lru_cache
def get_db_handler(connection_string: str = Settings.DATABASE_URL):
    return DBHandler(connection_string)


def get_metadata():
    for app in Settings.APPS:
        try:
            import_module(f"{app}.{Settings.MODELS_MODULE}")
        except ImportError:
            # TODO: Log the import error just in case
            continue

    return TimeStampedBaseModel.metadata


async def get_session():
    async with get_db_handler().begin_session() as session:
        yield session


Session = Annotated[AsyncSession, Depends(get_session)]
