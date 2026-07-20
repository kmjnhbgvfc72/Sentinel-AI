"""Unified advanced threat-hunting façade."""
from .attack_pattern import AttackPatternDetector
from .behavior_analyzer import BehaviorAnalyzer
from .hunting_rules import HuntingRulesEngine
from .ioc_engine import IOCEngine


class ThreatHunter:
    def __init__(self, ioc_engine: IOCEngine, rules: HuntingRulesEngine | None = None) -> None:
        self.iocs, self.rules = ioc_engine, rules or HuntingRulesEngine()
        self.behaviors, self.patterns = BehaviorAnalyzer(), AttackPatternDetector()

    def hunt(self, event: dict[str, object]) -> dict[str, object]:
        behaviors = [str(item) for item in event.get("behaviors", [])]
        return {"event_id": event.get("id"), "ioc_matches": self.iocs.detect(str(event.get("text", ""))), "behavior": self.behaviors.analyze(behaviors), "attack_patterns": self.patterns.detect(behaviors), "rule_matches": self.rules.evaluate(event)}
