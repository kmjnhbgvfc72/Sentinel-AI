"""Small offline MITRE ATT&CK mapping; production adapters may sync STIX data."""
MAPPINGS = {"powershell": ("T1059.001", "PowerShell"), "credential_dumping": ("T1003", "OS Credential Dumping"), "phishing": ("T1566", "Phishing"), "scheduled_task": ("T1053", "Scheduled Task/Job"), "dns_tunneling": ("T1071.004", "DNS")}


class MitreMapper:
    def map(self, behaviors: list[str]) -> list[dict[str, str]]:
        return [{"behavior": behavior, "technique_id": MAPPINGS[behavior][0], "technique": MAPPINGS[behavior][1]} for behavior in behaviors if behavior in MAPPINGS]
