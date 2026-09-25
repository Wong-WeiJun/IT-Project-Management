import uuid
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Literal
from zoneinfo import ZoneInfo


def get_datetime() -> datetime:
    return datetime.now(ZoneInfo("Australia/Sydney"))


class Incident(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    location: str
    severity: Literal["LOW", "MEDIUM", "HIGH"] = "LOW"
    status: Literal["ACTIVE", "CLOSED"] = "ACTIVE"
    created_at: datetime = Field(default_factory=get_datetime)
    updated_at: datetime = Field(default_factory=get_datetime)
