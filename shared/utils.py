from datetime import datetime, timezone
from functools import lru_cache
from typing import TYPE_CHECKING
from uuid import uuid4

from environs import Env

if TYPE_CHECKING:
    from shared.types import ASGIApp


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
    application: "ASGIApp", controller_name: str, version: str = "v1", **kwargs
):
    for mount in application.state._mounted_applications:
        for route in mount.app.routes:
            if route.name == controller_name:
                return mount.path + route.url_path_for(controller_name, **kwargs)

    raise AttributeError(f"The version {version!r} wasn't mounted in the application")
