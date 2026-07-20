const labels = { critical: "Critical", high: "High", medium: "Medium", low: "Low" };
export default function SeverityBadge({ severity }) { const value = severity?.toLowerCase() || "low"; return <span className={`badge severity-${value}`} aria-label={`Severity: ${labels[value] || value}`}>{labels[value] || value}</span>; }
