import { lazy, Suspense, useState } from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import { LoadingState } from "./components/PageState";
import Sidebar from "./components/Sidebar";

const Alerts = lazy(() => import("./pages/Alerts"));
const Assets = lazy(() => import("./pages/Assets"));
const Dashboard = lazy(() => import("./pages/Dashboard"));
const Reports = lazy(() => import("./pages/Reports"));
const Threats = lazy(() => import("./pages/Threats"));
const ThreatIntelligence = lazy(() => import("./pages/ThreatIntelligence"));
const AIThreatAnalysis = lazy(() => import("./pages/AIThreatAnalysis"));
const AttackAnalysis = lazy(() => import("./pages/AttackAnalysis"));

export default function App() {
  const [collapsed, setCollapsed] = useState(false); const [mobileOpen, setMobileOpen] = useState(false); const [timeRange, setTimeRange] = useState("24h");
  return <div className={`app-shell ${collapsed ? "sidebar-collapsed" : ""}`}><Sidebar {...{ collapsed, setCollapsed, mobileOpen, setMobileOpen }}/><div className="workspace"><Navbar onMenu={() => setMobileOpen(true)} {...{ timeRange, setTimeRange }}/><main className="page-content"><Suspense fallback={<LoadingState label="Loading workspace"/>}><Routes><Route path="/" element={<Dashboard timeRange={timeRange}/>}/><Route path="/threats" element={<Threats/>}/><Route path="/intelligence" element={<ThreatIntelligence/>}/><Route path="/ai-analysis" element={<AIThreatAnalysis/>}/><Route path="/attack-analysis" element={<AttackAnalysis/>}/><Route path="/alerts" element={<Alerts/>}/><Route path="/assets" element={<Assets/>}/><Route path="/reports" element={<Reports/>}/><Route path="/settings" element={<section className="card empty-card"><h2>Settings</h2><p>Platform configuration will be delivered with identity and role controls in a future phase.</p></section>}/><Route path="*" element={<Navigate to="/" replace/>}/></Routes></Suspense></main></div></div>;
}
