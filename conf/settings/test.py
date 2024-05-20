from .development import Settings as DevSettings


class Settings(DevSettings):
    ENVIRONMENT = "test"
    DATABASE_URL = "sqlite+aiosqlite:///:memory:"
