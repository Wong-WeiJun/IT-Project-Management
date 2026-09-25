from fastapi import FastAPI, APIRouter, Depends
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from database import get_db, Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Emergency Support Coordination System", version="1.0.0")


@app.get("/")
def home():
    return {"message": "Welcome to the Glizzy Emergency Support Coordination System!"}


@app.get("/health")
def health(db: Session = Depends(get_db)):
    return {
        "status": "ok",
        "service": "Emergency Support Coordination System",
        "database": db is not None,
    }
