from sqlalchemy.orm import Session
from app.db.models import Lead

PIPELINE_PRIORITY = {
    "NEW_LEAD": 1,
    "DNR_1": 2,
    "DNR_2": 3,
    "DNR_3": 4,
    "CONNECTED": 5,
    "QUALIFIED": 6,
    "HOT_PROSPECT": 7,
    "LEAD_WON": 8,
}


def choose_primary_lead(a: Lead, b: Lead):
    return (a, b) if PIPELINE_PRIORITY[a.current_stage] >= PIPELINE_PRIORITY[b.current_stage] else (b, a)


def merge_leads(db: Session, primary: Lead, secondary: Lead):
    secondary.is_merged = True
    secondary.merged_into_lead_id = primary.id
    db.commit()
