import flet as ft

def AprendizView(page: ft.Page, token: str, on_logout) -> ft.View:
    """Retorna la vista del Dashboard para el rol Aprendiz."""
    
    header = ft.Text("Dashboard del Aprendiz", size=24, weight="bold")
    xp_text = ft.Text("Experiencia (XP): 0", size=18)
    group_text = ft.Text("Grupo Actual: Ninguno", size=18)
    
    logout_btn = ft.ElevatedButton("Cerrar Sesión", on_click=lambda _: on_logout())

    return ft.Container(
        content=ft.Column(
            [
                ft.Row([header], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([ft.Column([xp_text, group_text, logout_btn], alignment=ft.MainAxisAlignment.CENTER)], alignment=ft.MainAxisAlignment.CENTER)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        expand=True,
    )
