from typing import TYPE_CHECKING

from shared.utils import get_env

if TYPE_CHECKING:
    from shared.types import EnvironmentChoices


module: "EnvironmentChoices" = (
    get_env().str("ENVIRONMENT", "development").lower().strip()
)


match module:
    case "development":
        from .development import Settings  # noqa
    case "test":
        from .test import Settings  # noqa
    case "staging":
        from .staging import Settings  # noqa
    case "production":
        from .production import Settings  # noqa
    case _:
        raise RuntimeError(f"Invalid environment: {module!r}")
