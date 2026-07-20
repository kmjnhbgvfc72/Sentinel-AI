# Threat Engine Architecture

Phase 3 is a standalone defensive intelligence service following the Phase 2 FastAPI/React conventions. Bounded collectors receive approved public-feed or internal telemetry, parsers validate and normalize it, the deterministic correlator produces explainable confidence and risk, SQLAlchemy persists normalized models, and read-only APIs supply SOC clients.

The layers are HTTP routes → application services → processing modules → SQLAlchemy models → PostgreSQL. SQLite is the zero-configuration local/test store. External collection is disabled by default. No module probes hosts, executes artifacts, obtains credentials, or attempts exploitation.

Data flow: trusted source → collector/redaction → parser → correlator → validated model → database → API → dashboard.
