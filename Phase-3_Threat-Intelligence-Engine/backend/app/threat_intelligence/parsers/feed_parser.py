from typing import Any


def parse_feed_record(raw: dict[str, Any]) -> dict[str, Any]:
    missing = {"name", "type", "severity", "source"}.difference(raw)
    if missing:
        raise ValueError(f"Missing feed fields: {', '.join(sorted(missing))}")
    return {"name": str(raw["name"]).strip(), "type": str(raw["type"]).strip().lower(), "description": str(raw.get("description", "No description supplied")).strip(), "severity": str(raw["severity"]).lower(), "risk_score": max(0, min(float(raw.get("risk_score", 50)), 100)), "confidence_score": max(0, min(float(raw.get("confidence_score", 50)), 100)), "source": str(raw["source"]).strip(), "status": str(raw.get("status", "active")).lower()}
