import flet as ft
import httpx

API_URL = "http://127.0.0.1:8000"

def main(page: ft.Page) -> None:
    """Punto de entrada principal de la vista de Flet."""
    page.title = "RoleCraft Login"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    username_field = ft.TextField(label="Usuario", autofocus=True)
    password_field = ft.TextField(label="Contraseña", password=True, can_reveal_password=True)
    msg_text = ft.Text(value="")

    def handle_login(e: ft.ControlEvent) -> None:
        """Manejador del evento de click en el botón."""
        if not username_field.value or not password_field.value:
            msg_text.value = "Ingresa usuario y contraseña"
            page.update()
            return
        do_login(username_field.value, password_field.value, msg_text, page)

    login_button = ft.ElevatedButton("Iniciar Sesión", on_click=handle_login)
    
    page.add(
        ft.Row([
            ft.Column([username_field, password_field, login_button, msg_text], 
                        alignment=ft.MainAxisAlignment.CENTER)
        ], alignment=ft.MainAxisAlignment.CENTER)
    )

def do_login(username: str, password: str, msg_text: ft.Text, page: ft.Page) -> None:
    """Realiza la petición HTTP al backend y actualiza la UI."""
    try:
        res = httpx.post(f"{API_URL}/login", json={"username": username, "password": password})
        if res.status_code == 200:
            msg_text.value = "¡Bienvenido a RoleCraft!"
            msg_text.color = ft.colors.GREEN
        else:
            msg_text.value = "Error: Credenciales inválidas"
            msg_text.color = ft.colors.RED
    except httpx.RequestError:
        msg_text.value = "Error conectando al servidor"
        msg_text.color = ft.colors.RED
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
