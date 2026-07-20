# Feed Integration Guide

Create feed records through an approved migration or administrative workflow. Supported formats are JSON (`indicators` or `data` arrays), CSV headers, and one-value-per-line text. Each record should provide `type`, `value`, `confidence`, `severity`, `threat_type`, and optional `tags`.

Only HTTPS endpoints are accepted. DNS is resolved before the request and non-global targets are rejected unless `ALLOW_PRIVATE_FEED_HOSTS=true` is deliberately set for a controlled internal deployment. Redirects are disabled to prevent validation bypass. Configure interval, timeout, and byte limits with environment variables.

Review source license, authenticity, update cadence, and reliability before enabling. `GET /api/feeds/status` exposes last outcome, accepted count, error, and latency.
