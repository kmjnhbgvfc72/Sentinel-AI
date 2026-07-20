# Data Flow

1. The browser loads the React SOC console.
2. `Dashboard` requests `GET /api/v1/health` through the centralized API service.
3. The FastAPI route delegates response construction to the system controller.
4. JSON travels back across the CORS-controlled boundary and updates the health panel.
5. Future domain routes will validate input, invoke a service, use a scoped SQLAlchemy session, and persist to PostgreSQL.

No sensitive token or database credential belongs in browser code. Future ingestion data should be normalized, provenance-tagged, deduplicated, and audited before it becomes available to detection services.
