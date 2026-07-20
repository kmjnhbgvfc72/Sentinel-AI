-- Phase 1 baseline migration. Safe to rerun on an initialized development database.
BEGIN;

CREATE INDEX IF NOT EXISTS idx_users_created_at ON users (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_threats_risk_score ON threats (risk_score DESC);

COMMIT;
