from fastapi.middleware.cors import CORSMiddleware

from conf.settings import ALLOWED_ORIGINS

cors_middleware_configuration = {
    "middleware_class": CORSMiddleware,
    "allow_origins": ALLOWED_ORIGINS,
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}
