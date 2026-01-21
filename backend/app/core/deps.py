from app.db.session import SessionLocal
from app.db.models import User


def get_current_user():
    db = SessionLocal()
    # TEMP: simulate logged-in manager
    return db.query(User).filter(User.email == "manager@crm.com").first()
