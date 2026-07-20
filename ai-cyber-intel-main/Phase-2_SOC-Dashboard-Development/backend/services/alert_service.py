from datetime import UTC, datetime

from data import ALERTS, ALERT_HISTORY
from schemas import AlertStatus
from services.query_service import filter_records, paginate, sort_records

TRANSITIONS = {
    "new": {"investigating", "acknowledged", "resolved"},
    "investigating": {"acknowledged", "resolved"},
    "acknowledged": {"investigating", "resolved"},
    "resolved": {"investigating"},
}


def list_alerts(page: int, page_size: int, search: str | None, severity: str | None, status: str | None, sort_by: str, sort_order: str) -> tuple[list[dict], dict]:
    records = filter_records(ALERTS, search=search, filters={"severity": severity, "status": status})
    records = sort_records(records, "alerts", sort_by, sort_order)
    return paginate(records, page, page_size)


def get_alert(alert_id: int) -> dict | None:
    return next((item for item in ALERTS if item["id"] == alert_id), None)


def change_status(alert_id: int, new_status: AlertStatus, changed_by: str) -> dict:
    alert = get_alert(alert_id)
    if not alert:
        raise LookupError("Alert not found")
    current = alert["status"]
    if new_status.value == current:
        raise ValueError("Alert already has the requested status")
    if new_status.value not in TRANSITIONS[current]:
        raise ValueError(f"Transition from {current} to {new_status.value} is not allowed")
    timestamp = datetime.now(UTC).isoformat()
    alert["status"] = new_status.value
    alert["updated_at"] = timestamp
    if new_status == AlertStatus.acknowledged:
        alert["acknowledged_at"] = timestamp
    if new_status == AlertStatus.resolved:
        alert["resolved_at"] = timestamp
    elif current == "resolved":
        alert["resolved_at"] = None
    ALERT_HISTORY.append({"id": len(ALERT_HISTORY) + 1, "alert_id": alert_id, "previous_status": current, "new_status": new_status.value, "changed_at": timestamp, "changed_by": changed_by})
    return alert
