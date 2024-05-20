from .base import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT = "development"
    DATABASE_URL = "sqlite+aiosqlite:///./database.db"
    ALLOWED_HOSTS = ["*"]
    ALLOWED_ORIGINS = ["*"]
    DEBUG = True
