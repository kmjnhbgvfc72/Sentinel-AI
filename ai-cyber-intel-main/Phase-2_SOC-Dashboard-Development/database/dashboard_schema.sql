BEGIN;

CREATE TABLE IF NOT EXISTS assets (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE,
    asset_type VARCHAR(40) NOT NULL,
    ip_address INET,
    hostname VARCHAR(253) UNIQUE,
    operating_system VARCHAR(150),
    department VARCHAR(100),
    health_status VARCHAR(20) NOT NULL DEFAULT 'healthy' CHECK (health_status IN ('healthy', 'warning', 'at-risk', 'offline')),
    risk_score SMALLINT NOT NULL DEFAULT 0 CHECK (risk_score BETWEEN 0 AND 100),
    last_seen_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT asset_network_identity CHECK (ip_address IS NOT NULL OR hostname IS NOT NULL)
);

CREATE INDEX IF NOT EXISTS idx_assets_type_health ON assets (asset_type, health_status);
CREATE INDEX IF NOT EXISTS idx_assets_risk ON assets (risk_score DESC);
CREATE INDEX IF NOT EXISTS idx_assets_last_seen ON assets (last_seen_at DESC);

COMMIT;
