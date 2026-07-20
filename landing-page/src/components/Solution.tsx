import { ArrowRight, Braces, BrainCircuit, GitBranch, ShieldCheck } from 'lucide-react'

const stages = [
  { icon: Braces, label: 'Collect & normalize', note: 'Signals become structured evidence' },
  { icon: BrainCircuit, label: 'Analyze & prioritize', note: 'AI results remain bounded and explainable' },
  { icon: GitBranch, label: 'Predict progression', note: 'Graph context exposes possible paths' },
  { icon: ShieldCheck, label: 'Investigate & respond', note: 'Analysts retain visibility and control' },
]

export function Solution() { return <section className="section solution" aria-labelledby="solution-title"><div className="container solution__frame"><div className="section-heading"><span className="kicker">ONE DEFENSIVE PIPELINE</span><h2 id="solution-title">From raw security event to<br/><em>an informed response.</em></h2><p>The system composes independently runnable phases through a central API gateway. It correlates defensive data without collapsing domain ownership, then gives analysts one place to understand priority and act.</p></div><div className="solution__flow">{stages.map(({ icon: Icon, label, note }, index) => <div className="solution-stage" key={label}><div className="solution-stage__icon"><Icon/></div><div><strong>{label}</strong><small>{note}</small></div>{index < stages.length - 1 && <ArrowRight className="solution-stage__arrow"/>}</div>)}</div></div></section> }
