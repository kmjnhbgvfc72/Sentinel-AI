INSERT INTO users (username, email)
VALUES ('soc_analyst', 'soc.analyst@example.invalid')
ON CONFLICT (username) DO NOTHING;

INSERT INTO threats (threat_name, severity, risk_score)
SELECT 'Example command-and-control indicator', 'high', 82.50
WHERE NOT EXISTS (SELECT 1 FROM threats WHERE threat_name = 'Example command-and-control indicator');

INSERT INTO alerts (message, status)
SELECT 'Example alert generated for development validation', 'open'
WHERE NOT EXISTS (SELECT 1 FROM alerts WHERE message = 'Example alert generated for development validation');
