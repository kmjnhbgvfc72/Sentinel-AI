def clamp(value: float, minimum: float = 0, maximum: float = 100) -> float:
    return round(max(minimum, min(float(value), maximum)), 2)


def severity_for_score(score: float) -> str:
    return "critical" if score >= 85 else "high" if score >= 70 else "medium" if score >= 40 else "low"
