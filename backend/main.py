from fastapi import FastAPI

from backend.api.v1.dpdp import router as dpdp_router
from backend.api.v1.risks import router as risk_router

app = FastAPI(
    title="CyGRC Platform API",
    description="Governance, Risk and Compliance Platform",
    version="1.0.0"
)

app.include_router(risk_router)
app.include_router(dpdp_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to CyGRC Platform 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "Healthy"
    }