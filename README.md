# Global Vaccination Analytics Project

A full-stack public-health analytics project built using WHO immunization data. The project analyzes vaccination coverage, disease incidence, reported cases, vaccine introduction, and vaccine schedule data to surface insights into vaccination trends, dose drop-off, regional disparities, vaccine rollout, and the relationship between vaccination coverage and disease incidence.

This project is a Python full-stack implementation of the original project brief, which specified SQL and Power BI. The current implementation provides a complete data pipeline and interactive web dashboard that can be developed and run locally from PyCharm.

## Architecture

WHO Excel Files
      ↓
Pandas ETL Pipeline
      ↓
PostgreSQL Database
      ↓
FastAPI REST API
      ↓
React + Vite Dashboard

## Project Structure

vaccination-project/
├── backend/
│   ├── app/                # FastAPI application
│   ├── data/               # WHO Excel datasets
│   ├── etl/                # Data extraction, transformation and loading
│   ├── sql/                # Database schema
│   ├── .env.example        # Database configuration template
│   ├── requirements.txt    # Python dependencies
│   └── README.md           # Backend setup and documentation
│
├── frontend/
│   ├── public/             # Public frontend assets
│   ├── src/                # React application
│   ├── .env.example        # Frontend configuration template
│   ├── package.json        # Node.js dependencies
│   └── README.md           # Frontend setup and documentation
│
├── Vaccination_Intelligence_FINAL.pbix
├── .gitignore
└── README.md

## Technology Stack

### Data and Backend

- Python
- Pandas
- PostgreSQL
- SQLAlchemy
- FastAPI
- Uvicorn

### Frontend

- React
- Vite
- Chart.js
- Framer Motion
- Axios
- React Router

### Business Intelligence

- Microsoft Power BI
- PostgreSQL

## Quick Start

Follow these steps to run the Global Vaccination Analytics project locally.

### 1. Backend Setup

Open PowerShell from the project folder and run:

cd C:\vaccination-project\backend

Create a Python virtual environment:

python -m venv .venv

Activate the environment:

.\.venv\Scripts\Activate.ps1

Install the required packages:

pip install -r requirements.txt

Create the environment configuration file:

Copy-Item .env.example .env

Open the `.env` file and enter your PostgreSQL database credentials.

Make sure PostgreSQL is installed and running.

Run the ETL pipeline to process the WHO Excel datasets and load the data into PostgreSQL:

python -m etl.clean_and_load

After the ETL completes successfully, start the FastAPI backend:

uvicorn app.main:app --reload --port 8000

The backend will be available at:

http://localhost:8000

The main analytics endpoint is:

http://localhost:8000/api/analytics/summary

Keep this terminal running.

For detailed backend instructions, see `backend/README.md`.

### 2. Frontend Setup

Open a second PowerShell terminal and run:

cd C:\vaccination-project\frontend

Install the required Node.js packages:

npm install

Create the frontend environment configuration file:

Copy-Item .env.example .env

Start the React development server:

npm run dev

The dashboard will be available at:

http://localhost:5173

Open this address in your browser.

For detailed frontend instructions, see `frontend/README.md`.

### 3. Application Flow

The project works through the following pipeline:

WHO Excel Data
        ↓
Pandas ETL Pipeline
        ↓
PostgreSQL Database
        ↓
FastAPI Backend
        ↓
React Dashboard

### 4. Quick Reference

PostgreSQL:
Make sure the PostgreSQL service is running.

ETL Pipeline:
python -m etl.clean_and_load

FastAPI Backend:
uvicorn app.main:app --reload --port 8000

Backend:
http://localhost:8000

Analytics API:
http://localhost:8000/api/analytics/summary

React Dashboard:
npm run dev

Frontend:
http://localhost:5173

### Important

Run the ETL pipeline before using the dashboard so that the WHO datasets are loaded into PostgreSQL.

Keep both the FastAPI backend terminal and React frontend terminal running while using the dashboard.

## Data Sources

The project uses five WHO Immunization Data Portal exports stored in `backend/data/`.

| Dataset | Description |
|---|---|
| `coverage-data.xlsx` | Vaccination coverage by country, year, and antigen |
| `incidence-rate-data.xlsx` | Disease incidence rates by country, year, and disease |
| `reported-cases-data.xlsx` | Reported disease cases by country, year, and disease |
| `vaccine-introduction-data.xlsx` | Vaccine introduction information by country and vaccine |
| `vaccine-schedule-data.xlsx` | National immunization schedules, dose rounds, target age, and population |

## Data Pipeline

The ETL pipeline processes the WHO datasets through three main stages:

1. Extract — Reads the WHO Excel files using Pandas.
2. Transform — Cleans and normalizes the datasets and creates dimension and fact tables.
3. Load — Loads the transformed data into PostgreSQL.

The resulting database contains normalized tables for countries, diseases, vaccines, vaccination coverage, disease incidence, reported cases, vaccine introduction, and vaccine schedules.

## Dashboard

The React dashboard provides five analytical areas.

### Overview

Provides high-level vaccination intelligence including:

- Global DTP3 vaccination coverage
- Total reported disease cases
- Countries tracked
- Countries with high DTP3 coverage
- Diseases tracked
- Global coverage distribution

### Coverage Explorer

Analyzes:

- DTP3 vaccination coverage by country
- Coverage distribution
- High- and low-coverage countries
- Vaccination coverage trends

### Disease Explorer

Analyzes:

- Reported disease cases
- Disease burden trends
- Trends across selected diseases
- Recent disease patterns

### Vaccine Rollout

Analyzes:

- Vaccine introduction timelines
- Vaccine rollout patterns
- Differences in vaccine introduction across countries

### Coverage vs. Disease

Analyzes:

- DTP3 vaccination coverage
- Pertussis incidence
- Correlation between vaccination coverage and disease incidence
- Country-level outliers

## Key Analysis Questions

The project addresses questions such as:

- How does vaccination coverage relate to disease incidence?
- What is the coverage drop-off between the first and third DTP doses?
- Which countries have relatively low vaccination coverage?
- How do vaccine introduction timelines differ across countries?
- Which countries show relatively high disease incidence alongside vaccination coverage?

Some questions from the original project brief cannot be answered using the available WHO datasets. In particular, the provided datasets do not contain demographic breakdowns such as:

- Gender
- Education level
- Urban versus rural population
- Socioeconomic group

These limitations are explicitly documented rather than being estimated or filled with unsupported data.

## Power BI

The project also includes a Power BI dashboard:

Vaccination_Intelligence_FINAL.pbix

The Power BI report provides additional analytical views, including:

- Global vaccination coverage
- Country-level coverage comparison
- Disease burden trends
- Vaccine introduction trends
- DTP1 versus DTP3 coverage
- DTP3 coverage versus pertussis incidence

Power BI can also connect directly to the PostgreSQL database after the ETL pipeline has been executed.

## Validation

The project was validated locally using the following checks:

- WHO datasets successfully processed through the ETL pipeline.
- PostgreSQL database populated successfully.
- FastAPI application started successfully on port 8000.
- Analytics API returned live database-derived results.
- React frontend loaded all five dashboard pages successfully.
- `npm run lint` completed with 0 warnings and 0 errors.
- `npm run build` completed successfully.
- Dashboard data was sourced from the PostgreSQL/FastAPI pipeline rather than mock data.

## Current Dataset Summary

Based on the processed WHO datasets:

| Metric | Value |
|---|---:|
| Countries tracked | 214 |
| Diseases tracked | 13 |
| Latest available year | 2023 |
| Global DTP3 coverage | 85.88% |
| Total reported cases | 5,889,519 |
| Countries with ≥90% DTP3 coverage | 107 |

## Submission Mapping

The original project brief requested SQL, a normalized database, Power BI dashboards, and documentation. The implementation maps these requirements as follows:

| Original Requirement | Project Implementation |
|---|---|
| SQL scripts | `backend/sql/schema.sql` |
| Normalized database | PostgreSQL |
| Data processing | `backend/etl/` |
| Interactive dashboard | React + Vite |
| Business intelligence dashboard | `Vaccination_Intelligence_FINAL.pbix` |
| Documentation | Root and backend/frontend README files |

## Important Notes

### Environment Variables

The actual `.env` files are intentionally excluded from version control because they contain local configuration and database credentials.

Use the provided `.env.example` files as templates.

### Generated and Local Files

The repository excludes development-specific files such as:

- Python virtual environments
- Node.js `node_modules`
- Build output
- Python cache files
- IDE configuration
- Local `.env` files
- Log files

These files are not required for the source-code submission.

### ETL Warning

The ETL process recreates the database tables when executed. Review the backend documentation before running the ETL pipeline against an existing database.

## Project Outcome

The completed system provides an end-to-end vaccination analytics workflow:

WHO Public Health Data
        ↓
Data Extraction
        ↓
Data Cleaning & Transformation
        ↓
Normalized PostgreSQL Database
        ↓
FastAPI Data Services
        ↓
Interactive React Dashboard
        +
Power BI Analytics

The project combines data engineering, database design, REST API development, frontend visualization, and business intelligence into a single vaccination analytics platform.
