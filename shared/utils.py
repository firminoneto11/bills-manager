from datetime import datetime, timezone
from functools import lru_cache
from typing import TYPE_CHECKING
from uuid import uuid4

from environs import Env

if TYPE_CHECKING:
    from fastapi import FastAPI


def utcnow():
    return datetime.now(tz=timezone.utc)


def generate_uuid():
    return str(uuid4())


@lru_cache(maxsize=1)
def get_env():
    env = Env()
    env.read_env()
    return env


def reverse_url(application: "FastAPI", controller_name: str, *args, **kwargs):
    return application.url_path_for(controller_name, **kwargs)
