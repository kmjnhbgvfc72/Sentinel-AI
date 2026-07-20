from dataclasses import dataclass


@dataclass(frozen=True)
class SecurityService:
    """Foundation for centralized validation and risk-scoring policies."""

    allowed_severities: tuple[str, ...] = ("low", "medium", "high", "critical")

    def normalize_severity(self, severity: str) -> str:
        normalized = severity.strip().lower()
        if normalized not in self.allowed_severities:
            raise ValueError("Unsupported threat severity")
        return normalized
