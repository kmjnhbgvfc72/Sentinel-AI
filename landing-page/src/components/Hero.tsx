import { ArrowDown, ArrowUpRight, Crosshair, Database, Radio, ShieldCheck } from 'lucide-react'
import { LINKS } from '../config/links'

export function Hero() {
  return <section className="hero section" id="platform" aria-labelledby="hero-title">
    <div className="hero__grid container">
      <div className="hero__content">
        <div className="eyebrow"><span /> AI-Powered Cyber Threat Intelligence</div>
        <h1 id="hero-title">Detect threats.<br />Predict attacks.<br /><em>Respond intelligently.</em></h1>
        <p className="hero__lead">An integrated Security Operations Center engineering platform that connects threat intelligence, explainable AI detection, attack-path analysis, incident workflows, and continuous threat hunting.</p>
        <div className="hero__actions">
          <a className="button button--primary" href={LINKS.dashboard} target="_blank" rel="noopener noreferrer">Explore Platform <ArrowUpRight /></a>
          <a className="button button--ghost" href="#workflow">View System Workflow <ArrowDown /></a>
        </div>
        <div className="hero__meta"><span><ShieldCheck /> Defensive by design</span><span><Database /> Phase-owned data</span><span><Radio /> Integrated telemetry</span></div>
      </div>
      <div className="radar-console" aria-label="Illustrative threat radar visualization">
        <div className="radar-console__top"><div><i /> GLOBAL SIGNAL MONITOR</div><span>DEMO VISUAL</span></div>
        <div className="radar">
          <div className="radar__rings" /><div className="radar__crosshair" /><div className="radar__sweep" />
          <span className="radar__node node--one"><i />IOC</span><span className="radar__node node--two"><i />AUTH</span><span className="radar__node node--three"><i />CVE</span>
          <div className="radar__core"><Crosshair /><strong>ANALYZING</strong><small>correlated signals</small></div>
        </div>
        <div className="radar-console__footer"><span><i className="dot dot--cyan"/> Intelligence</span><span><i className="dot dot--violet"/> Detection</span><span><i className="dot dot--blue"/> Prediction</span></div>
      </div>
    </div>
  </section>
}
