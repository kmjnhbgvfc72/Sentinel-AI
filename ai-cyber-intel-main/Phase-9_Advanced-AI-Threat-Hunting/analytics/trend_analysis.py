"""Time-bucketed threat trends."""
from collections import Counter


class TrendAnalyzer:
    def analyze(self, events: list[dict[str, object]]) -> list[dict[str, object]]:
        counts = Counter(str(event.get("timestamp", "unknown"))[:10] for event in events)
        return [{"date": date, "count": count} for date, count in sorted(counts.items())]
