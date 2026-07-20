# Incident response plan

## Triage

Assign an incident owner, preserve raw logs and alert evidence, classify severity, and
record the suspected scope in `POST /api/v1/responses/incidents`. Do not delete evidence.

## Containment

For confirmed compromise, use `block_ip`, `isolate_device`, or `disable_account` through
the response API. Require a second-person approval for critical incidents and verify the
provider result. If a provider is unavailable, keep the action simulated and use the
corresponding emergency runbook (firewall, EDR, or identity provider console).

## Eradication and recovery

Rotate affected credentials, patch the exploited service, rebuild untrusted hosts from a
known-good image, and restore only from verified backups. Run
`testing/recovery_testing.py` after restoration, then monitor for recurrence.

## Lessons learned

Within 72 hours, close the incident with timeline, indicators, root cause, actions taken,
model prediction quality, and follow-up controls. Retain audit and evidence according to
the organization's regulatory retention policy.
