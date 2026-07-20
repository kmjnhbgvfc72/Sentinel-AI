class TicketConnector:
    def create_ticket(self, title: str, description: str):
        return {"queued": True, "title": title, "description": description}
