from fastapi import Depends
from sqlalchemy.orm import Session

from config.settings import Settings, get_settings
from database.connection import get_db
from database.repository import ThreatIntelligenceRepository


def get_repository(session: Session = Depends(get_db)) -> ThreatIntelligenceRepository:
    return ThreatIntelligenceRepository(session)


def settings_dependency() -> Settings:
    return get_settings()
