"""Incident workflow orchestration."""
from .incident_manager import IncidentManager
from .playbook_executor import PlaybookExecutor


class WorkflowEngine:
    def __init__(self, incidents: IncidentManager | None = None, executor: PlaybookExecutor | None = None) -> None:
        self.incidents, self.executor = incidents or IncidentManager(), executor or PlaybookExecutor()

    def start(self, alert: dict[str, object], playbook: dict[str, object]) -> dict[str, object]:
        incident = self.incidents.create(str(alert.get("title", "Security alert")), str(alert.get("severity", "medium")))
        execution = self.executor.execute(playbook, alert)
        return {"incident": incident, "execution": execution}
