from app.attack_engine.utils.graph_helpers import clamp, risk_level


class AssetRiskEngine:
    def calculate(self, event: dict, asset_names: list[str]) -> list[dict]:
        score = clamp(event.get("risk_score", 0) * 0.45 + event.get("criticality", 50) * 0.3 + min(event.get("historical_incidents", 0) * 5, 100) * 0.15 + (15 if event.get("vulnerability_severity") in {"high", "critical"} else 0))
        return [{"asset_name": name, "asset_type": "database" if "data" in name.lower() or "database" in name.lower() else "server", "criticality": event.get("criticality", 50), "risk_score": score, "severity": risk_level(score)} for name in asset_names]
