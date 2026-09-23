import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

const client = axios.create({ baseURL: BASE_URL });

export const api = {
  getCountries: () => client.get("/countries").then((r) => r.data),
  getRegions: () => client.get("/regions").then((r) => r.data),
  getVaccines: () => client.get("/vaccines").then((r) => r.data),
  getDiseases: () => client.get("/diseases").then((r) => r.data),

  getKpiSummary: (params) => client.get("/analytics/summary", { params }).then((r) => r.data),
  getCorrelation: (params) => client.get("/analytics/correlation", { params }).then((r) => r.data),

  getCoverageTrend: (params) => client.get("/coverage/trend", { params }).then((r) => r.data),
  getCoverageByCountry: (params) => client.get("/coverage/by-country", { params }).then((r) => r.data),
  getDoseDropoff: (params) => client.get("/coverage/dose-dropoff", { params }).then((r) => r.data),

  getIncidenceTrend: (params) => client.get("/incidence/trend", { params }).then((r) => r.data),
  getCasesTrend: (params) => client.get("/cases/trend", { params }).then((r) => r.data),
  getCasesByCountry: (params) => client.get("/cases/by-country", { params }).then((r) => r.data),

  getIntroductionTimeline: (params) => client.get("/vaccine/introduction/timeline", { params }).then((r) => r.data),
  getIntroducibleVaccines: () => client.get("/vaccine/introduction/list").then((r) => r.data),
  getVaccineSchedule: (params) => client.get("/vaccine/schedule", { params }).then((r) => r.data),
};

export default api;
