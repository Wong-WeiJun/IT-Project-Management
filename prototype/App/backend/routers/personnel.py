from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas
from audit_logger import log_action

router = APIRouter(prefix="/api/personnel", tags=["personnel"])


def _with_incident_title(personnel: models.Personnel) -> models.Personnel:
    personnel.incident_title = personnel.incident.title if personnel.incident else None
    return personnel


@router.get("/", response_model=List[schemas.PersonnelResponse])
def get_all_personnel(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Personnel))
    return [_with_incident_title(p) for p in result.scalars().all()]


@router.get("/{personnel_id}", response_model=schemas.PersonnelResponse)
def get_personnel_by_id(personnel_id: str, db: Annotated[Session, Depends(get_db)]):
    personnel = db.execute(
        select(models.Personnel).where(models.Personnel.id == personnel_id)
    ).scalar_one_or_none()

    if not personnel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Personnel with ID {personnel_id} not found",
        )
    return _with_incident_title(personnel)


@router.post(
    "/", response_model=schemas.PersonnelResponse, status_code=status.HTTP_201_CREATED
)
def create_personnel(
    personnel_data: schemas.PersonnelCreate, db: Annotated[Session, Depends(get_db)]
):
    new_personnel = models.Personnel(**personnel_data.model_dump())
    db.add(new_personnel)
    db.commit()
    db.refresh(new_personnel)

    if new_personnel.assigned_incident_id:
        log_action(
            db,
            action="Assigned Personnel",
            entity_type="Personnel",
            entity_id=new_personnel.id,
            description=(
                f'Assigned {new_personnel.name} to "{new_personnel.incident.title}"'
            ),
        )

    return _with_incident_title(new_personnel)


@router.patch("/{personnel_id}", response_model=schemas.PersonnelResponse)
def update_personnel(
    personnel_id: str,
    personnel_update: schemas.PersonnelUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    personnel = db.execute(
        select(models.Personnel).where(models.Personnel.id == personnel_id)
    ).scalar_one_or_none()

    if not personnel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"personnel with ID {personnel_id} not found",
        )

    update_data = personnel_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(personnel, key, value)

    db.commit()
    db.refresh(personnel)

    if "assigned_incident_id" in update_data and personnel.assigned_incident_id:
        log_action(
            db,
            action="Assigned Personnel",
            entity_type="Personnel",
            entity_id=personnel.id,
            description=f'Assigned {personnel.name} to "{personnel.incident.title}"',
        )

    return _with_incident_title(personnel)
