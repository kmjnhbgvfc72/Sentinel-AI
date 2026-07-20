"""Automation safety and lifecycle tests."""
import pytest
from automation.incident_manager import IncidentManager
from automation.playbook_executor import PlaybookExecutor


def test_dangerous_action_requires_approval() -> None:
    result = PlaybookExecutor().execute({"name": "contain", "steps": [{"action": "isolate_host", "target_field": "host"}]}, {"host": "host-1"})
    assert result["status"] == "paused"
    assert result["steps"][0]["status"] == "approval_required"


def test_incident_transition_is_enforced() -> None:
    manager = IncidentManager()
    incident = manager.create("Defensive test", "high")
    manager.transition(str(incident["id"]), "investigating")
    with pytest.raises(ValueError):
        manager.transition(str(incident["id"]), "resolved")
