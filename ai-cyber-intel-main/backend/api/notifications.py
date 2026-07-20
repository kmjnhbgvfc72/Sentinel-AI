from datetime import datetime
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from backend.api.auth import current_user
from backend.database import get_db
from backend.models import Notification, User
from backend.services.notification_service import NotificationService

router = APIRouter(prefix="/notifications", tags=["Notifications"])


class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; title: str; message: str; notification_type: str; severity: Literal["low", "medium", "high", "critical"]
    is_read: bool; related_user: str | None; ip_address: str | None; created_at: datetime


class NotificationListResponse(BaseModel):
    data: list[NotificationResponse]; unread_count: int


@router.get("", response_model=NotificationListResponse)
def list_notifications(limit: int = Query(default=30, ge=1, le=100), _: User = Depends(current_user), db: Session = Depends(get_db)) -> NotificationListResponse:
    rows, unread = NotificationService(db).latest(limit)
    return NotificationListResponse(data=rows, unread_count=unread)


@router.put("/{notification_id}/read", response_model=NotificationResponse)
def mark_read(notification_id: int, _: User = Depends(current_user), db: Session = Depends(get_db)) -> Notification:
    item = NotificationService(db).mark_read(notification_id)
    if not item: raise HTTPException(status_code=404, detail="Notification not found")
    return item
