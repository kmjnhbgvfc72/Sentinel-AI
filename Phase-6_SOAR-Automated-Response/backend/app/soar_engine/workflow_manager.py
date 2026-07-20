from app.playbooks.workflow_engine import execute


class WorkflowManager:
    def __init__(self, session):
        self.session = session

    def run(self, incident_id, playbook):
        return execute(self.session, incident_id, playbook)
