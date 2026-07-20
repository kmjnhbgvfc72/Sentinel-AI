from collections.abc import Iterable
from typing import Any

ALLOWED_SORT_FIELDS = {
    "threats": {"id", "severity", "confidence_score", "first_detected_at", "last_detected_at", "title"},
    "alerts": {"id", "severity", "status", "created_at", "title"},
    "assets": {"id", "name", "asset_type", "health_status", "risk_score", "last_seen_at"},
}
SEVERITY_ORDER = {"low": 1, "medium": 2, "high": 3, "critical": 4}


def filter_records(records: Iterable[dict[str, Any]], *, search: str | None = None, filters: dict[str, str | None] | None = None) -> list[dict[str, Any]]:
    result = list(records)
    if search:
        needle = search.casefold()
        result = [item for item in result if any(needle in str(value).casefold() for value in item.values() if isinstance(value, (str, int)))]
    for field, value in (filters or {}).items():
        if value:
            result = [item for item in result if str(item.get(field, "")).casefold() == value.casefold()]
    return result


def sort_records(records: list[dict[str, Any]], resource: str, sort_by: str, sort_order: str) -> list[dict[str, Any]]:
    if sort_by not in ALLOWED_SORT_FIELDS[resource]:
        raise ValueError(f"Unsupported sort field for {resource}")
    key = (lambda item: SEVERITY_ORDER.get(item.get(sort_by), 0)) if sort_by == "severity" else (lambda item: item.get(sort_by) or "")
    return sorted(records, key=key, reverse=sort_order == "desc")


def paginate(records: list[dict[str, Any]], page: int, page_size: int) -> tuple[list[dict[str, Any]], dict[str, int]]:
    total = len(records)
    start = (page - 1) * page_size
    return records[start:start + page_size], {"page": page, "page_size": page_size, "total": total, "pages": max(1, (total + page_size - 1) // page_size)}
