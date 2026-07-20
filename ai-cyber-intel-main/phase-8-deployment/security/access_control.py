from collections.abc import Callable
from fastapi import Depends, HTTPException, status
from security.authentication import Principal, current_principal

ROLE_PERMISSIONS = {
    "viewer": {"threat:read", "alert:read", "health:read"},
    "analyst": {"threat:read", "alert:read", "alert:write", "prediction:run", "health:read"},
    "responder": {"threat:read", "alert:read", "response:execute", "incident:write", "health:read"},
    "admin": {"*"},
}


def require_permission(permission: str) -> Callable:
    async def dependency(principal: Principal = Depends(current_principal)) -> Principal:
        permissions = set().union(*(ROLE_PERMISSIONS.get(role, set()) for role in principal.roles))
        if "*" not in permissions and permission not in permissions:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permission")
        return principal
    return dependency

