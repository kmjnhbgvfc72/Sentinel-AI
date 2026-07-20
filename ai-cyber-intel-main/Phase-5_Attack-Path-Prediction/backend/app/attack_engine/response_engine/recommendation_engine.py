class RecommendationEngine:
    def generate(self, event: dict, assets: list[dict]) -> list[dict]:
        recommendations = [
            ("Review account and authentication activity", "high"),
            ("Monitor affected assets and preserve relevant telemetry", "high"),
        ]
        if event.get("vulnerability"):
            recommendations.append((f"Apply approved security updates for {event['vulnerability']}", "critical" if event.get("vulnerability_severity") == "critical" else "high"))
        if event.get("source_ip"):
            recommendations.append(("Validate the indicator with approved reputation sources and tune defensive controls", "medium"))
        return [{"threat_id": event["event_id"], "recommendation": text, "priority": priority, "status": "open"} for text, priority in recommendations]
