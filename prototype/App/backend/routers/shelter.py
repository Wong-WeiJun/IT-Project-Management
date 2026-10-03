from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas

router = APIRouter(prefix="/api/shelters", tags=["shelters"])


@router.get("/", response_model=List[schemas.ShelterResponse])
def get_all_shelters(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Shelter))
    return result.scalars().all()


@router.get("/{shelter_id}", response_model=schemas.ShelterResponse)
def get_shelter_by_id(shelter_id: str, db: Annotated[Session, Depends(get_db)]):
    shelter = db.execute(
        select(models.Shelter).where(models.Shelter.id == shelter_id)
    ).scalar_one_or_none()
    if not shelter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shelter with ID {shelter_id} not found",
        )
    return shelter


@router.post(
    "/", response_model=schemas.ShelterResponse, status_code=status.HTTP_201_CREATED
)
def create_shelter(
    data: schemas.ShelterCreate, db: Annotated[Session, Depends(get_db)]
):
    new_shelter = models.Shelter(**data.model_dump())
    db.add(new_shelter)
    db.commit()
    db.refresh(new_shelter)
    return new_shelter


@router.patch("/{shelter_id}", response_model=schemas.ShelterResponse)
def update_shelter(
    shelter_id: str,
    shelter_update: schemas.ShelterUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    shelter = db.execute(
        select(models.Shelter).where(models.Shelter.id == shelter_id)
    ).scalar_one_or_none()

    if not shelter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shelter with ID {shelter_id} not found",
        )

    update_data = shelter_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(shelter, key, value)

    db.commit()
    db.refresh(shelter)
    return shelter
