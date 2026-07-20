# Phase 8 deployment guide

## Prerequisites

- Docker 24+ and Compose v2 (or Kubernetes 1.28+ with an ingress controller).
- A PostgreSQL 15+ database and Redis 7+ for production.
- A Phase 7/7-trained `joblib` model mounted at `MODEL_PATH`.

## Docker Compose

```bash
cd phase-8-deployment
cp .env.example .env
mkdir -p secrets
openssl rand -base64 32 > secrets/postgres_password.txt
python -c 'from security.authentication import hash_password; print(hash_password("CHANGE-ME"))'
# Put the hash in ADMIN_PASSWORD_HASH and replace all example secrets.
docker compose -f deployment/docker/docker-compose.yml up -d --build
curl http://localhost:8000/health/ready
```

The API is served on port 8000, the React/Nginx dashboard on 8080, Prometheus on
9090, and Grafana on 3001. Never expose PostgreSQL or Redis directly to the Internet.

## Kubernetes

Create a namespace and secret, then apply the manifests. Set `DATABASE_URL`,
`REDIS_URL`, and `JWT_SECRET` using an external secret manager (Vault, cloud
secret manager, or sealed-secrets) before applying:

```bash
kubectl create namespace ai-soc
kubectl -n ai-soc create secret generic ai-soc-secrets \
  --from-literal=DATABASE_URL='postgresql+psycopg://...' \
  --from-literal=REDIS_URL='redis://:...@redis:6379/0' \
  --from-literal=JWT_SECRET="$(openssl rand -hex 32)"
kubectl -n ai-soc apply -f deployment/kubernetes/
kubectl -n ai-soc rollout status deployment/ai-soc-backend
```

Run migrations/schema initialization as a controlled release step. Backups are
performed by `database/backup_system.py`; test restores before enabling autonomous response.
