import { problems } from '../data/project'

export function Problem() {
  return <section className="section problem" aria-labelledby="problem-title"><div className="container"><div className="section-heading section-heading--split"><div><span className="kicker">THE OPERATIONAL GAP</span><h2 id="problem-title">Security teams have signals.<br/>They need <em>connected context.</em></h2></div><p>Modern defensive operations become slower when evidence, risk, and response live in separate workflows. The platform is engineered around that integration problem.</p></div><div className="problem__grid">{problems.map(({ title, text, icon: Icon }, index) => <article className="problem-card" key={title}><span className="problem-card__number">0{index + 1}</span><Icon/><h3>{title}</h3><p>{text}</p></article>)}</div></div></section>
}
