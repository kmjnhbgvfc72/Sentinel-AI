"""Explainable behavior-sequence analysis."""

WEIGHTS = {"powershell_encoded": 30, "credential_access": 35, "unusual_parent": 20, "persistence_change": 25, "lateral_movement": 35, "dns_beaconing": 30}


class BehaviorAnalyzer:
    def analyze(self, behaviors: list[str]) -> dict[str, object]:
        matched = sorted(set(behaviors) & WEIGHTS.keys())
        score = min(100, sum(WEIGHTS[item] for item in matched))
        return {"risk_score": score, "severity": "critical" if score >= 80 else "high" if score >= 60 else "medium" if score >= 30 else "low", "matched_behaviors": matched}
