
# user model

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db import Base  # declarative base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(512), nullable=False)
    role = Column(String(50), default="user", nullable=False)

    # Relationship to tasks
    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")