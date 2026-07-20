ROLES = {
    "Admin": {"*"},
    "SOC Analyst": {"incidents:write", "playbooks:execute"},
    "Viewer": {"incidents:read"},
}
