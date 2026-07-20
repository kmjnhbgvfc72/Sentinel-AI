"""Threat-intelligence enrichment pipeline."""
from .mitre_mapper import MitreMapper
from .reputation_engine import ReputationEngine


class IntelligenceProcessor:
    def __init__(self) -> None:
        self.mapper, self.reputation = MitreMapper(), ReputationEngine()

    def enrich(self, event: dict[str, object]) -> dict[str, object]:
        behaviors = [str(v) for v in event.get("behaviors", [])]
        reputation = self.reputation.score(float(event.get("confidence", 0.5)), sightings=int(event.get("sightings", 1)))
        return {**event, "mitre": self.mapper.map(behaviors), "reputation": reputation}
