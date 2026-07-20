from fastapi import HTTPException


def require_role(role: str, allowed: set[str]):
    if role not in allowed:
        raise HTTPException(403, "Insufficient permissions")
