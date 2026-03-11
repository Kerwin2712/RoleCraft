from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

# URL de conexión SQLite asíncrona
DATABASE_URL = "sqlite+aiosqlite:///./rolecraft.sqlite3"

# Instancia del motor de BD
engine = create_async_engine(DATABASE_URL, echo=False)

# Creador de sesiones
SessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# Base para los modelos
Base = declarative_base()

async def get_db():
    """Generador asíncrono para inyectar la sesión en FastAPI."""
    async with SessionLocal() as session:
        yield session
