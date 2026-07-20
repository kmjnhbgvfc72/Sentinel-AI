"""Interpretable attack-likelihood forecasting."""
from math import exp
from .confidence_score import ConfidenceScorer


class AttackForecaster:
    def __init__(self) -> None:
        self.confidence = ConfidenceScorer()

    def forecast(self, indicators: dict[str, float], horizon_hours: int = 24) -> dict[str, object]:
        if not 1 <= horizon_hours <= 720:
            raise ValueError("horizon must be between 1 and 720 hours")
        weights = {"threat_velocity": 1.1, "asset_exposure": 0.9, "vulnerability_score": 0.8, "adversary_activity": 1.2}
        linear = -2.0 + sum(weights[key] * min(1.0, max(0.0, float(indicators.get(key, 0)))) for key in weights)
        probability = round(1 / (1 + exp(-linear)), 4)
        confidence = self.confidence.calculate(probability, float(indicators.get("data_quality", 0.7)), int(indicators.get("evidence_count", 1)))
        return {"horizon_hours": horizon_hours, "attack_probability": probability, "confidence": confidence, "risk_band": "critical" if probability >= 0.8 else "high" if probability >= 0.6 else "medium" if probability >= 0.35 else "low", "drivers": sorted(weights, key=lambda k: indicators.get(k, 0), reverse=True)[:3]}
