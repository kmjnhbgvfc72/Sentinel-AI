import ipaddress
import logging
import socket
import time
from urllib.parse import urlsplit

import httpx

from app.errors import ServiceError
from app.schemas import IOCInput
from config.settings import Settings
from database.repository import ThreatIntelligenceRepository
from services.ioc_service import IOCService
from threat_intelligence.feed_parser import FeedParseError, FeedParser

logger = logging.getLogger(__name__)


class FeedService:
    def __init__(self, repository: ThreatIntelligenceRepository, settings: Settings):
        self.repository = repository
        self.settings = settings

    def list(self):
        return self.repository.list_feeds()

    def statuses(self):
        return self.repository.latest_statuses()

    def _validate_target(self, url: str) -> None:
        parts = urlsplit(url)
        if parts.scheme != "https" or not parts.hostname or parts.username or parts.password:
            raise ServiceError("Feed URL must use HTTPS without embedded credentials", code="unsafe_feed_url", status_code=422)
        try:
            addresses = {item[4][0] for item in socket.getaddrinfo(parts.hostname, parts.port or 443, type=socket.SOCK_STREAM)}
        except socket.gaierror as exc:
            raise ServiceError("Feed hostname could not be resolved", code="feed_resolution_failed", status_code=502) from exc
        if not self.settings.allow_private_feed_hosts:
            for address in addresses:
                ip = ipaddress.ip_address(address)
                if not ip.is_global:
                    raise ServiceError("Feed target resolves to a non-public address", code="unsafe_feed_url", status_code=422)

    async def sync(self, feed_ids: list[int] | None = None) -> list[dict]:
        feeds = self.repository.enabled_feeds()
        if feed_ids is not None:
            requested = set(feed_ids)
            feeds = [feed for feed in feeds if feed.id in requested]
            missing = requested - {feed.id for feed in feeds}
            if missing:
                raise ServiceError(f"Unknown or disabled feed IDs: {sorted(missing)}", code="invalid_feed_ids", status_code=422)
        results = []
        async with httpx.AsyncClient(timeout=self.settings.feed_request_timeout_seconds, follow_redirects=False) as client:
            for feed in feeds:
                results.append(await self._sync_one(feed, client))
        return results

    async def _sync_one(self, feed, client: httpx.AsyncClient) -> dict:
        started = time.monotonic()
        fetched = accepted = 0
        try:
            self._validate_target(feed.url)
            response = await client.get(feed.url, headers={"Accept": "application/json,text/csv,text/plain", "User-Agent": "AI-CTI-Defensive-Feed-Client/7.0"})
            response.raise_for_status()
            if len(response.content) > self.settings.feed_max_bytes:
                raise ServiceError("Feed response exceeds configured size limit", code="feed_too_large", status_code=502)
            rows = FeedParser.parse(response.text, feed.format)
            fetched = len(rows)
            ioc_service = IOCService(self.repository)
            for row in rows:
                try:
                    payload = IOCInput(
                        type=str(row.get("type", "domain")).lower(), value=str(row.get("value", "")),
                        threat_type=str(row.get("threat_type", "feed-indicator"))[:100],
                        confidence=max(0, min(100, int(row.get("confidence", 50)))),
                        severity=str(row.get("severity", "medium")).lower(), source=feed.name,
                        tags=row.get("tags", ["external-feed"]) if isinstance(row.get("tags", ["external-feed"]), list) else ["external-feed"],
                    )
                    ioc_service.create(payload)
                    accepted += 1
                except (ValueError, ServiceError):
                    continue
            status = "healthy"
            error = None
        except (httpx.HTTPError, FeedParseError, ServiceError) as exc:
            logger.warning("Feed sync failed for %s: %s", feed.name, exc)
            status, error = "error", str(exc)[:500]
        latency = round((time.monotonic() - started) * 1000)
        self.repository.add_status(feed_id=feed.id, status=status, fetched_count=fetched, accepted_count=accepted, error_message=error, latency_ms=latency)
        self.repository.add_history(action="feed_sync", entity_type="feed", entity_id=str(feed.id), details={"status": status, "fetched": fetched, "accepted": accepted})
        self.repository.session.commit()
        return {"feed_id": feed.id, "name": feed.name, "status": status, "fetched_count": fetched, "accepted_count": accepted, "latency_ms": latency, "error": error}
