from collections.abc import Iterable
from typing import Any

from app.threat_intelligence.parsers.log_parser import parse_log
from app.threat_intelligence.utils import sanitize_log_details

ALLOWED_LOG_TYPES = {"authentication", "firewall", "application"}


class LogCollector:
    def collect(self, records: Iterable[dict[str, Any]], *, max_records: int = 10_000) -> list[dict[str, Any]]:
        output = []
        for record in records:
            if len(output) >= max_records:
                break
            if record.get("log_type") not in ALLOWED_LOG_TYPES:
                raise ValueError("Unsupported log type")
            output.append(parse_log(sanitize_log_details(dict(record))))
        return output
