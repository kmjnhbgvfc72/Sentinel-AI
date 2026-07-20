# Phase 5 — Attack Path Prediction

Defensive graph analysis for mapping Phase 4 detections to possible relationships, paths, asset risk, vulnerability impact, and SOC recommendations.

## Setup

```bash
cd Phase-5_Attack-Path-Prediction
cp .env.example .env
# Replace POSTGRES_PASSWORD before Docker deployment.
```

Local backend uses SQLite; Docker overrides the database URL with PostgreSQL. No secrets are committed.

## Backend and model training

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. python -m app.attack_engine.prediction.train_model \
  --dataset ../ai_models/datasets/attack_patterns.csv \
  --output ../ai_models/trained_models \
  --metadata ../ai_models/model_metadata.json
uvicorn main:app --reload --port 8003
```

Set `AUTO_ANALYZE_PHASE4=true` to pull current Phase 4 predictions/risk scores during startup. It is disabled by default.

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Phase 5 UI: `http://localhost:5176`; API: `http://localhost:8003`; docs: `http://localhost:8003/docs`.

## Docker

```bash
docker compose up --build
```

## Testing

```bash
cd backend && PYTHONPATH=. pytest -q && python -m ruff check .
cd ../frontend && npm test && npm run lint && npm run build
```

## Phase 6 plan

Phase 6 can add analyst feedback loops, temporal graph learning, asset inventory synchronization, signed model promotion, drift monitoring, RBAC, and human-approved orchestration integrations.
