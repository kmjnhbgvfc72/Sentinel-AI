def risk_level(score: float) -> str:
    return "critical" if score >= 85 else "high" if score >= 70 else "medium" if score >= 40 else "low"


def clamp(value: float) -> float:
    return round(max(0.0, min(float(value), 100.0)), 2)
