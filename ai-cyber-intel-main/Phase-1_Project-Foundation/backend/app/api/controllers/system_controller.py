from datetime import UTC, datetime

from app.config.settings import get_settings


def get_system_health() -> dict[str, str]:
    settings = get_settings()
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "timestamp": datetime.now(UTC).isoformat(),
    }
