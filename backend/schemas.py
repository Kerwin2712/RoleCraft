from pydantic import BaseModel, EmailStr

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

    class Config:
        from_attributes = True
