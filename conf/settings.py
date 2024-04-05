from shared.utils import get_env

DATABASE_URL = get_env().str("DATABASE_URL")

ALLOWED_HOSTS = get_env().str("ALLOWED_HOSTS").split(",")

ALLOWED_ORIGINS = get_env().str("ALLOWED_ORIGINS").split(",")

APPS = ["apps.core"]
