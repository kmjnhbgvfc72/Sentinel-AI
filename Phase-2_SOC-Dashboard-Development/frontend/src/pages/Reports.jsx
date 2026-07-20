import { Download, Printer } from "lucide-react";
import { useCallback, useState } from "react";
import RiskChart from "../charts/RiskChart";
import { ErrorState, LoadingState } from "../components/PageState";
import { useApi } from "../hooks/useApi";
import { dashboardApi } from "../services/dashboardApi";
import { formatNumber, titleCase } from "../utils";

export default function Reports() {
  const [period, setPeriod] = useState({ start_date: "", end_date: "" }); const loader = useCallback(() => dashboardApi.report(period), [period]); const state = useApi(loader, [loader]);
  if (state.loading) return <LoadingState label="Preparing security report"/>; if (state.error) return <ErrorState error={state.error} retry={state.retry}/>; const report = state.data.data;
  return <><header className="page-heading print-heading"><div><p className="eyebrow">Security intelligence</p><h2>Security posture report</h2><p>Printable executive overview using the selected reporting period.</p></div><div className="report-actions"><button className="button secondary" onClick={() => window.print()}><Printer/>Print / Save PDF</button><a className="button" href={dashboardApi.exportUrl("threats")}><Download/>Export threat CSV</a></div></header><div className="filters report-filters"><label>Start date<input type="date" value={period.start_date} onChange={(e) => setPeriod((p) => ({ ...p, start_date: e.target.value }))}/></label><label>End date<input type="date" value={period.end_date} min={period.start_date} onChange={(e) => setPeriod((p) => ({ ...p, end_date: e.target.value }))}/></label></div><section className="report-grid"><article className="card report-score"><p className="eyebrow">Current posture</p><strong>{report.posture.risk.score}</strong><span>{titleCase(report.posture.risk.level)} risk</span><p>{report.trends}</p></article><article className="card chart-card"><h3>Threat severity breakdown</h3><RiskChart data={report.severity_breakdown}/></article><article className="card report-stat"><p>Alerts resolved</p><strong>{formatNumber(report.alert_resolution.resolved)}</strong><span>{report.alert_resolution.open} remain open</span></article><article className="card affected-assets"><h3>Most affected assets</h3>{report.most_affected_assets.map((asset) => <div key={asset.id}><span>{asset.name}</span><strong>{asset.open_alerts} alerts</strong></div>)}</article></section></>;
}
