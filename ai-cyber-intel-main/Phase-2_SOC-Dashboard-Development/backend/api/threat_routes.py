from typing import Literal

from fastapi import APIRouter, HTTPException, Query

from data import THREATS
from schemas import Severity, ThreatStatus
from services.query_service import filter_records, paginate, sort_records

router = APIRouter(prefix="/threats", tags=["Threats"])


@router.get("")
async def list_threats(
    page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100), search: str | None = Query(None, max_length=100),
    severity: Severity | None = None, status: ThreatStatus | None = None, threat_type: str | None = Query(None, max_length=100),
    start_date: str | None = None, end_date: str | None = None,
    sort_by: Literal["id", "severity", "confidence_score", "first_detected_at", "last_detected_at", "title"] = "last_detected_at",
    sort_order: Literal["asc", "desc"] = "desc",
) -> dict:
    del start_date, end_date
    records = filter_records(THREATS, search=search, filters={"severity": severity.value if severity else None, "status": status.value if status else None, "category": threat_type})
    records = sort_records(records, "threats", sort_by, sort_order)
    data, meta = paginate(records, page, page_size)
    return {"data": data, "meta": meta}


@router.get("/{threat_id}")
async def get_threat(threat_id: int) -> dict:
    threat = next((item for item in THREATS if item["id"] == threat_id), None)
    if not threat:
        raise HTTPException(status_code=404, detail="Threat not found")
    return {"data": threat}
