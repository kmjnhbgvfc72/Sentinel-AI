import axios from "axios";

const centralBase = import.meta.env.VITE_CENTRAL_API_BASE_URL;
const client = axios.create({ baseURL: centralBase ? `${centralBase}/phase/3/api` : (import.meta.env.VITE_THREAT_API_BASE_URL || "http://localhost:8001/api"), timeout: Number(import.meta.env.VITE_API_TIMEOUT_MS || 10000), headers: { Accept: "application/json" } });
client.interceptors.response.use((response) => response.data, (error) => Promise.reject(new Error(error.response?.data?.error?.message || "Threat intelligence engine is unavailable")));

export const threatIntelligenceApi = {
  threats: () => client.get("/threats", { params: { page_size: 8 } }),
  vulnerabilities: () => client.get("/vulnerabilities", { params: { page_size: 8 } }),
  indicators: () => client.get("/indicators", { params: { page_size: 8 } }),
  logs: () => client.get("/logs", { params: { page_size: 8 } }),
  statistics: () => client.get("/threat-statistics"),
};
