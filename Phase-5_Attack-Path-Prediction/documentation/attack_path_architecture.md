# Attack Path Architecture

Phase 5 is an independent defensive service. Phase 4 predictions and risk scores are normalized into an event, the graph builder creates relationships among indicators, users, assets, and vulnerabilities, NetworkX finds bounded simple paths, the predictor scores each path, asset risk aggregates exposure and criticality, and the response engine creates analyst recommendations. Results are persisted through SQLAlchemy and exposed to Phase 2/5 dashboards.

Phase 4 integration is opt-in through `AUTO_ANALYZE_PHASE4=true`; local demo data and deterministic scoring keep Phase 5 independently testable.
