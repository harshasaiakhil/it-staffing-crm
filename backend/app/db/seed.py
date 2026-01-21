from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.db.models import Role, User

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Roles
    roles = ["admin", "manager", "sales_rep"]
    role_map = {}

    for r in roles:
        role = db.query(Role).filter_by(name=r).first()
        if not role:
            role = Role(name=r)
            db.add(role)
            db.commit()
            db.refresh(role)
        role_map[r] = role

    # Users
    users = [
        {"name": "Admin User", "email": "admin@crm.com", "role": "admin"},
        {"name": "Manager User", "email": "manager@crm.com", "role": "manager"},
        {"name": "Sales Rep", "email": "sales@crm.com", "role": "sales_rep"},
    ]

    for u in users:
        exists = db.query(User).filter_by(email=u["email"]).first()
        if not exists:
            user = User(
                name=u["name"],
                email=u["email"],
                password_hash="test123",  # placeholder for now
                role_id=role_map[u["role"]].id
            )
            db.add(user)
            db.commit()

    db.close()
    print("✅ Users & roles seeded")

if __name__ == "__main__":
    seed()
