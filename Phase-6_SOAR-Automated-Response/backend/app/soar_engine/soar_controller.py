class SoarController:
    def __init__(self, incident_service, workflow_manager):
        self.incidents, self.workflows = incident_service, workflow_manager
