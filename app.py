import flet as ft

from ui.login_view import login_view
from ui.admin import *
from ui.trituradora import *
from ui.almacen import *
from ui.vulcanizadora import *



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


    # ── Navegacion entre las vistas ──────────────────────────────────────────────────────
    async def navigate(route):
        await page.push_route(route)

    async def logout():
        # ── Limpiar datos de la sesión ──────────────────────────────────────────────────────
        if hasattr(page, "empleado_id"):
            delattr(page, "empleado_id")

        if hasattr(page, "vulcanizadora_id"):
            delattr(page, "vulcanizadora_id")


        await page.push_route("/")

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
                    on_navigate=navigate,
                    on_logout=logout
                )
            )


        elif page.route == "/dashboard_trituradora":

            page.views.append(
                dashboard_trituradora(
                    page,
                    on_navigate=navigate,
                    on_logout=logout
                )
            )

        elif page.route == "/dashboard_vulcanizadora":
            vulcanizadora_id = getattr(page, "vulcanizadora_id", None)

            page.views.append(
                dashboard_vulcanizadora(
                    page,
                    vulcanizadora_id,
                    on_navigate=navigate,
                    on_logout=logout
                )
            )


        elif page.route == "/usuarios":

            page.views.append(
                empleados_admin(
                    page,
                    on_navigate=navigate,
                    on_logout=logout
                )
            )


        elif page.route == "/neumaticos":

            page.views.append(
                monitor_transporte(
                    page,
                    on_navigate=navigate,
                    on_logout=logout
                )
            )

        elif page.route == "/desechos":

            page.views.append(
                desechos_admin(
                    page,
                    on_navigate=navigate,
                    on_logout=logout
                )
            )

        elif page.route == "/inventario":

            page.views.append(
                panel_inventario(
                    page,
                    on_navigate=navigate,
                    on_logout=logout
                )
            )

        elif page.route == "/reportes":

            page.views.append(
                reportes_empleados_admin(
                    page,
                    on_navigate=navigate,
                    on_logout=logout
                )
            )

        elif page.route == "/transporte":

            page.views.append(
                transportes_admin (
                    page,
                    on_navigate=navigate,
                    on_logout=logout
                )
            )

        elif page.route == "/produccion":

            page.views.append(
                production_trituradora(
                    page,
                    on_navigate=navigate,
                    on_logout=logout
                )
            )
        elif page.route == "/maquinaria":

            page.views.append(
                equipos_triturador(
                    page,
                    on_navigate=navigate,
                    on_logout=logout
                )
            )
        elif page.route == "/reporte":
            empleado_id = getattr(page, "empleado_id", None)
            page.views.append(
                reportes_trituracion(
                    page,
                    empleado_id,
                    on_navigate=navigate,
                    on_logout=logout
                )
            )
        elif page.route == "/dashboard_almacen":
            page.views.append(
                dashboard_almacen(
                    page,
                    on_navigate=navigate,
                    on_logout=logout
                )
            )
        elif page.route == "/reportes_almacen":
            empleado_id = getattr(page, "empleado_id", None)
            page.views.append(
                reportes_almacen(
                    page,
                    empleado_id,
                    on_navigate=navigate,
                    on_logout=logout
                )
            )

        elif page.route == "/apollo":
            page.views.append(
                solicitud_apoyo(
                    page,
                    on_navigate=navigate,
                    on_logout=logout
                )
            )

        elif page.route == "/solicitudes":
            vulcanizadora_id = getattr(page, "vulcanizadora_id", None)
            page.views.append(
                reportes_vulcanizadora(
                    page,
                    vulcanizadora_id,
                    on_navigate=navigate,
                    on_logout=logout
                )
            )

        elif page.route == "/perfil":
            vulcanizadora_id = getattr(page, "vulcanizadora_id", None)
            page.views.append (
                perfil_view(
                    page,
                    vulcanizadora_id,
                    on_navigate=navigate,
                    on_logout=logout
                )
            )

        elif page.route == "/inventarioV":
            vulcanizadora_id = getattr(page, "vulcanizadora_id", None)
            page.views.append(
                inventario_view(
                    page,
                    vulcanizadora_id,
                    on_navigate=navigate,
                    on_logout=logout
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

    page.route = "/"
    route_change(None)


ft.run(main)
