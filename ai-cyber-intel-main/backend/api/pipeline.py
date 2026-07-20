from fastapi import APIRouter, Depends, Query

from backend.config import Settings, get_settings
from backend.services.pipeline_service import PipelineService

router = APIRouter(prefix="/pipeline", tags=["Cross-phase pipeline"])


@router.post("/synchronize")
async def synchronize(limit: int = Query(default=20, ge=1, le=100), settings: Settings = Depends(get_settings)) -> dict:
    return await PipelineService(settings).synchronize(limit)
