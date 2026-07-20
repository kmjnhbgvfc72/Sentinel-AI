from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import NotificationRequest
from app.notification.notification_service import NotificationService
from models import Notification
from database.soar_repository import get_db

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("")
def notifications(db: Session = Depends(get_db)):
    return [
        {
            "id": n.id,
            "channel": n.channel,
            "recipient": n.recipient,
            "subject": n.subject,
            "status": n.status,
        }
        for n in db.query(Notification).order_by(Notification.id.desc()).all()
    ]


@router.post("", status_code=201)
def queue_notification(data: NotificationRequest, db: Session = Depends(get_db)):
    return NotificationService(db).queue(data)
