from database.attack_repository import AttackRepository


class RiskService:
    def __init__(self, repository: AttackRepository):
        self.repository = repository

    def assets(self, limit: int = 100):
        return self.repository.assets(limit)
