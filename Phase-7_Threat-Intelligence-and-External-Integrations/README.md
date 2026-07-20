# Phase 7 — Threat Intelligence and External Integrations

Production-oriented defensive threat-intelligence service for feed health, IOC curation, reputation, exact-match correlation, and enrichment of the Phase 3–6 workflow. Demo indicators use IANA documentation ranges and reserved `.example` domains.

## Architecture

FastAPI routes call an application service layer; services use isolated validation/parsing/scoring engines and a SQLAlchemy repository. PostgreSQL is the deployment database and SQLite is supported for local development/tests. React/Vite provides a responsive SOC console.

## Quick start

```bash
cp .env.example .env
# Set secure POSTGRES_PASSWORD and matching DATABASE_URL values.
docker compose up --build
```

Backend: `cd backend && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && uvicorn main:app --reload --port 8005`

Frontend: `cd frontend && npm install && npm run dev`

Tests: `cd backend && pytest -q && ruff check .`; then `cd ../frontend && npm run lint && npm test && npm run build`.

### PEP 668 / externally-managed Python environments

Do not install the backend requirements into the operating system Python. Create and activate the local virtual environment first:

```bash
cd Phase-7_Threat-Intelligence-and-External-Integrations/backend
python -m venv .venv
source .venv/bin/activate       # Windows PowerShell: .venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8005
```

Run tools through the environment (`python -m pytest`, `python -m ruff`) so they cannot accidentally resolve to system packages. The `--break-system-packages` option is intentionally not required.

API documentation is available at `http://localhost:8005/docs`. See [documentation](documentation/) for architecture, operations, API, and deployment details.

## Delivered capabilities

- Feed lifecycle management, HTTPS-only synchronization, bounded downloads, parser/validation, scheduler, and per-feed health history.
- Normalized IOC CRUD for IPs, domains, URLs, hashes, and email indicators, with deduplication, expiry metadata, confidence, severity, and audit history.
- Deterministic local reputation lookups with a TTL cache. Provider credentials (AbuseIPDB and VirusTotal) are optional environment variables and are never persisted.
- Exact normalized IOC correlation against read-only adapters for Phase 3 logs, Phase 4 detections, Phase 5 attack paths, and Phase 6 incidents.
- SOC console pages for summary, feeds, IOCs, reputation, and correlation analysis.

## API surface

All application routes are under `/api` (for example `GET /api/feeds`); `/health` is unauthenticated service health. OpenAPI is exposed at `/docs`.

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/api/feeds` | List configured feeds |
| POST | `/api/feeds/sync` | Synchronize enabled feeds (optional `feed_ids`) |
| GET | `/api/feeds/status` | Latest health result per feed |
| GET/POST | `/api/ioc` | Query or create an indicator |
| DELETE | `/api/ioc/{id}` | Remove an indicator |
| GET | `/api/reputation/{ip\|domain\|url}/{value}` | Defensive reputation lookup |
| GET | `/api/correlation?refresh=true` | View or refresh cross-phase matches |
| GET | `/api/intelligence/summary` | Dashboard counters and feed coverage |

## Database and operations

`database/schema.sql` defines `threat_feeds`, `ioc_indicators`, `threat_intelligence_history`, `feed_status`, `reputation_cache`, and `correlation_results`; `seed_data.sql` contains safe documentation-range indicators and disabled feed placeholders. Use `docker compose up --build` for PostgreSQL-backed deployment, or run the documented local SQLite command for development.

See the dedicated guides for the [architecture](documentation/threat_intelligence_architecture.md), [IOC lifecycle](documentation/ioc_management_guide.md), [feed integration](documentation/feed_integration_guide.md), [correlation engine](documentation/correlation_engine.md), [API details](documentation/api_documentation.md), [cross-phase integration](documentation/integration_guide.md), and [deployment](documentation/deployment_guide.md).

## Security defaults

- Feed sync accepts HTTPS only, blocks credentials and private/non-global destinations, does not follow redirects, and enforces timeout/size limits.
- External credentials are optional environment variables and never logged or persisted.
- Correlation performs normalized exact matches to reduce false attribution.
- Seed feeds are disabled placeholders; operators must review licensing, authenticity, and trust before activation.
