from collections.abc import AsyncGenerator
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from config.soar_settings import get_settings


class Base(DeclarativeBase):
    pass


settings = get_settings()
connect_args = (
    {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
)
engine = create_engine(
    settings.database_url, connect_args=connect_args, pool_pre_ping=True
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def initialize_database():
    from models import incident_model  # noqa: F401

    Base.metadata.create_all(engine)


async def get_db() -> AsyncGenerator[Session, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


class SoarRepository:
    def __init__(self, session: Session):
        self.session = session

    def list(self, model, limit=100):
        return list(
            self.session.scalars(select(model).order_by(model.id.desc()).limit(limit))
        )
