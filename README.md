# FastAPI Production Template

Production-oriented FastAPI starter with:

- FastAPI + Uvicorn
- Async SQLAlchemy + PostgreSQL (`asyncpg`)
- Health and readiness endpoints
- Prometheus metrics instrumentation
- Sentry integration (optional)
- Pytest test setup
- Docker Compose for PostgreSQL + pgAdmin

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (recommended) or `pip`
- Docker Desktop (optional, for local database containers)

## Project Structure

```text
app/
  api/routes/
    health.py
    items.py
  core/
    database.py
    metrics.py
  models/
    item.py
  config.py
  main.py
tests/
docker-compose.yaml
```

## Environment Variables

Copy `.env.example` to `.env` and adjust values if needed:

```bash
cp .env.example .env
```

Current example values:

```env
POSTGRES_USER=fastapi_user
POSTGRES_PASSWORD=strongpassword123
POSTGRES_DB=fastapi_db
DB_PORT=5432
DATABASE_URL=postgresql+asyncpg://fastapi_user:strongpassword123@localhost:5432/fastapi_db
```

## Install Dependencies

Using `uv`:

```bash
uv sync
```

Or with `pip`:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Run Locally

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

App URLs:

- API: `http://localhost:8000`
- OpenAPI docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Run PostgreSQL + pgAdmin with Docker

```bash
docker compose up -d
```

Services from `docker-compose.yaml`:

- `db` (PostgreSQL 15.6)
- `pgadmin` (dpage/pgadmin4)

To stop:

```bash
docker compose down
```

To stop and remove volumes:

```bash
docker compose down -v
```

## API Endpoints

### Root

- `GET /` - app metadata

### Health

- `GET /health/` - liveness check
- `GET /health/ready` - readiness check including DB health

### Items

- `GET /api/items` - list items
- `POST /api/items` - create item

Example create payload:

```json
{
  "name": "Test Item",
  "description": "Test Description",
  "price": 100
}
```

## Testing

Run tests:

```bash
uv run pytest tests/ -v
```

Run with coverage:

```bash
uv run pytest tests/ -v --cov=app --cov-report=term --cov-report=html
```

Coverage HTML output is generated in `htmlcov/`.

## Observability

- Prometheus middleware is initialized in `app/core/metrics.py`.
- Sentry is configured in `app/main.py` and enabled when `SENTRY_DSN` is set.

## Notes

- On startup, `app/main.py` calls both DB initialization and table creation (`init_database()` + `init_db()`), so ensure PostgreSQL is reachable when running the app.
- If your test double (`FakeDB`) is used for async routes, its `commit`/`refresh` methods should be `async def`.
