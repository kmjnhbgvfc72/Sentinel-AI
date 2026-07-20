# Installation

## Prerequisites

- Docker Engine with Docker Compose, or PostgreSQL 15+ for manual setup
- Python 3.12+
- Node.js 20+ and npm

## Docker backend and database

From `Phase-1_Project-Foundation`:

```bash
docker compose up --build
```

The API runs at `http://localhost:8000`; PostgreSQL listens on port `5432`.

## Manual backend

Start PostgreSQL, update `.env`, then:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Frontend

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. Test the API with `curl http://localhost:8000/api/v1/health`, the Swagger UI at `http://localhost:8000/docs`, or `pytest` from `backend/`.
