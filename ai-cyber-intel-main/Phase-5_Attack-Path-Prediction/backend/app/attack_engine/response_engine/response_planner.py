from .recommendation_engine import RecommendationEngine


class ResponsePlanner:
    def __init__(self):
        self.engine = RecommendationEngine()

    def plan(self, event: dict, assets: list[dict]) -> list[dict]:
        return self.engine.generate(event, assets)
