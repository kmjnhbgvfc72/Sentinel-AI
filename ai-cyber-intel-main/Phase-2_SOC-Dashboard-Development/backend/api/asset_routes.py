from typing import Literal

from fastapi import APIRouter, HTTPException, Query

from data import ASSETS
from services.query_service import filter_records, paginate, sort_records

router = APIRouter(prefix="/assets", tags=["Assets"])


@router.get("")
async def list_assets(
    page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100), search: str | None = Query(None, max_length=100),
    asset_type: str | None = Query(None, max_length=50), health_status: str | None = Query(None, max_length=30), risk_level: Literal["low", "medium", "high", "critical"] | None = None,
    sort_by: Literal["id", "name", "asset_type", "health_status", "risk_score", "last_seen_at"] = "risk_score", sort_order: Literal["asc", "desc"] = "desc",
) -> dict:
    records = filter_records(ASSETS, search=search, filters={"asset_type": asset_type, "health_status": health_status})
    if risk_level:
        ranges = {"low": (0, 29), "medium": (30, 59), "high": (60, 79), "critical": (80, 100)}
        low, high = ranges[risk_level]
        records = [item for item in records if low <= item["risk_score"] <= high]
    records = sort_records(records, "assets", sort_by, sort_order)
    data, meta = paginate(records, page, page_size)
    return {"data": data, "meta": meta}


@router.get("/{asset_id}")
async def get_asset(asset_id: int) -> dict:
    asset = next((item for item in ASSETS if item["id"] == asset_id), None)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return {"data": asset}
