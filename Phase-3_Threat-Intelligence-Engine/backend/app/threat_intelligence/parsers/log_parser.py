import ipaddress
from datetime import UTC, datetime
from typing import Any


def parse_log(raw: dict[str, Any]) -> dict[str, Any]:
    event = str(raw.get("event_type", raw.get("event", "user_activity"))).strip().lower().replace(" ", "_")
    status = str(raw.get("status", raw.get("outcome", "unknown"))).strip().lower()
    address = raw.get("ip_address", raw.get("source_ip"))
    if address:
        address = str(ipaddress.ip_address(address))
    timestamp = raw.get("created_at", raw.get("timestamp", datetime.now(UTC)))
    parsed_time = datetime.fromisoformat(timestamp.replace("Z", "+00:00")) if isinstance(timestamp, str) else timestamp
    failed_count = max(0, int(raw.get("failed_login_count", 0)))
    unknown_ip = bool(raw.get("unknown_ip", False))
    abnormal_time = parsed_time.hour < 5 or parsed_time.hour >= 23
    score = min(100, failed_count * 6 + (30 if unknown_ip else 0) + (15 if abnormal_time else 0) + (20 if "suspicious" in event else 0))
    risk_level = "critical" if score >= 85 else "high" if score >= 70 else "medium" if score >= 40 else "low"
    return {"user_id": str(raw.get("user_id", "anonymous"))[:128], "event_type": event[:64], "ip_address": address, "device": str(raw.get("device", "unknown"))[:160], "status": status[:32], "risk_level": risk_level, "risk_score": float(score), "details": {"log_type": raw["log_type"], "failed_login_count": failed_count, "unknown_ip": unknown_ip, "abnormal_time": abnormal_time, **raw.get("metadata", {})}, "created_at": parsed_time}
