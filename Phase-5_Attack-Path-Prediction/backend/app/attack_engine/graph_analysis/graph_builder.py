from .attack_graph import AttackGraph


class GraphBuilder:
    def build(self, event: dict) -> tuple[AttackGraph, list[dict]]:
        graph = AttackGraph()
        edges = []
        source = event.get("source_ip") or event.get("threat_type", "Threat Event")
        user = event.get("user") or "User Account"
        source_asset = event.get("source_asset") or "Web Server"
        target = event.get("target_asset") or "Database Server"
        chain = [(source, user, "observes user account", "indicator"), (user, source_asset, "accesses asset", "user"), (source_asset, target, "connects to", "asset")]
        if event.get("vulnerability"):
            chain.insert(2, (source_asset, event["vulnerability"], "exposes vulnerability", "asset"))
        for left, right, relationship, node_type in chain:
            graph.add_relationship(left, right, relationship, node_type)
            edges.append({"node_type": node_type, "node_value": left, "relationship": relationship, "target_node": right})
        return graph, edges
