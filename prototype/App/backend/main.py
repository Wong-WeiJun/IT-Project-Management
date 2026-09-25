from fastapi import FastAPI, APIRouter

app = FastAPI(title="Emergency Support Coordination System", version="1.0.0")


@app.get("/")
def home():
    return {"message": "Welcome to the Glizzy Emergency Support Coordination System!"}


@app.get("/health")
def health():
    return {"status": "ok", "service": "Emergency Support Coordination System"}
