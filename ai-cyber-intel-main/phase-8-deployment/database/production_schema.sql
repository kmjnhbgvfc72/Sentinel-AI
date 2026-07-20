CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS threats (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(), source VARCHAR(32) NOT NULL,
  source_ip INET, category VARCHAR(64) NOT NULL, severity VARCHAR(16) NOT NULL CHECK (severity IN ('low','medium','high','critical')),
  risk_score NUMERIC(5,2) NOT NULL CHECK (risk_score BETWEEN 0 AND 100), details JSONB NOT NULL DEFAULT '{}', detected_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_threats_detected ON threats (detected_at DESC);
CREATE INDEX IF NOT EXISTS idx_threats_source_ip ON threats (source_ip);

CREATE TABLE IF NOT EXISTS alerts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(), threat_id UUID REFERENCES threats(id) ON DELETE SET NULL,
  title VARCHAR(200) NOT NULL, severity VARCHAR(16) NOT NULL, status VARCHAR(24) NOT NULL DEFAULT 'open', description TEXT NOT NULL, created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_alerts_status ON alerts(status, created_at DESC);

CREATE TABLE IF NOT EXISTS incidents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(), title VARCHAR(200) NOT NULL, severity VARCHAR(16) NOT NULL,
  status VARCHAR(24) NOT NULL DEFAULT 'open', evidence JSONB NOT NULL DEFAULT '{}', actions JSONB NOT NULL DEFAULT '[]', created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS response_audit (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(), action VARCHAR(32) NOT NULL, target VARCHAR(255) NOT NULL,
  actor VARCHAR(100) NOT NULL, success BOOLEAN NOT NULL, live_mode BOOLEAN NOT NULL DEFAULT false, result JSONB NOT NULL DEFAULT '{}', created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_response_audit_created ON response_audit(created_at DESC);

CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(), username VARCHAR(100) UNIQUE NOT NULL, password_hash TEXT NOT NULL,
  roles TEXT[] NOT NULL DEFAULT ARRAY['viewer'], active BOOLEAN NOT NULL DEFAULT true, created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE OR REPLACE FUNCTION prevent_audit_mutation() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN RAISE EXCEPTION 'response_audit is append-only'; END $$;
DROP TRIGGER IF EXISTS response_audit_immutable ON response_audit;
CREATE TRIGGER response_audit_immutable BEFORE UPDATE OR DELETE ON response_audit FOR EACH ROW EXECUTE FUNCTION prevent_audit_mutation();

