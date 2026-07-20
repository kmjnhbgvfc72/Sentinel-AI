import os

os.environ["DATABASE_URL"] = "sqlite:///./test_threat_intelligence.db"
os.environ["DEMO_DATA_ENABLED"] = "true"

import pytest
from httpx import ASGITransport, AsyncClient

from app.config import get_settings

get_settings.cache_clear()
from app.database import Base, SessionLocal, engine  # noqa: E402
from app.seed import seed_demo_data  # noqa: E402
from main import app  # noqa: E402


@pytest.fixture(autouse=True)
def database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        seed_demo_data(session)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as test_client:
        yield test_client
