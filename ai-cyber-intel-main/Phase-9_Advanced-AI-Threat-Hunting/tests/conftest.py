"""Shared Phase 9 test fixtures."""
import sys
import asyncio
from pathlib import Path
import pytest
import httpx

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from config.settings import Settings  # noqa: E402
from run_phase9 import create_app  # noqa: E402


class ASGITestClient:
    """Small synchronous wrapper that avoids environment-specific portal threads."""

    def __init__(self) -> None:
        self.app = create_app(Settings(api_key=None))

    def request(self, method: str, path: str, **kwargs):
        async def send():
            transport = httpx.ASGITransport(app=self.app)
            async with httpx.AsyncClient(transport=transport, base_url="http://test") as session:
                return await session.request(method, path, **kwargs)
        return asyncio.run(send())

    def get(self, path: str, **kwargs):
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs):
        return self.request("POST", path, **kwargs)


@pytest.fixture
def client() -> ASGITestClient:
    return ASGITestClient()
