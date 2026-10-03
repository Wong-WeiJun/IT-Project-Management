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
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RequestBase(BaseModel):
    requester_name: str
    requester_contact: str
    location: str
    description: str
    priority: Literal["LOW", "MEDIUM", "HIGH"] = "LOW"


class RequestCreate(RequestBase):
    incident_id: str


class RequestUpdate(BaseModel):
    requester_name: Optional[str] = None
    requester_contact: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[Literal["LOW", "MEDIUM", "HIGH"]] = None
    status: Optional[Literal["OPEN", "IN_PROGRESS", "RESOLVED"]] = None


class RequestResponse(RequestBase):
    id: str
    incident_id: str
    status: Literal["OPEN", "IN_PROGRESS", "RESOLVED"]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PersonnelBase(BaseModel):
    name: str
    role: Literal[
        "Medical",
        "Search & Rescue",
        "Fire Response",
        "Logistics",
        "Volunteer",
        "Coordinator",
    ]
    contact: str


class PersonnelCreate(PersonnelBase):
    assigned_incident_id: Optional[str] = None


class PersonnelUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[
        Literal[
            "Medical",
            "Search & Rescue",
            "Fire Response",
            "Logistics",
            "Volunteer",
            "Coordinator",
        ]
    ] = None
    contact: Optional[str] = None
    status: Optional[Literal["AVAILABLE", "ASSIGNED", "UNAVAILABLE"]] = None
    assigned_incident_id: Optional[str] = None


class PersonnelResponse(PersonnelBase):
    id: str
    status: Literal["AVAILABLE", "ASSIGNED", "UNAVAILABLE"]
    assigned_incident_id: Optional[str] = None
    incident_title: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ShelterBase(BaseModel):
    name: str
    location: str
    capacity: int
    status: Literal["OPEN", "CLOSED", "FULL"] = "OPEN"


class ShelterCreate(ShelterBase):
    pass


class ShelterUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    capacity: Optional[int] = None
    status: Optional[Literal["OPEN", "CLOSED", "FULL"]] = None
    occupied: Optional[int] = None


class ShelterResponse(ShelterBase):
    name: str
    capacity: int
    occupied: int
    status: Literal["OPEN", "CLOSED", "FULL"] = "OPEN"
