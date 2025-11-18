from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict
from datetime import datetime
import os

# Database helpers (provided by environment/project template)
try:
    from database import db, create_document, get_documents
except Exception:
    db = None
    def create_document(collection_name: str, data: Dict[str, Any]):
        return {"_id": "mock", **data}
    def get_documents(collection_name: str, filter_dict: Dict[str, Any] | None = None, limit: int | None = None):
        return []

from schemas import Appointment, Newsletter

app = FastAPI(title="VetCare API", version="1.0.0")

# CORS for frontend
frontend_url = os.getenv("FRONTEND_URL", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "service": "VetCare API"}


@app.get("/test")
def test_db():
    try:
        # Attempt a simple query
        _ = get_documents("healthcheck", {}, 1)
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@app.post("/appointments")
def create_appointment(payload: Appointment):
    try:
        doc = create_document("appointment", payload.model_dump())
        return {"message": "Appointment requested", "appointment": doc}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/appointments")
def list_appointments(limit: int = 50):
    try:
        docs = get_documents("appointment", {}, limit)
        return {"items": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/newsletter")
def subscribe_newsletter(payload: Newsletter):
    try:
        # prevent duplicates
        existing = get_documents("newsletter", {"email": payload.email}, 1)
        if existing:
            return {"message": "Already subscribed"}
        doc = create_document("newsletter", payload.model_dump())
        return {"message": "Subscribed", "subscriber": doc}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class Question(BaseModel):
    name: str
    email: str
    message: str


@app.post("/questions")
def ask_question(payload: Question):
    try:
        doc = create_document("question", payload.model_dump() | {"created_at": datetime.utcnow().isoformat()})
        return {"message": "We received your question", "ticket": doc}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
