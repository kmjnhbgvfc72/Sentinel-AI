# AI API Documentation

## `POST /api/ai/analyze`

Accepts one validated security event and returns anomaly status/score, threat type, confidence, risk score, severity, behavior flags, alert status, and model version. Counts and scores are bounded. Credential-like metadata fields are rejected.

## `GET /api/ai/predictions`

Returns latest stored predictions. Optional `limit` is 1–200.

## `GET /api/ai/risk-score`

Returns latest bounded risk scores and severities. Optional `limit` is 1–200.

## `GET /api/ai/alerts`

Returns AI-generated security alerts, priorities, status, event association, and timestamps. Optional `limit` is 1–200.

## `GET /health`

Returns service health, version, and UTC timestamp. Interactive OpenAPI documentation is available at `/docs`.
