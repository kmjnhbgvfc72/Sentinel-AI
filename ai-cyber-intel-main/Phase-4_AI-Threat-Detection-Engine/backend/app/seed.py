from sqlalchemy import func, select

from app.schemas import SecurityEvent
from config.ai_settings import Settings
from database.ai_repository import AIPrediction, SessionLocal
from services.ai_service import AIService


def seed_demo_data(settings: Settings) -> None:
    with SessionLocal() as session:
        if session.scalar(select(func.count()).select_from(AIPrediction)):
            return
        service = AIService(session, settings)
        service.analyze(SecurityEvent(event_id="demo-auth-001", event_type="authentication", severity="critical", failed_login_count=12, ioc_reputation=91, vulnerability_score=8.8, activity_frequency=40, historical_average=4, unknown_ip=True, new_device=True, abnormal_time=True))
        service.analyze(SecurityEvent(event_id="demo-malware-002", event_type="malware indicator", severity="high", ioc_reputation=88, vulnerability_score=6.5, malware_indicator=True, activity_frequency=8, historical_average=5))
        service.analyze(SecurityEvent(event_id="demo-access-003", event_type="data access", severity="medium", data_access_volume=75_000_000, activity_frequency=18, historical_average=5, location_changed=True))
