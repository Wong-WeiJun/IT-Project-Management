from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas
from audit_logger import log_action

router = APIRouter(prefix="/api/requests", tags=["requests"])


@router.get("/", response_model=List[schemas.RequestResponse])
def get_all_requests(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Request))
    return result.scalars().all()


@router.get("/{request_id}", response_model=schemas.RequestResponse)
def get_request_by_id(request_id: str, db: Annotated[Session, Depends(get_db)]):
    request = db.execute(
        select(models.Request).where(models.Request.id == request_id)
    ).scalar_one_or_none()
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Request with ID {request_id} not found",
        )
    return request


@router.post(
    "/", response_model=schemas.RequestResponse, status_code=status.HTTP_201_CREATED
)
def create_request(
    data: schemas.RequestCreate, db: Annotated[Session, Depends(get_db)]
):
    new_request = models.Request(**data.model_dump())
    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    log_action(
        db,
        action="Created Request",
        entity_type="Request",
        entity_id=new_request.id,
        description=(
            f"Created request from {new_request.requester_name} "
            f'for "{new_request.incident.title}"'
        ),
    )

    return new_request


@router.patch("/{request_id}", response_model=schemas.RequestResponse)
def update_request(
    request_id: str,
    request_update: schemas.RequestUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    request = db.execute(
        select(models.Request).where(models.Request.id == request_id)
    ).scalar_one_or_none()

    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Request with ID {request_id} not found",
        )

    update_data = request_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(request, key, value)

    db.commit()
    db.refresh(request)
    return request
