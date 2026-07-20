from dataclasses import dataclass

from backend.config import Settings


@dataclass(frozen=True)
class PhaseDefinition:
    number: int
    name: str
    role: str
    base_url: str
    health_path: str


def build_registry(settings: Settings) -> dict[int, PhaseDefinition]:
    return {
        1: PhaseDefinition(1, "Project Foundation", "foundation", settings.phase1_url, "/api/v1/health"),
        2: PhaseDefinition(2, "SOC Dashboard", "soc", settings.phase2_url, "/health"),
        3: PhaseDefinition(3, "Threat Intelligence Engine", "intelligence", settings.phase3_url, "/health"),
        4: PhaseDefinition(4, "AI Threat Detection", "detection", settings.phase4_url, "/health"),
        5: PhaseDefinition(5, "Attack Path Prediction", "prediction", settings.phase5_url, "/health"),
        6: PhaseDefinition(6, "SOAR Automated Response", "response", settings.phase6_url, "/health"),
        7: PhaseDefinition(7, "External Intelligence", "external-intelligence", settings.phase7_url, "/health"),
        8: PhaseDefinition(8, "Deployment and Monitoring", "operations", settings.phase8_url, "/health/ready"),
        9: PhaseDefinition(9, "Advanced Threat Hunting", "hunting", settings.phase9_url, "/health"),
    }
