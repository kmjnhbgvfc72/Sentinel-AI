import asyncio

from backend.config import Settings
from backend.integrations.phase_client import PhaseClient
from backend.integrations.registry import build_registry


class HealthService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.registry = build_registry(settings)

    async def all_phases(self) -> list[dict]:
        return await asyncio.gather(*(PhaseClient(phase, self.settings).health() for phase in self.registry.values()))
