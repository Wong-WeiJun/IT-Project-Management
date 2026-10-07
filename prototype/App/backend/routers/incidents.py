from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas
from audit_logger import log_action

router = APIRouter(prefix="/api/incidents", tags=["incidents"])


@router.get("/", response_model=List[schemas.IncidentResponse])
def get_all_incidents(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Incident))
    return result.scalars().all()


@router.get("/{incident_id}", response_model=schemas.IncidentResponse)
def get_incident_by_id(incident_id: str, db: Annotated[Session, Depends(get_db)]):
    incident = db.execute(
        select(models.Incident).where(models.Incident.id == incident_id)
    ).scalar_one_or_none()

    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident with ID {incident_id} not found",
        )
    return incident


@router.post(
    "/", response_model=schemas.IncidentResponse, status_code=status.HTTP_201_CREATED
)
def create_incident(
    incident_data: schemas.IncidentCreate, db: Annotated[Session, Depends(get_db)]
):
    new_incident = models.Incident(**incident_data.model_dump())
    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)

    log_action(
        db,
        action="Created Incident",
        entity_type="Incident",
        entity_id=new_incident.id,
        description=f'Created "{new_incident.title}"',
    )

    return new_incident


@router.patch("/{incident_id}", response_model=schemas.IncidentResponse)
def update_incident(
    incident_id: str,
    incident_update: schemas.IncidentUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    incident = db.execute(
        select(models.Incident).where(models.Incident.id == incident_id)
    ).scalar_one_or_none()

    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident with ID {incident_id} not found",
        )

    update_data = incident_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(incident, key, value)

    db.commit()
    db.refresh(incident)
    return incident
