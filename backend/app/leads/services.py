from sqlalchemy.orm import Session
from app.db.models import Lead


def find_duplicate_lead(db: Session, email: str, phone: str):
    return db.query(Lead).filter(
        Lead.is_merged == False,
        (Lead.email == email) | (Lead.phone == phone)
    ).first()


def merge_leads(db: Session, primary: Lead, duplicate: Lead):
    duplicate.is_merged = True
    duplicate.merged_into_lead_id = primary.id
    db.commit()
