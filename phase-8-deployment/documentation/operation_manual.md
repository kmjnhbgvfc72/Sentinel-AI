# SOC operation manual

The service exposes OpenAPI at `/api/docs`. Authenticate at
`POST /api/v1/auth/token` using the configured administrator account and send the
returned bearer token on API requests.

## Normal workflow

1. Ingest normalized firewall, server, EDR, or network events at `POST /api/v1/threats`.
2. Review alerts at `GET /api/v1/alerts` and predictions at `POST /api/v1/predictions`.
3. Validate indicators with threat intelligence and record an incident.
4. Execute a response through `POST /api/v1/responses/execute`. Responses are dry-run
   by default; set `AUTO_RESPONSE_ENABLED=true` only after provider callbacks and approvals
   are configured.

## Monitoring and SLOs

Scrape `/metrics` with Prometheus. Alert on readiness failures, elevated 5xx rate,
latency, CPU/memory saturation, model load failures, and response-audit errors.
Use `/health/live` for liveness and `/health/ready` for traffic readiness.

## Safety controls

All response actions validate targets, require the responder permission, and append an
immutable audit record. Keep autonomous response disabled during model changes, incident
containment reviews, and provider outages. Rotate JWT, database, Redis, and encryption
keys using the external secrets manager.
