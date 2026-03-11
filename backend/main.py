from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import jwt

from backend.database import engine, Base, get_db
from backend.models import User, Group
from backend.schemas import UserCreate, UserLogin, UserResponse, Token, GroupResponse
from backend.security import get_password_hash, verify_password, create_access_token, SECRET_KEY, ALGORITHM

app = FastAPI(title="RoleCraft API")

# Esquema para leer token Bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.on_event("startup")
async def startup() -> None:
    """Inicializa la base de datos."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# ---- DEPENDENCIAS JWT ----
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    """Valida el token y retorna el usuario actual."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
        
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user

def get_expert_user(current_user: User = Depends(get_current_user)) -> User:
    """Verifica que el usuario actual tenga el rol de experto."""
    if current_user.role != "experto":
        raise HTTPException(status_code=403, detail="No tienes permisos de experto")
    return current_user

# ---- RUTAS ----
@app.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """Registro de nuevos usuarios. Siempre se crean como 'aprendiz'."""
    result = await db.execute(select(User).where(User.username == user.username))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    
    new_user = User(
        username=user.username, email=user.email,
        password_hash=get_password_hash(user.password),
        role="aprendiz"
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@app.post("/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    """Login de usuarios que retorna un JWT con su rol."""
    result = await db.execute(select(User).where(User.username == user.username))
    db_user = result.scalars().first()
    
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
        
    token = create_access_token(data={"sub": db_user.username, "role": db_user.role})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/experto/grupos", response_model=list[GroupResponse])
async def get_grupos(db: AsyncSession = Depends(get_db), current_expert: User = Depends(get_expert_user)):
    """Retorna todos los grupos del sistema (solo accesible por expertos)."""
    result = await db.execute(select(Group))
    return result.scalars().all()
