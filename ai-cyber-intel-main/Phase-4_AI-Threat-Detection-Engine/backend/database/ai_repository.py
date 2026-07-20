from collections.abc import AsyncGenerator
from datetime import UTC, datetime

from sqlalchemy import DateTime, Float, JSON, String, Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from config.ai_settings import get_settings


class Base(DeclarativeBase):
    pass


class AIPrediction(Base):
    __tablename__ = "ai_predictions"
    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[str] = mapped_column(String(128), index=True)
    prediction: Mapped[str] = mapped_column(String(100), index=True)
    confidence_score: Mapped[float] = mapped_column(Float)
    anomaly: Mapped[bool] = mapped_column(default=False)
    features: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), index=True)


class RiskScore(Base):
    __tablename__ = "risk_scores"
    id: Mapped[int] = mapped_column(primary_key=True)
    threat_id: Mapped[str] = mapped_column(String(128), index=True)
    risk_score: Mapped[float] = mapped_column(Float)
    severity: Mapped[str] = mapped_column(String(20), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), index=True)


class AIAlert(Base):
    __tablename__ = "ai_alerts"
    id: Mapped[int] = mapped_column(primary_key=True)
    alert_type: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[str] = mapped_column(Text)
    priority: Mapped[str] = mapped_column(String(20), index=True)
    status: Mapped[str] = mapped_column(String(30), default="new", index=True)
    event_id: Mapped[str] = mapped_column(String(128), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), index=True)


settings = get_settings()
connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


async def get_db() -> AsyncGenerator[Session, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def initialize_database() -> None:
    Base.metadata.create_all(bind=engine)


class AIRepository:
    def __init__(self, session: Session):
        self.session = session

    def save_analysis(self, *, event_id: str, prediction: str, confidence: float, anomaly: bool, features: dict, risk_score: float, severity: str, alert: dict | None) -> tuple[AIPrediction, RiskScore, AIAlert | None]:
        prediction_row = AIPrediction(event_id=event_id, prediction=prediction, confidence_score=confidence, anomaly=anomaly, features=features)
        risk_row = RiskScore(threat_id=event_id, risk_score=risk_score, severity=severity)
        alert_row = AIAlert(event_id=event_id, **alert) if alert else None
        self.session.add_all([prediction_row, risk_row] + ([alert_row] if alert_row else []))
        self.session.commit()
        return prediction_row, risk_row, alert_row

    def predictions(self, limit: int) -> list[AIPrediction]:
        return list(self.session.scalars(select(AIPrediction).order_by(AIPrediction.created_at.desc()).limit(limit)))

    def risks(self, limit: int) -> list[RiskScore]:
        return list(self.session.scalars(select(RiskScore).order_by(RiskScore.created_at.desc()).limit(limit)))

    def alerts(self, limit: int) -> list[AIAlert]:
        return list(self.session.scalars(select(AIAlert).order_by(AIAlert.created_at.desc()).limit(limit)))
