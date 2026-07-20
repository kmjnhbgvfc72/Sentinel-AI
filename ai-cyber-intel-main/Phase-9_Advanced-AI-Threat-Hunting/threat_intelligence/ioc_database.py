"""Thread-safe IOC repository with PostgreSQL-compatible domain semantics."""
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from ipaddress import ip_address
from threading import RLock
from urllib.parse import urlparse
from uuid import uuid4
import re

IOC_TYPES = {"ipv4", "ipv6", "domain", "url", "sha256", "md5", "email"}


@dataclass(frozen=True)
class IOC:
    id: str
    type: str
    value: str
    confidence: float
    source: str
    tags: tuple[str, ...]
    first_seen: str


def validate_ioc(ioc_type: str, value: str) -> str:
    value = value.strip().lower()
    if ioc_type not in IOC_TYPES:
        raise ValueError("unsupported IOC type")
    if ioc_type.startswith("ipv"):
        parsed = ip_address(value)
        if parsed.version != int(ioc_type[-1]):
            raise ValueError("IP version does not match IOC type")
    elif ioc_type == "domain" and not re.fullmatch(r"(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}", value):
        raise ValueError("invalid domain")
    elif ioc_type == "url" and urlparse(value).scheme not in {"http", "https"}:
        raise ValueError("invalid URL")
    elif ioc_type in {"sha256", "md5"} and not re.fullmatch(r"[0-9a-f]{64}" if ioc_type == "sha256" else r"[0-9a-f]{32}", value):
        raise ValueError("invalid hash")
    elif ioc_type == "email" and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value):
        raise ValueError("invalid email")
    return value


class IOCDatabase:
    def __init__(self) -> None:
        self._items: dict[str, IOC] = {}
        self._lock = RLock()

    def upsert(self, ioc_type: str, value: str, confidence: float = 0.5, source: str = "manual", tags: list[str] | None = None) -> IOC:
        value = validate_ioc(ioc_type, value)
        if not 0 <= confidence <= 1:
            raise ValueError("confidence must be between zero and one")
        key = f"{ioc_type}:{value}"
        with self._lock:
            existing = self._items.get(key)
            item = IOC(existing.id if existing else str(uuid4()), ioc_type, value, confidence, source, tuple(sorted(set(tags or []))), existing.first_seen if existing else datetime.now(timezone.utc).isoformat())
            self._items[key] = item
            return item

    def get(self, ioc_type: str, value: str) -> IOC | None:
        return self._items.get(f"{ioc_type}:{value.strip().lower()}")

    def search(self, query: str = "", ioc_type: str | None = None) -> list[dict[str, object]]:
        query = query.lower()
        with self._lock:
            return [asdict(i) for i in self._items.values() if (not query or query in i.value) and (not ioc_type or i.type == ioc_type)]

    def count(self) -> int:
        return len(self._items)
