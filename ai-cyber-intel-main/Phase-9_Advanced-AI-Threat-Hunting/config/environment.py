"""Environment validation helpers."""
from dataclasses import dataclass
from .settings import Settings


@dataclass(frozen=True)
class EnvironmentStatus:
    valid: bool
    warnings: tuple[str, ...]


def validate_environment(settings: Settings) -> EnvironmentStatus:
    """Validate deployment-sensitive configuration without exposing secrets."""
    warnings: list[str] = []
    if settings.environment == "production" and not settings.api_key:
        warnings.append("PHASE9_API_KEY is required in production")
    if settings.environment == "production" and "localhost" in settings.database_url:
        warnings.append("production database points to localhost")
    return EnvironmentStatus(not warnings, tuple(warnings))
