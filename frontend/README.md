# Vaccination Analytics — Frontend (React + Vite + Chart.js)

A dashboard that visualizes global vaccination coverage, disease
incidence/cases, vaccine rollout timelines, and coverage-vs-disease
correlation, backed by the FastAPI backend in `../backend`.

## Pages

- **Overview** — global KPIs, top/bottom countries by DTP3 coverage
- **Coverage Explorer** — coverage trend + 1st-vs-3rd dose drop-off, by country/vaccine
- **Disease Trends** — incidence rate & reported cases over time, top countries by cases
- **Vaccine Rollout** — % of countries per WHO region that introduced a vaccine, by year; national immunization schedule table
- **Coverage vs. Disease** — scatter plot correlating coverage with incidence, with an outlier table

## Setup

Requires Node.js 18+.

```bash
cd frontend
npm install
cp .env.example .env    # adjust VITE_API_URL if your backend runs elsewhere
npm run dev
```

Open http://localhost:5173. Make sure the backend (`../backend`) is
running on http://localhost:8000 first — see `../backend/README.md`.

## Build for production

```bash
npm run build      # outputs to dist/
npm run preview    # preview the production build locally
```

## Tech

- **Vite** + **React 19**
- **react-router-dom** for page navigation
- **chart.js** + **react-chartjs-2** for line/bar/scatter charts
- **axios** for API calls (see `src/api.js`)

## Project structure

```
frontend/
├── src/
│   ├── api.js            All backend API calls in one place
│   ├── chartSetup.js     Chart.js registration + shared color/options
│   ├── App.jsx           Routes
│   ├── main.jsx          Entry point
│   ├── index.css         Design tokens & global styles
│   ├── components/       Sidebar, KpiCard, StatusMessage
│   └── pages/            One file per page (see list above)
├── index.html
├── vite.config.js
└── package.json
```
