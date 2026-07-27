import flet as ft

from ui.login_view import login_view
from ui.admin.dashboard_admin import dashboard_admin


async def main(page: ft.Page):
    page.title = "Neusomic - Sistema de Acceso"
    page.theme_mode = ft.ThemeMode.DARK
    page.fonts = {
        "Manrope": "https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&display=swap"
    }
    page.theme = ft.Theme(font_family="Manrope")
    page.padding = 0
    page.spacing = 0



    def route_change(e):

        page.views.clear()

        if page.route == "/":
            page.views.append(login_view(page))

        elif page.route == "/dashboard_admin":
            page.views.append(dashboard_admin(page))

        page.update()


    async def view_pop(e):

        if len(page.views) > 1:
            page.views.pop()
            await page.push_route(page.views[-1].route)


    page.on_route_change = route_change
    page.on_view_pop = view_pop


    # Cargar primera pantalla
    page.route = "/"
    route_change(None)


ft.run(main)
