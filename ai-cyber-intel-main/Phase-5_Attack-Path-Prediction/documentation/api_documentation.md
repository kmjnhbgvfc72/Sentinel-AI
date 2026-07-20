# API Documentation

- `POST /api/attack/analyze`: validates an event, builds its graph, predicts paths, computes affected-asset risk, persists results, and returns paths/assets/recommendations.
- `GET /api/attack/paths`: returns bounded persisted paths with score and risk level; supports `limit`.
- `GET /api/attack/graph`: returns graph edges for visualization.
- `GET /api/risk/assets`: returns asset risk and criticality; supports `limit`.
- `GET /api/recommendations`: returns defensive recommendations and workflow status; supports `limit`.
- `GET /health`: service health/version.

All APIs return JSON, validate bounds, use security headers, and expose OpenAPI at `/docs`.
