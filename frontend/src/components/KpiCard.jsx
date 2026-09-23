/**
 * KpiCard — shared metric card used across dashboard pages.
 * Backward compatible with the existing { label, value, tone } API.
 * tone: "good" | "warn" | "bad" | undefined — colors a status dot next
 * to the value; undefined renders a neutral dot.
 */
export default function KpiCard({ label, value, tone, caption }) {
  return (
    <div className="panel kpi-card">
      <div className="kpi-label">{label}</div>
      <div className={"kpi-value" + (tone ? ` ${tone}` : "")}>{value}</div>
      {caption && <div className="kpi-label" style={{ marginTop: -2 }}>{caption}</div>}
    </div>
  );
}
