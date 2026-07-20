from copy import deepcopy

ASSETS = [
    {"id": 1, "name": "payments-api-01", "asset_type": "Server", "ip_address": "10.20.4.21", "hostname": "payments-api-01.internal", "operating_system": "Ubuntu 24.04 LTS", "department": "Payments", "health_status": "at-risk", "risk_score": 86, "last_seen_at": "2026-07-17T08:42:00Z", "open_alerts": 4},
    {"id": 2, "name": "identity-gateway", "asset_type": "Gateway", "ip_address": "10.20.1.10", "hostname": "identity-gw.internal", "operating_system": "Hardened Linux", "department": "Identity", "health_status": "warning", "risk_score": 68, "last_seen_at": "2026-07-17T08:44:00Z", "open_alerts": 3},
    {"id": 3, "name": "finance-db-primary", "asset_type": "Database", "ip_address": "10.20.8.12", "hostname": "finance-db.internal", "operating_system": "PostgreSQL Appliance", "department": "Finance", "health_status": "healthy", "risk_score": 34, "last_seen_at": "2026-07-17T08:45:00Z", "open_alerts": 1},
    {"id": 4, "name": "analyst-ws-14", "asset_type": "Workstation", "ip_address": "10.30.14.77", "hostname": "analyst-ws-14.internal", "operating_system": "Windows 11 Enterprise", "department": "Security", "health_status": "healthy", "risk_score": 21, "last_seen_at": "2026-07-17T08:40:00Z", "open_alerts": 0},
    {"id": 5, "name": "customer-portal", "asset_type": "Application", "ip_address": "10.20.5.31", "hostname": "portal.internal", "operating_system": "Container Platform", "department": "Digital", "health_status": "warning", "risk_score": 57, "last_seen_at": "2026-07-17T08:41:00Z", "open_alerts": 2},
]

THREATS = [
    {"id": 1, "external_id": "THR-2026-1042", "title": "Anomalous outbound beacon pattern", "description": "Periodic encrypted connections deviated from the asset's established network baseline.", "category": "Command and control indicator", "severity": "critical", "confidence_score": 94, "source": "Network analytics", "target_asset_id": 1, "target_asset": "payments-api-01", "first_detected_at": "2026-07-17T06:18:00Z", "last_detected_at": "2026-07-17T08:31:00Z", "status": "investigating", "evidence": "Consistent interval timing and a newly observed destination were detected; no payload content was retained.", "suggested_response": "Isolate outbound access for the destination, preserve relevant telemetry, and validate approved service dependencies.", "affected_assets": ["payments-api-01"], "timeline": ["06:18 — baseline deviation detected", "06:24 — analyst review opened", "08:31 — latest matching event"]},
    {"id": 2, "external_id": "THR-2026-1038", "title": "Unusual privileged configuration change", "description": "A protected identity policy was changed outside its normal maintenance window.", "category": "Identity anomaly", "severity": "high", "confidence_score": 88, "source": "Identity monitoring", "target_asset_id": 2, "target_asset": "identity-gateway", "first_detected_at": "2026-07-17T05:41:00Z", "last_detected_at": "2026-07-17T05:46:00Z", "status": "contained", "evidence": "Policy change timing and actor behavior differed from the approved change record.", "suggested_response": "Verify the change owner, review audit logs, and restore the approved policy if unauthorized.", "affected_assets": ["identity-gateway"], "timeline": ["05:41 — policy change observed", "05:46 — protective rule restored", "06:02 — investigation assigned"]},
    {"id": 3, "external_id": "THR-2026-1031", "title": "Suspicious process ancestry", "description": "Endpoint telemetry identified an uncommon parent-child process relationship.", "category": "Endpoint behavior", "severity": "medium", "confidence_score": 76, "source": "Endpoint detection", "target_asset_id": 4, "target_asset": "analyst-ws-14", "first_detected_at": "2026-07-16T22:12:00Z", "last_detected_at": "2026-07-16T22:12:00Z", "status": "resolved", "evidence": "The process chain was rare but mapped to a signed internal maintenance utility.", "suggested_response": "Confirm the signed binary hash and retain the exception with an expiration date.", "affected_assets": ["analyst-ws-14"], "timeline": ["22:12 — behavior detected", "22:34 — binary signature verified", "23:01 — case resolved"]},
    {"id": 4, "external_id": "THR-2026-1027", "title": "Elevated authentication failure rate", "description": "Authentication failures exceeded the adaptive baseline for a service account.", "category": "Authentication anomaly", "severity": "high", "confidence_score": 81, "source": "Authentication analytics", "target_asset_id": 5, "target_asset": "customer-portal", "first_detected_at": "2026-07-16T18:03:00Z", "last_detected_at": "2026-07-16T18:19:00Z", "status": "active", "evidence": "Failures originated from known infrastructure but exceeded the service account's expected rate.", "suggested_response": "Validate the deployment configuration, rotate the service credential if exposure is suspected, and review dependent services.", "affected_assets": ["customer-portal", "identity-gateway"], "timeline": ["18:03 — threshold exceeded", "18:10 — service owner notified", "18:19 — failure rate returned to baseline"]},
    {"id": 5, "external_id": "THR-2026-1019", "title": "Database query-volume deviation", "description": "Read volume increased beyond the learned business-hour profile.", "category": "Data access anomaly", "severity": "low", "confidence_score": 64, "source": "Database activity monitoring", "target_asset_id": 3, "target_asset": "finance-db-primary", "first_detected_at": "2026-07-16T13:20:00Z", "last_detected_at": "2026-07-16T14:02:00Z", "status": "resolved", "evidence": "Queries mapped to an approved quarterly reporting job.", "suggested_response": "Document the reporting window and update the expected-volume baseline.", "affected_assets": ["finance-db-primary"], "timeline": ["13:20 — volume deviation detected", "13:48 — job owner confirmed", "14:02 — baseline note updated"]},
]

ALERTS = [
    {"id": 1, "threat_id": 1, "asset_id": 1, "title": "Outbound beacon cadence detected", "description": "Network behavior requires analyst validation.", "severity": "critical", "source": "Network analytics", "asset": "payments-api-01", "status": "new", "created_at": "2026-07-17T08:31:00Z", "updated_at": "2026-07-17T08:31:00Z", "acknowledged_at": None, "resolved_at": None},
    {"id": 2, "threat_id": 2, "asset_id": 2, "title": "Protected policy modified", "description": "An identity control changed outside the approved window.", "severity": "high", "source": "Identity monitoring", "asset": "identity-gateway", "status": "investigating", "created_at": "2026-07-17T05:41:00Z", "updated_at": "2026-07-17T06:02:00Z", "acknowledged_at": "2026-07-17T05:52:00Z", "resolved_at": None},
    {"id": 3, "threat_id": 4, "asset_id": 5, "title": "Authentication baseline exceeded", "description": "A service account generated an unusual failure volume.", "severity": "high", "source": "Authentication analytics", "asset": "customer-portal", "status": "acknowledged", "created_at": "2026-07-16T18:03:00Z", "updated_at": "2026-07-16T18:10:00Z", "acknowledged_at": "2026-07-16T18:10:00Z", "resolved_at": None},
    {"id": 4, "threat_id": 3, "asset_id": 4, "title": "Rare process relationship", "description": "An uncommon process chain was validated as approved.", "severity": "medium", "source": "Endpoint detection", "asset": "analyst-ws-14", "status": "resolved", "created_at": "2026-07-16T22:12:00Z", "updated_at": "2026-07-16T23:01:00Z", "acknowledged_at": "2026-07-16T22:18:00Z", "resolved_at": "2026-07-16T23:01:00Z"},
]

THREAT_TRENDS = [
    {"time": "00:00", "critical": 1, "high": 2, "medium": 4, "low": 6},
    {"time": "04:00", "critical": 1, "high": 3, "medium": 3, "low": 5},
    {"time": "08:00", "critical": 3, "high": 5, "medium": 6, "low": 8},
    {"time": "12:00", "critical": 2, "high": 4, "medium": 8, "low": 9},
    {"time": "16:00", "critical": 2, "high": 6, "medium": 7, "low": 10},
    {"time": "20:00", "critical": 1, "high": 4, "medium": 5, "low": 7},
]

_INITIAL_ALERTS = deepcopy(ALERTS)
ALERT_HISTORY: list[dict] = []


def reset_alerts() -> None:
    ALERTS[:] = deepcopy(_INITIAL_ALERTS)
    ALERT_HISTORY.clear()
