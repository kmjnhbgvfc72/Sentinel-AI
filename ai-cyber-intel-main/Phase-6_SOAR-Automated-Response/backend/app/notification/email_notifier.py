class EmailNotifier:
    def send(self, recipient, subject, body):
        return {
            "channel": "email",
            "queued": True,
            "recipient": recipient,
            "subject": subject,
        }
