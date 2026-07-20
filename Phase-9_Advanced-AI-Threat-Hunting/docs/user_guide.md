# User Guide

## Typical workflow

1. Add trusted IOCs with `POST /api/v1/intelligence/iocs`.
2. Submit events to `POST /api/v1/hunting/search`.
3. Enrich intelligence with ATT&CK and reputation using `POST /api/v1/intelligence/enrich`.
4. Train on numeric historical features using `POST /api/v1/learning/retrain`.
5. Record analyst verdicts using `POST /api/v1/learning/feedback`.
6. Generate attack, attack-path, and asset-risk forecasts under `/api/v1/predictions`.
7. Consume `/api/v1/analytics/dashboard` from the React application.

IOC confidence is expressed from 0 to 1. Risk outputs include both numeric scores and human-readable bands. Forecasts are decision support, not proof of compromise; analysts should verify evidence before response.

## Safe operation

Use only authorized telemetry. Never upload secrets or unrestricted personal data. Validate feed licenses and retention policy. YARA scanning is bounded to 10 MiB and ten seconds. Automated containment remains simulated unless a separately reviewed response adapter is installed.
