import axios from "axios";
const client = axios.create({ baseURL: import.meta.env.VITE_ATTACK_API_BASE_URL || "http://localhost:8003/api", timeout: 10000, headers: { Accept: "application/json" } });
client.interceptors.response.use((response) => response.data, (error) => Promise.reject(new Error(error.response?.data?.error?.message || "Attack path engine is unavailable")));
export const attackApi = { paths: () => client.get("/attack/paths"), graph: () => client.get("/attack/graph"), assets: () => client.get("/risk/assets"), recommendations: () => client.get("/recommendations") };
