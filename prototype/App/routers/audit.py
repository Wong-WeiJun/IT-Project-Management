from typing import Annotated, List
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas

router = APIRouter(prefix="/api/audit", tags=["audit"])


@router.get("/", response_model=List[schemas.AuditLogResponse])
def get_audit_log(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(models.AuditLog).order_by(models.AuditLog.timestamp.desc())
    )
    return result.scalars().all()
