class SIEMConnector:
    def ingest(self, event: dict):
        return {"accepted": True, "event": event}
