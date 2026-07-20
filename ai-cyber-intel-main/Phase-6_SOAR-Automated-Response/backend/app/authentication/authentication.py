from fastapi import Header, HTTPException
from config.soar_settings import get_settings


def current_user(authorization: str | None = Header(default=None)) -> str:
    if not authorization:
        return "system"
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or token != get_settings().admin_token:
        raise HTTPException(401, "Invalid authentication token")
    return "admin"
