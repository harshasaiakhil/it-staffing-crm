from pydantic import BaseModel
from typing import Optional


class LeadCreate(BaseModel):
    candidate_name: str
    email: str
    phone: str
    current_stage: Optional[str] = "NEW_LEAD"
    assigned_to: Optional[int] = None
