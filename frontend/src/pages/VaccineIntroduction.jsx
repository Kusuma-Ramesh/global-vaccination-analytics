import { useEffect, useMemo, useState } from "react";
import { Line } from "react-chartjs-2";
import api from "../api.js";
import StatusMessage from "../components/StatusMessage.jsx";
import { baseOptions, chartColors } from "../chartSetup.js";

const REGION_COLORS = {
  AFRO: "#4f8cff",
  AMRO: "#37c99a",
  EMRO: "#f5b94d",
  EURO: "#f2607a",
  SEARO: "#7c5cff",
  WPRO: "#38bdf8",
};

export default function VaccineIntroduction() {
  const [vaccineList, setVaccineList] = useState([]);
  const [vaccine, setVaccine] = useState("");
  const [timeline, setTimeline] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [countries, setCountries] = useState([]);
  const [countryCode, setCountryCode] = useState("IND");
  const [schedule, setSchedule] = useState([]);

  useEffect(() => {
    Promise.all([api.getIntroducibleVaccines(), api.getCountries()]).then(([v, c]) => {
      setVaccineList(v);
      setVaccine(v[0] || "");
      setCountries(c);
    });
  }, []);

  useEffect(() => {
    if (!vaccine) return;
    let cancelled = false;
    setLoading(true);
    setError(null);
    api
      .getIntroductionTimeline({ vaccine_description: vaccine })
      .then((data) => !cancelled && setTimeline(data))
      .catch((e) => !cancelled && setError(e.message))
      .finally(() => !cancelled && setLoading(false));
    return () => {
      cancelled = true;
    };
  }, [vaccine]);

  useEffect(() => {
    if (!countryCode) return;
    api.getVaccineSchedule({ country_code: countryCode }).then(setSchedule);
  }, [countryCode]);

  const regions = useMemo(() => [...new Set(timeline.map((t) => t.who_region))].filter(Boolean).sort(), [timeline]);
  const years = useMemo(() => [...new Set(timeline.map((t) => t.year))].sort((a, b) => a - b), [timeline]);

  const chartData = {
    labels: years,
    datasets: regions.map((region) => ({
      label: region,
      data: years.map((y) => timeline.find((t) => t.year === y && t.who_region === region)?.pct_introduced ?? null),
      borderColor: REGION_COLORS[region] || chartColors.accent,
      backgroundColor: "transparent",
      tension: 0.25,
      pointRadius: 2,
      spanGaps: true,
    })),
  };

  return (
    <>
      <div className="page-header">
        <h1 className="page-title">Vaccine Rollout</h1>
        <p className="page-subtitle">Compare how quickly WHO regions introduced a given vaccine into their national programs.</p>
      </div>

      <div className="controls-row">
        <div className="field">
          <label>Vaccine</label>
          <select value={vaccine} onChange={(e) => setVaccine(e.target.value)}>
            {vaccineList.map((v) => (
              <option key={v} value={v}>
                {v}
              </option>
            ))}
          </select>
        </div>
      </div>

      <StatusMessage loading={loading} error={error} empty={!loading && !error && timeline.length === 0} />

      {!loading && !error && timeline.length > 0 && (
        <div className="panel" style={{ marginBottom: 18 }}>
          <div className="panel-title">
            % of countries with the vaccine introduced, by WHO region
            <small>{vaccine}</small>
          </div>
          <div className="chart-wrap">
            <Line data={chartData} options={baseOptions} />
          </div>
        </div>
      )}

      <div className="panel">
        <div className="panel-title">
          National vaccination schedule
          <small>Full immunization schedule for the selected country (latest reported year per vaccine)</small>
        </div>
        <div className="controls-row" style={{ marginBottom: 12 }}>
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
        </div>
        <table>
          <thead>
            <tr>
              <th>Vaccine</th>
              <th>Round</th>
              <th>Target population</th>
              <th>Age administered</th>
              <th>Year</th>
            </tr>
          </thead>
          <tbody>
            {schedule.slice(0, 30).map((r, i) => (
              <tr key={i}>
                <td>{r.vaccine_description}</td>
                <td>{r.schedule_rounds ?? "—"}</td>
                <td>{r.target_pop_description ?? "—"}</td>
                <td>{r.age_administered ?? "—"}</td>
                <td>{r.year}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {schedule.length === 0 && <div className="empty">No schedule data for this country.</div>}
      </div>
    </>
  );
}
