import React from "react"; import {createRoot} from "react-dom/client"; import SOARDashboard from "./dashboard/SOARDashboard"; import "./styles.css";
createRoot(document.getElementById("root")).render(<React.StrictMode><SOARDashboard/></React.StrictMode>);
