from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.threat_intelligence.models import ActivityLog, Indicator, Malware, Threat, Vulnerability


def seed_demo_data(session: Session) -> None:
    if session.scalar(select(func.count()).select_from(Threat)):
        return
    now = datetime.now(UTC)
    session.add_all([
        Threat(name="Suspicious IP with repeated authentication failures", type="correlated activity", description="Reputation, authentication telemetry, and vulnerability exposure were correlated.", severity="critical", risk_score=92, confidence_score=91, source="Phase 3 correlator", created_at=now),
        Threat(name="Newly observed command-and-control domain", type="domain indicator", description="An approved reputation feed identified suspicious infrastructure.", severity="high", risk_score=78, confidence_score=84, source="Curated IOC feed", created_at=now - timedelta(hours=3)),
        Threat(name="Authentication anomaly under review", type="authentication anomaly", description="Failures exceeded the approved adaptive threshold.", severity="medium", risk_score=58, confidence_score=73, source="Authentication logs", created_at=now - timedelta(hours=8)),
        Vulnerability(cve_id="CVE-2026-41001", description="Sample critical vulnerability for the defensive intelligence workflow.", severity="critical", cvss_score=9.8, risk_level="critical", affected_products=["Example Gateway 4.x"], published_at=now - timedelta(days=1)),
        Vulnerability(cve_id="CVE-2026-41002", description="Sample high severity managed component vulnerability.", severity="high", cvss_score=8.1, risk_level="high", affected_products=["Example Framework 8.x"], published_at=now - timedelta(days=2)),
        Indicator(indicator_type="ip", value="198.51.100.42", confidence_score=90, reputation_score=92, threat_category="command-and-control", country="ZZ", status="malicious", last_seen_at=now),
        Indicator(indicator_type="domain", value="suspicious-example.test", confidence_score=82, reputation_score=86, threat_category="phishing infrastructure", status="malicious", last_seen_at=now - timedelta(hours=2)),
        Indicator(indicator_type="sha256", value="a" * 64, confidence_score=76, reputation_score=74, threat_category="malware artifact", status="suspicious", last_seen_at=now - timedelta(hours=5)),
        Malware(hash="a" * 64, hash_type="sha256", family="ExampleFamily", severity="high", detection_date=now - timedelta(hours=5)),
        ActivityLog(user_id="service-portal", event_type="multiple_failed_logins", ip_address="198.51.100.42", device="unknown-browser", status="failed", risk_level="critical", risk_score=90, details={"log_type": "authentication", "failed_login_count": 10}, created_at=now - timedelta(minutes=9)),
        ActivityLog(user_id="analyst-104", event_type="successful_login", ip_address="192.0.2.15", device="managed-workstation", status="success", risk_level="low", risk_score=5, details={"log_type": "authentication"}, created_at=now - timedelta(minutes=18)),
    ])
    session.commit()
