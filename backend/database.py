from collections.abc import Generator

from sqlalchemy import URL, create_engine, inspect, text
from sqlalchemy.orm import Session, sessionmaker

from backend.config import get_settings
from backend.models import Base

settings = get_settings()
database_url = settings.database_url or URL.create(
    "postgresql+psycopg",
    username=settings.database_user,
    password=settings.database_password,
    host=settings.database_host,
    port=settings.database_port,
    database=settings.database_name,
)
engine = create_engine(database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session


def initialize_database() -> None:
    """Idempotently upgrades new and already-running central database volumes."""
    Base.metadata.create_all(bind=engine)
    # create_all deliberately never mutates existing tables. Add only the new nullable/defaulted
    # columns so installations with security log history are upgraded without data loss.
    existing = {column["name"] for column in inspect(engine).get_columns("security_logs")}
    additions = {
        "status": "VARCHAR(20)",
        "ip_address": "VARCHAR(45)",
        "user_agent": "VARCHAR(512)",
        "device_information": "VARCHAR(512)",
        "location_information": "VARCHAR(255)",
        "failure_reason": "VARCHAR(500)",
        "created_at": "TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP",
    }
    with engine.begin() as connection:
        for name, sql_type in additions.items():
            if name not in existing:
                connection.execute(text(f"ALTER TABLE security_logs ADD COLUMN {name} {sql_type}"))
        connection.execute(text("CREATE INDEX IF NOT EXISTS ix_security_logs_status ON security_logs (status)"))
        connection.execute(text("CREATE INDEX IF NOT EXISTS ix_security_logs_ip_address ON security_logs (ip_address)"))
    alert_columns = {column["name"] for column in inspect(engine).get_columns("alerts")}
    if "attempt_count" not in alert_columns:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE alerts ADD COLUMN attempt_count INTEGER"))
