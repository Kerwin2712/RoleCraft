from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.database import engine, Base, get_db
from backend.models import User
from backend.schemas import UserCreate, UserLogin, UserResponse
from backend.security import get_password_hash, verify_password

app = FastAPI(title="RoleCraft API")

@app.on_event("startup")
async def startup() -> None:
    """Inicializa la base de datos."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """Punto de entrada para registro de nuevos usuarios."""
    return await _process_register(user, db)

async def _process_register(user: UserCreate, db: AsyncSession) -> User:
    """Procesa el registro aislando lógica para que las funciones sean cortas."""
    result = await db.execute(select(User).where(User.username == user.username))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    
    new_user = User(
        username=user.username, email=user.email,
        password_hash=get_password_hash(user.password)
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@app.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    """Punto de entrada para el login de usuarios."""
    return await _process_login(user, db)

async def _process_login(user: UserLogin, db: AsyncSession) -> dict:
    """Valida credenciales y retorna confirmación del login."""
    result = await db.execute(select(User).where(User.username == user.username))
    db_user = result.scalars().first()
    
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
        
    return {"message": "Login exitoso", "user_id": db_user.id}
