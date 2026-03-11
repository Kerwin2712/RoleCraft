import asyncio
import sys
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.database import SessionLocal, engine, Base
from backend.models import User
from backend.security import get_password_hash

async def create_expert(username: str, email: str, password: str):
    """Crea un usuario experto o lo actualiza si ya existe."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as db:
        result = await db.execute(select(User).where(User.username == username))
        existing_user = result.scalars().first()

        if existing_user:
            existing_user.role = "experto"
            print(f"Usuario {username} actualizado a rol experto.")
        else:
            new_expert = User(
                username=username,
                email=email,
                password_hash=get_password_hash(password),
                role="experto"
            )
            db.add(new_expert)
            print(f"Usuario {username} creado como experto.")
        
        await db.commit()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python create_expert.py <username> <email> <password>")
        sys.exit(1)
        
    asyncio.run(create_expert(sys.argv[1], sys.argv[2], sys.argv[3]))
