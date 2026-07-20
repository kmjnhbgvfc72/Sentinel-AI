# Threat Intelligence Architecture

The HTTP layer is limited to validation and serialization. `services/` coordinates use cases, `threat_intelligence/` contains pure domain engines, `database/` owns persistence, and `models/` defines storage entities. This dependency direction keeps feed formats, reputation providers, and upstream Phase APIs replaceable.

Flow: external feed → target safety check → bounded fetch → parser → IOC normalization/validation → repository → scoring/correlation → Phase 4 detection context, Phase 5 path risk, and Phase 6 response context → dashboard/API.

The scheduler is opt-in, runs one coalesced sync job, and owns no database session between executions. Earlier phases are optional runtime dependencies; adapter failures are logged at informational level and do not fail core intelligence APIs.
