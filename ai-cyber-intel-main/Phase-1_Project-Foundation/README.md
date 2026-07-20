# AI Cyber Threat Intelligence System — Phase 1

A scalable foundation for an AI-assisted Security Operations Center. Phase 1 provides a responsive SOC dashboard, a layered REST API, PostgreSQL persistence, reproducible containers, tests, and architecture documentation.

## Technology stack

- Frontend: React, Vite, JavaScript
- Backend: Python, FastAPI, SQLAlchemy, Pydantic Settings
- Database: PostgreSQL
- Infrastructure: Docker Compose

## Quick start

1. Review `.env` and replace the development database password where appropriate.
2. Start the API and database: `docker compose up --build`.
3. In another terminal, run `cd frontend && npm install && npm run dev`.
4. Open `http://localhost:5173`.

For a manual Python environment, run:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## API verification

```bash
curl http://localhost:8000/api/v1/health
cd backend && pytest
```

Interactive development documentation is at `http://localhost:8000/docs`. Detailed setup, architecture, data flow, and the five-phase roadmap are in `documentation/`.

## Production note

The checked-in `.env` values support local development only. Before deployment, use managed secrets, TLS, least-privilege database roles, authenticated APIs, network policy, rate limits, centralized audit logs, vulnerability scanning, and pinned/verified dependency updates.
