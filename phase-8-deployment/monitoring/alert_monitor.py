from collections import Counter


def alert_summary(alerts: list[dict]) -> dict:
    return {"total": len(alerts), "by_severity": dict(Counter(a.get("severity", "unknown") for a in alerts)), "open": sum(a.get("status") == "open" for a in alerts)}

