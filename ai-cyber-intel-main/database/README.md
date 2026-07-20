# Central database

`central_schema.sql` contains integration-owned metadata only. Each phase remains the owner of its domain tables. The central application references phase records through stable string identifiers and does not directly mutate phase schemas.

Apply with:

```bash
psql "$CENTRAL_DATABASE_URL" -v ON_ERROR_STOP=1 -f database/central_schema.sql
```
