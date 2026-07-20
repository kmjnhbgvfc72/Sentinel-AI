# Phase 6 — SOAR Automated Response

This service provides defensive incident tracking, playbook workflows, safe response recommendations, notifications, reports, authentication hooks, and audit logging for the AI CTI system.

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env
PYTHONPATH=. uvicorn main:app --reload --port 8004
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Tests and checks:

```bash
cd backend && PYTHONPATH=. pytest -q && ruff check .
cd ../frontend && npm test && npm run lint && npm run build
```

API endpoints include `/api/incidents`, `/api/playbooks`, `/api/playbooks/workflows`, `/api/responses/recommend`, `/api/notifications`, and `/api/reports`. Phase 7 can replace the token adapter with enterprise OIDC, add approval gates, and connect production queues.
