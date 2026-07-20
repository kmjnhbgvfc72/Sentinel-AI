import re
from typing import Any

DOMAIN_PATTERN = re.compile(r"^(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$")


class DomainReputationCollector:
    def normalize(self, record: dict[str, Any]) -> dict[str, Any]:
        domain = record["domain"].strip().lower().rstrip(".")
        if not DOMAIN_PATTERN.fullmatch(domain):
            raise ValueError("Invalid domain indicator")
        score = max(0.0, min(float(record.get("reputation_score", 0)), 100.0))
        return {"indicator_type": "domain", "value": domain, "reputation_score": score, "confidence_score": float(record.get("confidence_score", score)), "threat_category": record.get("category", "unknown"), "country": None, "status": record.get("status", "suspicious")}
