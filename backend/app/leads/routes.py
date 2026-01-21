from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Lead, User
from app.leads.services import find_duplicate_lead, merge_leads
from app.core.deps import get_current_user
from app.schemas.lead import LeadCreate

router = APIRouter(prefix="/leads", tags=["Leads"])


# -----------------------------
# CREATE LEAD (with merge logic)
# -----------------------------
@router.post("/")
def create_lead(
    payload: LeadCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    duplicate = find_duplicate_lead(db, payload.email, payload.phone)

    new_lead = Lead(
        candidate_name=payload.candidate_name,
        email=payload.email,
        phone=payload.phone,
        current_stage=payload.current_stage,
        assigned_to=payload.assigned_to,
    )

    # If duplicate exists → merge
    if duplicate:
        db.add(new_lead)
        db.commit()
        merge_leads(db, duplicate, new_lead)
        return duplicate

    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)
    return new_lead


# -----------------------------
# LIST LEADS (ROLE AWARE)
# -----------------------------
@router.get("/")
def get_leads(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    query = db.query(Lead).filter(Lead.is_merged == False)

    # Sales reps see only their leads
    if user.role.name == "sales_rep":
        query = query.filter(Lead.assigned_to == user.id)

    return query.all()


# -----------------------------
# UPDATE LEAD STAGE (PIPELINE)
# -----------------------------
@router.put("/{lead_id}/stage")
def update_stage(
    lead_id: int,
    payload: dict,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    lead = db.query(Lead).filter(
        Lead.id == lead_id,
        Lead.is_merged == False
    ).first()

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    # Sales reps can only move their own leads
    if user.role.name == "sales_rep" and lead.assigned_to != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    lead.current_stage = payload.get("stage")
    db.commit()
    db.refresh(lead)
    return lead


# -----------------------------
# ASSIGN / REASSIGN LEAD
# (Manager & Admin only)
# -----------------------------
@router.put("/{lead_id}/assign/{user_id}")
def assign_lead(
    lead_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if user.role.name not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Not allowed")

    lead = db.query(Lead).filter(
        Lead.id == lead_id,
        Lead.is_merged == False
    ).first()

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    lead.assigned_to = user_id
    db.commit()
    db.refresh(lead)
    return lead
