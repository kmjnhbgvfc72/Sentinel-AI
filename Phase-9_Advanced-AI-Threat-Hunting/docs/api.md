# API Reference

The canonical, executable API reference is generated at `/openapi.json`, with interactive documentation at `/docs` and `/redoc`. All functional routes use the `/api/v1` prefix. When `PHASE9_API_KEY` is set, send it as `X-API-Key`.

| Area | Method and path | Purpose |
| --- | --- | --- |
| Operations | `GET /health` | Liveness and configuration status |
| Hunting | `POST /api/v1/hunting/search` | Hunt one normalized event |
| Hunting | `GET /api/v1/hunting/iocs` | Search IOCs |
| Intelligence | `POST /api/v1/intelligence/iocs` | Validate and upsert an IOC |
| Intelligence | `GET /api/v1/intelligence/iocs` | Query IOCs |
| Intelligence | `POST /api/v1/intelligence/enrich` | ATT&CK/reputation enrichment |
| Predictions | `POST /api/v1/predictions/attacks` | Attack likelihood forecast |
| Predictions | `POST /api/v1/predictions/paths` | Likely graph paths |
| Predictions | `POST /api/v1/predictions/risk` | Asset risk forecast |
| Analytics | `POST /api/v1/analytics/summary` | Detection statistics and trends |
| Analytics | `GET /api/v1/analytics/dashboard` | Executive KPIs |
| Learning | `POST /api/v1/learning/retrain` | Train and register a model |
| Learning | `POST /api/v1/learning/assess` | Score features |
| Learning | `POST /api/v1/learning/feedback` | Submit analyst verdict |
| Learning | `GET /api/v1/learning/versions` | List model versions |

Example:

```bash
curl -X POST http://localhost:8090/api/v1/intelligence/iocs \
  -H 'Content-Type: application/json' -H "X-API-Key: $PHASE9_API_KEY" \
  -d '{"type":"domain","value":"malicious.example","confidence":0.9,"source":"analyst"}'
```

Validation failures return 422, missing/invalid credentials return 401, and scoring before training returns 409.
