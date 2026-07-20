"""Executive dashboard aggregation."""


class ExecutiveDashboard:
    def build(self, statistics: dict[str, object], risk: float, incidents: list[dict[str, object]]) -> dict[str, object]:
        open_incidents = sum(item.get("status") != "closed" for item in incidents)
        return {"kpis": {"detections": statistics.get("total", 0), "aggregate_risk": risk, "open_incidents": open_incidents, "precision": statistics.get("precision")}, "risk_posture": "critical" if risk >= 75 else "elevated" if risk >= 40 else "guarded"}
