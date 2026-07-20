from collections import Counter, deque
from datetime import UTC, datetime, timedelta


class NetworkMonitor:
    def __init__(self, threshold: int = 100, window_seconds: int = 60):
        self.threshold, self.window = threshold, timedelta(seconds=window_seconds)
        self.events = deque()

    def observe(self, source_ip: str, destination: str, bytes_sent: int) -> dict | None:
        now = datetime.now(UTC); self.events.append((now, source_ip, destination, bytes_sent))
        while self.events and now - self.events[0][0] > self.window: self.events.popleft()
        count = Counter(event[1] for event in self.events)[source_ip]
        return {"category": "traffic-burst", "source_ip": source_ip, "event_count": count, "destination": destination} if count >= self.threshold else None

