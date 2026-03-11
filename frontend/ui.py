import flet as ft
from frontend.views.login_view import LoginView
from frontend.views.register_view import RegisterView
from frontend.views.aprendiz_view import AprendizView
from frontend.views.experto_view import ExpertoView

def main(page: ft.Page) -> None:
    """Enrutador principal de la aplicación."""
    page.title = "RoleCraft"
    page.theme_mode = ft.ThemeMode.DARK
    session_data = {"token": None}
    
    def on_login_success(token: str, role: str) -> None:
        """Callback al iniciar sesión exitosamente."""
        session_data["token"] = token
        page.route = f"/{role}"
        route_change(None)
        
    def on_register_success() -> None:
        """Callback tras registrar aprendiz exitosamente."""
        page.route = "/"
        route_change(None)
        
    def on_logout() -> None:
        """Callback al cerrar sesión."""
        session_data["token"] = None
        page.route = "/"
        route_change(None)

    def route_change(e) -> None:
        """Manejador del cambio de rutas."""
        page.controls.clear()
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        token = session_data.get("token")
        
        if page.route == "/":
            page.add(LoginView(page, on_login_success, lambda: navigate_to("/register")))
        elif page.route == "/register":
            page.add(RegisterView(page, on_register_success, lambda: navigate_to("/")))
        elif page.route == "/aprendiz":
            page.add(AprendizView(page, token, on_logout))
        elif page.route == "/experto":
            page.add(ExpertoView(page, token, on_logout))
        page.update()

    def navigate_to(route: str):
        page.route = route
        route_change(None)

    page.on_route_change = route_change
    page.route = "/"
    route_change(None)

if __name__ == "__main__":
    ft.run(main, view=ft.AppView.WEB_BROWSER)
