CREATE TABLE IF NOT EXISTS audit_logs (id SERIAL PRIMARY KEY, actor VARCHAR(120), action VARCHAR(120), resource VARCHAR(120), details TEXT, created_at TIMESTAMP);
