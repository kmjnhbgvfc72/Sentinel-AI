import axios from "axios";
const client = axios.create({ baseURL: import.meta.env.VITE_AI_API_BASE_URL || "http://localhost:8002/api", timeout: 10000, headers: { Accept: "application/json" } });
client.interceptors.response.use((response) => response.data, (error) => Promise.reject(new Error(error.response?.data?.error?.message || "AI detection service is unavailable")));
export const aiApi = { analyze: (event) => client.post("/ai/analyze", event), predictions: () => client.get("/ai/predictions"), risks: () => client.get("/ai/risk-score"), alerts: () => client.get("/ai/alerts") };
