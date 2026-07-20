SEVERITY_WEIGHT = {"low": 10, "medium": 30, "high": 55, "critical": 75}


class ThreatScoreCalculator:
    def calculate(self, *, confidence: int, severity: str, reliability: int = 70, sightings: int = 1) -> int:
        score = SEVERITY_WEIGHT.get(severity, 30)
        score += confidence * 0.15
        score += reliability * 0.08
        score += min(sightings, 10) * 0.5
        return max(0, min(100, round(score)))

    @staticmethod
    def verdict(score: int) -> str:
        if score >= 80:
            return "malicious"
        if score >= 50:
            return "suspicious"
        return "unknown"
