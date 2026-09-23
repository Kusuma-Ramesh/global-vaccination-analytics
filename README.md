# Global Vaccination Analytics Project

Analyzes WHO vaccination coverage, disease incidence, reported cases,
vaccine introduction, and vaccine schedule data to surface public-health
insights: coverage trends, dose drop-off rates, regional disparities in
vaccine rollout, and the correlation between coverage and disease
incidence.

This is a Python full-stack rebuild of the original project brief (which
called for SQL + Power BI) so the whole thing can be run and developed
from **PyCharm**:

```
WHO Excel files  →  ETL (pandas)  →  PostgreSQL  →  FastAPI  →  React dashboard
```

## Structure

```
vaccination-project/
├── backend/     FastAPI + PostgreSQL + ETL pipeline  (see backend/README.md)
└── frontend/    React + Vite + Chart.js dashboard     (see frontend/README.md)
```

## Quick start

1. **Backend** — set up PostgreSQL, run the ETL, start the API.
Full instructions: [`backend/README.md`](backend/README.md)

```powershell
  cd backend

python -m venv .venv

.\\\\\\\\.venv\\\\\\\\Scripts\\\\\\\\Activate.ps1

pip install -r requirements.txt

copy .env.example .env

python -m etl.clean\\\\\\\_and\\\\\\\_load

uvicorn app.main:app --reload --port 8000  

```



2. **Frontend** — install and start the dashboard.
Full instructions: [`frontend/README.md`](frontend/README.md)



```powershell
   cd frontend
   npm install
   cp .env.example .env
   npm run dev
   ```

3. Open http://localhost:5173 in your browser.

## Data sources

Five WHO Immunization Data Portal exports are included in
`backend/data/`:

|File|Contents|
|-|-|
|`coverage-data.xlsx`|Vaccination coverage % by country/year/antigen|
|`incidence-rate-data.xlsx`|Disease incidence rate by country/year/disease|
|`reported-cases-data.xlsx`|Raw reported case counts by country/year/disease|
|`vaccine-introduction-data.xlsx`|Whether/when each country introduced each vaccine|
|`vaccine-schedule-data.xlsx`|National immunization schedules (dose rounds, target age/population)|

## What this answers

The API and dashboard together answer the project's key analysis
questions, e.g.:

* How does vaccination coverage correlate with disease incidence? → **Coverage vs. Disease** page
* What's the drop-off rate between the 1st and 3rd dose? → **Coverage Explorer** page
* Which countries have low coverage and need targeted resources? → **Overview** page (bottom-10 chart)
* Are there disparities in vaccine introduction timelines across WHO regions? → **Vaccine Rollout** page
* Which regions have high disease incidence despite reasonable coverage? → **Coverage vs. Disease** page (outlier table)

Some brief-listed questions (e.g. by gender, education level, urban vs.
rural, socioeconomic group) aren't answerable from this dataset — the WHO
files don't include those demographic breakdowns. Worth calling out
explicitly in your write-up/documentation deliverable.

## Notes for your submission

The original brief asks for SQL scripts, a normalized database, Power BI
dashboards, and documentation. This project maps onto that as:

* **SQL scripts** → `backend/sql/schema.sql`
* **Normalized database** → PostgreSQL, loaded by `backend/etl/`
* **Interactive dashboards** → the React frontend (in place of Power BI)
* **Documentation** → this README + the two sub-READMEs, plus the "Notes
on data cleaning decisions" section in `backend/README.md`

If your evaluator specifically requires Power BI/Tableau dashboards
rather than a custom web app, you can still connect Power BI directly to
this PostgreSQL database (Power BI → Get Data → PostgreSQL database) once
the ETL has loaded it — the schema is already normalized and ready for
that.



\## Validation



The project was validated locally with the following checks:



\- WHO datasets successfully processed through the ETL pipeline.

\- PostgreSQL database populated successfully.

\- FastAPI application starts successfully on port 8000.

\- Analytics API returns live database-derived results.

\- React frontend loads all five dashboard pages successfully.

\- `npm run lint` → 0 warnings and 0 errors.

\- `npm run build` → production build completed successfully.

\- Dashboard data is sourced from the PostgreSQL/FastAPI pipeline rather than mock data.



\### Current dataset summary



\- Countries tracked: 214

\- Diseases tracked: 13

\- Latest available year: 2023

\- Global DTP3 coverage: 85.88%

\- Reported cases: 5,889,519

\- Countries with ≥90% DTP3 coverage: 107

