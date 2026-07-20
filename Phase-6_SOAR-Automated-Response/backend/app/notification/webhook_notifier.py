class WebhookNotifier:
    def send(self, endpoint, payload):
        return {
            "channel": "webhook",
            "queued": True,
            "endpoint": endpoint,
            "payload": payload,
        }
