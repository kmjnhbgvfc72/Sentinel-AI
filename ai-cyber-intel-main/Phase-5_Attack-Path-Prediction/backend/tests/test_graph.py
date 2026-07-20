from app.attack_engine.graph_analysis import GraphBuilder
from app.attack_engine.risk_engine import AssetRiskEngine


def test_graph_builds_expected_relationship_chain():
    graph, edges = GraphBuilder().build({"source_ip": "198.51.100.42", "user": "admin", "source_asset": "Web Server", "target_asset": "Database Server", "vulnerability": "CVE-2026-41001"})
    assert graph.paths("198.51.100.42", "Database Server")
    assert any(edge["relationship"] == "exposes vulnerability" for edge in edges)


def test_asset_risk_is_bounded_and_critical():
    asset = AssetRiskEngine().calculate({"risk_score": 95, "criticality": 95, "historical_incidents": 3, "vulnerability_severity": "critical"}, ["Database Server"])[0]
    assert asset["risk_score"] <= 100
    assert asset["severity"] == "critical"
