from datetime import UTC, datetime, timedelta
from typing import Annotated
import hmac
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from config import get_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")
hasher = PasswordHasher()


class Principal(BaseModel):
    username: str
    roles: list[str]


def hash_password(password: str) -> str:
    return hasher.hash(password)


def verify_password(password: str, encoded: str) -> bool:
    if not encoded:
        return False
    try:
        return hasher.verify(encoded, password)
    except VerifyMismatchError:
        return False


def create_access_token(username: str, roles: list[str]) -> str:
    settings = get_settings()
    now = datetime.now(UTC)
    claims = {"sub": username, "roles": roles, "iat": now, "exp": now + timedelta(minutes=settings.access_token_minutes), "iss": "ai-soc", "aud": "ai-soc-api"}
    return jwt.encode(claims, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def authenticate_admin(username: str, password: str) -> Principal | None:
    settings = get_settings()
    valid_user = hmac.compare_digest(username.encode(), settings.admin_username.encode())
    valid_password = verify_password(password, settings.admin_password_hash)
    return Principal(username=username, roles=["admin", "analyst", "responder", "viewer"]) if valid_user and valid_password else None


async def current_principal(token: Annotated[str, Depends(oauth2_scheme)]) -> Principal:
    settings = get_settings()
    try:
        claims = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm], audience="ai-soc-api", issuer="ai-soc")
        return Principal(username=claims["sub"], roles=claims.get("roles", []))
    except (jwt.PyJWTError, KeyError) as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token", headers={"WWW-Authenticate": "Bearer"}) from exc

