BEGIN;

CREATE TABLE IF NOT EXISTS users (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS threats (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    threat_name VARCHAR(255) NOT NULL,
    severity VARCHAR(20) NOT NULL CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    risk_score NUMERIC(5, 2) NOT NULL CHECK (risk_score BETWEEN 0 AND 100)
);

CREATE TABLE IF NOT EXISTS alerts (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    message TEXT NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('open', 'investigating', 'resolved')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_threats_severity ON threats (severity);
CREATE INDEX IF NOT EXISTS idx_alerts_status_created ON alerts (status, created_at DESC);

COMMIT;
