# AI Architecture

Phase 4 is an independent defensive analysis service. Validated Phase 3 events flow through credential-safe preprocessing, stable feature engineering, anomaly detection, threat classification, behavior analysis, risk prediction, persistence, and alert generation. FastAPI provides the boundary, SQLAlchemy supports SQLite/PostgreSQL, and Phase 2 consumes read-only result APIs.

The trained models are Isolation Forest for anomalies, Random Forest Classifier for threat type, and Random Forest Regressor for risk. Each uses a fixed random state and recorded feature order. If artifacts are missing, deterministic explainable rules keep the service operational and explicitly report the fallback model version.

Joblib artifacts are loaded only from the operator-controlled model directory. Never load untrusted pickle or Joblib files because model serialization can execute code during deserialization.
