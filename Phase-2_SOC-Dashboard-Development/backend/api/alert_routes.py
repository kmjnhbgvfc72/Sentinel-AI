from typing import Literal

from fastapi import APIRouter, HTTPException, Query

from schemas import AlertStatus, AlertStatusUpdate, Severity
from services import alert_service

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("")
async def list_alerts(
    page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100), search: str | None = Query(None, max_length=100),
    severity: Severity | None = None, status: AlertStatus | None = None,
    sort_by: Literal["id", "severity", "status", "created_at", "title"] = "created_at",
    sort_order: Literal["asc", "desc"] = "desc",
) -> dict:
    data, meta = alert_service.list_alerts(page, page_size, search, severity.value if severity else None, status.value if status else None, sort_by, sort_order)
    return {"data": data, "meta": meta}


@router.get("/{alert_id}")
async def get_alert(alert_id: int) -> dict:
    alert = alert_service.get_alert(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"data": alert}


@router.patch("/{alert_id}/status")
async def update_alert_status(alert_id: int, update: AlertStatusUpdate) -> dict:
    try:
        return {"data": alert_service.change_status(alert_id, update.status, update.changed_by), "message": "Alert status updated"}
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
