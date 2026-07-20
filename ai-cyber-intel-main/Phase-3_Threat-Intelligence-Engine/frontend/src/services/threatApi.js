import axios from "axios";
const client = axios.create({ baseURL: import.meta.env.VITE_API_BASE_URL || "/api", timeout: 10000, headers: { Accept: "application/json" } });
client.interceptors.response.use((response) => response.data, (error) => Promise.reject(new Error(error.response?.data?.error?.message || "Threat intelligence service is unavailable")));
export const threatApi = { threats: () => client.get("/threats"), vulnerabilities: () => client.get("/vulnerabilities"), indicators: () => client.get("/indicators"), logs: () => client.get("/logs"), statistics: () => client.get("/threat-statistics") };
