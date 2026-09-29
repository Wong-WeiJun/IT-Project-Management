from fastapi import FastAPI, APIRouter, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from database import get_db, Base, engine
import models
from routers import incidents, requests


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Emergency Support Coordination System",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(incidents.router)
app.include_router(requests.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home():
    return FileResponse("templates/incidents.html")


@app.get("/incidents.html")
def incidents_page():
    return FileResponse("templates/incidents.html")


@app.get("/incidents_detail.html")
def incident_detail_page():
    return FileResponse("templates/incidents_detail.html")


@app.get("/requests.html")
def requests_page():
    return FileResponse("templates/requests.html")


@app.get("/requests_detail.html")
def requests_detail_page():
    return FileResponse("templates/requests_detail.html")


@app.get("/health")
def health(db: Session = Depends(get_db)):
    return {
        "status": "ok",
        "service": "Emergency Support Coordination System",
        "database": db is not None,
    }
