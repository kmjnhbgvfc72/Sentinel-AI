# API Documentation

All APIs are read-only JSON endpoints below `/api`. Invalid queries return structured HTTP 422 errors. OpenAPI is available at `/docs`.

- `GET /api/threats`: newest threats; supports `page`, `page_size`, `severity`, and exact `threat_type`.
- `GET /api/vulnerabilities`: CVE, description, severity, CVSS, affected products, and publication time; supports pagination and severity.
- `GET /api/indicators`: IOC value/type, confidence/reputation, category, country, status, and observation times; supports pagination and type.
- `GET /api/threat-statistics`: total/high-risk/critical counts, average/overall risk, critical vulnerabilities, suspicious events, and severity distribution.
- `GET /api/logs`: sanitized defensive events used by the existing Phase 2 integration; supports pagination and risk level.
- `GET /health`: service health, version, and UTC timestamp.
