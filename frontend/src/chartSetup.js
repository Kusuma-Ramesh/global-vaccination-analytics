import { Chart as ChartJS, registerables } from "chart.js";

ChartJS.register(...registerables);

// Design-system aligned palette — mirrors the CSS custom properties in
// index.css. Chart.js can't read CSS variables directly, so values are
// mirrored here; keep in sync with :root if the token system changes.
export const chartColors = {
  accent: "#2fa79d",
  accentSoft: "rgba(47, 167, 157, 0.16)",
  accentLine: "#4bc0b3",
  good: "#5cb488",
  goodSoft: "rgba(92, 180, 136, 0.16)",
  bad: "#d67d86",
  badSoft: "rgba(214, 125, 134, 0.16)",
  warn: "#d1a052",
  warnSoft: "rgba(209, 160, 82, 0.16)",
  grid: "rgba(233, 238, 250, 0.07)",
  text: "#a6afc4",
  textStrong: "#eef1f7",
};

const fontFamily = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";

export const baseOptions = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: { mode: "index", intersect: false },
  animation: { duration: 260, easing: "easeOutQuart" },
  plugins: {
    legend: {
      labels: {
        color: chartColors.text,
        boxWidth: 10,
        boxHeight: 10,
        usePointStyle: true,
        font: { family: fontFamily, size: 12, weight: "500" },
        padding: 16,
      },
    },
    tooltip: {
      backgroundColor: "#131826",
      titleColor: "#eef1f7",
      bodyColor: "#a6afc4",
      borderColor: "rgba(233, 238, 250, 0.12)",
      borderWidth: 1,
      cornerRadius: 8,
      padding: 10,
      titleFont: { family: fontFamily, size: 12.5, weight: "600" },
      bodyFont: { family: fontFamily, size: 12 },
      boxPadding: 4,
      displayColors: true,
      usePointStyle: true,
    },
  },
  scales: {
    x: {
      ticks: { color: chartColors.text, font: { family: fontFamily, size: 11.5 } },
      grid: { color: chartColors.grid },
      border: { color: "rgba(233, 238, 250, 0.12)" },
    },
    y: {
      ticks: { color: chartColors.text, font: { family: fontFamily, size: 11.5 } },
      grid: { color: chartColors.grid },
      border: { display: false },
    },
  },
};
