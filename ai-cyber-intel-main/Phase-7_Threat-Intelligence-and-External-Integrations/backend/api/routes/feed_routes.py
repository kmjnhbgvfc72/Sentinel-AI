from fastapi import APIRouter, Depends

from api.dependencies import get_repository, settings_dependency
from app.schemas import FeedResponse, FeedSyncRequest
from config.settings import Settings
from database.repository import ThreatIntelligenceRepository
from services.feed_service import FeedService

router = APIRouter(tags=["Threat Feeds"])


@router.get("/feeds", response_model=list[FeedResponse])
def list_feeds(repository: ThreatIntelligenceRepository = Depends(get_repository)):
    return FeedService(repository, settings_dependency()).list()


@router.post("/feeds/sync")
async def sync_feeds(payload: FeedSyncRequest | None = None, repository: ThreatIntelligenceRepository = Depends(get_repository), settings: Settings = Depends(settings_dependency)):
    return {"results": await FeedService(repository, settings).sync(payload.feed_ids if payload else None)}


@router.get("/feeds/status")
def feed_status(repository: ThreatIntelligenceRepository = Depends(get_repository)):
    rows = FeedService(repository, settings_dependency()).statuses()
    return [{"id": row.id, "feed_id": row.feed_id, "feed_name": row.feed.name, "status": row.status, "fetched_count": row.fetched_count, "accepted_count": row.accepted_count, "error_message": row.error_message, "latency_ms": row.latency_ms, "checked_at": row.checked_at} for row in rows]
