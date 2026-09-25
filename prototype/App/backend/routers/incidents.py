from fastapi import APIRouter
from database import get_db
from typing import Annotated
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/incidents", tags=["incidents"])

@router.get("/")
def get_all_incidents(db: Annotated[]):
    

