# Deployment Guide

Copy `.env.example` to `.env`, replace password placeholders with strong unique values, and ensure `DATABASE_URL` matches the database credentials. Never commit `.env`. Set approved CORS origins and upstream Phase URLs. Leave private feed hosts and the scheduler disabled until reviewed.

Run `docker compose config`, then `docker compose up --build -d`. Validate `curl http://localhost:8005/health`, open the UI on port 5177, and review container logs. Back up the PostgreSQL volume, rotate provider credentials, and terminate TLS at a trusted reverse proxy. Restrict ingress and egress to required destinations.

For upgrades, back up the database, apply reviewed migrations, deploy backend, then frontend. Monitor feed error ratio, sync latency, accepted/rejected IOC counts, database growth, correlation volume, and upstream Phase availability.
