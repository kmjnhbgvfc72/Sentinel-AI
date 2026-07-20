"""Approval-aware response action manager."""


class ResponseManager:
    SAFE_ACTIONS = {"enrich_ioc", "collect_telemetry", "create_ticket", "notify"}

    def execute(self, action: str, target: str, approved: bool = False) -> dict[str, object]:
        requires_approval = action not in self.SAFE_ACTIONS
        if requires_approval and not approved:
            return {"action": action, "target": target, "status": "approval_required"}
        return {"action": action, "target": target, "status": "completed", "simulated": True}
