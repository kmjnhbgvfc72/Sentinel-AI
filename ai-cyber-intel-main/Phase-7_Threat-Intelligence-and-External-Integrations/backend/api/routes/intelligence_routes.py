from fastapi import APIRouter, Depends

from api.dependencies import get_repository, settings_dependency
from config.settings import Settings
from database.repository import ThreatIntelligenceRepository
from services.correlation_service import CorrelationService
from services.integration_service import IntegrationService

router = APIRouter(tags=["Correlation and Intelligence"])


def service(repository: ThreatIntelligenceRepository, settings: Settings) -> CorrelationService:
    return CorrelationService(repository, IntegrationService(settings))


@router.get("/correlation")
async def correlations(refresh: bool = False, repository: ThreatIntelligenceRepository = Depends(get_repository), settings: Settings = Depends(settings_dependency)):
    rows = await service(repository, settings).correlate(refresh=refresh)
    return [{"id": row.id, "ioc_id": row.ioc_id, "external_event_id": row.external_event_id, "source_phase": row.source_phase, "match_type": row.match_type, "score": row.score, "context": row.context, "created_at": row.created_at} for row in rows]


@router.get("/intelligence/summary")
def summary(repository: ThreatIntelligenceRepository = Depends(get_repository), settings: Settings = Depends(settings_dependency)):
    return service(repository, settings).summary()
