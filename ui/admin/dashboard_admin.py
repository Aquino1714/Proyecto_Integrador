import flet as ft

def dashboard_admin(page):
    return ft.View(
        route="/dashboard_admin",
        controls=[
            ft.Text("Dashboard administrador"),
            ft.Text("Contenido aquí")
        ]
    )
