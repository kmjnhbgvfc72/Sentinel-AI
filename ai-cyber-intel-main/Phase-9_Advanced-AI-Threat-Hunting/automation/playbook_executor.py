"""Deterministic defensive playbook execution."""
from .response_manager import ResponseManager


class PlaybookExecutor:
    def __init__(self, responses: ResponseManager | None = None) -> None:
        self.responses = responses or ResponseManager()

    def execute(self, playbook: dict[str, object], context: dict[str, object], approved: bool = False) -> dict[str, object]:
        results = []
        for step in playbook.get("steps", []):
            target = str(context.get(str(step.get("target_field", "target")), "unknown"))
            result = self.responses.execute(str(step["action"]), target, approved)
            results.append(result)
            if result["status"] == "approval_required":
                break
        return {"playbook": playbook.get("name", "unnamed"), "status": "completed" if all(i["status"] == "completed" for i in results) else "paused", "steps": results}
