from datetime import UTC, datetime, timedelta

from app.errors import ServiceError
from config.settings import Settings
from database.repository import ThreatIntelligenceRepository
from threat_intelligence.scoring import ThreatScoreCalculator
from threat_intelligence.validation import IOCValidationError, normalize_ioc


class ReputationService:
    def __init__(self, repository: ThreatIntelligenceRepository, settings: Settings):
        self.repository = repository
        self.settings = settings
        self.scorer = ThreatScoreCalculator()

    async def lookup(self, ioc_type: str, value: str) -> dict:
        try:
            normalized = normalize_ioc(ioc_type, value)
        except IOCValidationError as exc:
            raise ServiceError(str(exc), code="invalid_indicator", status_code=422) from exc
        cached = self.repository.get_reputation(ioc_type, normalized)
        if cached:
            return self._serialize(cached, cached=True)
        local = self.repository.find_ioc(ioc_type, normalized)
        sources: list[str] = []
        if local:
            score = self.scorer.calculate(confidence=local.confidence, severity=local.severity, sightings=1)
            sources.append(local.source)
            details = {"local_ioc_id": local.id, "threat_type": local.threat_type, "confidence": local.confidence, "note": "Local defensive intelligence match"}
        else:
            score, details = 0, {"note": "No local or configured-provider intelligence found"}
        row = self.repository.upsert_reputation(indicator_type=ioc_type, value=value, normalized_value=normalized, score=score, verdict=self.scorer.verdict(score), sources=sources, details=details, expires_at=datetime.now(UTC) + timedelta(seconds=self.settings.reputation_cache_ttl_seconds), updated_at=datetime.now(UTC))
        self.repository.session.commit()
        self.repository.session.refresh(row)
        return self._serialize(row, cached=False)

    @staticmethod
    def _serialize(row, *, cached: bool) -> dict:
        return {"type": row.indicator_type, "value": row.value, "score": row.score, "verdict": row.verdict, "sources": row.sources, "details": row.details, "cached": cached}
