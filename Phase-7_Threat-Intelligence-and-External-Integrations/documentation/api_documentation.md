# API Documentation

All business endpoints use `/api`; OpenAPI is served at `/docs` and `/openapi.json`.

| Method | Path | Purpose |
|---|---|---|
| GET | `/feeds` | List configured feeds |
| POST | `/feeds/sync` | Sync all enabled or selected `feed_ids` |
| GET | `/feeds/status` | Latest health per feed |
| GET | `/ioc` | List/filter IOCs by `type`, `active`, `limit` |
| POST | `/ioc` | Validate and add/refresh an IOC |
| DELETE | `/ioc/{id}` | Delete an IOC |
| GET | `/reputation/ip/{ip}` | IP reputation |
| GET | `/reputation/domain/{domain}` | Domain reputation |
| GET | `/reputation/url/{url}` | URL reputation (URL-encode value) |
| GET | `/correlation` | Results; `refresh=true` polls Phases 3–6 |
| GET | `/intelligence/summary` | Dashboard totals and feed coverage |

Errors use `{"error":{"code":"...","message":"..."}}`; validation may include `fields`. Deploy authentication at an API gateway or add the organization’s identity provider before exposing the service beyond a trusted network.
