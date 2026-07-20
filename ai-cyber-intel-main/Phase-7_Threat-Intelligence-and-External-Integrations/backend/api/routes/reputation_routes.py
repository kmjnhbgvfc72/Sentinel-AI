from fastapi import APIRouter, Depends, Path

from api.dependencies import get_repository, settings_dependency
from app.schemas import ReputationResponse
from config.settings import Settings
from database.repository import ThreatIntelligenceRepository
from services.reputation_service import ReputationService

router = APIRouter(prefix="/reputation", tags=["Reputation"])


async def lookup(kind: str, value: str, repository: ThreatIntelligenceRepository, settings: Settings):
    return await ReputationService(repository, settings).lookup(kind, value)


@router.get("/ip/{ip}", response_model=ReputationResponse)
async def reputation_ip(ip: str, repository: ThreatIntelligenceRepository = Depends(get_repository), settings: Settings = Depends(settings_dependency)):
    return await lookup("ip", ip, repository, settings)


@router.get("/domain/{domain}", response_model=ReputationResponse)
async def reputation_domain(domain: str, repository: ThreatIntelligenceRepository = Depends(get_repository), settings: Settings = Depends(settings_dependency)):
    return await lookup("domain", domain, repository, settings)


@router.get("/url/{url:path}", response_model=ReputationResponse)
async def reputation_url(url: str = Path(), repository: ThreatIntelligenceRepository = Depends(get_repository), settings: Settings = Depends(settings_dependency)):
    return await lookup("url", url, repository, settings)
