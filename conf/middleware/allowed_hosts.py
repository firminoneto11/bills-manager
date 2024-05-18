from fastapi.middleware.trustedhost import TrustedHostMiddleware

from conf import Settings

allowed_hosts_middleware_configuration = {
    "middleware_class": TrustedHostMiddleware,
    "allowed_hosts": Settings.ALLOWED_HOSTS,
}
