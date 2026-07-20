from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.schemas import IOCInput
from database.repository import ThreatIntelligenceRepository
from models.entities import FeedStatus, ThreatFeed
from services.ioc_service import IOCService


def seed_demo_data(session: Session) -> None:
    repository = ThreatIntelligenceRepository(session)
    if not session.scalar(select(ThreatFeed.id).limit(1)):
        feeds = [
            ThreatFeed(name="Defensive Community Feed", url="https://feeds.example.org/iocs.json", format="json", reliability=75, enabled=False),
            ThreatFeed(name="Internal SOC Curated", url="https://intel.example.org/curated.csv", format="csv", reliability=90, enabled=False),
        ]
        session.add_all(feeds)
        session.flush()
        session.add_all([FeedStatus(feed_id=feed.id, status="disabled", fetched_count=0, accepted_count=0, checked_at=datetime.now(UTC)) for feed in feeds])
        session.commit()
    if not repository.list_iocs(limit=1):
        examples = [
            IOCInput(type="ip", value="198.51.100.42", threat_type="simulated-command-and-control", confidence=88, severity="critical", source="SOC Training", tags=["documentation-range", "defensive-test"]),
            IOCInput(type="domain", value="suspicious.example", threat_type="simulated-phishing", confidence=72, severity="high", source="SOC Training", tags=["reserved-domain", "defensive-test"]),
            IOCInput(type="url", value="https://malicious.example/payload", threat_type="simulated-malicious-url", confidence=65, severity="high", source="SOC Training", tags=["reserved-domain", "defensive-test"]),
        ]
        for payload in examples:
            IOCService(repository).create(payload)
