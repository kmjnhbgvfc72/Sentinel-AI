"""Notification adapter with channel allow-listing."""


class NotificationService:
    def __init__(self) -> None:
        self.outbox: list[dict[str, str]] = []

    def send(self, channel: str, recipient: str, message: str) -> dict[str, str]:
        if channel not in {"email", "slack", "webhook"}:
            raise ValueError("unsupported notification channel")
        notification = {"channel": channel, "recipient": recipient, "message": message, "status": "queued"}
        self.outbox.append(notification)
        return notification
