BEGIN;

INSERT INTO assets (name, asset_type, ip_address, hostname, operating_system, department, health_status, risk_score, last_seen_at)
VALUES
    ('payments-api-01', 'Server', '10.20.4.21', 'payments-api-01.internal', 'Ubuntu 24.04 LTS', 'Payments', 'at-risk', 86, CURRENT_TIMESTAMP),
    ('identity-gateway', 'Gateway', '10.20.1.10', 'identity-gw.internal', 'Hardened Linux', 'Identity', 'warning', 68, CURRENT_TIMESTAMP),
    ('finance-db-primary', 'Database', '10.20.8.12', 'finance-db.internal', 'PostgreSQL Appliance', 'Finance', 'healthy', 34, CURRENT_TIMESTAMP)
ON CONFLICT (name) DO NOTHING;

INSERT INTO threats (external_id, title, description, category, severity, confidence_score, source, target_asset_id, first_detected_at, last_detected_at, status)
SELECT 'THR-DEMO-001', 'Anomalous outbound beacon pattern', 'Periodic encrypted connections deviated from the established baseline.', 'Command and control indicator', 'critical', 94, 'Network analytics', id, CURRENT_TIMESTAMP - INTERVAL '2 hours', CURRENT_TIMESTAMP, 'investigating'
FROM assets WHERE name = 'payments-api-01'
ON CONFLICT (external_id) DO NOTHING;

INSERT INTO alerts (threat_id, asset_id, title, description, severity, source, status)
SELECT threats.id, assets.id, 'Outbound beacon cadence detected', 'Network behavior requires analyst validation.', 'critical', 'Network analytics', 'new'
FROM threats JOIN assets ON assets.name = 'payments-api-01' WHERE threats.external_id = 'THR-DEMO-001'
AND NOT EXISTS (SELECT 1 FROM alerts WHERE title = 'Outbound beacon cadence detected');

COMMIT;
