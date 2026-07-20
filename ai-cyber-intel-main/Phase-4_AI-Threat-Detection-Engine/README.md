# Phase 4 — AI Threat Detection Engine

A defensive AI analytics service that consumes normalized Phase 3 events, extracts security features, detects anomalies, classifies threat patterns, predicts bounded risk, generates alerts, and supplies Phase 2 SOC dashboards.

## Environment

```bash
cd Phase-4_AI-Threat-Detection-Engine
cp .env.example .env
# Replace POSTGRES_PASSWORD before Docker deployment.
```

Local Uvicorn defaults to SQLite. Docker overrides the backend database URL with PostgreSQL values from `.env`. No API keys, passwords, or credentials are committed.

## Backend and training

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. python -m app.ai_engine.training.train_model \
  --dataset ../ai_models/datasets/training_data.csv \
  --output ../ai_models/trained_models \
  --metadata ../ai_models/model_metadata.json
uvicorn main:app --reload --port 8002
```

The service works before training through its explainable fallback, but trained artifacts are recommended. Only load trusted locally generated Joblib files.

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Phase 4 UI is `http://localhost:5175`, API is `http://localhost:8002`, and OpenAPI is `http://localhost:8002/docs`.

## Docker

```bash
docker compose up --build
```

Run Phase 3 on port 8001 and set `AUTO_ANALYZE_PHASE3=true` for a startup-time pull of its latest threats and sanitized logs. It remains disabled by default so Phase 4 can run independently. Phase 2 reads Phase 4 through `VITE_AI_API_BASE_URL=http://localhost:8002/api` and exposes `/ai-analysis`.

## Testing

```bash
cd backend && PYTHONPATH=. pytest -q && python -m ruff check .
cd ../frontend && npm test && npm run lint && npm run build
```

Example analysis:

```bash
curl -X POST http://localhost:8002/api/ai/analyze \
  -H 'Content-Type: application/json' \
  -d '{"event_id":"manual-001","event_type":"authentication","severity":"high","failed_login_count":10,"ioc_reputation":90,"unknown_ip":true}'
```

## Phase 5 plan

Phase 5 can add analyst feedback, model registry/promotion, drift monitoring, scheduled retraining, richer explainability, RBAC, signed artifacts, audit workflows, and coordinated incident response. Automated actions should remain human-approved and defensive.
