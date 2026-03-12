from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class Group(Base):
    """Modelo para representar los grupos de aprendices."""
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    status = Column(String(50), default="En desarrollo")
    phase = Column(Integer, default=1)
    vacant_roles = Column(String(255), default="")
    
    users = relationship("User", back_populates="group")

class User(Base):
    """Modelo de base de datos para los usuarios del sistema."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    xp = Column(Integer, default=0)
    
    # Habilidades Verticales (Especialidad)
    skill_backend = Column(Integer, default=0)
    skill_frontend = Column(Integer, default=0)
    skill_pm = Column(Integer, default=0)
    
    # Habilidades Horizontales (Supervivencia)
    skill_git = Column(Integer, default=0)
    skill_ia = Column(Integer, default=0)
    skill_sql = Column(Integer, default=0)
    
    role = Column(String(50), default="aprendiz", nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)

    group = relationship("Group", back_populates="users")

    @property
    def xp_multiplier(self):
        """Calcula el multiplicador basado en habilidades horizontales."""
        from config import HORIZONTAL_SKILL_REWARD, BASE_MULTIPLIER, XP_ROUND_DECIMALS
        
        # Asumiendo que el 'nivel' es el XP dividido por una base o simplemente el XP acumulado
        # Para este ejemplo, usaremos un bono de 0.1 por cada 10 puntos de XP en horizontales
        # (Ajustable según el diseño final de 'niveles')
        bonus = (self.skill_git + self.skill_ia + self.skill_sql) / 10 * HORIZONTAL_SKILL_REWARD
        return round(BASE_MULTIPLIER + bonus, XP_ROUND_DECIMALS)

    def calculate_gain(self, base_xp):
        """Calcula el XP final ganado aplicando el multiplicador."""
        from config import XP_ROUND_DECIMALS
        return round(base_xp * self.xp_multiplier, XP_ROUND_DECIMALS)
