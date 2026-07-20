# System Architecture

Phase 1 establishes a modular three-tier architecture:

```text
React/Vite client -> FastAPI REST API -> PostgreSQL
                         |
              routes -> controllers -> services
                         |
                  SQLAlchemy models
```

The frontend owns presentation and calls versioned `/api/v1` endpoints. FastAPI separates transport, orchestration, business policy, persistence, configuration, and logging. PostgreSQL stores normalized operational data. Docker Compose provides a reproducible local backend and database environment.

## Security boundaries

- Browser access is restricted by an explicit CORS allowlist.
- SQLAlchemy and parameterized SQL prevent query-string interpolation.
- Database constraints validate severity, score, and alert state at rest.
- The backend container runs as a non-root user with privilege escalation disabled.
- Development credentials are placeholders; production deployments must use a secrets manager, TLS, authentication, rate limiting, audit logging, and network isolation.

This separation allows later threat-feed workers, AI inference services, and attack-path graph systems to be introduced without coupling them to the UI.
