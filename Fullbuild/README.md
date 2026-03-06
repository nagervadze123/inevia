# Fullbuild - Startup Builder OS (Agent Edition)

## Quickstart
1. `cp .env.example .env`
2. `docker compose up --build`
3. Open `http://localhost:3000`

Backend runs migrations at startup using Alembic.

## Architecture
- FastAPI backend with SQLAlchemy 2 + Alembic
- Multi-agent orchestrator with strict Pydantic v2 JSON schemas
- Celery + Redis for background heavy runs (assets, commerce, distribution, build_all)
- Next.js App Router frontend with project dashboard + run polling

## API
- Auth: `/api/auth/register`, `/api/auth/login`, `/api/auth/logout`
- Projects: `/api/projects`, `/api/projects/{id}`
- Workflow: `/api/projects/{id}/run`, `/api/projects/{id}/runs`
- Results: opportunities, strategy, assets, listings, calendars, strategy select

## Testing
From `backend/`:
- `pytest`
