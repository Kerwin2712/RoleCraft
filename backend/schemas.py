from pydantic import BaseModel, EmailStr
from typing import Optional

class GroupResponse(BaseModel):
    """Esquema para retornar la información de un grupo."""
    id: int
    name: str
    status: str
    
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    """Esquema para creación de un nuevo usuario."""
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    """Esquema para la autenticación en el login."""
    username: str
    password: str

class UserResponse(BaseModel):
    """Esquema para retornar la información del usuario."""
    id: int
    username: str
    email: str
    xp: int
    role: str
    group_id: Optional[int] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    """Esquema para el token JWT de respuesta."""
    access_token: str
    token_type: str
