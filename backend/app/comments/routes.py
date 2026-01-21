from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Lead, User
from datetime import datetime

router = APIRouter(prefix="/comments", tags=["Comments"])

COMMENTS = []  # temporary in-memory (DB later)


@router.post("/{lead_id}")
def add_comment(
    lead_id: int,
    user_id: int,
    text: str,
    db: Session = Depends(get_db)
):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        return {"error": "Lead not found"}

    comment = {
        "lead_id": lead_id,
        "user_id": user_id,
        "text": text,
        "time": datetime.utcnow()
    }

    COMMENTS.append(comment)
    return {"message": "Comment added"}


@router.get("/{lead_id}")
def get_comments(lead_id: int):
    return [c for c in COMMENTS if c["lead_id"] == lead_id]
