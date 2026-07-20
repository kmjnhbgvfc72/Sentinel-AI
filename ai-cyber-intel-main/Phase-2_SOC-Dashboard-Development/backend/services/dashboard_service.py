from collections import Counter

from data import ALERTS, ASSETS, THREATS, THREAT_TRENDS


def summary() -> dict:
    active_threats = sum(item["status"] in {"active", "investigating"} for item in THREATS)
    return {
        "active_threats": active_threats,
        "critical_alerts": sum(item["severity"] == "critical" and item["status"] != "resolved" for item in ALERTS),
        "protected_assets": len(ASSETS),
        "events_monitored": 128_493,
        "resolved_incidents": sum(item["status"] == "resolved" for item in ALERTS),
        "risk": {"score": 72, "level": "high", "trend": -4, "previous_score": 76},
    }


def threat_trends(range_key: str) -> dict:
    return {"range": range_key, "points": THREAT_TRENDS}


def risk_distribution() -> list[dict]:
    counts = Counter(item["severity"] for item in THREATS)
    total = max(1, len(THREATS))
    return [{"severity": severity, "count": counts[severity], "percentage": round(counts[severity] * 100 / total, 1)} for severity in ("critical", "high", "medium", "low")]


def recent_alerts(limit: int) -> list[dict]:
    return sorted(ALERTS, key=lambda item: item["created_at"], reverse=True)[:limit]


def top_assets(limit: int) -> list[dict]:
    return sorted(ASSETS, key=lambda item: item["risk_score"], reverse=True)[:limit]
