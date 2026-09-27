import uuid
from datetime import datetime
from typing import Literal, Optional
from zoneinfo import ZoneInfo
from pydantic import BaseModel, ConfigDict, Field


def get_datetime() -> datetime:
    return datetime.now(ZoneInfo("Australia/Sydney"))


class IncidentBase(BaseModel):
    title: str
    description: str
    location: str
    severity: Literal["LOW", "MEDIUM", "HIGH"] = "LOW"
    status: Literal["ACTIVE", "CLOSED"] = "ACTIVE"


class IncidentCreate(IncidentBase):
    pass


class IncidentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    severity: Optional[Literal["LOW", "MEDIUM", "HIGH"]] = None
    status: Optional[Literal["ACTIVE", "CLOSED"]] = None


class IncidentResponse(IncidentBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=get_datetime)
    updated_at: datetime = Field(default_factory=get_datetime)

    model_config = ConfigDict(from_attributes=True)
