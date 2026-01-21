import os
from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Resume

router = APIRouter(prefix="/resumes", tags=["Resumes"])

@router.post("/upload/{lead_id}")
def upload_resume(lead_id: int, file: UploadFile, db: Session = Depends(get_db)):
    upload_dir = f"uploads/resumes/{lead_id}"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = f"{upload_dir}/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    resume = Resume(
        lead_id=lead_id,
        file_name=file.filename,
        file_key=file_path,
        storage_type="local",
        is_download_allowed=True
    )

    db.add(resume)
    db.commit()
    return {"message": "Resume uploaded successfully"}
