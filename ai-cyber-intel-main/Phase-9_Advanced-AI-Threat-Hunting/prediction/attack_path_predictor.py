"""Graph-based likely attack-path discovery."""
from collections import deque


class AttackPathPredictor:
    def predict(self, edges: list[dict[str, object]], start: str, targets: list[str], max_depth: int = 6) -> list[dict[str, object]]:
        graph: dict[str, list[tuple[str, float]]] = {}
        for edge in edges:
            graph.setdefault(str(edge["source"]), []).append((str(edge["target"]), float(edge.get("probability", 0.5))))
        queue = deque([(start, [start], 1.0)])
        paths = []
        while queue:
            node, path, probability = queue.popleft()
            if node in targets and node != start:
                paths.append({"path": path, "probability": round(probability, 4)})
                continue
            if len(path) > max_depth:
                continue
            for neighbor, edge_probability in graph.get(node, []):
                if neighbor not in path:
                    queue.append((neighbor, path + [neighbor], probability * edge_probability))
        return sorted(paths, key=lambda item: item["probability"], reverse=True)[:10]
