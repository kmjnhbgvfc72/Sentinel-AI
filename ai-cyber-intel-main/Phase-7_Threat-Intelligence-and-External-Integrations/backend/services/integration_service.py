import logging

import httpx

from config.settings import Settings

logger = logging.getLogger(__name__)


class IntegrationService:
    """Read-only adapters for prior defensive phases; failures degrade gracefully."""

    def __init__(self, settings: Settings):
        self.settings = settings

    async def fetch_events(self) -> list[tuple[str, dict]]:
        targets = [
            ("phase3", f"{self.settings.phase3_api_url}/logs"),
            ("phase4", f"{self.settings.phase4_api_url}/ai/predictions"),
            ("phase5", f"{self.settings.phase5_api_url}/attack/paths"),
            ("phase6", f"{self.settings.phase6_api_url}/incidents"),
        ]
        events: list[tuple[str, dict]] = []
        async with httpx.AsyncClient(timeout=self.settings.integration_timeout_seconds) as client:
            for phase, url in targets:
                try:
                    response = await client.get(url, headers={"Accept": "application/json"})
                    response.raise_for_status()
                    payload = response.json()
                    rows = payload if isinstance(payload, list) else payload.get("items", payload.get("data", []))
                    events.extend((phase, row) for row in rows if isinstance(row, dict))
                except (httpx.HTTPError, ValueError, TypeError) as exc:
                    logger.info("Optional %s integration unavailable: %s", phase, exc)
        return events
