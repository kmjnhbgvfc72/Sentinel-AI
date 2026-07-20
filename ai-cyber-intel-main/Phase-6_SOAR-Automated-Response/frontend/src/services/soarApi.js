import axios from "axios";
const api=axios.create({baseURL:import.meta.env.VITE_SOAR_API_BASE_URL||"http://localhost:8004/api"});
export const getIncidents=()=>api.get("/incidents").then(r=>r.data); export const createIncident=(data)=>api.post("/incidents",data).then(r=>r.data); export const getPlaybooks=()=>api.get("/playbooks").then(r=>r.data); export const getWorkflows=()=>api.get("/playbooks/workflows").then(r=>r.data); export const getReports=()=>api.get("/reports").then(r=>r.data); export default api;
