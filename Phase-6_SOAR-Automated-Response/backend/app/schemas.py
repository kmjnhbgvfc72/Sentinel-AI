from datetime import datetime
from pydantic import BaseModel, Field


class IncidentCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = ""
    severity: str = "medium"
    source: str = "manual"
    assignee: str | None = None


class IncidentUpdate(BaseModel):
    status: str | None = None
    severity: str | None = None
    assignee: str | None = None


class IncidentOut(IncidentCreate):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class AnalyzeRequest(BaseModel):
    title: str = Field(min_length=3)
    severity: str = "medium"
    source: str = "phase4"
    description: str = ""


class NotificationRequest(BaseModel):
    channel: str = "webhook"
    recipient: str = Field(min_length=1)
    subject: str = Field(min_length=1)
