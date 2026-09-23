import { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import api from "../api.js";
import StatusMessage from "../components/StatusMessage.jsx";
import { baseOptions, chartColors } from "../chartSetup.js";

export default function CoverageExplorer() {
  const [countries, setCountries] = useState([]);
  const [vaccines, setVaccines] = useState([]);

  const [countryCode, setCountryCode] = useState("IND");
  const [vaccineCode, setVaccineCode] = useState("DTPCV3");
  const [category, setCategory] = useState("WUENIC");

  const [trend, setTrend] = useState([]);
  const [dropoff, setDropoff] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([api.getCountries(), api.getVaccines()]).then(([c, v]) => {
      setCountries(c);
      setVaccines(v);
    });
  }, []);

  useEffect(() => {
    if (!countryCode || !vaccineCode) return;
    let cancelled = false;
    setLoading(true);
    setError(null);

    Promise.all([
      api.getCoverageTrend({ country_code: countryCode, vaccine_code: vaccineCode, coverage_category: category }),
      api.getDoseDropoff({ country_code: countryCode, coverage_category: category }),
    ])
      .then(([t, d]) => {
        if (cancelled) return;
        setTrend(t);
        setDropoff(d);
      })
      .catch((e) => !cancelled && setError(e.message))
      .finally(() => !cancelled && setLoading(false));

    return () => {
      cancelled = true;
    };
  }, [countryCode, vaccineCode, category]);

  const trendData = {
    labels: trend.map((p) => p.year),
    datasets: [
      {
        label: "Coverage (%)",
        data: trend.map((p) => p.coverage),
        borderColor: chartColors.accent,
        backgroundColor: chartColors.accentSoft,
        fill: true,
        tension: 0.3,
        pointRadius: 2,
      },
    ],
  };

  const dropoffData = {
    labels: dropoff.map((p) => p.year),
    datasets: [
      {
        label: "1st dose coverage (%)",
        data: dropoff.map((p) => p.dose1_coverage),
        borderColor: chartColors.good,
        backgroundColor: chartColors.goodSoft,
        tension: 0.3,
        pointRadius: 2,
      },
      {
        label: "3rd dose coverage (%)",
        data: dropoff.map((p) => p.dose3_coverage),
        borderColor: chartColors.bad,
        backgroundColor: chartColors.badSoft,
        tension: 0.3,
        pointRadius: 2,
      },
    ],
  };

  const latestDropout = [...dropoff].reverse().find((d) => d.dropout_rate_pct != null);

  return (
    <>
      <div className="page-header">
        <h1 className="page-title">Coverage Explorer</h1>
        <p className="page-subtitle">Track vaccination coverage over time and the drop-off between 1st and 3rd doses.</p>
      </div>

      <div className="controls-row">
        <div className="field">
          <label>Country</label>
          <select value={countryCode} onChange={(e) => setCountryCode(e.target.value)}>
            {countries.map((c) => (
              <option key={c.country_code} value={c.country_code}>
                {c.country_name}
              </option>
            ))}
          </select>
        </div>
        <div className="field">
          <label>Vaccine / Antigen</label>
          <select value={vaccineCode} onChange={(e) => setVaccineCode(e.target.value)}>
            {vaccines.map((v) => (
              <option key={v.vaccine_code} value={v.vaccine_code}>
                {v.vaccine_description || v.vaccine_code}
              </option>
            ))}
          </select>
        </div>
        <div className="field">
          <label>Coverage type</label>
          <select value={category} onChange={(e) => setCategory(e.target.value)}>
            <option value="WUENIC">WUENIC (WHO/UNICEF estimate)</option>
            <option value="ADMIN">Administrative</option>
            <option value="OFFICIAL">Official</option>
          </select>
        </div>
      </div>

      <StatusMessage loading={loading} error={error} empty={!loading && !error && trend.length === 0} />

      {!loading && !error && (
        <div className="grid grid-2">
          <div className="panel">
            <div className="panel-title">
              Coverage trend
              <small>{vaccines.find((v) => v.vaccine_code === vaccineCode)?.vaccine_description || vaccineCode}</small>
            </div>
            <div className="chart-wrap">
              <Line data={trendData} options={baseOptions} />
            </div>
          </div>

          <div className="panel">
            <div className="panel-title">
              1st vs. 3rd dose drop-off (DTP)
              <small>
                {latestDropout ? `Latest dropout rate: ${latestDropout.dropout_rate_pct}% (${latestDropout.year})` : "No data"}
              </small>
            </div>
            <div className="chart-wrap">
              <Line data={dropoffData} options={baseOptions} />
            </div>
          </div>
        </div>
      )}
    </>
  );
}
