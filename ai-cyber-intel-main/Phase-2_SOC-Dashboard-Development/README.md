# Phase 2 — SOC Dashboard Development

A responsive defensive Security Operations Center dashboard built with React 19, Vite, React Router, Axios, Recharts, Lucide, FastAPI, Pydantic, SQLAlchemy-compatible PostgreSQL schemas, and pytest.

## Prerequisites

- Python 3.12 or 3.13 (Python 3.14 support varies by compiled dependency)
- Node.js 20.19+ and npm
- PostgreSQL 15+ or Docker Compose for the database

## Environment

Copy `.env.example` to `.env`, replace the development database password, and adjust origins/URLs for your environment:

```bash
cp .env.example .env
```

`CORS_ORIGINS` is a JSON list. `VITE_API_BASE_URL=/api` uses the Vite development proxy configured by `SOC_API_PROXY_TARGET`. Dashboard polling defaults to 30 seconds and pauses while the browser tab is hidden. No production secret belongs in a Vite variable because those variables are public browser code.

## Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

OpenAPI is available at the server's `/docs` path. Run tests with `python -m pytest -q`.

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Tests, lint, and production build:

```bash
npm test
npm run lint
npm run build
```

## PostgreSQL setup

From `database/`, apply the scripts in order with `psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f <file>`: `dashboard_schema.sql`, `threat_schema.sql`, `alerts_schema.sql`, then `seed_data.sql`. See `database/README.md` for exact commands and rollback guidance.

Alternatively, after creating `.env`, start the database and API with:

```bash
docker compose up --build
```

## API summary

- Health: `GET /health`, `GET /api/health`
- Dashboard: summary, threat trends, risk distribution, recent alerts, top assets under `/api/dashboard`
- Threats: list/filter and details under `/api/threats`
- Alerts: list, details, and validated status transitions under `/api/alerts`
- Assets: list/filter and details under `/api/assets`
- Reports: security summary and functional CSV export under `/api/reports`

## Known limitations

The Phase 2 API intentionally runs against deterministic defensive demo records through a service/repository boundary. PostgreSQL schemas and migration scripts are production-oriented, but a SQLAlchemy repository adapter, authentication/RBAC, multi-user concurrency, and durable alert-history writes are deferred. Dashboard data uses configurable polling rather than streaming, so the UI labels it as polling rather than real-time monitoring. Browser print provides PDF output; there is no server PDF renderer.
