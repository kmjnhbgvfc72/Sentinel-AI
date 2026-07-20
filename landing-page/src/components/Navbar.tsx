import { Menu, X } from 'lucide-react'
import { useEffect, useState } from 'react'
import { LINKS } from '../config/links'
import { Brand } from './Brand'

const navigation = [
  ['Platform', '#platform'], ['Features', '#features'], ['Workflow', '#workflow'],
  ['Architecture', '#architecture'], ['About', '#about'],
]

export function Navbar() {
  const [open, setOpen] = useState(false)
  useEffect(() => {
    const close = () => setOpen(false)
    window.addEventListener('resize', close)
    return () => window.removeEventListener('resize', close)
  }, [])
  return <header className="nav-shell">
    <nav className="nav container" aria-label="Primary navigation">
      <Brand />
      <button className="nav__toggle" aria-expanded={open} aria-controls="mobile-navigation" onClick={() => setOpen(!open)}>
        <span className="sr-only">{open ? 'Close menu' : 'Open menu'}</span>{open ? <X /> : <Menu />}
      </button>
      <div id="mobile-navigation" className={`nav__links ${open ? 'is-open' : ''}`}>
        {navigation.map(([label, href]) => <a key={href} href={href} onClick={() => setOpen(false)}>{label}</a>)}
        <a className="button button--small button--primary" href={LINKS.dashboard} target="_blank" rel="noopener noreferrer">Open Dashboard</a>
      </div>
    </nav>
  </header>
}
