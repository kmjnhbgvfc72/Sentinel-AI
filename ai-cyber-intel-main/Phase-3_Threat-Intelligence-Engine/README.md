# Phase 3 — Threat Intelligence Engine

A defensive Threat Intelligence Platform module that collects and normalizes approved intelligence, stores vulnerabilities and IOCs, safely analyzes security logs, correlates evidence into explainable risk, and supplies SOC and future AI pipelines.

## Environment

```bash
cd Phase-3_Threat-Intelligence-Engine
cp .env.example .env
# Replace POSTGRES_PASSWORD before Docker deployment.
```

Never commit `.env`. Local Uvicorn uses SQLite. Docker Compose overrides `DATABASE_URL` inside the backend container using `POSTGRES_*` values and connects to PostgreSQL.

## Local backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

## Local frontend

```bash
cd frontend
npm install
npm run dev
```

## Docker

```bash
docker compose up --build
```

API: `http://localhost:8001`; docs: `http://localhost:8001/docs`; Phase 3 UI: `http://localhost:5174`.

## Tests and API checks

```bash
cd backend && .venv/bin/pytest -q && .venv/bin/python -m ruff check .
cd ../frontend && npm test && npm run lint && npm run build
curl http://localhost:8001/api/threats
curl http://localhost:8001/api/vulnerabilities
curl http://localhost:8001/api/indicators
curl http://localhost:8001/api/threat-statistics
```

## Phase 2 and Phase 4

Phase 2 reads `VITE_THREAT_API_BASE_URL` (default `http://localhost:8001/api`) for its `/intelligence` page and main overview. It gracefully retains its core dashboard if Phase 3 is unavailable.

Phase 4 can consume normalized severity, risk, confidence, type, CVSS, reputation, source, timestamps, and log-event features. The deterministic correlator remains an auditable baseline for model evaluation and drift detection; credentials are never AI features.
