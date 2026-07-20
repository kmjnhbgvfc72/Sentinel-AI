from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from backend.config import Settings, get_settings
from backend.database import get_db
from backend.models import User
from backend.services.auth_service import AuthService, InvalidCredentials
from backend.services.notification_service import NotificationService

router = APIRouter(prefix="/auth", tags=["Authentication"])
bearer = HTTPBearer(auto_error=False)


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=80)
    password: str = Field(min_length=1, max_length=1024)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: str
    role: str
    created_at: datetime


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime
    user: UserResponse


def current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> User:
    user = AuthService(db, settings.auth_token_ttl_minutes).user_for_token(credentials.credentials) if credentials else None
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required", headers={"WWW-Authenticate": "Bearer"})
    return user


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, request: Request, db: Session = Depends(get_db), settings: Settings = Depends(get_settings)) -> LoginResponse:
    try:
        token, session, user = AuthService(db, settings.auth_token_ttl_minutes).authenticate(payload.username, payload.password)
    except InvalidCredentials as exc:
        NotificationService(db).create(title="Failed Login Attempt", message=f"Authentication was rejected for {payload.username.strip() or 'unknown user'}.", notification_type="failed_login", severity="medium", related_user=payload.username.strip() or None, ip_address=request.client.host if request.client else None)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc), headers={"WWW-Authenticate": "Bearer"}) from exc
    return LoginResponse(access_token=token, expires_at=session.expires_at, user=user)


@router.get("/me", response_model=UserResponse)
def me(user: User = Depends(current_user)) -> User:
    return user
