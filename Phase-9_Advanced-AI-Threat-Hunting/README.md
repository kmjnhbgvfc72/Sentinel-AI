# Phase 9 — Advanced AI Threat Hunting

The final project phase combines continuous anomaly learning, threat hunting, IOC and intelligence management, explainable forecasting, approval-aware security automation, and enterprise analytics behind a FastAPI API.

## Quick start

```bash
cd Phase-9_Advanced-AI-Threat-Hunting
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PHASE9_DATABASE_URL='postgresql+psycopg://phase9@localhost:5432/threat_intelligence'
export PHASE9_API_KEY='replace-with-a-secret'
python run_phase9.py
```

Open `http://localhost:8090/docs` for Swagger UI or `/redoc` for ReDoc. Supply `X-API-Key` when `PHASE9_API_KEY` is configured.

## Design

- `ai_learning`: adaptive anomaly models, feedback, retraining, scheduling, versions
- `threat_hunting`: IOC, YARA, behavior, patterns, correlation, rules
- `threat_intelligence`: feeds, CVEs, ATT&CK, reputation, IOC repository
- `prediction`: attacks, paths, asset risk, confidence, recommendations
- `automation`: workflows, playbooks, responses, notifications, incidents
- `analytics`: trends, statistics, reports, charts, executive dashboard
- `api`: versioned FastAPI routers
- `config`: typed environment configuration and logging

The default repository is an in-memory demonstration adapter. Its narrow interface is ready to be replaced by a PostgreSQL repository without changing domain services. Destructive response actions require explicit approval and are simulated by default.

## Test

```bash
pytest -q
```

Configuration, API examples, architecture, and operational guidance are in [`docs/`](docs/).
