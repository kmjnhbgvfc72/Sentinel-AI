import csv
import io

from fastapi import APIRouter, Query, Response

from data import ALERTS, ASSETS, THREATS
from services.dashboard_service import risk_distribution, summary

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/security-summary")
async def security_summary(start_date: str | None = None, end_date: str | None = None) -> dict:
    return {"data": {"period": {"start": start_date, "end": end_date}, "posture": summary(), "severity_breakdown": risk_distribution(), "alert_resolution": {"resolved": sum(a["status"] == "resolved" for a in ALERTS), "open": sum(a["status"] != "resolved" for a in ALERTS)}, "most_affected_assets": sorted(ASSETS, key=lambda item: item["open_alerts"], reverse=True)[:5], "trends": "Risk decreased by 4 points compared with the previous reporting period."}}


@router.get("/export.csv", response_class=Response)
async def export_csv(dataset: str = Query("threats", pattern="^(threats|alerts|assets)$")) -> Response:
    records = {"threats": THREATS, "alerts": ALERTS, "assets": ASSETS}[dataset]
    safe_fields = {"threats": ["external_id", "title", "category", "severity", "confidence_score", "source", "target_asset", "status"], "alerts": ["id", "title", "severity", "source", "asset", "status", "created_at"], "assets": ["id", "name", "asset_type", "hostname", "department", "health_status", "risk_score", "open_alerts"]}[dataset]
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=safe_fields, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(records)
    return Response(output.getvalue(), media_type="text/csv", headers={"Content-Disposition": f'attachment; filename="soc-{dataset}.csv"'})
