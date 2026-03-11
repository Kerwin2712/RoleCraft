from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de conexión SQLite síncrona
DATABASE_URL = "sqlite:///./rolecraft.sqlite3"

# Instancia del motor de BD síncrona, check_same_thread false for simple flask requests
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

# Creador de sesiones síncrono
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

def get_db():
    """Generador para inyectar la sesión."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
