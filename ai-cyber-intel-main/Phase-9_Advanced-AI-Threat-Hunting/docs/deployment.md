# Deployment Guide

## Runtime

Use Python 3.12, install `requirements.txt`, and run behind a TLS-terminating reverse proxy:

```bash
uvicorn run_phase9:app --host 0.0.0.0 --port 8090 --workers 2
```

Required production environment variables:

- `PHASE9_ENVIRONMENT=production`
- `PHASE9_DATABASE_URL` with a least-privilege PostgreSQL account
- `PHASE9_API_KEY` sourced from a secret manager
- `PHASE9_CORS_ORIGINS=https://your-react-application.example`
- `PHASE9_MODEL_DIRECTORY` on durable, access-controlled storage

## Container pattern

The included multi-stage `Dockerfile` runs as a non-root user and uses `/health` as its health check. Build and run it with:

```bash
docker build -t ai-cti-phase9:9.0.0 .
docker run --rm -p 8090:8090 --env-file /secure/path/phase9.env ai-cti-phase9:9.0.0
```

Never bake `.env` or credentials into an image.

## PostgreSQL and scaling

Create separate read/write roles, require TLS, enable backups, and apply retention controls to security telemetry. The included in-memory repository is for demonstration and tests; replace it before horizontal scaling. Run scheduled training and response playbooks in workers with durable queues and idempotency keys.

## Observability and security

Forward structured logs without request secrets, measure latency/error/model-drift metrics, alert on authentication failures, restrict ingress, scan images and dependencies, sign releases, and perform restore tests. Roll back by deploying the previous image and activating the previous immutable model version.
