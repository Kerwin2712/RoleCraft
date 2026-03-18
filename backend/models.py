from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from backend.database import Base
from datetime import datetime

class Group(Base):
    """Modelo para representar los grupos de aprendices."""
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    status = Column(String(50), default="En desarrollo")
    phase = Column(Integer, default=1)
    vacant_roles = Column(String(255), default="")
    
    users = relationship("User", back_populates="group")

class Module(Base):
    """Modelo para los módulos de entrenamiento."""
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    video_url = Column(String(255), nullable=True)
    xp_reward = Column(Integer, default=50)
    prerequisite_id = Column(Integer, ForeignKey("modules.id"), nullable=True)

    prerequisite = relationship("Module", remote_side=[id])

class UserModuleProgress(Base):
    """Rastreo de progreso de módulos por usuario."""
    __tablename__ = "user_module_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    completed_at = Column(String(50), nullable=True) # ISO Format
    status = Column(String(20), default="available") # locked, available, completed
    
    # Nuevo: Lógica de evaluación circular
    evaluation_queue = Column(Text, nullable=True) # JSON String de IDs de preguntas
    current_streak = Column(Integer, default=0)

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

    # Nuevo: Economía Virtual e Inflexión
    coins = Column(Integer, default=0)
    question_stock = Column(Integer, default=20)
    last_stock_recharge = Column(DateTime, default=datetime.now)
    
    # Fase de Diagnóstico e Inflexión
    is_polyglot = Column(Integer, nullable=True) # Usamos Integer como bool (0/1)
    last_exam_attempt = Column(DateTime, nullable=True)

    group = relationship("Group", back_populates="users")
    training_progress = relationship("UserModuleProgress", backref="user")

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
