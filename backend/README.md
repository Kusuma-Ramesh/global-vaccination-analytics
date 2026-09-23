# Vaccination Analytics — Backend (FastAPI + PostgreSQL)

This backend cleans the 5 WHO Excel datasets, loads them into a normalized
PostgreSQL database, and serves the data over a REST API for the React
frontend (or Power BI / Excel / anything else that can call an HTTP API).

## 1. Project layout

```
backend/
├── app/                  FastAPI application
│   ├── main.py           App entry point (creates the FastAPI app)
│   ├── config.py         Settings (reads backend/.env)
│   ├── database.py       SQLAlchemy engine/session
│   ├── models.py         SQLAlchemy ORM models (mirrors sql/schema.sql)
│   ├── schemas.py        Pydantic response models
│   └── routers/          One router file per topic (coverage, disease, ...)
├── etl/                  Extract -> Transform -> Load pipeline
│   ├── extract.py        Reads the raw .xlsx files
│   ├── transform.py      Cleans & normalizes into dimension/fact frames
│   ├── load.py           Bulk-loads into PostgreSQL
│   └── clean_and_load.py Orchestrator script (run this one)
├── sql/schema.sql        Database schema (dimension + fact tables)
├── data/                 The 5 WHO .xlsx source files (already included)
├── requirements.txt
└── .env.example          Copy to .env and edit
```

## 2. Open in PyCharm

1. Open PyCharm → **Open** → select the `backend` folder (or the whole
   `vaccination-project` folder and mark `backend` as a source root).
2. PyCharm will usually offer to create a virtualenv automatically. If not:
   **File → Settings → Project → Python Interpreter → Add Interpreter →
   Virtualenv Environment**, based on `backend/requirements.txt`.
3. Or from the terminal inside PyCharm:

   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate      # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

## 3. Install & start PostgreSQL

You need a running PostgreSQL server (locally installed, or via Docker).

**Option A — Docker (fastest):**
```bash
docker run --name vaccination-postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:16
```

**Option B — Native install:** install PostgreSQL from
https://www.postgresql.org/download/ and make sure the server is running.

Then create the database (skip if using the Docker command above with a
fresh container — you can create it via `psql` either way):

```bash
psql -U postgres -h localhost -c "CREATE DATABASE vaccination_db;"
```

## 4. Configure environment variables

```bash
cd backend
cp .env.example .env
```

Edit `.env` if your PostgreSQL user/password/host/port differ from the
defaults (`postgres` / `postgres` / `localhost` / `5432`).

## 5. Run the ETL pipeline (clean data + load into Postgres)

From the `backend/` folder, with your virtualenv active:

```bash
python -m etl.clean_and_load
```

This will:
1. Read the 5 `.xlsx` files in `backend/data/`
2. Clean them (drop WHO aggregate/footer rows, fix years, dedupe, clip
   outliers, coerce types)
3. Recreate the database schema from `sql/schema.sql`
4. Bulk-load everything into PostgreSQL (~700k rows total — takes a
   minute or two)

You should see progress logs for each step. Re-run any time you want to
refresh the database from scratch (the schema is dropped & recreated
each run).

## 6. Run the API

```bash
uvicorn app.main:app --reload --port 8000
```

- API root: http://localhost:8000
- Interactive Swagger docs (auto-generated): http://localhost:8000/docs
- Health check: http://localhost:8000/api/health

In PyCharm, you can also right-click `app/main.py` → doesn't run directly
(it's an ASGI app object, not a script) — instead create a **Run
Configuration**: Module name `uvicorn`, parameters
`app.main:app --reload --port 8000`, working directory = `backend/`.

## 7. Key API endpoints

| Endpoint | Purpose |
|---|---|
| `GET /api/countries` | List of countries with WHO region |
| `GET /api/vaccines` | List of vaccines/antigens |
| `GET /api/diseases` | List of tracked diseases |
| `GET /api/coverage/trend` | Coverage over time for a country + vaccine |
| `GET /api/coverage/by-country` | Coverage ranking across countries for a vaccine + year |
| `GET /api/coverage/dose-dropoff` | 1st vs 3rd dose drop-off rate |
| `GET /api/incidence/trend` | Incidence rate over time |
| `GET /api/cases/trend` | Reported cases over time |
| `GET /api/cases/by-country` | Cases ranking across countries |
| `GET /api/vaccine/introduction/timeline` | Rollout of a vaccine by WHO region/year |
| `GET /api/vaccine/schedule` | National immunization schedule for a country |
| `GET /api/analytics/correlation` | Coverage vs. incidence, paired by country |
| `GET /api/analytics/summary` | Global KPI summary |

Full parameter details are in the Swagger docs at `/docs` once the server
is running.

## Notes on data cleaning decisions

- Rows where `GROUP` is an aggregate (`GLOBAL`, `WHO_REGIONS`, `WB_SHORT`,
  etc.) or a trailing metadata/footer row are dropped — only country-level
  rows are kept in the fact tables.
- `YEAR` is coerced to a number and restricted to 1974–2035 (WHO's
  Expanded Programme on Immunization began in 1974); invalid years are
  dropped.
- `COVERAGE` is clipped to 0–150% (values above 100% do occur in WHO
  administrative data due to population-estimate mismatches, but absurd
  outliers are removed).
- Exact duplicate rows are removed from every table.
- Country/disease/vaccine dimension tables are built by deduplicating the
  reference columns across every source file so the same code always maps
  to one canonical name.
