import flet as ft
import jwt
from frontend.api_service import login_user

def LoginView(page: ft.Page, on_login_success, on_navigate_register) -> ft.Container:
    """Retorna la vista del formulario de Login."""
    username_field = ft.TextField(label="Usuario", autofocus=True)
    password_field = ft.TextField(label="Contraseña", password=True, can_reveal_password=True)
    msg_text = ft.Text(value="")

    def handle_login(e: ft.ControlEvent) -> None:
        if not username_field.value or not password_field.value:
            _show_msg("Ingresa usuario y contraseña", msg_text, page, ft.colors.RED)
            return
            
        res = login_user(username_field.value, password_field.value)
        if res["success"]:
            token = res["data"]["access_token"]
            role = _get_role_from_token(token)
            on_login_success(token, role)
        else:
            _show_msg(res["error"], msg_text, page, ft.colors.RED)

    login_button = ft.ElevatedButton("Iniciar Sesión", on_click=handle_login)
    register_button = ft.TextButton("¿No tienes cuenta? Regístrate aquí", on_click=lambda _: on_navigate_register())
    
    return ft.Container(
        content=ft.Row(
            [
                ft.Column(
                    [
                        ft.Text("RoleCraft Login", size=30, weight="bold"),
                        username_field, 
                        password_field, 
                        login_button, 
                        register_button,
                        msg_text
                    ], 
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        expand=True,
    )

def _show_msg(text: str, msg_element: ft.Text, page: ft.Page, color: str) -> None:
    msg_element.value = text
    msg_element.color = color
    page.update()

def _get_role_from_token(token: str) -> str:
    """Decodifica el token sin verificar firma (solo Frontend) para extraer el rol."""
    payload = jwt.decode(token, options={"verify_signature": False})
    return payload.get("role", "aprendiz")

