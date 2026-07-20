BEGIN;

CREATE TABLE IF NOT EXISTS alerts (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    threat_id BIGINT REFERENCES threats(id) ON DELETE SET NULL,
    asset_id BIGINT REFERENCES assets(id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    severity VARCHAR(20) NOT NULL CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    source VARCHAR(120) NOT NULL,
    status VARCHAR(24) NOT NULL DEFAULT 'new' CHECK (status IN ('new', 'investigating', 'acknowledged', 'resolved')),
    acknowledged_at TIMESTAMPTZ,
    resolved_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT alert_has_context CHECK (threat_id IS NOT NULL OR asset_id IS NOT NULL),
    CONSTRAINT resolved_timestamp_consistency CHECK (status <> 'resolved' OR resolved_at IS NOT NULL)
);

CREATE TABLE IF NOT EXISTS alert_status_history (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    alert_id BIGINT NOT NULL REFERENCES alerts(id) ON DELETE CASCADE,
    previous_status VARCHAR(24) NOT NULL CHECK (previous_status IN ('new', 'investigating', 'acknowledged', 'resolved')),
    new_status VARCHAR(24) NOT NULL CHECK (new_status IN ('new', 'investigating', 'acknowledged', 'resolved')),
    changed_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    changed_by VARCHAR(100) NOT NULL,
    CONSTRAINT actual_status_change CHECK (previous_status <> new_status)
);

CREATE INDEX IF NOT EXISTS idx_alerts_status_severity ON alerts (status, severity);
CREATE INDEX IF NOT EXISTS idx_alerts_asset_created ON alerts (asset_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_alerts_threat ON alerts (threat_id);
CREATE INDEX IF NOT EXISTS idx_alert_history_alert_time ON alert_status_history (alert_id, changed_at DESC);

COMMIT;
