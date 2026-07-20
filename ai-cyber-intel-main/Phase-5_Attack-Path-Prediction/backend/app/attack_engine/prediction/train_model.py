import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor


def train(dataset: Path, output: Path, metadata: Path) -> None:
    frame = pd.read_csv(dataset)
    required = {"path_length", "risk_score"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing columns: {', '.join(sorted(missing))}")
    model = RandomForestRegressor(n_estimators=100, random_state=42).fit(frame[["path_length", "risk_score"]], frame["risk_adjustment"])
    output.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output / "attack_prediction_model.pkl")
    metadata.write_text(json.dumps({"model_version": "5.0.0", "trained_at": datetime.now(UTC).isoformat(), "rows": len(frame), "features": ["path_length", "risk_score"], "algorithm": "RandomForestRegressor", "random_state": 42}, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, default=Path("../ai_models/datasets/attack_patterns.csv"))
    parser.add_argument("--output", type=Path, default=Path("../ai_models/trained_models"))
    parser.add_argument("--metadata", type=Path, default=Path("../ai_models/model_metadata.json"))
    args = parser.parse_args()
    train(args.dataset, args.output, args.metadata)
