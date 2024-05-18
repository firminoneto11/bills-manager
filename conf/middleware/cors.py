from fastapi.middleware.cors import CORSMiddleware

from conf import Settings

cors_middleware_configuration = {
    "middleware_class": CORSMiddleware,
    "allow_origins": Settings.ALLOWED_ORIGINS,
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}
