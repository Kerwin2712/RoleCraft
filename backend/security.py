from passlib.context import CryptContext

# Contexto de encriptación usando bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Retorna el hash de una contraseña plana usando bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña plana coincide con su hash."""
    return pwd_context.verify(plain_password, hashed_password)
