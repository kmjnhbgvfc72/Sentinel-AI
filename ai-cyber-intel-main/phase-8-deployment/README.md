# Phase 8 — Production Deployment & Autonomous Cyber Defense

This directory is a deployable enterprise SOC slice: FastAPI APIs, PostgreSQL models,
Redis-ready configuration, model-backed prediction with a deterministic fallback,
Prometheus metrics, a React dashboard, policy-gated response adapters, and Docker/Kubernetes
manifests.

## Quick start

```bash
cd phase-8-deployment
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
PYTHONPATH=. uvicorn main:app --reload
```

Open `http://localhost:8000/api/docs`. The default SQLite URL is intended only for local
development; configure PostgreSQL, external secrets, TLS termination, and a real Phase 7
model in production. Autonomous actions remain dry-run until explicitly enabled.

See [deployment_guide.md](documentation/deployment_guide.md),
[operation_manual.md](documentation/operation_manual.md), and
[incident_response_plan.md](documentation/incident_response_plan.md).
