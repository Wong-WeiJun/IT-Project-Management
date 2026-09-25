from typing import Literal, Optional
from pydantic import BaseModel


class IncidentBase(BaseModel):
    title: str
    description: str
    location: str
    severity: Literal["LOW", "MEDIUM", "HIGH"] = "LOW"
    status: Literal["ACTIVE", "CLOSED"] = "ACTIVE"
