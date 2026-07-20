import axios from "axios";

const centralBase = import.meta.env.VITE_CENTRAL_API_BASE_URL;
const api = axios.create({ baseURL: centralBase ? `${centralBase}/phase/2/api` : (import.meta.env.VITE_API_BASE_URL || "/api"), timeout: Number(import.meta.env.VITE_API_TIMEOUT_MS || 10000), headers: { Accept: "application/json" } });

function normalizeError(error) {
  if (error.code === "ECONNABORTED") return new Error("The security service timed out. Please retry.");
  const detail = error.response?.data?.detail || error.response?.data?.error?.message;
  return new Error(typeof detail === "string" ? detail : "Security data is temporarily unavailable.");
}

async function request(config) {
  try { return (await api(config)).data; } catch (error) { throw normalizeError(error); }
}

export const dashboardApi = {
  summary: () => request({ url: "/dashboard/summary" }),
  threatTrends: (range = "24h") => request({ url: "/dashboard/threat-trends", params: { range } }),
  riskDistribution: () => request({ url: "/dashboard/risk-distribution" }),
  recentAlerts: (limit = 5) => request({ url: "/dashboard/recent-alerts", params: { limit } }),
  topAssets: (limit = 5) => request({ url: "/dashboard/top-assets", params: { limit } }),
  threats: (params = {}) => request({ url: "/threats", params }),
  threat: (id) => request({ url: `/threats/${id}` }),
  alerts: (params = {}) => request({ url: "/alerts", params }),
  alert: (id) => request({ url: `/alerts/${id}` }),
  updateAlertStatus: (id, status) => request({ method: "patch", url: `/alerts/${id}/status`, data: { status, changed_by: "soc-analyst" } }),
  assets: (params = {}) => request({ url: "/assets", params }),
  asset: (id) => request({ url: `/assets/${id}` }),
  report: (params = {}) => request({ url: "/reports/security-summary", params }),
  exportUrl: (dataset = "threats") => `${api.defaults.baseURL}/reports/export.csv?dataset=${encodeURIComponent(dataset)}`,
};
