"""Analyst feedback aggregation and false-positive control."""
from collections import defaultdict
from threading import RLock


class FeedbackEngine:
    def __init__(self) -> None:
        self._items: list[dict[str, object]] = []
        self._lock = RLock()

    def record(self, detection_id: str, verdict: str, rule_id: str = "unknown") -> dict[str, object]:
        if verdict not in {"true_positive", "false_positive", "unknown"}:
            raise ValueError("unsupported verdict")
        item = {"detection_id": detection_id, "verdict": verdict, "rule_id": rule_id}
        with self._lock:
            self._items.append(item)
        return item

    def quality(self) -> dict[str, object]:
        with self._lock:
            counts: dict[str, int] = defaultdict(int)
            for item in self._items:
                counts[str(item["verdict"])] += 1
        labeled = counts["true_positive"] + counts["false_positive"]
        precision = counts["true_positive"] / labeled if labeled else 0.0
        return {"total": len(self._items), "precision": round(precision, 4), "counts": dict(counts)}

    def noisy_rules(self, minimum_feedback: int = 3, threshold: float = 0.5) -> list[str]:
        grouped: dict[str, list[bool]] = defaultdict(list)
        for item in self._items:
            if item["verdict"] != "unknown":
                grouped[str(item["rule_id"])].append(item["verdict"] == "false_positive")
        return [rule for rule, values in grouped.items() if len(values) >= minimum_feedback and sum(values) / len(values) >= threshold]
