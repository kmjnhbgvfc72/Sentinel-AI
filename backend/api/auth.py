from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from backend.config import Settings, get_settings
from backend.database import get_db
from backend.models import SecurityLog, User
from backend.services.auth_service import AuthService, InvalidCredentials
from backend.services.detection_service import SecurityDetectionService
from backend.services.threat_intelligence_service import ThreatIntelligenceService

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
    username = payload.username.strip().lower()
    ip_address = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "")[:512]
    location = request.headers.get(settings.trusted_location_header, "")[:255] or None if settings.trusted_location_header else None
    try:
        token, session, user = AuthService(db, settings.auth_token_ttl_minutes).authenticate(payload.username, payload.password)
    except InvalidCredentials as exc:
        security_log = SecurityLog(
            event_type="LOGIN", username=username, status="FAILED", ip_address=ip_address,
            user_agent=user_agent, device_information=user_agent or None, location_information=location,
            failure_reason=str(exc), source_ip=ip_address,
            severity="medium", description=str(exc),
        )
        db.add(security_log)
        db.commit()
        SecurityDetectionService(db).detect_brute_force(username, ip_address)
        ThreatIntelligenceService(db).analyze_authentication(security_log)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc), headers={"WWW-Authenticate": "Bearer"}) from exc
    security_log = SecurityLog(
        event_type="LOGIN", username=user.username, status="SUCCESS", ip_address=ip_address,
        user_agent=user_agent, device_information=user_agent or None, location_information=location,
        source_ip=ip_address, severity="low", description="Successful login",
    )
    db.add(security_log)
    db.commit()
    ThreatIntelligenceService(db).analyze_authentication(security_log)
    return LoginResponse(access_token=token, expires_at=session.expires_at, user=user)


@router.get("/me", response_model=UserResponse)
def me(user: User = Depends(current_user)) -> User:
    return user


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> None:
    ip_address = request.client.host if request.client else "unknown"
    location = request.headers.get(settings.trusted_location_header, "")[:255] or None if settings.trusted_location_header else None
    AuthService(db, settings.auth_token_ttl_minutes).revoke_token(credentials.credentials)
    db.add(SecurityLog(
        event_type="LOGOUT", username=user.username, status="SUCCESS", ip_address=ip_address,
        user_agent=request.headers.get("user-agent", "")[:512],
        device_information=request.headers.get("user-agent", "")[:512] or None,
        location_information=location, source_ip=ip_address,
        severity="low", description="Successful logout",
    ))
    db.commit()
