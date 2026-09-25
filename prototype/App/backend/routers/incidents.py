from typing import Annotated, List
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas

router = APIRouter(prefix="/api/incidents", tags=["incidents"])


@router.get("/", response_model=List[schemas.IncidentResponse])
def get_all_incidents(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Incident))
    return result.scalars().all()
