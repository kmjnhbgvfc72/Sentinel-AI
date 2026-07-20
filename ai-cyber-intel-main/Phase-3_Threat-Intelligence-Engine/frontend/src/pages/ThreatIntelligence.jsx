import { useCallback, useEffect, useState } from "react";
import IOCViewer from "../components/IOCViewer";
import LogViewer from "../components/LogViewer";
import ThreatFeed from "../components/ThreatFeed";
import ThreatStatistics from "../components/ThreatStatistics";
import ThreatTimeline from "../components/ThreatTimeline";
import VulnerabilityTable from "../components/VulnerabilityTable";
import { threatApi } from "../services/threatApi";

export default function ThreatIntelligence() { const [state, setState] = useState({ loading: true, error: null }); const load = useCallback(async () => { setState({ loading: true, error: null }); try { const [threats, vulnerabilities, indicators, logs, statistics] = await Promise.all([threatApi.threats(), threatApi.vulnerabilities(), threatApi.indicators(), threatApi.logs(), threatApi.statistics()]); setState({ loading: false, error: null, threats: threats.data, vulnerabilities: vulnerabilities.data, indicators: indicators.data, logs: logs.data, statistics: statistics.data }); } catch (error) { setState({ loading: false, error: error.message }); } }, []); useEffect(() => { load(); }, [load]); return <main className="workspace"><header><div><p className="eyebrow">Sentinel AI · Phase 3</p><h1>Threat Intelligence</h1><p>Normalized and correlated defensive intelligence.</p></div><span className="status">Engine online</span></header>{state.loading ? <div className="state">Loading intelligence…</div> : state.error ? <div className="state error"><strong>Unable to load intelligence</strong><p>{state.error}</p><button onClick={load}>Try again</button></div> : <div className="dashboard-grid"><ThreatStatistics statistics={state.statistics}/><ThreatFeed threats={state.threats}/><VulnerabilityTable vulnerabilities={state.vulnerabilities}/><IOCViewer indicators={state.indicators}/><LogViewer logs={state.logs}/><ThreatTimeline threats={state.threats}/></div>}</main>; }
