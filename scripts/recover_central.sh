#!/usr/bin/env bash
set -Eeuo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
compose_file="$project_root/docker-compose.central.yml"
env_file="$project_root/.env"
compose=(docker compose --env-file "$env_file" -f "$compose_file")

if [[ ! -f "$env_file" ]]; then
  echo "Missing $env_file. Create it from .env.central.example first." >&2
  exit 1
fi

if ! grep -qE '^CENTRAL_POSTGRES_PASSWORD=.+$' "$env_file"; then
  echo "CENTRAL_POSTGRES_PASSWORD must be set to a non-empty value in $env_file." >&2
  exit 1
fi

echo "[1/7] Starting central PostgreSQL..."
"${compose[@]}" up -d central-database

echo "[2/7] Waiting for PostgreSQL readiness..."
database_ready=false
for _ in {1..30}; do
  if "${compose[@]}" exec -T central-database pg_isready -U cti -d cti_central >/dev/null 2>&1; then
    database_ready=true
    break
  fi
  sleep 2
done
if [[ "$database_ready" != true ]]; then
  "${compose[@]}" logs --tail=100 central-database
  echo "PostgreSQL did not become ready." >&2
  exit 1
fi

echo "[3/7] Synchronizing the existing database role password..."
"${compose[@]}" exec -T central-database sh -ec \
  'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -v new_password="$POSTGRES_PASSWORD"' <<'SQL'
ALTER ROLE cti WITH PASSWORD :'new_password';
SQL

echo "[4/7] Rebuilding the central API image..."
"${compose[@]}" build --no-cache central-api

echo "[5/7] Recreating only the central API container..."
"${compose[@]}" up -d --no-deps --force-recreate central-api

echo "[6/7] Initializing authentication and security tables..."
"${compose[@]}" exec -T central-api python -m backend.scripts.init_db

echo "[7/7] Synchronizing the configured administrator..."
"${compose[@]}" exec -T central-api python -c '
from sqlalchemy import select
from backend.config import get_settings
from backend.database import SessionLocal
from backend.models import User
from backend.services.auth_service import AuthService, hash_password

settings = get_settings()
if not settings.bootstrap_admin_password:
    raise SystemExit("CENTRAL_BOOTSTRAP_ADMIN_PASSWORD must be configured")
with SessionLocal() as db:
    user = db.scalar(select(User).where(User.username == settings.bootstrap_admin_username))
    if user:
        user.password_hash = hash_password(settings.bootstrap_admin_password)
        user.role = "admin"
        db.commit()
    else:
        AuthService(db).create_user(
            settings.bootstrap_admin_username,
            settings.bootstrap_admin_email,
            settings.bootstrap_admin_password,
            "admin",
        )
'

echo "Central recovery completed. Checking API health..."
"${compose[@]}" ps
curl --fail --silent --show-error http://localhost:8100/health
echo
echo "Login with CENTRAL_BOOTSTRAP_ADMIN_USERNAME and CENTRAL_BOOTSTRAP_ADMIN_PASSWORD from .env."
