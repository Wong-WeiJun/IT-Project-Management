import uuid
from datetime import datetime
from typing import Literal, Optional
from zoneinfo import ZoneInfo
from pydantic import BaseModel, ConfigDict, Field, model_validator


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
    occupied: int = 0

    @model_validator(mode="after")
    def check_capacity(self) -> "ShelterCreate":
        if self.occupied > self.capacity:
            raise ValueError("Occupied cannot exceed capacity")
        return self


class ShelterUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    capacity: Optional[int] = None
    status: Optional[Literal["OPEN", "CLOSED", "FULL"]] = None
    occupied: Optional[int] = None

    @model_validator(mode="after")
    def check_capacity(self) -> "ShelterUpdate":
        if self.capacity is not None and self.occupied is not None:
            if self.occupied > self.capacity:
                raise ValueError("Occupied cannot exceed capacity")
        return self


class ShelterResponse(ShelterBase):
    id: str
    occupied: int

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def check_capacity(self) -> "ShelterResponse":
        if self.occupied > self.capacity:
            raise ValueError(
                f"Occupied count ({self.occupied}) cannot exceed capacity ({self.capacity})"
            )
        return self


class ResourceBase(BaseModel):
    name: str
    category: str
    quantity_total: int


class ResourceCreate(ResourceBase):
    quantity_available: Optional[int] = None

    @model_validator(mode="after")
    def default_available(self) -> "ResourceCreate":
        if self.quantity_available is None:
            self.quantity_available = self.quantity_total
        if self.quantity_available > self.quantity_total:
            raise ValueError("Available quantity cannot exceed total quantity")
        return self


class ResourceResponse(ResourceBase):
    id: str
    quantity_available: int
    quantity_allocated: int

    model_config = ConfigDict(from_attributes=True)


class ResourceAllocate(BaseModel):
    quantity: int
    incident_id: str

    @model_validator(mode="after")
    def positive_quantity(self) -> "ResourceAllocate":
        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        return self
