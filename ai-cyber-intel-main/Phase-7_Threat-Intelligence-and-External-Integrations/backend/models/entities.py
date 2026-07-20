from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Index, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.connection import Base


def utcnow() -> datetime:
    return datetime.now(UTC)


class ThreatFeed(Base):
    __tablename__ = "threat_feeds"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    url: Mapped[str] = mapped_column(String(2048))
    format: Mapped[str] = mapped_column(String(20), default="json")
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    reliability: Mapped[int] = mapped_column(Integer, default=70)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)
    statuses: Mapped[list["FeedStatus"]] = relationship(back_populates="feed", cascade="all, delete-orphan")


class IOCIndicator(Base):
    __tablename__ = "ioc_indicators"
    __table_args__ = (UniqueConstraint("type", "normalized_value", name="uq_ioc_type_value"), Index("ix_ioc_active_type", "active", "type"))
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(20), index=True)
    value: Mapped[str] = mapped_column(String(2048))
    normalized_value: Mapped[str] = mapped_column(String(2048), index=True)
    threat_type: Mapped[str] = mapped_column(String(100), default="unknown")
    confidence: Mapped[int] = mapped_column(Integer, default=50)
    severity: Mapped[str] = mapped_column(String(20), default="medium", index=True)
    source: Mapped[str] = mapped_column(String(120), default="manual")
    tags: Mapped[list] = mapped_column(JSON, default=list)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    first_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class ThreatIntelligenceHistory(Base):
    __tablename__ = "threat_intelligence_history"
    id: Mapped[int] = mapped_column(primary_key=True)
    action: Mapped[str] = mapped_column(String(50), index=True)
    entity_type: Mapped[str] = mapped_column(String(50))
    entity_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    details: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)


class FeedStatus(Base):
    __tablename__ = "feed_status"
    id: Mapped[int] = mapped_column(primary_key=True)
    feed_id: Mapped[int] = mapped_column(ForeignKey("threat_feeds.id", ondelete="CASCADE"), index=True)
    status: Mapped[str] = mapped_column(String(20), index=True)
    fetched_count: Mapped[int] = mapped_column(Integer, default=0)
    accepted_count: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    checked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)
    feed: Mapped[ThreatFeed] = relationship(back_populates="statuses")


class ReputationCache(Base):
    __tablename__ = "reputation_cache"
    __table_args__ = (UniqueConstraint("indicator_type", "normalized_value", name="uq_reputation_indicator"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    indicator_type: Mapped[str] = mapped_column(String(20))
    value: Mapped[str] = mapped_column(String(2048))
    normalized_value: Mapped[str] = mapped_column(String(2048), index=True)
    score: Mapped[int] = mapped_column(Integer)
    verdict: Mapped[str] = mapped_column(String(20))
    sources: Mapped[list] = mapped_column(JSON, default=list)
    details: Mapped[dict] = mapped_column(JSON, default=dict)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class CorrelationResult(Base):
    __tablename__ = "correlation_results"
    id: Mapped[int] = mapped_column(primary_key=True)
    ioc_id: Mapped[int] = mapped_column(ForeignKey("ioc_indicators.id", ondelete="CASCADE"), index=True)
    external_event_id: Mapped[str] = mapped_column(String(120), index=True)
    source_phase: Mapped[str] = mapped_column(String(20), index=True)
    match_type: Mapped[str] = mapped_column(String(30))
    score: Mapped[float] = mapped_column(Float)
    context: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)
