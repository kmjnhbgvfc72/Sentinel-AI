from datetime import datetime
from typing import Literal

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, ConfigDict, Field, IPvAnyAddress
from sqlalchemy.orm import Session

from backend.api.auth import current_user
from backend.config import Settings, get_settings
from backend.database import get_db
from backend.models import SecurityLog, User
from backend.services.log_service import LogService, SecurityPipeline

router = APIRouter(prefix="/logs", tags=["Security logs"])
Severity = Literal["low", "medium", "high", "critical"]


class LogCreate(BaseModel):
    event_type: str = Field(min_length=2, max_length=120, pattern=r"^[a-zA-Z0-9_.:\- ]+$")
    username: str | None = Field(default=None, max_length=80)
    source_ip: IPvAnyAddress
    severity: Severity = "medium"
    description: str = Field(default="", max_length=4000)


class LogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    event_type: str
    username: str
    status: str | None
    ip_address: str | None
    user_agent: str | None
    device_information: str | None
    location_information: str | None
    failure_reason: str | None
    created_at: datetime
    source_ip: str
    severity: str
    description: str
    timestamp: datetime


class LogListResponse(BaseModel):
    data: list[LogResponse]
    total: int
    limit: int
    offset: int


class LogCreatedResponse(BaseModel):
    log: LogResponse
    pipeline: dict


@router.get("", response_model=LogListResponse)
def list_logs(
    search: str | None = Query(default=None, max_length=200),
    severity: Severity | None = None,
    event_type: str | None = Query(default=None, max_length=120),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    _: User = Depends(current_user),
    db: Session = Depends(get_db),
) -> LogListResponse:
    rows, total = LogService(db).list(search=search, severity=severity, event_type=event_type, limit=limit, offset=offset)
    return LogListResponse(data=rows, total=total, limit=limit, offset=offset)


@router.post("", response_model=LogCreatedResponse, status_code=status.HTTP_201_CREATED)
async def create_log(
    payload: LogCreate,
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> LogCreatedResponse:
    values = payload.model_dump(mode="json")
    values["username"] = (payload.username or user.username).strip()
    values["source_ip"] = str(payload.source_ip)
    log = LogService(db).create(values)
    pipeline = await SecurityPipeline(settings).process(log)
    return LogCreatedResponse(log=log, pipeline=pipeline)
