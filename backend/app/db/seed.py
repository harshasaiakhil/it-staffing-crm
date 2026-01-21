from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.db.models import Role, User, Lead


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # ---------------- ROLES ----------------
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

    # ---------------- USERS ----------------
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
                password_hash="test123",  # placeholder
                role_id=role_map[u["role"]].id
            )
            db.add(user)
            db.commit()

    # ---------------- LEADS ----------------
    if not db.query(Lead).count():
        manager = db.query(User).filter_by(email="manager@crm.com").first()
        sales = db.query(User).filter_by(email="sales@crm.com").first()

        leads = [
            Lead(
                candidate_name="John Doe",
                phone="9999999999",
                email="john@demo.com",
                current_stage="NEW_LEAD",
                assigned_to=manager.id
            ),
            Lead(
                candidate_name="Anita Sharma",
                phone="8888888888",
                email="anita@demo.com",
                current_stage="CONNECTED",
                assigned_to=manager.id
            ),
            Lead(
                candidate_name="Rahul Verma",
                phone="7777777777",
                email="rahul@demo.com",
                current_stage="HOT_PROSPECT",
                assigned_to=sales.id
            ),
        ]

        db.add_all(leads)
        db.commit()
        print("✅ Leads seeded")

    db.close()
    print("✅ Users & roles seeded")


if __name__ == "__main__":
    seed()
