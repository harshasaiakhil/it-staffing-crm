from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
from app.auth.routes import router as auth_router
from app.leads.routes import router as lead_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="IT Staffing CRM")

app.include_router(auth_router)
app.include_router(lead_router)


@app.get("/")
def root():
    return {"status": "CRM backend running"}
