import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config.settings import Settings
from database.connection import SessionLocal
from database.repository import ThreatIntelligenceRepository
from services.feed_service import FeedService

logger = logging.getLogger(__name__)


class FeedScheduler:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.scheduler = AsyncIOScheduler(timezone="UTC")

    async def run_sync(self) -> None:
        with SessionLocal() as session:
            await FeedService(ThreatIntelligenceRepository(session), self.settings).sync()

    def start(self) -> None:
        if not self.settings.feed_scheduler_enabled:
            return
        self.scheduler.add_job(self.run_sync, "interval", minutes=self.settings.feed_sync_interval_minutes, id="feed-sync", max_instances=1, coalesce=True)
        self.scheduler.start()
        logger.info("Feed scheduler started")

    def shutdown(self) -> None:
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)
