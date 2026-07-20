export default function Header() {
  return (
    <header className="topbar">
      <div className="brand">
        <span className="brand-mark" aria-hidden="true">S</span>
        <div>
          <p className="eyebrow">Threat Intelligence Platform</p>
          <h1>Sentinel AI</h1>
        </div>
      </div>
      <div className="analyst-profile">
        <span className="live-indicator" aria-hidden="true" />
        SOC Console Online
      </div>
    </header>
  );
}
