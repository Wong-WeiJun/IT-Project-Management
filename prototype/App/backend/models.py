import uuid
from datetime import datetime
from zoneinfo import ZoneInfo
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


def get_datetime() -> datetime:
    return datetime.now(ZoneInfo("Australia/Sydney"))


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    location = Column(String, nullable=False)

    severity = Column(String, default="LOW", nullable=False)
    status = Column(String, default="ACTIVE", nullable=False)

    created_at = Column(DateTime(timezone=True), default=get_datetime, nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        default=get_datetime,
        onupdate=get_datetime,
        nullable=False,
    )

    requests = relationship(
        "Request", back_populates="incident", cascade="all, delete-orphan"
    )


class Request(Base):
    __tablename__ = "requests"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    incident_id = Column(
        String, ForeignKey("incidents.id", ondelete="CASCADE"), nullable=False
    )
    requester_name = Column(String, nullable=False)
    requester_contact = Column(String, nullable=False)
    location = Column(String, nullable=False)
    description = Column(String, nullable=False)
    priority = Column(String, default="LOW", nullable=False)
    status = Column(String, default="OPEN", nullable=False)
    created_at = Column(DateTime(timezone=True), default=get_datetime, nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        default=get_datetime,
        onupdate=get_datetime,
        nullable=False,
    )
    incident = relationship("Incident", back_populates="requests")
