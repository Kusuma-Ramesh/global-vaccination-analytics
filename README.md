# Global Vaccination Analytics Project

A full-stack public-health analytics project built using WHO immunization data. The project analyzes vaccination coverage, disease incidence, reported cases, vaccine introduction, and immunization schedules to provide interactive insights into global vaccination trends and disease burden.

The implementation combines a Python ETL pipeline, PostgreSQL database, FastAPI backend, React dashboard, and Power BI report.

---

## Architecture

    WHO Excel Datasets
            ↓
    Pandas ETL Pipeline
            ↓
    PostgreSQL Database
            ↓
    FastAPI REST API
            ↓
    React + Vite Dashboard

    PostgreSQL Database
            ↓
       Power BI Report

---

## Technology Stack

| Layer | Technologies |
|---|---|
| Data Source | WHO Immunization Data Portal |
| Data Processing | Python, Pandas |
| Database | PostgreSQL |
| Backend | FastAPI, SQLAlchemy, Uvicorn |
| Frontend | React, Vite |
| Visualization | Chart.js, Framer Motion |
| Business Intelligence | Microsoft Power BI |
| Version Control | Git, GitHub |

---

## Project Structure

    vaccination-project/
    ├── backend/
    │   ├── app/
    │   │   ├── routers/
    │   │   │   ├── analytics.py
    │   │   │   ├── coverage.py
    │   │   │   ├── disease.py
    │   │   │   ├── lookups.py
    │   │   │   └── vaccines.py
    │   │   ├── config.py
    │   │   ├── database.py
    │   │   ├── main.py
    │   │   ├── models.py
    │   │   └── schemas.py
    │   ├── data/
    │   │   ├── coverage-data.xlsx
    │   │   ├── incidence-rate-data.xlsx
    │   │   ├── reported-cases-data.xlsx
    │   │   ├── vaccine-introduction-data.xlsx
    │   │   └── vaccine-schedule-data.xlsx
    │   ├── etl/
    │   │   ├── clean_and_load.py
    │   │   ├── extract.py
    │   │   ├── load.py
    │   │   └── transform.py
    │   ├── sql/
    │   │   └── schema.sql
    │   ├── .env.example
    │   ├── README.md
    │   └── requirements.txt
    ├── frontend/
    │   ├── public/
    │   ├── src/
    │   │   ├── components/
    │   │   │   ├── KpiCard.jsx
    │   │   │   ├── PageTransition.jsx
    │   │   │   ├── Sidebar.jsx
    │   │   │   └── StatusMessage.jsx
    │   │   ├── pages/
    │   │   │   ├── Dashboard.jsx
    │   │   │   ├── CoverageExplorer.jsx
    │   │   │   ├── DiseaseExplorer.jsx
    │   │   │   ├── VaccineIntroduction.jsx
    │   │   │   └── Correlation.jsx
    │   │   ├── api.js
    │   │   ├── App.jsx
    │   │   ├── chartSetup.js
    │   │   ├── index.css
    │   │   └── main.jsx
    │   ├── .env.example
    │   ├── index.html
    │   ├── package.json
    │   ├── package-lock.json
    │   ├── README.md
    │   └── vite.config.js
    ├── Vaccination_Intelligence_FINAL.pbix
    ├── README.md
    └── .gitignore

---

## Data Sources

The project uses five WHO Immunization Data Portal exports.

| Dataset | Description |
|---|---|
| `coverage-data.xlsx` | Vaccination coverage percentages by country, year, and antigen |
| `incidence-rate-data.xlsx` | Disease incidence rates by country, year, and disease |
| `reported-cases-data.xlsx` | Reported disease cases by country, year, and disease |
| `vaccine-introduction-data.xlsx` | Vaccine introduction information by country and vaccine |
| `vaccine-schedule-data.xlsx` | National immunization schedules, dose rounds, target age, and population |

All source datasets are stored in `backend/data/`.

---

## ETL Pipeline

The ETL pipeline processes the WHO datasets through three stages.

### 1. Extract

Reads the WHO Excel datasets using Pandas.

### 2. Transform

Cleans and standardizes the source data and prepares normalized dimension and fact tables.

### 3. Load

Creates the PostgreSQL schema and loads the processed datasets into the database.

The main ETL entry point is:

    python -m etl.clean_and_load

---

## Database Design

The PostgreSQL database uses a normalized structure consisting of dimension and fact tables.

### Dimension Tables

| Table | Purpose |
|---|---|
| `dim_country` | Country information |
| `dim_disease` | Disease information |
| `dim_vaccine` | Vaccine information |

### Fact Tables

| Table | Purpose |
|---|---|
| `fact_coverage` | Vaccination coverage measurements |
| `fact_incidence_rate` | Disease incidence rates |
| `fact_reported_cases` | Reported disease cases |
| `fact_vaccine_introduction` | Vaccine introduction records |
| `fact_vaccine_schedule` | Immunization schedule records |

The database schema is available in `backend/sql/schema.sql`.

---

## Dashboard

The React dashboard provides five analytical views.

| Page | Purpose |
|---|---|
| Overview | Global vaccination KPIs and high-level trends |
| Coverage Explorer | Country-level vaccination coverage and dose comparisons |
| Disease Explorer | Disease burden and reported case trends |
| Vaccine Rollout | Vaccine introduction trends across countries |
| Coverage vs Disease | Relationship between vaccination coverage and disease incidence |

---

## Key Dashboard Metrics

| Metric | Value |
|---|---:|
| Countries Tracked | 214 |
| Diseases Tracked | 13 |
| Latest Available Year | 2023 |
| Global DTP3 Coverage | 85.88% |
| Total Reported Cases | 5,889,519 |
| Countries with ≥90% DTP3 Coverage | 107 |

---

## Key Analysis Questions

The project provides analysis for questions such as:

- How does vaccination coverage relate to disease incidence?
- What is the coverage difference between the first and third doses?
- Which countries have relatively low DTP3 coverage?
- How has disease burden changed over time?
- How have vaccine introductions changed across countries?
- Which countries show high disease incidence despite vaccination coverage?
- What are the global vaccination coverage patterns?

---

# Quick Start

Follow the steps below to run the project locally.

## 1. Backend Setup

Make sure PostgreSQL is installed and running.

Open PowerShell from the project directory:

    cd C:\vaccination-project\backend

Create a Python virtual environment:

    python -m venv .venv

Activate the environment:

    .\.venv\Scripts\Activate.ps1

Install the required packages:

    pip install -r requirements.txt

Create the environment configuration file:

    Copy-Item .env.example .env

Open `.env` and enter your PostgreSQL database credentials.

Run the ETL pipeline:

    python -m etl.clean_and_load

After the ETL completes successfully, start the FastAPI backend:

    uvicorn app.main:app --reload --port 8000

Backend:

    http://localhost:8000

Analytics API:

    http://localhost:8000/api/analytics/summary

Keep this terminal running.

For detailed backend instructions, see `backend/README.md`.

---

## 2. Frontend Setup

Open a second PowerShell terminal.

Navigate to the frontend:

    cd C:\vaccination-project\frontend

Install the Node.js dependencies:

    npm install

Create the frontend environment file:

    Copy-Item .env.example .env

Start the React development server:

    npm run dev

Dashboard:

    http://localhost:5173

Open the address above in your browser.

For detailed frontend instructions, see `frontend/README.md`.

---

## 3. Application Flow

| Step | Action |
|---:|---|
| 1 | Start PostgreSQL |
| 2 | Run the ETL pipeline |
| 3 | Start the FastAPI backend |
| 4 | Start the React frontend |
| 5 | Open the dashboard in a browser |

### Important

- Run the ETL pipeline before using the dashboard if the database has not already been populated.
- Keep the FastAPI backend running while using the React dashboard.
- Keep the React development server running while using the dashboard.
- PostgreSQL must be available for the backend to retrieve data.

---

## API

The FastAPI backend provides endpoints for the dashboard's analytical requirements.

| Endpoint Group | Purpose |
|---|---|
| `/api/analytics` | Global analytical summaries |
| `/api/coverage` | Vaccination coverage data |
| `/api/disease` | Disease and reported-case data |
| `/api/lookups` | Country, disease, and vaccine lookup data |
| `/api/vaccines` | Vaccine introduction and schedule data |

### Main Analytics Endpoint

    http://localhost:8000/api/analytics/summary

---

## Power BI Report

The project includes the Power BI report:

`Vaccination_Intelligence_FINAL.pbix`

The report contains:

- Global vaccination KPI cards
- Global DTP3 vaccination coverage
- Country-level coverage analysis
- Lowest DTP3 coverage countries
- First-dose versus third-dose coverage
- Disease burden trends
- Vaccine introduction trends
- DTP3 coverage versus pertussis incidence
- Year-based filtering

The Power BI report uses the normalized PostgreSQL data model.

---

## Validation

The project was validated locally before submission.

| Validation | Result |
|---|---|
| WHO datasets processed through ETL | Successful |
| PostgreSQL database populated | Successful |
| FastAPI application startup | Successful |
| Analytics API response | Successful |
| React dashboard pages | Successful |
| `npm run lint` | 0 warnings, 0 errors |
| `npm run build` | Successful |
| Dashboard data source | PostgreSQL + FastAPI |
| Mock dashboard data | Not used |

---

## Dataset Validation Summary

| Metric | Result |
|---|---:|
| Countries Tracked | 214 |
| Diseases Tracked | 13 |
| Latest Available Year | 2023 |
| Global DTP3 Coverage | 85.88% |
| Total Reported Cases | 5,889,519 |
| Countries with ≥90% DTP3 Coverage | 107 |

---

## Data Limitations

The available WHO datasets do not contain every demographic dimension mentioned in the original project brief.

The following analyses cannot be directly produced from the supplied datasets:

- Gender-based vaccination analysis
- Education-level analysis
- Urban versus rural comparison
- Socioeconomic-group analysis

These limitations are documented rather than estimated or filled with synthetic values.

---

## Security and Repository Notes

Sensitive local configuration files are intentionally excluded from version control.

The following files and directories are ignored:

- `.env`
- `.venv/`
- `venv/`
- `node_modules/`
- `dist/`
- `__pycache__/`
- `*.pyc`
- `.idea/`
- `*.log`
- `.DS_Store`

Actual local PostgreSQL credentials are not included in the repository.

The repository contains the source code, ETL pipeline, SQL schema, WHO datasets, configuration examples, documentation, React dashboard, and Power BI report.

---

## Deliverables

| Deliverable | Location |
|---|---|
| Python ETL Pipeline | `backend/etl/` |
| PostgreSQL Schema | `backend/sql/schema.sql` |
| FastAPI Backend | `backend/app/` |
| WHO Datasets | `backend/data/` |
| React Dashboard | `frontend/` |
| Power BI Report | `Vaccination_Intelligence_FINAL.pbix` |
| Main Documentation | `README.md` |
| Backend Documentation | `backend/README.md` |
| Frontend Documentation | `frontend/README.md` |

---

## Project Status

The project has been validated locally and committed to GitHub.

The repository contains the complete implementation, including:

- WHO vaccination datasets
- Pandas ETL pipeline
- Normalized PostgreSQL database schema
- FastAPI backend
- React and Vite dashboard
- Chart.js visualizations
- Power BI report
- Project documentation
- Configuration examples
