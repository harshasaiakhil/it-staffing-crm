from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password_hash = Column(String)
    role_id = Column(Integer, ForeignKey("roles.id"))

    role = relationship("Role")


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True)
    candidate_name = Column(String)
    phone = Column(String, index=True)
    email = Column(String, index=True)
    current_stage = Column(String, default="NEW_LEAD")
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_merged = Column(Boolean, default=False)
    merged_into_lead_id = Column(Integer, nullable=True)

    owner = relationship("User")
