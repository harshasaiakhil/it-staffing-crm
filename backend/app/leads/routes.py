from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Lead
from app.leads.services import find_duplicate_lead

router = APIRouter(prefix="/leads", tags=["Leads"])


@router.post("/")
def create_lead(
    candidate_name: str,
    phone: str,
    email: str,
    db: Session = Depends(get_db)
):
    if find_duplicate_lead(db, phone, email):
        raise HTTPException(status_code=400, detail="Lead already exists")

    lead = Lead(
        candidate_name=candidate_name,
        phone=phone,
        email=email
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead


@router.get("/")
def list_leads(db: Session = Depends(get_db)):
    return db.query(Lead).filter(Lead.is_merged == False).all()
