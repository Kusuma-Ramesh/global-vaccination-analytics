import { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import api from "../api.js";
import StatusMessage from "../components/StatusMessage.jsx";
import { baseOptions, chartColors } from "../chartSetup.js";

export default function DiseaseExplorer() {
  const [countries, setCountries] = useState([]);
  const [diseases, setDiseases] = useState([]);

  const [countryCode, setCountryCode] = useState("IND");
  const [diseaseCode, setDiseaseCode] = useState("MEASLES");

  const [incidence, setIncidence] = useState([]);
  const [cases, setCases] = useState([]);
  const [topCases, setTopCases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([api.getCountries(), api.getDiseases()]).then(([c, d]) => {
      setCountries(c);
      setDiseases(d);
    });
  }, []);

  useEffect(() => {
    if (!countryCode || !diseaseCode) return;
    let cancelled = false;
    setLoading(true);
    setError(null);

    Promise.all([
      api.getIncidenceTrend({ country_code: countryCode, disease_code: diseaseCode }),
      api.getCasesTrend({ country_code: countryCode, disease_code: diseaseCode }),
      api.getCasesByCountry({ disease_code: diseaseCode, year: 2023 }),
    ])
      .then(([inc, cas, top]) => {
        if (cancelled) return;
        setIncidence(inc);
        setCases(cas);
        setTopCases(top.slice(0, 10));
      })
      .catch((e) => !cancelled && setError(e.message))
      .finally(() => !cancelled && setLoading(false));

    return () => {
      cancelled = true;
    };
  }, [countryCode, diseaseCode]);

  const incidenceData = {
    labels: incidence.map((p) => p.year),
    datasets: [
      {
        label: "Incidence rate",
        data: incidence.map((p) => p.incidence_rate),
        borderColor: chartColors.warn,
        backgroundColor: "rgba(245, 185, 77, 0.15)",
        tension: 0.3,
        pointRadius: 2,
        fill: true,
      },
    ],
  };

  const casesData = {
    labels: cases.map((p) => p.year),
    datasets: [
      {
        label: "Reported cases",
        data: cases.map((p) => p.cases),
        borderColor: chartColors.bad,
        backgroundColor: chartColors.badSoft,
        tension: 0.3,
        pointRadius: 2,
        fill: true,
      },
    ],
  };

  return (
    <>
      <div className="page-header">
        <h1 className="page-title">Disease Trends</h1>
        <p className="page-subtitle">Explore how disease incidence and reported case counts have changed over time.</p>
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
          <label>Disease</label>
          <select value={diseaseCode} onChange={(e) => setDiseaseCode(e.target.value)}>
            {diseases.map((d) => (
              <option key={d.disease_code} value={d.disease_code}>
                {d.disease_description || d.disease_code}
              </option>
            ))}
          </select>
        </div>
      </div>

      <StatusMessage loading={loading} error={error} />

      {!loading && !error && (
        <>
          <div className="grid grid-2" style={{ marginBottom: 18 }}>
            <div className="panel">
              <div className="panel-title">
                Incidence rate over time
                <small>{diseases.find((d) => d.disease_code === diseaseCode)?.disease_description}</small>
              </div>
              <div className="chart-wrap">
                <Line data={incidenceData} options={baseOptions} />
              </div>
            </div>
            <div className="panel">
              <div className="panel-title">
                Reported cases over time
                <small>{diseases.find((d) => d.disease_code === diseaseCode)?.disease_description}</small>
              </div>
              <div className="chart-wrap">
                <Line data={casesData} options={baseOptions} />
              </div>
            </div>
          </div>

          <div className="panel">
            <div className="panel-title">
              Countries with highest reported cases (2023)
              <small>{diseases.find((d) => d.disease_code === diseaseCode)?.disease_description}</small>
            </div>
            <table>
              <thead>
                <tr>
                  <th>Country</th>
                  <th>WHO Region</th>
                  <th>Cases</th>
                </tr>
              </thead>
              <tbody>
                {topCases.map((r) => (
                  <tr key={r.country_code}>
                    <td>{r.country_name}</td>
                    <td>{r.who_region}</td>
                    <td>{r.cases?.toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </>
  );
}
