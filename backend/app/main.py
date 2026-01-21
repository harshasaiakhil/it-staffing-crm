from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine

from app.auth.routes import router as auth_router
from app.leads.routes import router as lead_router
from app.pipeline.routes import router as pipeline_router
from app.comments.routes import router as comment_router
from app.resumes.routes import router as resume_router

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="IT Staffing CRM")

# Register routers
app.include_router(auth_router)
app.include_router(lead_router)
app.include_router(pipeline_router)
app.include_router(comment_router)
app.include_router(resume_router)


@app.get("/")
def root():
    return {"status": "CRM backend running"}
