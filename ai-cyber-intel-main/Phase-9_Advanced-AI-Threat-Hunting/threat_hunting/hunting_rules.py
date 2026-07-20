"""Declarative hunting-rule engine."""
from dataclasses import dataclass


@dataclass(frozen=True)
class HuntingRule:
    id: str
    field: str
    operator: str
    value: object
    severity: str = "medium"


class HuntingRulesEngine:
    def __init__(self) -> None:
        self.rules: dict[str, HuntingRule] = {}

    def add(self, rule: HuntingRule) -> None:
        if rule.operator not in {"equals", "contains", "gte"}:
            raise ValueError("unsupported rule operator")
        self.rules[rule.id] = rule

    def evaluate(self, event: dict[str, object]) -> list[dict[str, str]]:
        matches = []
        for rule in self.rules.values():
            actual = event.get(rule.field)
            hit = actual == rule.value if rule.operator == "equals" else str(rule.value).lower() in str(actual).lower() if rule.operator == "contains" else float(actual or 0) >= float(rule.value)
            if hit:
                matches.append({"rule_id": rule.id, "severity": rule.severity})
        return matches
