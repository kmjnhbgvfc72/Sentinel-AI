"""Correlate events by shared entities in a bounded time window."""
from collections import defaultdict


class ThreatCorrelator:
    def correlate(self, events: list[dict[str, object]]) -> list[dict[str, object]]:
        entities: dict[str, list[str]] = defaultdict(list)
        for event in events:
            for entity in event.get("entities", []):
                entities[str(entity)].append(str(event.get("id", "unknown")))
        return [{"entity": entity, "event_ids": sorted(set(ids)), "strength": min(1.0, len(set(ids)) / 3)} for entity, ids in entities.items() if len(set(ids)) > 1]
