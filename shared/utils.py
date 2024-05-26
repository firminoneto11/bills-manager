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


def reverse_url(
    application: "FastAPI", controller_name: str, version: str = "v1", *args, **kwargs
):
    for mount in application.routes:
        if mount.name == version:
            for route in mount.routes:
                if route.name == controller_name:
                    endpoint = mount.path + route.url_path_for(
                        controller_name, **kwargs
                    )
                    return endpoint
    raise AttributeError(f"The version {version!r} was not mounted in the application")
