"""IOC extraction and lookup engine."""
import re
from threat_intelligence.ioc_database import IOCDatabase

PATTERNS = {"ipv4": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"), "domain": re.compile(r"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,63}\b"), "sha256": re.compile(r"\b[a-fA-F0-9]{64}\b")}


class IOCEngine:
    def __init__(self, database: IOCDatabase) -> None:
        self.database = database

    def extract(self, text: str) -> list[dict[str, str]]:
        found, seen = [], set()
        for ioc_type, pattern in PATTERNS.items():
            for value in pattern.findall(text):
                key = (ioc_type, value.lower())
                if key not in seen:
                    seen.add(key)
                    found.append({"type": ioc_type, "value": value.lower()})
        return found

    def detect(self, text: str) -> list[dict[str, object]]:
        matches = []
        for item in self.extract(text):
            known = self.database.get(item["type"], item["value"])
            if known:
                matches.append({**item, "known": True, "confidence": known.confidence, "source": known.source})
        return matches
