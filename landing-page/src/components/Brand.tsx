import { Shield } from 'lucide-react'

export function Brand() {
  return <a className="brand" href="#top" aria-label="AI Cyber Threat Intelligence home">
    <span className="brand__mark"><Shield aria-hidden="true" /></span>
    <span className="brand__copy"><strong>AEGIS<span>INTEL</span></strong><small>AI CYBER THREAT INTELLIGENCE</small></span>
  </a>
}
