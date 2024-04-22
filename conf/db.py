from importlib import import_module
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shared.connection_handler import get_db_handler as _get_db_handler
from shared.models import TimeStampedBaseModel

from .settings import APPS, DATABASE_URL, MODELS_MODULE


def get_db_handler(connection_string: str = DATABASE_URL):
    return _get_db_handler(connection_string)


def get_metadata():
    [import_module(f"{app}.{MODELS_MODULE}") for app in APPS]
    return TimeStampedBaseModel.metadata


DbSessionDep = Annotated[AsyncSession, Depends(get_db_handler().get_session)]
