import flet as ft
from frontend.api_service import register_user

def RegisterView(page: ft.Page, on_register_success, on_navigate_login) -> ft.Container:
    """Retorna la vista del formulario de Registro."""
    username_field = ft.TextField(label="Usuario", autofocus=True)
    email_field = ft.TextField(label="Email")
    password_field = ft.TextField(label="Contraseña", password=True, can_reveal_password=True)
    msg_text = ft.Text(value="")

    def handle_register(e: ft.ControlEvent) -> None:
        if not username_field.value or not email_field.value or not password_field.value:
            _show_msg("Todos los campos son obligatorios", msg_text, page, ft.colors.RED)
            return
            
        res = register_user(username_field.value, email_field.value, password_field.value)
        if res["success"]:
            on_register_success()
        else:
            _show_msg(res["error"], msg_text, page, ft.colors.RED)

    register_button = ft.ElevatedButton("Completar Registro", on_click=handle_register)
    login_button = ft.TextButton("¿Ya tienes cuenta? Inicia sesión", on_click=lambda _: on_navigate_login())
    
    return ft.Container(
        content=ft.Row(
            [
                ft.Column(
                    [
                        ft.Text("Registro de Aprendiz", size=30, weight="bold"),
                        username_field, 
                        email_field,
                        password_field, 
                        register_button, 
                        login_button,
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
