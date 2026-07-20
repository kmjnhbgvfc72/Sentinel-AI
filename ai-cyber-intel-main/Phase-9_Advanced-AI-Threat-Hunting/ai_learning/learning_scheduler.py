"""Non-blocking retraining schedule metadata."""
from datetime import datetime, timedelta, timezone


class LearningScheduler:
    def __init__(self, interval_seconds: int = 86_400) -> None:
        if interval_seconds < 60:
            raise ValueError("interval must be at least 60 seconds")
        self.interval = timedelta(seconds=interval_seconds)
        self.last_run: datetime | None = None

    def due(self, now: datetime | None = None) -> bool:
        now = now or datetime.now(timezone.utc)
        return self.last_run is None or now >= self.last_run + self.interval

    def mark_completed(self, now: datetime | None = None) -> None:
        self.last_run = now or datetime.now(timezone.utc)

    def status(self) -> dict[str, str | bool | None]:
        return {"due": self.due(), "last_run": self.last_run.isoformat() if self.last_run else None, "next_run": (self.last_run + self.interval).isoformat() if self.last_run else None}
