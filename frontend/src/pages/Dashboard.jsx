import { useEffect, useState } from "react";
import { Bar } from "react-chartjs-2";
import { motion, useReducedMotion } from "framer-motion";
import api from "../api.js";
import KpiCard from "../components/KpiCard.jsx";
import StatusMessage from "../components/StatusMessage.jsx";
import { baseOptions, chartColors } from "../chartSetup.js";

const heroContainerVariants = {
  hidden: {},
  show: { transition: { staggerChildren: 0.08 } },
};

const heroItemVariants = {
  hidden: { opacity: 0, y: 10 },
  show: { opacity: 1, y: 0, transition: { duration: 0.5, ease: [0.16, 1, 0.3, 1] } },
};

export default function Dashboard() {
  const [kpi, setKpi] = useState(null);
  const [topCountries, setTopCountries] = useState([]);
  const [bottomCountries, setBottomCountries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const shouldReduceMotion = useReducedMotion();

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);

    Promise.all([
      api.getKpiSummary({}),
      api.getCoverageByCountry({ vaccine_code: "DTPCV3", year: 2023 }),
    ])
      .then(([kpiData, byCountry]) => {
        if (cancelled) return;
        setKpi(kpiData);
        const withValues = byCountry.filter((c) => c.coverage !== null);
        setTopCountries(withValues.slice(0, 10));
        setBottomCountries([...withValues].sort((a, b) => a.coverage - b.coverage).slice(0, 10));
      })
      .catch((e) => !cancelled && setError(e.message))
      .finally(() => !cancelled && setLoading(false));

    return () => {
      cancelled = true;
    };
  }, []);

  const makeBarData = (rows, color) => ({
    labels: rows.map((r) => r.country_name),
    datasets: [
      {
        label: "DTP3 coverage (%)",
        data: rows.map((r) => r.coverage),
        backgroundColor: color,
        borderRadius: 4,
      },
    ],
  });

  const HeroWrap = shouldReduceMotion ? "div" : motion.div;
  const HeroItem = shouldReduceMotion ? "div" : motion.div;
  const heroWrapProps = shouldReduceMotion
    ? {}
    : { variants: heroContainerVariants, initial: "hidden", animate: "show" };
  const heroItemProps = shouldReduceMotion ? {} : { variants: heroItemVariants };

  return (
    <>
      <HeroWrap className="hero" {...heroWrapProps}>
        <div className="hero-content">
          <HeroItem {...heroItemProps}>
            <h1 className="hero-title">Vaccination Intelligence</h1>
          </HeroItem>
          <HeroItem {...heroItemProps}>
            <p className="hero-tagline">Global Health Surveillance &amp; Vaccination Analytics</p>
          </HeroItem>
          <HeroItem {...heroItemProps}>
            <p className="hero-description">
              A data-driven view into global vaccination coverage, disease burden, vaccine
              introduction, and public-health trends — drawing on WHO and UNICEF immunization
              surveillance data across the countries and reporting years available in this
              platform.
            </p>
          </HeroItem>
        </div>

        <HeroItem className="hero-meta" aria-label="Data coverage summary" {...heroItemProps}>
          <div className="hero-meta-item">
            {kpi ? (
              <span className="hero-meta-value">{kpi.countries_tracked}</span>
            ) : (
              <span className="hero-meta-value is-loading" aria-hidden="true" />
            )}
            <span className="hero-meta-label">Countries tracked</span>
          </div>
          <div className="hero-meta-item">
            {kpi ? (
              <span className="hero-meta-value">{kpi.diseases_tracked}</span>
            ) : (
              <span className="hero-meta-value is-loading" aria-hidden="true" />
            )}
            <span className="hero-meta-label">Diseases monitored</span>
          </div>
          <div className="hero-meta-item">
            {kpi ? (
              <span className="hero-meta-value">{kpi.latest_year}</span>
            ) : (
              <span className="hero-meta-value is-loading" aria-hidden="true" />
            )}
            <span className="hero-meta-label">Latest reporting year</span>
          </div>
        </HeroItem>
      </HeroWrap>

      <div className="section-heading-row">
        <h2 className="section-heading">Global snapshot</h2>
        <span className="section-heading-note">DTP3 coverage · latest WHO-reported year</span>
      </div>

      <StatusMessage loading={loading} error={error} />

      {!loading && !error && kpi && (
        <>
          <div className="grid grid-4" style={{ marginBottom: 18 }}>
            <KpiCard label={`Global DTP3 coverage (${kpi.latest_year})`} value={kpi.global_avg_coverage != null ? `${kpi.global_avg_coverage}%` : "—"} tone="good" />
            <KpiCard label={`Reported cases (${kpi.latest_year})`} value={kpi.total_reported_cases?.toLocaleString() ?? "—"} tone="bad" />
            <KpiCard label="Countries tracked" value={kpi.countries_tracked} />
            <KpiCard label="Countries ≥ 90% DTP3 coverage" value={kpi.countries_high_coverage} tone="good" />
          </div>

          <div className="grid grid-2">
            <div className="panel">
              <div className="panel-title">
                Top 10 countries by DTP3 coverage
                <small>2023 · WUENIC estimate</small>
              </div>
              <div className="chart-wrap">
                <Bar
                  data={makeBarData(topCountries, chartColors.good)}
                  options={{ ...baseOptions, indexAxis: "y", plugins: { ...baseOptions.plugins, legend: { display: false } } }}
                />
              </div>
            </div>

            <div className="panel">
              <div className="panel-title">
                Bottom 10 countries by DTP3 coverage
                <small>2023 · WUENIC estimate — priority for intervention</small>
              </div>
              <div className="chart-wrap">
                <Bar
                  data={makeBarData(bottomCountries, chartColors.bad)}
                  options={{ ...baseOptions, indexAxis: "y", plugins: { ...baseOptions.plugins, legend: { display: false } } }}
                />
              </div>
            </div>
          </div>
        </>
      )}
    </>
  );
}

