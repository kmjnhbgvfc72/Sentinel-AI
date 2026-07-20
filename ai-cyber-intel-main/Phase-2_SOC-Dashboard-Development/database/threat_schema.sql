BEGIN;

CREATE TABLE IF NOT EXISTS threats (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    external_id VARCHAR(80) NOT NULL UNIQUE,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(100) NOT NULL,
    severity VARCHAR(20) NOT NULL CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    confidence_score SMALLINT NOT NULL CHECK (confidence_score BETWEEN 0 AND 100),
    source VARCHAR(120) NOT NULL,
    target_asset_id BIGINT REFERENCES assets(id) ON DELETE SET NULL,
    first_detected_at TIMESTAMPTZ NOT NULL,
    last_detected_at TIMESTAMPTZ NOT NULL,
    status VARCHAR(24) NOT NULL CHECK (status IN ('active', 'investigating', 'contained', 'resolved')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_detection_window CHECK (last_detected_at >= first_detected_at)
);

CREATE INDEX IF NOT EXISTS idx_threats_severity_status ON threats (severity, status);
CREATE INDEX IF NOT EXISTS idx_threats_target_asset ON threats (target_asset_id);
CREATE INDEX IF NOT EXISTS idx_threats_last_detected ON threats (last_detected_at DESC);
CREATE INDEX IF NOT EXISTS idx_threats_category ON threats (category);

COMMIT;
