# Model Training

The training pipeline loads a local CSV, verifies all required features and targets, trains three reproducible scikit-learn estimators, and saves them under `ai_models/trained_models/`. It also writes model version, timestamp, row count, feature order, algorithms, and random state to `model_metadata.json`.

Run from `backend` after installing requirements:

```bash
PYTHONPATH=. python -m app.ai_engine.training.train_model \
  --dataset ../ai_models/datasets/training_data.csv \
  --output ../ai_models/trained_models \
  --metadata ../ai_models/model_metadata.json
```

The included dataset is synthetic and suitable for software verification, not production accuracy claims. Production promotion requires representative authorized data, train/validation/test separation, class-balance review, precision/recall and false-positive analysis, bias checks, signed artifact provenance, approval, monitoring, and rollback.
