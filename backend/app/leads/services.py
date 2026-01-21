from sqlalchemy.orm import Session
from app.db.models import Lead
from app.leads.merge import choose_primary_lead, merge_leads


def find_duplicate_lead(db: Session, phone: str, email: str):
    return db.query(Lead).filter(
        ((Lead.phone == phone) | (Lead.email == email)),
        Lead.is_merged == False
    ).first()


def handle_duplicate(db: Session, new_lead: Lead):
    duplicate = find_duplicate_lead(db, new_lead.phone, new_lead.email)
    if duplicate:
        primary, secondary = choose_primary_lead(duplicate, new_lead)
        merge_leads(db, primary, secondary)
        return primary
    return new_lead
