import { TrendingDown, TrendingUp } from "lucide-react";

export default function RiskScore({ score, label, trend = 0, loading = false }) {
  if (loading) return <section className="card risk-card skeleton" aria-busy="true">Loading risk score…</section>;
  if (score === null || score === undefined) return <section className="card risk-card empty-card">Risk score is not available.</section>;
  const safeScore = Math.min(100, Math.max(0, score));
  const TrendIcon = trend <= 0 ? TrendingDown : TrendingUp;
  return <section className="card risk-card" aria-label={`Overall risk score ${safeScore} out of 100, ${label}`}><div className="risk-ring" style={{ "--score": `${safeScore * 3.6}deg` }}><div><strong>{safeScore}</strong><span>/ 100</span></div></div><div><p className="eyebrow">Overall risk</p><h2>{label}</h2><p className={`trend ${trend <= 0 ? "positive" : "negative"}`}><TrendIcon size={16}/>{Math.abs(trend)} points vs previous period</p><p className="muted">Weighted exposure across active threats, alert severity, and affected assets.</p></div></section>;
}
