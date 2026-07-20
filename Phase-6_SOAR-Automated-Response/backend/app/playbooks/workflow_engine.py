from models import Playbook, Workflow
import json

DEFAULT_PLAYBOOKS = [
    {
        "name": "Suspicious Login Response",
        "trigger": "Suspicious Login",
        "steps": [
            "Validate alert",
            "Review account activity",
            "Notify SOC analyst",
            "Document outcome",
        ],
    },
    {
        "name": "Critical Vulnerability Triage",
        "trigger": "Critical Vulnerability",
        "steps": [
            "Confirm affected asset",
            "Assign remediation",
            "Monitor exposure",
            "Close with evidence",
        ],
    },
]


def ensure_playbooks(session):
    if session.query(Playbook).count() == 0:
        for item in DEFAULT_PLAYBOOKS:
            session.add(
                Playbook(
                    name=item["name"],
                    trigger=item["trigger"],
                    steps=json.dumps(item["steps"]),
                )
            )
        session.commit()


def execute(session, incident_id, playbook):
    steps = json.loads(playbook.steps)
    workflow = Workflow(
        incident_id=incident_id,
        playbook=playbook.name,
        status="completed",
        steps_completed=len(steps),
    )
    session.add(workflow)
    session.commit()
    session.refresh(workflow)
    return workflow
