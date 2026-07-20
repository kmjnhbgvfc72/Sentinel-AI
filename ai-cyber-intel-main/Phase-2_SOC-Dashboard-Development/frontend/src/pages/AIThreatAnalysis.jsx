import { useCallback, useEffect, useState } from "react";
import { ErrorState, LoadingState } from "../components/PageState";
import SeverityBadge from "../components/SeverityBadge";
import { aiDetectionApi } from "../services/aiDetectionApi";
import { formatDate } from "../utils";

export default function AIThreatAnalysis() {
  const [state, setState] = useState({ loading: true, error: null });
  const load = useCallback(async () => { setState({ loading: true, error: null }); try { const [predictions, risks, alerts] = await Promise.all([aiDetectionApi.predictions(), aiDetectionApi.risks(), aiDetectionApi.alerts()]); setState({ loading: false, error: null, predictions: predictions.data, risks: risks.data, alerts: alerts.data }); } catch (error) { setState({ loading: false, error: error.message }); } }, []);
  useEffect(() => { load(); }, [load]);
  if (state.loading) return <LoadingState label="Loading AI threat analysis"/>;
  if (state.error) return <ErrorState error={state.error} retry={load}/>;
  const latest = state.risks[0]; const confidence = state.predictions[0]?.confidence_score || 0;
  return <><header className="page-heading"><div><p className="eyebrow">Phase 4 detection engine</p><h2>AI Threat Analysis</h2><p>Explainable anomaly detection, threat classification, and security risk prediction.</p></div></header><section className="summary-grid"><article className="summary-card"><div><p>Latest AI risk</p><strong>{latest?.risk_score ?? 0}</strong></div></article><article className="summary-card"><div><p>Threat confidence</p><strong>{confidence.toFixed(1)}%</strong></div></article><article className="summary-card"><div><p>Open AI alerts</p><strong>{state.alerts.filter((item) => item.status !== "resolved").length}</strong></div></article></section><section className="lower-grid"><article className="card"><div className="section-heading"><div><p className="eyebrow">Model output</p><h2>Recent predictions</h2></div></div><div className="asset-list">{state.predictions.map((item) => <div className="asset-row" key={item.id}><div><strong>{item.prediction}</strong><span>{item.event_id} · {formatDate(item.created_at)}</span></div><div className="asset-risk"><strong>{item.confidence_score}%</strong><span>{item.anomaly ? "Anomaly" : "Observed"}</span></div></div>)}</div></article><article className="card"><div className="section-heading"><div><p className="eyebrow">AI queue</p><h2>Generated alerts</h2></div></div><div className="alert-list">{state.alerts.map((item) => <article className="list-row" key={item.id}><div><strong>{item.alert_type}</strong><small>{item.description}</small><small>{formatDate(item.created_at)}</small></div><SeverityBadge severity={item.priority}/></article>)}</div></article></section></>;
}
