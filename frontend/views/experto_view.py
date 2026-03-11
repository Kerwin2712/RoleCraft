import flet as ft
from frontend.api_service import get_expert_groups

def ExpertoView(page: ft.Page, token: str, on_logout) -> ft.View:
    """Retorna el Panel de Monitoreo para el rol Experto."""
    header = ft.Text("Panel de Monitoreo (Experto)", size=24, weight="bold")
    logout_btn = ft.ElevatedButton("Cerrar Sesión", on_click=lambda _: on_logout())
    
    list_view = ft.ListView(expand=1, spacing=10, padding=20)
    
    def load_groups():
        res = get_expert_groups(token)
        if res.get("success"):
            for g in res["data"]:
                btn = ft.ElevatedButton(f"Unirse/Intervenir", on_click=lambda e: print("Unirse al grupo!"))
                row = ft.Row([ft.Text(f"{g['name']} - {g['status']}"), btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                list_view.controls.append(row)
        else:
            list_view.controls.append(ft.Text(res.get("error", "Error cargando grupos")))
        page.update()

    # Cargar los grupos al iniciar la vista
    load_groups()

    return ft.Container(
        content=ft.Column(
            [
                ft.Row([header, logout_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                list_view
            ]
        ),
        expand=True,
    )
