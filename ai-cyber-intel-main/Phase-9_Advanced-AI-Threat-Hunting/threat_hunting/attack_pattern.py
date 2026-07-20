"""Known defensive attack-pattern recognition."""

PATTERNS = {"credential-to-lateral-movement": {"credential_access", "lateral_movement"}, "scripted-persistence": {"powershell_encoded", "persistence_change"}, "covert-command-channel": {"dns_beaconing", "unusual_parent"}}


class AttackPatternDetector:
    def detect(self, behaviors: list[str]) -> list[dict[str, object]]:
        observed = set(behaviors)
        return [{"pattern": name, "coverage": round(len(required & observed) / len(required), 2), "matched": sorted(required & observed)} for name, required in PATTERNS.items() if required <= observed]
