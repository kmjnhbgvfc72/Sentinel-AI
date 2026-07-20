import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

import joblib
from sklearn.ensemble import IsolationForest, RandomForestClassifier, RandomForestRegressor

from app.ai_engine.training.dataset_loader import load_dataset
from app.ai_engine.training.feature_engineering import FEATURE_COLUMNS


def train(dataset_path: Path, output_directory: Path, metadata_path: Path) -> dict:
    frame = load_dataset(dataset_path)
    missing = set(FEATURE_COLUMNS + ["threat_type", "risk_score"]).difference(frame.columns)
    if missing:
        raise ValueError(f"Missing training columns: {', '.join(sorted(missing))}")
    features = frame[FEATURE_COLUMNS].astype(float)
    anomaly = IsolationForest(n_estimators=100, contamination=0.2, random_state=42).fit(features)
    classifier = RandomForestClassifier(n_estimators=120, random_state=42, class_weight="balanced").fit(features, frame["threat_type"])
    risk = RandomForestRegressor(n_estimators=120, random_state=42).fit(features, frame["risk_score"].astype(float))
    output_directory.mkdir(parents=True, exist_ok=True)
    joblib.dump(anomaly, output_directory / "anomaly_model.pkl")
    joblib.dump(classifier, output_directory / "threat_classifier.pkl")
    joblib.dump(risk, output_directory / "risk_prediction_model.pkl")
    metadata = {"model_version": "4.0.0", "trained_at": datetime.now(UTC).isoformat(), "training_rows": len(frame), "feature_columns": FEATURE_COLUMNS, "algorithms": {"anomaly": "IsolationForest", "classifier": "RandomForestClassifier", "risk": "RandomForestRegressor"}, "random_state": 42}
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    return metadata


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train defensive Phase 4 models")
    parser.add_argument("--dataset", type=Path, default=Path("../ai_models/datasets/training_data.csv"))
    parser.add_argument("--output", type=Path, default=Path("../ai_models/trained_models"))
    parser.add_argument("--metadata", type=Path, default=Path("../ai_models/model_metadata.json"))
    arguments = parser.parse_args()
    train(arguments.dataset, arguments.output, arguments.metadata)
