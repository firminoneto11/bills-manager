import tomllib
from typing import TYPE_CHECKING

from shared.utils import get_env

if TYPE_CHECKING:
    from shared.types import EnvironmentChoices


with open("pyproject.toml", mode="rb") as file:
    py_project = tomllib.load(file)["tool"]["poetry"]


class BaseSettings:
    ENVIRONMENT: "EnvironmentChoices" = (
        get_env().str("ENVIRONMENT", "development").lower().strip()
    )

    MODELS_MODULE = "models"
    APPS = [
        "apps.core",
        "apps.bills",
    ]

    APP_NAME: str = py_project["name"]
    APP_DESCRIPTION: str = py_project["description"]
    APP_VERSION: str = py_project["version"]

    API_PREFIX = "/api"
    DOCS_URL = "/docs"
    REDOC_URL = "/redoc"
    OPENAPI_URL = "/openapi.json"

    # NOTE: These are here only for type checking purposes. They should be set on the
    # other files.
    if TYPE_CHECKING:
        DATABASE_URL: str
        ALLOWED_HOSTS: list[str]
        ALLOWED_ORIGINS: list[str]
        DEBUG: bool
