from dataclasses import dataclass


@dataclass(frozen=True)
class RiskFactors:
    anomaly_score: float
    asset_criticality: float
    threat_confidence: float
    exposure: float


def calculate_risk(factors: RiskFactors) -> float:
    values = [factors.anomaly_score, factors.asset_criticality, factors.threat_confidence, factors.exposure]
    if any(not 0 <= value <= 1 for value in values):
        raise ValueError("Risk factors must be between 0 and 1")
    return round(100 * (0.35 * values[0] + 0.3 * values[1] + 0.25 * values[2] + 0.1 * values[3]), 2)


def risk_level(score: float) -> str:
    return "critical" if score >= 85 else "high" if score >= 65 else "medium" if score >= 35 else "low"

