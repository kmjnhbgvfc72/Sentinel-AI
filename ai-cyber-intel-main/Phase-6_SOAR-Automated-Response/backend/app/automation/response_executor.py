class ResponseExecutor:
    def execute(self, action: str):
        return {"action": action, "status": "recommended", "safe": True}
