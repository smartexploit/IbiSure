from fastapi import FastAPI
from pydantic import BaseModel, Field

from backend.address_resolver import resolve_address


app = FastAPI(
    title="IbiSure API",
    description=(
        "A Nigerian address-resolution prototype. "
        "Results are candidates, not verified locations."
    ),
    version="0.1.0",
)


class ResolveRequest(BaseModel):
    address: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Informal address or landmark description",
        examples=["Near the big roundabout, Ado-Ekiti"],
    )


@app.get("/")
def home():
    return {
        "name": "IbiSure",
        "status": "online",
        "version": "0.1.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "IbiSure address resolver",
    }


@app.post("/resolve")
def resolve(request: ResolveRequest):
    return resolve_address(request.address)
