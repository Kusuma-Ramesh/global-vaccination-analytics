import { useEffect, useState } from "react";
import { Scatter } from "react-chartjs-2";
import api from "../api.js";
import StatusMessage from "../components/StatusMessage.jsx";
import { baseOptions, chartColors } from "../chartSetup.js";

export default function Correlation() {
  const [vaccines, setVaccines] = useState([]);
  const [diseases, setDiseases] = useState([]);

  const [vaccineCode, setVaccineCode] = useState("MCV1");
  const [diseaseCode, setDiseaseCode] = useState("MEASLES");
  const [year, setYear] = useState(2023);

  const [points, setPoints] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([api.getVaccines(), api.getDiseases()]).then(([v, d]) => {
      setVaccines(v);
      setDiseases(d);
    });
  }, []);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    api
      .getCorrelation({ vaccine_code: vaccineCode, disease_code: diseaseCode, year })
      .then((data) => !cancelled && setPoints(data.filter((p) => p.coverage != null && p.incidence_rate != null)))
      .catch((e) => !cancelled && setError(e.message))
      .finally(() => !cancelled && setLoading(false));
    return () => {
      cancelled = true;
    };
  }, [vaccineCode, diseaseCode, year]);

  const scatterData = {
    datasets: [
      {
        label: `${year}`,
        data: points.map((p) => ({ x: p.coverage, y: p.incidence_rate, country: p.country_name })),
        backgroundColor: chartColors.accent,
        pointRadius: 4,
        pointHoverRadius: 6,
      },
    ],
  };

  const scatterOptions = {
    ...baseOptions,
    scales: {
      x: { ...baseOptions.scales.x, title: { display: true, text: "Vaccination coverage (%)", color: chartColors.text } },
      y: { ...baseOptions.scales.y, title: { display: true, text: "Incidence rate", color: chartColors.text } },
    },
    plugins: {
      ...baseOptions.plugins,
      tooltip: {
        ...baseOptions.plugins.tooltip,
        callbacks: {
          label: (ctx) => `${ctx.raw.country}: ${ctx.raw.x}% coverage, ${ctx.raw.y} incidence rate`,
        },
      },
    },
  };

  // Highlight outliers: high coverage but still notable incidence
  const outliers = [...points]
    .filter((p) => p.coverage >= 80)
    .sort((a, b) => b.incidence_rate - a.incidence_rate)
    .slice(0, 8);

  return (
    <>
      <div className="page-header">
        <h1 className="page-title">Coverage vs. Disease Incidence</h1>
        <p className="page-subtitle">
          Each point is a country. Look for the pattern (higher coverage → lower incidence) and the outliers that break it.
        </p>
      </div>

      <div className="controls-row">
        <div className="field">
          <label>Vaccine</label>
          <select value={vaccineCode} onChange={(e) => setVaccineCode(e.target.value)}>
            {vaccines.map((v) => (
              <option key={v.vaccine_code} value={v.vaccine_code}>
                {v.vaccine_description || v.vaccine_code}
              </option>
            ))}
          </select>
        </div>
        <div className="field">
          <label>Disease</label>
          <select value={diseaseCode} onChange={(e) => setDiseaseCode(e.target.value)}>
            {diseases.map((d) => (
              <option key={d.disease_code} value={d.disease_code}>
                {d.disease_description || d.disease_code}
              </option>
            ))}
          </select>
        </div>
        <div className="field">
          <label>Year</label>
          <input type="number" value={year} min={1980} max={2023} onChange={(e) => setYear(Number(e.target.value))} />
        </div>
      </div>

      <StatusMessage loading={loading} error={error} empty={!loading && !error && points.length === 0} />

      {!loading && !error && points.length > 0 && (
        <div className="grid grid-2">
          <div className="panel">
            <div className="panel-title">
              Coverage vs. incidence scatter
              <small>{points.length} countries with data for both metrics</small>
            </div>
            <div className="chart-wrap">
              <Scatter data={scatterData} options={scatterOptions} />
            </div>
          </div>

          <div className="panel">
            <div className="panel-title">
              High coverage, notable incidence
              <small>Countries with ≥80% coverage worth investigating for vaccine effectiveness gaps</small>
            </div>
            <table>
              <thead>
                <tr>
                  <th>Country</th>
                  <th>Coverage (%)</th>
                  <th>Incidence rate</th>
                </tr>
              </thead>
              <tbody>
                {outliers.map((o) => (
                  <tr key={o.country_code}>
                    <td>{o.country_name}</td>
                    <td>{o.coverage}</td>
                    <td>{o.incidence_rate}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            {outliers.length === 0 && <div className="empty">No high-coverage outliers for this selection.</div>}
          </div>
        </div>
      )}
    </>
  );
}
