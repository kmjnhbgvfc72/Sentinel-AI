from typing import Any

SEVERITY_BY_SCORE = [(9, "critical"), (7, "high"), (4, "medium"), (0, "low")]


def parse_cve(raw: dict[str, Any]) -> dict[str, Any]:
    cve = raw.get("cve", raw)
    metrics = cve.get("metrics", {})
    groups = metrics.get("cvssMetricV31") or metrics.get("cvssMetricV30") or metrics.get("cvssMetricV2") or []
    score = float(groups[0].get("cvssData", {}).get("baseScore", 0)) if groups else 0.0
    severity = next(label for minimum, label in SEVERITY_BY_SCORE if score >= minimum)
    description = next((item["value"] for item in cve.get("descriptions", []) if item.get("lang") == "en"), "No description supplied")
    products = []
    for config in cve.get("configurations", []):
        for node in config.get("nodes", []):
            products.extend(match.get("criteria", "") for match in node.get("cpeMatch", []) if match.get("vulnerable"))
    return {"cve_id": cve["id"], "description": description, "severity": severity, "cvss_score": score, "risk_level": severity, "affected_products": products[:50], "published_at": cve.get("published")}
