"""Portable report generation."""
from datetime import datetime, timezone


class ReportGenerator:
    def generate(self, title: str, statistics: dict[str, object], trends: list[dict[str, object]]) -> dict[str, object]:
        return {"title": title, "generated_at": datetime.now(timezone.utc).isoformat(), "summary": statistics, "trends": trends, "classification": "INTERNAL"}
