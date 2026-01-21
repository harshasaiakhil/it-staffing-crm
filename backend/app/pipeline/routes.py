from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Lead
from app.activities.services import log_activity

router = APIRouter(prefix="/pipeline", tags=["Pipeline"])

@router.put("/{lead_id}/move")
def move_stage(lead_id: int, stage: str, db: Session = Depends(get_db), user=Depends()):
    lead = db.query(Lead).get(lead_id)

    if stage == "LEAD_WON" and user.role.name == "sales_rep":
        raise HTTPException(status_code=403, detail="Approval required")

    old_stage = lead.current_stage
    lead.current_stage = stage
    db.commit()

    log_activity(
        db,
        lead_id,
        "STAGE_CHANGED",
        user.id,
        f"{old_stage} → {stage}"
    )
    return {"message": "Stage updated"}
