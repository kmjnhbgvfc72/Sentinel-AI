# Database migration

Apply files in dependency order:

```bash
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f dashboard_schema.sql
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f threat_schema.sql
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f alerts_schema.sql
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f seed_data.sql
```

Take a verified backup before migration. To roll back Phase 2, remove the objects in reverse dependency order inside a maintenance window:

```sql
BEGIN;
DROP TABLE IF EXISTS alert_status_history;
DROP TABLE IF EXISTS alerts;
DROP TABLE IF EXISTS threats;
DROP TABLE IF EXISTS assets;
COMMIT;
```

The current API uses its deterministic demo repository so Phase 2 runs without infrastructure. The SQL is the PostgreSQL persistence contract for the repository adapter planned next; do not run rollback SQL against a database containing required operational records.
