CREATE TABLE IF NOT EXISTS notifications (id SERIAL PRIMARY KEY, channel VARCHAR(30), recipient VARCHAR(300), subject VARCHAR(200), status VARCHAR(30), created_at TIMESTAMP);
