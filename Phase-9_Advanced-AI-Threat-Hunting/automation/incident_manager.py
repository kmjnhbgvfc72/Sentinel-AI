"""Thread-safe incident lifecycle management."""
from datetime import datetime, timezone
from threading import RLock
from uuid import uuid4


class IncidentManager:
    TRANSITIONS = {"open": {"investigating", "closed"}, "investigating": {"contained", "closed"}, "contained": {"resolved", "investigating"}, "resolved": {"closed"}, "closed": set()}

    def __init__(self) -> None:
        self._items: dict[str, dict[str, object]] = {}
        self._lock = RLock()

    def create(self, title: str, severity: str = "medium") -> dict[str, object]:
        if severity not in {"low", "medium", "high", "critical"}:
            raise ValueError("unsupported severity")
        incident = {"id": str(uuid4()), "title": title, "severity": severity, "status": "open", "created_at": datetime.now(timezone.utc).isoformat(), "history": []}
        with self._lock:
            self._items[str(incident["id"])] = incident
        return dict(incident)

    def transition(self, incident_id: str, status: str) -> dict[str, object]:
        with self._lock:
            incident = self._items.get(incident_id)
            if not incident:
                raise KeyError("incident not found")
            if status not in self.TRANSITIONS[str(incident["status"])]:
                raise ValueError("invalid incident transition")
            incident["history"].append({"from": incident["status"], "to": status, "at": datetime.now(timezone.utc).isoformat()})
            incident["status"] = status
            return dict(incident)

    def list(self) -> list[dict[str, object]]:
        return [dict(item) for item in self._items.values()]
