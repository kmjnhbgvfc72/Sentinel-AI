# Central integration architecture

The central application composes the existing phase services without moving, renaming, or importing their internal modules. Each phase remains independently runnable and owns its domain behavior and persistence.

## Runtime flow

```text
Phase 3 normalized events -> Phase 4 AI detection -> Phase 5 attack paths
          ^                         |                       |
          |                         +--------+--------------+
Phase 7 external IOCs                        v
                                      Phase 6 SOAR
                                             |
                                             v
                                      Phase 9 hunting

Phase 2 SOC dashboard -> Central API gateway -> every phase API
Phase 1 -> shared foundation and PostgreSQL conventions
Phase 8 -> deployment, health, Prometheus, Grafana, and operations
```

## Central API

- `GET /health`: central process health.
- `GET /api/v1/system/health`: concurrent health check for Phases 1-9.
- `GET /api/v1/system/topology`: phase ownership and data flow.
- `GET /api/v1/system/overview`: fault-tolerant aggregate SOC view.
- `POST /api/v1/pipeline/synchronize`: explicit Phase 3 -> 4 -> 5 synchronization.
- `/api/v1/phase/{number}/{path}`: same-origin reverse gateway to an existing phase API.

The synchronization route is intentionally a `POST` because it creates Phase 4 and Phase 5 records. It is not run automatically at application startup.

## Database ownership

The central `integration` schema stores only lineage, an event outbox contract, and phase-health snapshots. Domain records remain in phase-owned schemas. This avoids a second competing definition of threats, detections, paths, incidents, and IOCs.

## Dashboard compatibility

Set `VITE_CENTRAL_API_BASE_URL=http://localhost:8100/api/v1` to route the existing Phase 2 dashboard through the central gateway. If the variable is unset, all original Phase 2 service URLs remain active.
