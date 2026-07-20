"""CVE normalization and prioritization."""
import re


class CVEManager:
    def process(self, record: dict[str, object]) -> dict[str, object]:
        cve_id = str(record.get("id", "")).upper()
        if not re.fullmatch(r"CVE-\d{4}-\d{4,}", cve_id):
            raise ValueError("invalid CVE identifier")
        cvss = max(0.0, min(10.0, float(record.get("cvss", 0))))
        exploited = bool(record.get("known_exploited", False))
        priority = "critical" if exploited or cvss >= 9 else "high" if cvss >= 7 else "medium" if cvss >= 4 else "low"
        return {**record, "id": cve_id, "cvss": cvss, "priority": priority}
