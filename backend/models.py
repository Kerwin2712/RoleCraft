from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class Group(Base):
    """Modelo para representar los grupos de aprendices."""
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    status = Column(String(50), default="En desarrollo")
    
    users = relationship("User", back_populates="group")

class User(Base):
    """Modelo de base de datos para los usuarios del sistema."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    xp = Column(Integer, default=0)
    role = Column(String(50), default="aprendiz", nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)

    group = relationship("Group", back_populates="users")
