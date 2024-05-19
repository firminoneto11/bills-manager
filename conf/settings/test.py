from .development import Settings as DevSettings


class Settings(DevSettings):
    DATABASE_URL = "sqlite+aiosqlite:///:memory:"
