from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas

router = APIRouter(prefix="/api/resources", tags=["resources"])


def _with_allocated(resource: models.Resource) -> models.Resource:
    resource.quantity_allocated = resource.quantity_total - resource.quantity_available
    return resource


@router.get("/", response_model=List[schemas.ResourceResponse])
def get_all_resources(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Resource))
    return [_with_allocated(r) for r in result.scalars().all()]


@router.get("/{resource_id}", response_model=schemas.ResourceResponse)
def get_resource_by_id(resource_id: str, db: Annotated[Session, Depends(get_db)]):
    resource = db.execute(
        select(models.Resource).where(models.Resource.id == resource_id)
    ).scalar_one_or_none()

    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with ID {resource_id} not found",
        )
    return _with_allocated(resource)


@router.post(
    "/", response_model=schemas.ResourceResponse, status_code=status.HTTP_201_CREATED
)
def create_resource(
    data: schemas.ResourceCreate, db: Annotated[Session, Depends(get_db)]
):
    new_resource = models.Resource(**data.model_dump())
    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)
    return _with_allocated(new_resource)


@router.post("/{resource_id}/allocate", response_model=schemas.ResourceResponse)
def allocate_resource(
    resource_id: str,
    allocation: schemas.ResourceAllocate,
    db: Annotated[Session, Depends(get_db)],
):
    resource = db.execute(
        select(models.Resource).where(models.Resource.id == resource_id)
    ).scalar_one_or_none()

    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with ID {resource_id} not found",
        )

    incident = db.execute(
        select(models.Incident).where(models.Incident.id == allocation.incident_id)
    ).scalar_one_or_none()

    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident with ID {allocation.incident_id} not found",
        )

    if allocation.quantity > resource.quantity_available:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Cannot allocate {allocation.quantity} {resource.name} "
                f"({resource.quantity_available} available)"
            ),
        )

    resource.quantity_available -= allocation.quantity
    db.commit()
    db.refresh(resource)

    return _with_allocated(resource)
