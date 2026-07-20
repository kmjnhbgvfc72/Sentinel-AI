from datetime import UTC, datetime

from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from models.entities import CorrelationResult, FeedStatus, IOCIndicator, ReputationCache, ThreatFeed, ThreatIntelligenceHistory


class ThreatIntelligenceRepository:
    def __init__(self, session: Session):
        self.session = session

    def list_feeds(self) -> list[ThreatFeed]:
        return list(self.session.scalars(select(ThreatFeed).order_by(ThreatFeed.name)))

    def enabled_feeds(self) -> list[ThreatFeed]:
        return list(self.session.scalars(select(ThreatFeed).where(ThreatFeed.enabled.is_(True))))

    def get_feed(self, feed_id: int) -> ThreatFeed | None:
        return self.session.get(ThreatFeed, feed_id)

    def list_iocs(self, *, ioc_type: str | None = None, active: bool | None = None, limit: int = 200) -> list[IOCIndicator]:
        query = select(IOCIndicator)
        if ioc_type:
            query = query.where(IOCIndicator.type == ioc_type)
        if active is not None:
            query = query.where(IOCIndicator.active.is_(active))
        return list(self.session.scalars(query.order_by(desc(IOCIndicator.last_seen)).limit(limit)))

    def get_ioc(self, ioc_id: int) -> IOCIndicator | None:
        return self.session.get(IOCIndicator, ioc_id)

    def find_ioc(self, ioc_type: str, normalized_value: str) -> IOCIndicator | None:
        return self.session.scalar(select(IOCIndicator).where(IOCIndicator.type == ioc_type, IOCIndicator.normalized_value == normalized_value))

    def upsert_ioc(self, **values) -> tuple[IOCIndicator, bool]:
        existing = self.find_ioc(values["type"], values["normalized_value"])
        if existing:
            existing.last_seen = values.get("last_seen", datetime.now(UTC))
            existing.confidence = max(existing.confidence, values.get("confidence", 0))
            existing.active = True
            existing.tags = sorted(set(existing.tags + values.get("tags", [])))
            return existing, False
        item = IOCIndicator(**values)
        self.session.add(item)
        self.session.flush()
        return item, True

    def delete_ioc(self, item: IOCIndicator) -> None:
        self.session.delete(item)

    def add_status(self, **values) -> FeedStatus:
        status = FeedStatus(**values)
        self.session.add(status)
        return status

    def latest_statuses(self) -> list[FeedStatus]:
        latest = select(FeedStatus.feed_id, func.max(FeedStatus.id).label("max_id")).group_by(FeedStatus.feed_id).subquery()
        return list(self.session.scalars(select(FeedStatus).join(latest, FeedStatus.id == latest.c.max_id).order_by(FeedStatus.feed_id)))

    def add_history(self, **values) -> None:
        self.session.add(ThreatIntelligenceHistory(**values))

    def get_reputation(self, ioc_type: str, normalized_value: str) -> ReputationCache | None:
        return self.session.scalar(select(ReputationCache).where(ReputationCache.indicator_type == ioc_type, ReputationCache.normalized_value == normalized_value, ReputationCache.expires_at > datetime.now(UTC)))

    def upsert_reputation(self, **values) -> ReputationCache:
        row = self.session.scalar(select(ReputationCache).where(ReputationCache.indicator_type == values["indicator_type"], ReputationCache.normalized_value == values["normalized_value"]))
        if row:
            for key, value in values.items():
                setattr(row, key, value)
            return row
        row = ReputationCache(**values)
        self.session.add(row)
        return row

    def add_correlation(self, **values) -> CorrelationResult:
        existing = self.session.scalar(select(CorrelationResult).where(CorrelationResult.ioc_id == values["ioc_id"], CorrelationResult.external_event_id == values["external_event_id"], CorrelationResult.source_phase == values["source_phase"]))
        if existing:
            existing.score = values["score"]
            existing.context = values["context"]
            return existing
        row = CorrelationResult(**values)
        self.session.add(row)
        return row

    def list_correlations(self, limit: int = 100) -> list[CorrelationResult]:
        return list(self.session.scalars(select(CorrelationResult).order_by(desc(CorrelationResult.created_at)).limit(limit)))

    def counts(self) -> dict[str, int]:
        return {
            "feeds": self.session.scalar(select(func.count()).select_from(ThreatFeed)) or 0,
            "active_iocs": self.session.scalar(select(func.count()).select_from(IOCIndicator).where(IOCIndicator.active.is_(True))) or 0,
            "critical_iocs": self.session.scalar(select(func.count()).select_from(IOCIndicator).where(IOCIndicator.active.is_(True), IOCIndicator.severity == "critical")) or 0,
            "correlations": self.session.scalar(select(func.count()).select_from(CorrelationResult)) or 0,
        }
