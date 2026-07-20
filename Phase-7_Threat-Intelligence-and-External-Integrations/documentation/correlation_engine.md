# Correlation Engine

The engine reads active IOCs and defensive events from Phase 3 logs, Phase 4 predictions, Phase 5 attack paths, and Phase 6 incidents. Candidate fields are normalized and matched exactly. It persists source phase, external event ID, IOC ID, match type, bounded context, and a 0–100 combined score.

The score blends 60% upstream risk/confidence with 40% IOC confidence, severity, and source reliability. It is prioritization context—not an autonomous verdict. Analysts should verify high-impact decisions. Refresh with `GET /api/correlation?refresh=true`; ordinary reads return stored results without contacting upstream services.
