from pathlib import Path

import joblib


class PathPredictionModel:
    def __init__(self, path: Path | None = None):
        self.model = joblib.load(path) if path and path.is_file() else None

    def adjustment(self, features: list[float]) -> float:
        if self.model:
            return float(self.model.predict([features])[0])
        return 0.0
