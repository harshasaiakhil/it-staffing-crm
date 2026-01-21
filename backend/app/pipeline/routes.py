from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Lead, User

router = APIRouter(prefix="/pipeline", tags=["Pipeline"])

PIPELINE_STAGES = [
    "NEW_LEAD",
    "DNR_1",
    "DNR_2",
    "DNR_3",
    "CONNECTED",
    "QUALIFIED",
    "HOT_PROSPECT",
    "LEAD_WON"
]


@router.put("/{lead_id}/move")
def move_lead_stage(
    lead_id: int,
    new_stage: str,
    user_id: int,  # temporary (later from auth)
    db: Session = Depends(get_db)
):
    if new_stage not in PIPELINE_STAGES:
        raise HTTPException(status_code=400, detail="Invalid pipeline stage")

    lead = db.query(Lead).filter(Lead.id == lead_id, Lead.is_merged == False).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    user = db.query(User).filter(User.id == user_id).first()

    if new_stage == "LEAD_WON" and user.role.name == "sales_rep":
        raise HTTPException(status_code=403, detail="Only Manager/Admin can mark Lead Won")

    lead.current_stage = new_stage
    db.commit()

    return {"message": f"Lead moved to {new_stage}"}
