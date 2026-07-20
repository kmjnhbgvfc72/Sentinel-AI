CREATE TABLE IF NOT EXISTS workflows (id SERIAL PRIMARY KEY, incident_id INTEGER, playbook VARCHAR(160), status VARCHAR(30), steps_completed INTEGER, created_at TIMESTAMP);
