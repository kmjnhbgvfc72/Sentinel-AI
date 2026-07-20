"""Defensive feed ingestion and deduplication."""
from .ioc_database import IOCDatabase


class FeedManager:
    def __init__(self, database: IOCDatabase) -> None:
        self.database = database

    def ingest(self, records: list[dict[str, object]], source: str) -> dict[str, object]:
        accepted, rejected = 0, []
        for index, record in enumerate(records):
            try:
                self.database.upsert(str(record["type"]), str(record["value"]), float(record.get("confidence", 0.5)), source, list(record.get("tags", [])))
                accepted += 1
            except (KeyError, TypeError, ValueError) as exc:
                rejected.append({"index": index, "reason": str(exc)})
        return {"source": source, "accepted": accepted, "rejected": rejected}
