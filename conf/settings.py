import tomllib

from shared.utils import get_env

with open("pyproject.toml", mode="rb") as file:
    py_project = tomllib.load(file)["tool"]["poetry"]


class Settings:
    DATABASE_URL: str = get_env().str("DATABASE_URL")

    ALLOWED_HOSTS: list[str] = get_env().str("ALLOWED_HOSTS").split(",")

    ALLOWED_ORIGINS: list[str] = get_env().str("ALLOWED_ORIGINS").split(",")

    APPS = ["apps.core", "apps.bills"]

    MODELS_MODULE = "models"

    DEBUG: bool = get_env().bool("DEBUG", True)

    APP_NAME: str = py_project["name"]
    APP_DESCRIPTION: str = py_project["description"]
    APP_VERSION: str = py_project["version"]

    API_PREFIX = "/api"
    DOCS_URL = "/docs"
    REDOC_URL = "/redoc"
    OPENAPI_URL = "/openapi.json"
