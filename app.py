import flet as ft

from ui.login_view import login_view
from ui.admin.dashboard_admin import dashboard_admin
from ui.admin.empleados_admin import empleados_admin
from ui.admin.monitorTransporte_admin import monitor_transporte



async def main(page: ft.Page):
    page.title = "Neusomic - Sistema de Acceso"
    page.theme_mode = ft.ThemeMode.DARK

    page.fonts = {
        "Manrope": "https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&display=swap"
    }

    page.theme = ft.Theme(
        font_family="Manrope"
    )

    page.padding = 0
    page.spacing = 0


    # Navegación entre vistas
    async def navigate(route):
        await page.push_route(route)

    def route_change(e):

        page.views.clear()

        if page.route == "/":

            page.views.append(
                login_view(page)
            )


        elif page.route == "/dashboard_admin":

            page.views.append(
                dashboard_admin(
                    page,
                    on_navigate=navigate
                )
            )


        elif page.route == "/usuarios":

            page.views.append(
                empleados_admin(
                    page,
                    on_navigate=navigate
                )
            )


        elif page.route == "/neumaticos":

            page.views.append(
                monitor_transporte(
                    page,
                    on_navigate=navigate
                )
            )

        page.update()

    def view_pop(e):

        if len(page.views) > 1:

            page.views.pop()

            page.route = page.views[-1].route
            page.update()


    page.on_route_change = route_change
    page.on_view_pop = view_pop


    # Primera pantalla
    page.route = "/"
    route_change(None)


ft.run(main)
