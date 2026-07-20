from sqlalchemy.exc import OperationalError

from backend.config import get_settings


def database_connection_error(exc: OperationalError) -> SystemExit:
    settings = get_settings()
    host = settings.database_host if not settings.database_url else settings.database_url.split("@", 1)[-1].split("/", 1)[0]
    message = [f"Unable to connect to the configured database host: {host}."]
    if "localhost" in host or "127.0.0.1" in host:
        message.extend([
            "The central PostgreSQL service is private to the Docker Compose network.",
            "Run this command inside the central API container:",
            "  docker compose -f docker-compose.central.yml exec central-api python -m backend.scripts.init_db",
        ])
    else:
        message.append("Check CENTRAL_DATABASE_URL and confirm PostgreSQL is healthy.")
    return SystemExit("\n".join(message))
