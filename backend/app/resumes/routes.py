import os
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Lead

router = APIRouter(prefix="/resumes", tags=["Resumes"])

UPLOAD_DIR = "uploads/resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/{lead_id}", response_model=None)
def upload_resume(
    lead_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    file_path = os.path.join(UPLOAD_DIR, f"{lead_id}_{file.filename}")

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return {
        "message": "Resume uploaded successfully",
        "file_path": file_path,
    }
