import { useEffect, useState } from 'react'
import { Download, FileBarChart, FileText, ShieldCheck } from 'lucide-react'
import { reportsApi, unwrapList } from '../api/api'
import { PageHeader } from './Threats'

export default function Reports() {
  const [reports, setReports] = useState([])
  useEffect(() => { reportsApi.list().then(data => setReports(unwrapList(data, ['reports']))).catch(() => {}) }, [])
  const fallback = [{ title: 'Daily Threat Report', type: 'Daily intelligence', icon: FileBarChart }, { title: 'Attack Summary', type: 'Threat analysis', icon: ShieldCheck }, { title: 'Risk Analysis', type: 'AI analytics', icon: FileText }, { title: 'Incident Report', type: 'SOAR operations', icon: FileText }]
  const rows = reports.length ? reports : fallback
  return <div className="page"><PageHeader eyebrow="AI security reporting" title="Reports & Intelligence Briefings" text="Cross-phase reporting for analysts, leadership, compliance, and incident review." /><section className="report-analytics panel"><div><span>Threat coverage</span><strong>9 phases</strong><i style={{width:'92%'}}/></div><div><span>Detection confidence</span><strong>87%</strong><i style={{width:'87%'}}/></div><div><span>Response readiness</span><strong>100%</strong><i style={{width:'100%'}}/></div></section><section className="report-grid">{rows.map((report, i) => { const Icon = report.icon || FileText; return <article className="panel report-card" key={report.id || i}><div className="report-icon"><Icon /></div><span>{report.type || report.report_type || 'Security report'}</span><h2>{report.title || report.name}</h2><p>{report.description || 'Consolidated charts, statistics, and findings from the central threat intelligence pipeline.'}</p><div className="report-spark">{[35,62,48,78,57,86,72].map((height,j)=><i style={{height:`${height}%`}} key={j}/>)}</div><button className="button secondary" disabled={!report.download_url}><Download size={16}/>Generate report</button></article> })}</section></div>
}
