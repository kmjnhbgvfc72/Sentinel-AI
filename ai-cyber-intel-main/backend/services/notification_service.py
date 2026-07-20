from sqlalchemy import func, select, update
from sqlalchemy.orm import Session

from backend.models import Notification


class NotificationService:
    """Central in-app notification store for security-relevant events."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, *, title: str, message: str, notification_type: str, severity: str = "medium", related_user: str | None = None, ip_address: str | None = None) -> Notification:
        item = Notification(title=title, message=message, notification_type=notification_type, severity=severity, related_user=related_user, ip_address=ip_address)
        self.db.add(item); self.db.commit(); self.db.refresh(item)
        return item

    def create_for_log(self, *, event_type: str, severity: str, username: str, source_ip: str, description: str) -> Notification | None:
        normalized = event_type.lower()
        if "brute" in normalized:
            return self.create(title="BRUTE FORCE ATTACK DETECTED", message=description or f"Repeated authentication failures detected from {source_ip}.", notification_type="brute_force", severity="high", related_user=username, ip_address=source_ip)
        if severity == "critical":
            return self.create(title="Critical Security Threat Detected", message=description or f"Critical {event_type} event detected.", notification_type="critical_threat", severity="critical", related_user=username, ip_address=source_ip)
        if "login" in normalized and ("fail" in normalized or "suspicious" in normalized):
            return self.create(title="Failed Login Attempt", message=description or f"Authentication was rejected for {username}.", notification_type="failed_login", severity="medium", related_user=username, ip_address=source_ip)
        return None

    def latest(self, limit: int = 30) -> tuple[list[Notification], int]:
        rows = self.db.scalars(select(Notification).order_by(Notification.created_at.desc()).limit(limit)).all()
        unread = self.db.scalar(select(func.count()).select_from(Notification).where(Notification.is_read.is_(False))) or 0
        return list(rows), unread

    def mark_read(self, notification_id: int) -> Notification | None:
        item = self.db.get(Notification, notification_id)
        if not item: return None
        item.is_read = True; self.db.commit(); self.db.refresh(item)
        return item

    def mark_all_read(self) -> None:
        self.db.execute(update(Notification).where(Notification.is_read.is_(False)).values(is_read=True)); self.db.commit()
