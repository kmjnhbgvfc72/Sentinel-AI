from typing import Any

import httpx

from backend.config import Settings
from backend.integrations.registry import PhaseDefinition


class PhaseUnavailable(RuntimeError):
    pass


class PhaseClient:
    def __init__(self, phase: PhaseDefinition, settings: Settings):
        self.phase = phase
        self.settings = settings

    def _service_headers(self) -> dict[str, str]:
        headers = {"Accept": "application/json", "X-Central-Phase": str(self.phase.number)}
        if self.phase.number == 6 and self.settings.phase6_token:
            headers["Authorization"] = f"Bearer {self.settings.phase6_token}"
        if self.phase.number == 9 and self.settings.phase9_api_key:
            headers["X-API-Key"] = self.settings.phase9_api_key
        return headers

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: Any = None,
        content: bytes | None = None,
        content_type: str | None = None,
    ) -> httpx.Response:
        headers = self._service_headers()
        if content_type:
            headers["Content-Type"] = content_type
        try:
            async with httpx.AsyncClient(base_url=self.phase.base_url, timeout=self.settings.request_timeout_seconds) as client:
                return await client.request(method, path, params=params, content=content, headers=headers)
        except httpx.HTTPError as exc:
            raise PhaseUnavailable(f"Phase {self.phase.number} is unavailable") from exc

    async def json(self, method: str, path: str, **kwargs: Any) -> Any:
        response = await self.request(method, path, **kwargs)
        response.raise_for_status()
        return response.json()

    async def health(self) -> dict[str, Any]:
        try:
            response = await self.request("GET", self.phase.health_path)
            payload = response.json() if response.headers.get("content-type", "").startswith("application/json") else {}
            return {"phase": self.phase.number, "name": self.phase.name, "role": self.phase.role, "status": "healthy" if response.is_success else "degraded", "status_code": response.status_code, "details": payload}
        except (PhaseUnavailable, ValueError):
            return {"phase": self.phase.number, "name": self.phase.name, "role": self.phase.role, "status": "unavailable", "status_code": None, "details": {}}
