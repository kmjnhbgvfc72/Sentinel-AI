from fastapi import APIRouter, Depends, Query, Response, status

from api.dependencies import get_repository
from app.schemas import IOCInput, IOCResponse
from database.repository import ThreatIntelligenceRepository
from services.ioc_service import IOCService

router = APIRouter(tags=["Indicators of Compromise"])


@router.get("/ioc", response_model=list[IOCResponse])
def list_iocs(ioc_type: str | None = Query(default=None, alias="type"), active: bool | None = None, limit: int = Query(default=200, ge=1, le=1000), repository: ThreatIntelligenceRepository = Depends(get_repository)):
    return IOCService(repository).list(ioc_type, active, limit)


@router.post("/ioc", response_model=IOCResponse, status_code=status.HTTP_201_CREATED)
def create_ioc(payload: IOCInput, response: Response, repository: ThreatIntelligenceRepository = Depends(get_repository)):
    item, created = IOCService(repository).create(payload)
    if not created:
        response.status_code = status.HTTP_200_OK
    return item


@router.delete("/ioc/{ioc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ioc(ioc_id: int, repository: ThreatIntelligenceRepository = Depends(get_repository)):
    IOCService(repository).delete(ioc_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
