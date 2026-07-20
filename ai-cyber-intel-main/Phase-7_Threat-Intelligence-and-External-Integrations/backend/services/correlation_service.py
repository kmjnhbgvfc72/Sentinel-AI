from database.repository import ThreatIntelligenceRepository
from services.integration_service import IntegrationService
from threat_intelligence.matching import IOCMatchingEngine
from threat_intelligence.scoring import ThreatScoreCalculator


class CorrelationService:
    def __init__(self, repository: ThreatIntelligenceRepository, integrations: IntegrationService):
        self.repository = repository
        self.integrations = integrations
        self.matcher = IOCMatchingEngine()
        self.scorer = ThreatScoreCalculator()

    async def correlate(self, *, refresh: bool = False) -> list:
        if refresh:
            iocs = self.repository.list_iocs(active=True, limit=5000)
            for phase, event in await self.integrations.fetch_events():
                for ioc in self.matcher.match(iocs, event):
                    event_id = str(event.get("id") or event.get("event_id") or event.get("prediction_id") or f"{phase}-{ioc.id}-{hash(str(sorted(event.items())))}")[:120]
                    base = int(event.get("risk_score", event.get("confidence", 50)) or 50)
                    score = min(100, round(base * 0.6 + self.scorer.calculate(confidence=ioc.confidence, severity=ioc.severity) * 0.4))
                    self.repository.add_correlation(ioc_id=ioc.id, external_event_id=event_id, source_phase=phase, match_type="exact", score=score, context={key: value for key, value in event.items() if key in {"source_ip", "destination_ip", "domain", "url", "severity", "threat_type", "asset"}})
            self.repository.add_history(action="correlation_refresh", entity_type="system", details={"sources": ["phase3", "phase4", "phase5", "phase6"]})
            self.repository.session.commit()
        return self.repository.list_correlations()

    def summary(self) -> dict:
        counts = self.repository.counts()
        statuses = self.repository.latest_statuses()
        healthy = sum(status.status == "healthy" for status in statuses)
        return {**counts, "healthy_feeds": healthy, "unhealthy_feeds": len(statuses) - healthy, "coverage_percent": round((healthy / counts["feeds"] * 100), 1) if counts["feeds"] else 0, "integration_phases": [3, 4, 5, 6]}
