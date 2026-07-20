import logging
from pathlib import Path
from threading import RLock
import joblib

logger = logging.getLogger(__name__)


class ModelLoader:
    def __init__(self, path: str):
        self.path = Path(path)
        self._model = None
        self._mtime = None
        self._lock = RLock()

    def load(self):
        with self._lock:
            if not self.path.exists():
                logger.warning("Model not found at %s; deterministic risk engine active", self.path)
                return None
            mtime = self.path.stat().st_mtime
            if self._model is None or mtime != self._mtime:
                candidate = joblib.load(self.path)
                if not hasattr(candidate, "predict_proba") and not hasattr(candidate, "predict"):
                    raise TypeError("Model must implement predict or predict_proba")
                self._model, self._mtime = candidate, mtime
                logger.info("Loaded model from %s", self.path)
            return self._model

    @property
    def loaded(self) -> bool:
        return self._model is not None

