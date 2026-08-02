import flet as ft

from ui.colors import *
from ui.admin.components import (
    stat_card,
    bar_chart_widget,
    pie_chart_widget,
    orders_table_widget,
    waste_reports_widget,
)


# ── Sidebar ──────────────────────────────────────────────────────────────────
def sidebar(active_route: str = "/dashboard_almacen", on_navigate=None):
    items = [
        ("/dashboard_almacen", "Panel principal", ft.Icons.COMPUTER_OUTLINED, True),
        ("/inventario", "Inventario", ft.Icons.FACTORY_OUTLINED, False),
        ("/reportes_almacen", "Reportes", ft.Icons.BAR_CHART_OUTLINED, False),
    ]

    def nav_item(route, label, icon, is_admin):
        is_active = route == active_route

        async def navigate_click(e):
            if on_navigate:
                await on_navigate(route)

        return ft.Container(
            on_click=navigate_click,
            ink=True,
            content=ft.Row(
                controls=[
                    ft.Icon(
                        icon,
                        color=SIDEBAR_ACTIVE if is_active else SIDEBAR_TEXT,
                        size=18
                    ),
                    ft.Text(
                        label,
                        size=12,
                        color=SIDEBAR_TEXT_ACTIVE if is_active else SIDEBAR_TEXT
                    ),
                ],
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding.symmetric(horizontal=24, vertical=16),
            border_radius=8,
            bgcolor=(
                ft.Colors.with_opacity(0.18, SIDEBAR_ACTIVE)
                if is_active else None
            ),
            border=(
                ft.Border(left=ft.BorderSide(3, SIDEBAR_ACTIVE))
                if is_active else None
            ),
        )

    return ft.Container(
        width=220,  # más ancho, acorde al mockup
        bgcolor=SIDEBAR_BG,
        padding=ft.Padding.only(left=10, right=10, top=18, bottom=14),
        content=ft.Column(
            controls=[
                ft.Divider(height=1, color=DIVIDER),
                ft.Container(height=10),
                *[nav_item(*it) for it in items],
                ft.Container(expand=True),
                ft.Divider(height=1, color=DIVIDER),
                ft.Container(height=10),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.LOGOUT, color="#f87171", size=16),
                            ft.Text("Cerrar sesión", size=12, color="#f87171"),
                        ],
                        spacing=8,
                    ),
                    padding=ft.Padding.symmetric(horizontal=12, vertical=9),
                    border=ft.Border.all(1, "#f87171"),
                    border_radius=8,
                ),
            ],
            spacing=4,
            expand=True,
        ),
    )


# ── Modal "Sobre nosotros" ────────────────────────────────────────────────────
def about_dialog(page: ft.Page):
    dialog = ft.AlertDialog(
        modal=True,
        bgcolor=CARD_BG,
        title=ft.Text("Sobre Neusomic", color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
        content=ft.Text(
            "Neusomic es la plataforma de gestión logística para recolección de "
            "neumáticos usados, control de inventario, trituración, pesaje de "
            "materia prima (caucho limpio) y distribución de pavimento asfáltico "
            "modificado a empresas constructoras.",
            color=TEXT_SECONDARY,
            size=13,
        ),
        actions=[
            ft.TextButton(
                "Cerrar",
                style=ft.ButtonStyle(color=STAT_BLUE),
                on_click=lambda e: page.close(dialog),
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    return dialog


# ── Top bar ──────────────────────────────────────────────────────────────────
def topbar(page: ft.Page, active_route: str):
    dialog = about_dialog(page)

    TITULOS = {
        "/dashboard_almacen": "Dashboard",
        "/produccion": "Inventario",
        "/reportesu_almacen": "Reportes",
    }

    titulo = TITULOS.get(active_route, "Dashboard")

    logo = ft.Image(
        src="assets/images/logo.png",
        width=100,
        height=90,
        fit=ft.BoxFit.CONTAIN,
    )

    return ft.Container(
        content=ft.Row(
            controls=[
                logo,
                ft.Container(width=20),

                ft.Text(
                    titulo,
                    size=20,
                    color="#fff",
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Container(expand=True),

                ft.Container(
                    content=ft.Icon(ft.Icons.NOTIFICATIONS_NONE, color="#f97316", size=18),
                    padding=6,
                ),

                ft.Text("Almacen", size=14, color="rgba(255,255,255,0.5"),
                ft.Text("|", size=14, color="rgba(255,255,255,0.5)"),

                ft.Container(
                    content=ft.Icon(ft.Icons.ACCOUNT_CIRCLE, color="#fff", size=28),
                    padding=6,
                    bgcolor="rgba(255,255,255,0.15)",
                    border_radius=20,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        padding=ft.Padding.symmetric(horizontal=24, vertical=3),
        bgcolor=TOPBAR_BG,
    )


# ── Stat cards row ───────────────────────────────────────────────────────────
def stat_row():
    return ft.Row(
        controls=[
            stat_card("Total neumáticos", "3,500 Pzas", "+10.4% ", STAT_BLUE),
            stat_card("Peso acumulado", "49.9 t", "", STAT_ORANGE),
            stat_card("Capacidad utilizada", "28, 400 Kg", "", STAT_TEAL),
            stat_card("Lotes registrados", "3 lotes", "", STAT_RED),
        ],
        spacing=12,
        expand=True,
    )


# ── Main dashboard view ──────────────────────────────────────────────────────
def dashboard_almacen(page: ft.Page, on_navigate=None):
    active_route = "/dashboard_almacen"

    info_button = ft.Container(
        content=ft.Icon(ft.Icons.INFO_OUTLINE, color="#ffffff", size=18),
        padding=8,
        border_radius=18,
        border = ft.Border.all(1, "#ffffff"),
        ink=True,
        tooltip="Saber más sobre nosotros",
        #on_click=lambda e: page.open(about_dialog(page)),
    )

    content_area = ft.Stack(
        controls=[
            ft.Container(
                expand=True,
                padding=20,
                bgcolor=MAIN_BG,
                content=ft.Column(
                    controls=[
                        stat_row(),
                        ft.Container(height=12),
                        ft.Row(
                            controls=[
                                bar_chart_widget(),
                                pie_chart_widget(),
                            ],
                            spacing=12,
                            expand=True,
                        ),
                        ft.Container(height=12),
                        ft.Row(
                            controls=[
                                orders_table_widget(),
                                waste_reports_widget(),
                            ],
                            spacing=12,
                            expand=True,
                        ),
                    ],
                    spacing=0,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                ),
            ),

            # Botón abajo a la derecha del contenido
            ft.Container(
                content=info_button,
                right=20,
                bottom=20,
            ),
        ],
        expand=True,
    )

    return ft.View(
        route="/dashboard_almacen",
        padding=0,
        bgcolor=MAIN_BG,
        controls=[
            ft.Column(
                controls=[
                    topbar(page, active_route),
                    ft.Row(
                        controls=[
                            sidebar(active_route=active_route, on_navigate=on_navigate),
                            content_area,
                        ],
                        spacing=0,
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            ),
        ],
    )
