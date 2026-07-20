# Data Processing Flow

1. **Collection:** approved CVEs, reputation records, malware hashes, and authorized logs enter bounded collectors.
2. **Processing:** parsers validate identifiers, IP/domain/hash syntax, types, and ranges; sensitive log keys are removed.
3. **Correlation:** IOC reputation, authentication failures, vulnerability severity, and log risk produce explainable severity, confidence, and risk.
4. **Storage:** SQLAlchemy persists normalized threats, vulnerabilities, indicators, malware metadata, and sanitized logs.
5. **Dashboard:** paginated APIs provide consistent `{data, meta}` envelopes to Phase 2 and the Phase 3 React UI.
6. **AI preparation:** Phase 4 receives stable fields, timestamps, provenance, confidence, and deterministic baseline labels.
