CREATE TABLE IF NOT EXISTS reports (id SERIAL PRIMARY KEY, report_type VARCHAR(80), title VARCHAR(200), content TEXT, created_at TIMESTAMP);
