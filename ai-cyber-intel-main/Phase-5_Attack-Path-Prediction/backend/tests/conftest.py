import os

os.environ["DATABASE_URL"] = "sqlite:///./test_attack_prediction.db"
os.environ["MODEL_DIRECTORY"] = "./tests/missing-models"
os.environ["MODEL_METADATA_PATH"] = "./tests/missing-metadata.json"
os.environ["DEMO_DATA_ENABLED"] = "false"

import pytest
from httpx import ASGITransport, AsyncClient

from config.attack_settings import get_settings

get_settings.cache_clear()
from database.attack_repository import Base, engine  # noqa: E402
from models import Asset, AttackGraphEdge, AttackPath, Recommendation, RiskScore  # noqa: F401,E402
from main import app  # noqa: E402


@pytest.fixture(autouse=True)
def database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as test_client:
        yield test_client
