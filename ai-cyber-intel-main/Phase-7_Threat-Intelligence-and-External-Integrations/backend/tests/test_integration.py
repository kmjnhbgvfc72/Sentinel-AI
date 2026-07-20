from unittest.mock import AsyncMock

import pytest

from app.schemas import IOCInput
from config.settings import get_settings
from database.connection import SessionLocal
from database.repository import ThreatIntelligenceRepository
from services.correlation_service import CorrelationService
from services.ioc_service import IOCService


@pytest.mark.asyncio
async def test_cross_phase_exact_correlation():
    with SessionLocal() as session:
        repository = ThreatIntelligenceRepository(session)
        IOCService(repository).create(IOCInput(type="ip", value="198.51.100.8", confidence=90, severity="critical", source="test"))
        integrations = AsyncMock()
        integrations.fetch_events.return_value = [("phase4", {"id": "prediction-1", "source_ip": "198.51.100.8", "risk_score": 90})]
        rows = await CorrelationService(repository, integrations).correlate(refresh=True)
        assert len(rows) == 1
        assert rows[0].source_phase == "phase4"
        assert rows[0].score >= 80
