"""Prioritized defensive recommendations."""


class RecommendationEngine:
    def recommend(self, risk: dict[str, object]) -> list[dict[str, object]]:
        recommendations = []
        mappings = {"credential_access": ("Reset affected credentials and enforce phishing-resistant MFA", 95), "lateral_movement": ("Isolate the host and restrict east-west traffic", 90), "vulnerable_public_asset": ("Patch or remove the public exposure", 88), "dns_beaconing": ("Block the domain and inspect DNS telemetry", 85)}
        for driver in risk.get("drivers", []):
            if driver in mappings:
                action, priority = mappings[driver]
                recommendations.append({"driver": driver, "action": action, "priority": priority, "requires_approval": True})
        return sorted(recommendations, key=lambda item: item["priority"], reverse=True)
