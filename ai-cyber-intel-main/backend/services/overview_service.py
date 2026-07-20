import asyncio
from typing import Any

from backend.config import Settings
from backend.integrations.phase_client import PhaseClient
from backend.integrations.registry import build_registry


class OverviewService:
    """Builds one fault-tolerant SOC view without coupling phase domain code."""

    def __init__(self, settings: Settings):
        registry = build_registry(settings)
        self.clients = {number: PhaseClient(phase, settings) for number, phase in registry.items()}

    async def _optional(self, phase: int, path: str) -> Any:
        try:
            return await self.clients[phase].json("GET", path)
        except Exception:
            return None

    async def build(self) -> dict[str, Any]:
        dashboard, intelligence, detections, paths, incidents, external, hunting = await asyncio.gather(
            self._optional(2, "/api/dashboard/summary"),
            self._optional(3, "/api/threat-statistics"),
            self._optional(4, "/api/ai/alerts?limit=10"),
            self._optional(5, "/api/attack/paths?limit=10"),
            self._optional(6, "/api/incidents"),
            self._optional(7, "/api/intelligence/summary"),
            self._optional(9, "/api/v1/analytics/dashboard"),
        )
        return {
            "dashboard": dashboard,
            "threat_intelligence": intelligence,
            "ai_detection": detections,
            "attack_paths": paths,
            "incidents": incidents,
            "external_intelligence": external,
            "advanced_hunting": hunting,
        }
