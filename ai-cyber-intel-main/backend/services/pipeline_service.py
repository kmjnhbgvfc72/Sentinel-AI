from typing import Any

from backend.config import Settings
from backend.integrations.phase_client import PhaseClient
from backend.integrations.registry import build_registry


class PipelineService:
    """Explicit synchronization bridge for the current phase HTTP contracts."""

    def __init__(self, settings: Settings):
        registry = build_registry(settings)
        self.clients = {number: PhaseClient(phase, settings) for number, phase in registry.items()}

    async def synchronize(self, limit: int = 20) -> dict[str, Any]:
        source = await self.clients[3].json("GET", f"/api/logs?page_size={limit}")
        analyzed: list[dict] = []
        predicted: list[dict] = []
        errors: list[dict] = []

        for row in source.get("data", []):
            details = row.get("details") or {}
            event = {
                "event_id": f"phase3-log-{row['id']}",
                "event_type": row.get("event_type", "unknown"),
                "severity": row.get("risk_level", "low"),
                "failed_login_count": int(details.get("failed_login_count", 0)),
                "unknown_ip": bool(details.get("unknown_ip", False)),
                "abnormal_time": bool(details.get("abnormal_time", False)),
                "activity_frequency": float(details.get("activity_frequency", 0)),
                "historical_average": float(details.get("historical_average", 0)),
            }
            try:
                result = await self.clients[4].json("POST", "/api/ai/analyze", content=_json_bytes(event), content_type="application/json")
                detection = result["data"]
                analyzed.append(detection)
                attack_event = {
                    "event_id": event["event_id"],
                    "threat_type": detection.get("threat_type", "Unknown Threat"),
                    "severity": detection.get("severity", event["severity"]),
                    "confidence": detection.get("confidence", 50),
                    "risk_score": detection.get("risk_score", 0),
                    "source_ip": row.get("ip_address") or "unknown",
                    "user": row.get("user_id") or "unknown",
                    "source_asset": details.get("source_asset", "Unknown Source"),
                    "target_asset": details.get("target_asset", "Unknown Target"),
                }
                path_result = await self.clients[5].json("POST", "/api/attack/analyze", content=_json_bytes(attack_event), content_type="application/json")
                predicted.append(path_result["data"])
            except Exception as exc:
                errors.append({"event_id": event["event_id"], "error": str(exc)})

        return {"source_events": len(source.get("data", [])), "detections_created": len(analyzed), "path_analyses_created": len(predicted), "errors": errors}


def _json_bytes(value: dict) -> bytes:
    import json

    return json.dumps(value).encode("utf-8")
