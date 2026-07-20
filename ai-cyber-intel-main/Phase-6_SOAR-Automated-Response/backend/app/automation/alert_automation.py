def classify_alert(title: str, severity: str) -> str:
    return (
        "Critical Vulnerability Triage"
        if "vulnerability" in title.lower() or severity == "critical"
        else "Suspicious Login Response"
    )
