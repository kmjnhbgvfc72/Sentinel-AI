"""Asset risk forecasting."""


class RiskForecaster:
    def forecast(self, assets: list[dict[str, object]]) -> dict[str, object]:
        results = []
        for asset in assets:
            likelihood = min(1.0, max(0.0, float(asset.get("likelihood", 0))))
            impact = min(10.0, max(0.0, float(asset.get("impact", 0))))
            control = min(1.0, max(0.0, float(asset.get("control_effectiveness", 0))))
            risk = round(likelihood * impact * (1 - control) * 10, 2)
            results.append({"asset": asset.get("asset"), "risk_score": risk, "band": "critical" if risk >= 75 else "high" if risk >= 50 else "medium" if risk >= 25 else "low"})
        return {"assets": sorted(results, key=lambda item: item["risk_score"], reverse=True), "aggregate_risk": round(sum(i["risk_score"] for i in results) / len(results), 2) if results else 0.0}
