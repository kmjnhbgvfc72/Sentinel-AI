# IOC Management Guide

Supported types are IP, domain, URL, hash, and email. Values are normalized before a `(type, normalized_value)` uniqueness check. Confidence is 0–100; severity is low, medium, high, or critical. Tags should express provenance and handling constraints.

Use `POST /api/ioc` for curated defensive indicators and `DELETE /api/ioc/{id}` only after confirming the indicator is no longer required. Reposting an existing IOC refreshes `last_seen`, keeps the highest confidence, and merges tags. Do not enter credentials, personal data, or unverified indicators.

All mutations create audit-oriented history entries. Production retention and legal review should be configured according to organizational policy.
