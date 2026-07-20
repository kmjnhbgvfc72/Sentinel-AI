# Architecture

## Context

Phase 9 is a self-contained bounded context layered above the capabilities delivered in Phases 1–8. It does not import phase directories directly because their hyphenated names and differing dependency sets would create fragile runtime coupling. Integration occurs through normalized IOC/event dictionaries and versioned REST contracts.

```text
React / SIEM / SOAR clients
          |
     FastAPI v1 + API-key boundary
          |
 Learning | Hunting | Intelligence | Prediction | Analytics
          |                 |
  model registry      automation approval gate
          |                 |
 PostgreSQL adapter / model artifacts / external feed adapters
```

## Components and data flow

Feed records are validated and deduplicated by `IOCDatabase`, enriched with reputation and ATT&CK techniques, then queried by the hunter. The hunter combines known-IOC matches, behaviors, attack patterns, and declarative rules. Numeric event features train an Isolation Forest; analyst verdicts measure precision and identify noisy rules. Prediction services use bounded, explainable scores. Automation separates safe enrichment from actions that require approval. Analytics returns JSON suited to React charting.

## Production qualities

- Application factory and explicit service container support isolation and testing.
- Typed configuration is environment-only; secrets are never committed.
- IOC and request validation occur at trust boundaries.
- Repository/model interfaces are replaceable by PostgreSQL and an artifact store.
- API routes are versioned and OpenAPI is generated automatically.
- Response actions are simulated and approval-gated by default.
- Thread locks protect mutable demonstration stores.

For multi-worker deployment, replace in-memory repositories with PostgreSQL and use a distributed scheduler/task queue for retraining and playbooks.
