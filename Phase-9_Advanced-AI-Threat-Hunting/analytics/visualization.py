"""React-friendly visualization specifications."""


def chart_spec(title: str, data: list[dict[str, object]], x: str, y: str) -> dict[str, object]:
    return {"type": "line", "title": title, "data": data, "encoding": {"x": {"field": x, "type": "temporal"}, "y": {"field": y, "type": "quantitative"}}}
