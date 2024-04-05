from fastapi.middleware.trustedhost import TrustedHostMiddleware

from conf.settings import ALLOWED_HOSTS

allowed_hosts_middleware_configuration = {
    "middleware_class": TrustedHostMiddleware,
    "allowed_hosts": ALLOWED_HOSTS,
}
