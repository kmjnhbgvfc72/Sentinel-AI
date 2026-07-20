"""Detection statistics."""
from collections import Counter


def detection_statistics(events: list[dict[str, object]]) -> dict[str, object]:
    severities = Counter(str(event.get("severity", "unknown")) for event in events)
    true_positive = sum(event.get("verdict") == "true_positive" for event in events)
    false_positive = sum(event.get("verdict") == "false_positive" for event in events)
    labeled = true_positive + false_positive
    return {"total": len(events), "by_severity": dict(severities), "precision": round(true_positive / labeled, 4) if labeled else None, "false_positive_rate": round(false_positive / labeled, 4) if labeled else None}
