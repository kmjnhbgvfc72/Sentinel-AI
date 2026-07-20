import {
  Activity, BellRing, Binary, Bot, BrainCircuit, ChartNoAxesCombined, CircleGauge,
  Database, FileChartColumn, GitBranch, Network, Radar, RefreshCw, ScanSearch,
  ServerCog, ShieldCheck, Siren, Waypoints,
} from 'lucide-react'

export const trustPoints = [
  'Real-time monitoring', 'AI-powered detection', 'Threat intelligence',
  'Attack-path prediction', 'Automated response', 'Continuous learning',
]

export const problems = [
  { title: 'Alert overload', text: 'High-volume security signals make it difficult to distinguish urgent evidence from routine noise.', icon: BellRing },
  { title: 'Fragmented context', text: 'Threats, indicators, vulnerabilities, assets, and incidents often live in disconnected tools.', icon: Network },
  { title: 'Slow investigation', text: 'Manual correlation delays the analyst path from initial signal to an explainable decision.', icon: ScanSearch },
  { title: 'Unknown progression', text: 'A detection alone does not show how risk could move through relationships and monitored assets.', icon: GitBranch },
  { title: 'Delayed response', text: 'Disconnected workflows add time between prioritization, incident creation, and a controlled response.', icon: Siren },
]

export const capabilities = [
  { title: 'Unified SOC dashboard', text: 'A responsive command view for risk, alerts, threats, assets, and cross-phase operational context.', icon: CircleGauge, phase: 'Phase 2' },
  { title: 'Security monitoring', text: 'Central health, security-log visibility, alert tracking, and phase-aware system status.', icon: Activity, phase: 'Phases 1, 2 & 8' },
  { title: 'Threat intelligence', text: 'Normalized IOCs, vulnerabilities, feed health, reputation context, and exact-match correlation.', icon: Radar, phase: 'Phases 3 & 7' },
  { title: 'AI threat detection', text: 'Feature extraction, anomaly analysis, bounded risk scoring, classification, and explainable alerts.', icon: BrainCircuit, phase: 'Phase 4' },
  { title: 'Attack-path prediction', text: 'Defensive graph analysis connecting detections to possible paths, assets, and recommendations.', icon: Waypoints, phase: 'Phase 5' },
  { title: 'SOAR response', text: 'Incident tracking, playbooks, response recommendations, notifications, reporting, and audit workflows.', icon: Bot, phase: 'Phase 6' },
  { title: 'Advanced threat hunting', text: 'Behavior, IOC, pattern, and rule-based hunting with approval-aware security automation.', icon: ScanSearch, phase: 'Phase 9' },
  { title: 'Assets and exposure', text: 'Monitored system context and risk visibility support investigation and attack-path analysis.', icon: ServerCog, phase: 'Phases 2 & 5' },
  { title: 'Reporting and analytics', text: 'Security summaries, trends, statistics, charts, exports, and executive dashboard views.', icon: FileChartColumn, phase: 'Phases 2, 6 & 9' },
]

export const workflow = [
  { number: '01', title: 'Collect', text: 'Approved intelligence, IOCs, vulnerabilities, sanitized logs, and monitored security events.', icon: Database },
  { number: '02', title: 'Normalize', text: 'Validate and structure evidence into consistent, bounded defensive inputs.', icon: Binary },
  { number: '03', title: 'Detect', text: 'Analyze behavior, classify patterns, and identify explainable anomalies.', icon: BrainCircuit },
  { number: '04', title: 'Prioritize', text: 'Calculate risk, confidence, and severity to focus analyst attention.', icon: ChartNoAxesCombined },
  { number: '05', title: 'Predict', text: 'Map possible attack relationships, exposed assets, and recommended actions.', icon: GitBranch },
  { number: '06', title: 'Investigate', text: 'Bring evidence, detections, paths, and intelligence into the SOC workflow.', icon: ScanSearch },
  { number: '07', title: 'Respond', text: 'Track incidents and execute approved manual or automated playbook steps.', icon: ShieldCheck },
  { number: '08', title: 'Learn', text: 'Feed analyst outcomes into hunting, analytics, and controlled model improvement.', icon: RefreshCw },
]

export const technologies = [
  { name: 'React 19', group: 'Interface', detail: 'SOC and module interfaces' },
  { name: 'Vite', group: 'Interface', detail: 'Frontend development and builds' },
  { name: 'JavaScript', group: 'Interface', detail: 'Existing platform interface logic' },
  { name: 'Python', group: 'Backend', detail: 'Security services and AI modules' },
  { name: 'FastAPI', group: 'Backend', detail: 'Versioned REST APIs and gateway' },
  { name: 'SQLAlchemy', group: 'Data', detail: 'Repository and persistence layer' },
  { name: 'PostgreSQL', group: 'Data', detail: 'Central and phase-owned persistence' },
  { name: 'Docker Compose', group: 'Operations', detail: 'Reproducible service deployment' },
  { name: 'Prometheus', group: 'Operations', detail: 'Metrics in the deployment phase' },
  { name: 'Grafana', group: 'Operations', detail: 'Operational monitoring dashboards' },
]
