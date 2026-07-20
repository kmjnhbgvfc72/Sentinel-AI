from database.attack_repository import AttackRepository


class ResponseService:
    def __init__(self, repository: AttackRepository):
        self.repository = repository

    def recommendations(self, limit: int = 100):
        return self.repository.recommendations(limit)
