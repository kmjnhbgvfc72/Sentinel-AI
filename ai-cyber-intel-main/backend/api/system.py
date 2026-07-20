from fastapi import APIRouter, Depends

from backend.config import Settings, get_settings
from backend.integrations.registry import build_registry
from backend.services.health_service import HealthService
from backend.services.overview_service import OverviewService

router = APIRouter(prefix="/system", tags=["Central system"])


@router.get("/health")
async def health(settings: Settings = Depends(get_settings)) -> dict:
    phases = await HealthService(settings).all_phases()
    available = sum(item["status"] == "healthy" for item in phases)
    return {"status": "healthy", "central_api": settings.app_version, "available_phases": available, "total_phases": len(phases), "phases": phases}


@router.get("/topology")
def topology(settings: Settings = Depends(get_settings)) -> dict:
    phases = build_registry(settings)
    return {"phases": [{"phase": item.number, "name": item.name, "role": item.role} for item in phases.values()], "flow": [3, 4, 5, 6, 9], "supporting_phases": [1, 2, 7, 8]}


@router.get("/overview")
async def overview(settings: Settings = Depends(get_settings)) -> dict:
    return await OverviewService(settings).build()
