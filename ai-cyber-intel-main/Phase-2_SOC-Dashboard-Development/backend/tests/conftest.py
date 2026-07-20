import pytest
from httpx import ASGITransport, AsyncClient

from data import reset_alerts
from main import app


@pytest.fixture(autouse=True)
def reset_state():
    reset_alerts()
    yield


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app, raise_app_exceptions=False), base_url="http://test") as test_client:
        yield test_client
