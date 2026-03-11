import httpx
from typing import Dict, Any

API_URL = "http://127.0.0.1:8000"

def login_user(username: str, password: str) -> Dict[str, Any]:
    """Hace la petición de login y retorna el token y error si lo hay."""
    try:
        res = httpx.post(f"{API_URL}/login", json={"username": username, "password": password})
        if res.status_code == 200:
            return {"success": True, "data": res.json()}
        return {"success": False, "error": "Credenciales inválidas"}
    except httpx.RequestError:
        return {"success": False, "error": "Error conectando al servidor"}

def get_expert_groups(token: str) -> Dict[str, Any]:
    """Obtiene los grupos disponibles para un experto."""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        res = httpx.get(f"{API_URL}/experto/grupos", headers=headers)
        if res.status_code == 200:
            return {"success": True, "data": res.json()}
        return {"success": False, "error": "Acceso denegado"}
    except httpx.RequestError:
        return {"success": False, "error": "Error de conexión"}

def register_user(username: str, email: str, password: str) -> Dict[str, Any]:
    """Hace la petición para registrar un nuevo usuario (Aprendiz)."""
    try:
        res = httpx.post(f"{API_URL}/register", json={"username": username, "email": email, "password": password})
        if res.status_code == 200:
            return {"success": True, "data": res.json()}
        if res.status_code == 400:
            return {"success": False, "error": res.json().get("detail", "Error en registro")}
        return {"success": False, "error": "Error interno del servidor"}
    except httpx.RequestError:
        return {"success": False, "error": "Error conectando al servidor"}
