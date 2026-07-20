import ipaddress
from typing import Any


class IPReputationCollector:
    def normalize(self, record: dict[str, Any]) -> dict[str, Any]:
        address = str(ipaddress.ip_address(record["ip_address"]))
        score = max(0.0, min(float(record.get("reputation_score", 0)), 100.0))
        return {"indicator_type": "ip", "value": address, "reputation_score": score, "confidence_score": float(record.get("confidence_score", score)), "threat_category": record.get("threat_category", "unknown"), "country": record.get("country"), "status": "malicious" if score >= 80 else "suspicious" if score >= 50 else "observed"}
