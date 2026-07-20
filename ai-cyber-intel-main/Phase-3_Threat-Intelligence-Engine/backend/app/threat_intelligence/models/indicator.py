from datetime import UTC, datetime

from sqlalchemy import DateTime, Float, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Indicator(Base):
    __tablename__ = "indicators"
    __table_args__ = (UniqueConstraint("indicator_type", "value", name="uq_indicator_type_value"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    indicator_type: Mapped[str] = mapped_column(String(30), index=True)
    value: Mapped[str] = mapped_column(String(512), index=True)
    confidence_score: Mapped[float] = mapped_column(Float)
    reputation_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    threat_category: Mapped[str] = mapped_column(String(100))
    country: Mapped[str | None] = mapped_column(String(2), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="suspicious")
    first_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
