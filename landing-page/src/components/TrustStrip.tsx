import { Check } from 'lucide-react'
import { trustPoints } from '../data/project'

export function TrustStrip() { return <section className="trust-strip" aria-label="Platform capabilities"><div className="container trust-strip__inner">{trustPoints.map(point => <span key={point}><Check />{point}</span>)}</div></section> }
