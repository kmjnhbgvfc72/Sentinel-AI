from datetime import datetime
from typing import Any

import httpx

from app.config import Settings


class CVECollector:
    def __init__(self, settings: Settings):
        self.settings = settings

    async def collect(self, *, modified_after: datetime | None = None, limit: int = 20) -> list[dict[str, Any]]:
        if not self.settings.external_feeds_enabled:
            return []
        params: dict[str, str | int] = {"resultsPerPage": min(limit, 100)}
        if modified_after:
            params["lastModStartDate"] = modified_after.isoformat()
        headers = {"apiKey": self.settings.nvd_api_key} if self.settings.nvd_api_key else {}
        async with httpx.AsyncClient(timeout=self.settings.request_timeout_seconds) as client:
            response = await client.get(self.settings.nvd_api_url, params=params, headers=headers)
            response.raise_for_status()
            return response.json().get("vulnerabilities", [])
