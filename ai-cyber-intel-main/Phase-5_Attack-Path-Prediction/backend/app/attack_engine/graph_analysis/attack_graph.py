import networkx as nx


class AttackGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_relationship(self, source: str, destination: str, relationship: str, node_type: str = "entity") -> None:
        self.graph.add_node(source, node_type=node_type)
        self.graph.add_node(destination, node_type="asset")
        self.graph.add_edge(source, destination, relationship=relationship)

    def paths(self, source: str, destination: str, cutoff: int = 6) -> list[list[str]]:
        if source not in self.graph or destination not in self.graph:
            return []
        return list(nx.all_simple_paths(self.graph, source, destination, cutoff=cutoff))
