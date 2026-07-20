"""Explainable reputation scoring."""


class ReputationEngine:
    def score(self, confidence: float, source_reliability: float = 0.7, sightings: int = 1, age_days: int = 0) -> dict[str, object]:
        freshness = max(0.1, 1 - age_days / 365)
        corroboration = min(1.0, 0.3 + sightings * 0.1)
        score = round(100 * (0.5 * confidence + 0.3 * source_reliability + 0.2 * corroboration) * freshness, 2)
        return {"score": score, "classification": "malicious" if score >= 70 else "suspicious" if score >= 40 else "unknown", "factors": {"freshness": round(freshness, 3), "corroboration": corroboration}}
