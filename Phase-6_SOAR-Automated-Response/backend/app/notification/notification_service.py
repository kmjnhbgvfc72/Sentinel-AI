from models import Notification


class NotificationService:
    def __init__(self, session):
        self.session = session

    def queue(self, request):
        item = Notification(
            channel=request.channel,
            recipient=request.recipient,
            subject=request.subject,
        )
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item
