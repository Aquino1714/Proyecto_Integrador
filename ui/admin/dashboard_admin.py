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
def sidebar(active_route: str = "/dashboard_admin", on_navigate=None, on_logout=None):
    items = [
        ("/dashboard_admin", "Administrador", ft.Icons.ADMIN_PANEL_SETTINGS_OUTLINED, True),
        ("/usuarios", "Empleados", ft.Icons.BADGE_OUTLINED, False),
        #("/neumaticos", "Monitor\ntransporte", ft.Icons.LOCAL_SHIPPING_OUTLINED, False),
        ("/desechos", "Reportes \ndesechos", ft.Icons.DELETE_OUTLINED, False),
        ("/reportes", "Reportes", ft.Icons.ANALYTICS_OUTLINED, False),
        ("/transporte", "Transporte", ft.Icons.DIRECTIONS_BUS_OUTLINED, False),
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

    async def logout_click(e):
        if on_logout:
            await on_logout()

    return ft.Container(
        width=220,
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
                    ink=True,
                    on_click=logout_click,
                ),
            ],
            spacing=4,
            expand=True,
        ),
    )


# ── Modal "Sobre nosotros" ────────────────────────────────────────────────────
def about_dialog(page: ft.Page):
    def close_about(e):
        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        modal=True,
        bgcolor=CARD_BG,
        title=ft.Row(
            controls=[
                ft.Container(
                    width=42,
                    height=42,
                    border_radius=10,
                    bgcolor=ft.Colors.with_opacity(0.12, STAT_BLUE),
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(
                        ft.Icons.RECYCLING_OUTLINED,
                        color=STAT_BLUE,
                        size=25,
                    ),
                ),
                ft.Column(
                    controls=[
                        ft.Text(
                            "Sobre Neusomic",
                            color=TEXT_PRIMARY,
                            size=19,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(
                            "Innovación, reciclaje y construcción sostenible",
                            color=TEXT_SECONDARY,
                            size=11,
                        ),
                    ],
                    spacing=2,
                    tight=True,
                ),
            ],
            spacing=12,
        ),

        content=ft.Container(
            width=720,
            height=560,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                spacing=18,
                controls=[

                    # ─────────────────────────────────────────────────────
                    # INTRODUCCIÓN
                    # ─────────────────────────────────────────────────────
                    ft.Container(
                        padding=18,
                        border_radius=12,
                        bgcolor=ft.Colors.with_opacity(0.06, STAT_BLUE),
                        border=ft.Border.all(
                            1,
                            ft.Colors.with_opacity(0.20, STAT_BLUE)
                        ),
                        content=ft.Column(
                            spacing=8,
                            controls=[
                                ft.Text(
                                    "¿Quiénes somos?",
                                    size=15,
                                    weight=ft.FontWeight.BOLD,
                                    color=STAT_BLUE,
                                ),
                                ft.Text(
                                    "Neusomic es una empresa mexicana dedicada a la "
                                    "gestión integral y aprovechamiento de neumáticos "
                                    "fuera de uso. Nuestro objetivo es transformar "
                                    "un residuo de difícil manejo en materia prima "
                                    "útil para nuevos procesos industriales y de "
                                    "construcción.",
                                    size=13,
                                    color=TEXT_PRIMARY,
                                ),
                                ft.Text(
                                    "A través de procesos de recolección, "
                                    "clasificación, trituración, separación y "
                                    "distribución, buscamos reducir el impacto "
                                    "ambiental generado por los neumáticos "
                                    "desechados y fomentar una economía circular.",
                                    size=13,
                                    color=TEXT_SECONDARY,
                                ),
                            ],
                        ),
                    ),

                    # ─────────────────────────────────────────────────────
                    # MISIÓN / VISIÓN
                    # ─────────────────────────────────────────────────────
                    ft.Row(
                        controls=[
                            ft.Container(
                                expand=True,
                                padding=16,
                                border_radius=10,
                                bgcolor=ft.Colors.with_opacity(
                                    0.06,
                                    STAT_ORANGE
                                ),
                                content=ft.Column(
                                    spacing=7,
                                    controls=[
                                        ft.Icon(
                                            ft.Icons.FLAG_OUTLINED,
                                            color=STAT_ORANGE,
                                            size=22,
                                        ),
                                        ft.Text(
                                            "Misión",
                                            size=14,
                                            weight=ft.FontWeight.BOLD,
                                            color=STAT_ORANGE,
                                        ),
                                        ft.Text(
                                            "Gestionar responsablemente los "
                                            "neumáticos fuera de uso mediante "
                                            "procesos eficientes de recuperación "
                                            "y transformación, generando valor "
                                            "ambiental, social y económico.",
                                            size=12,
                                            color=TEXT_SECONDARY,
                                        ),
                                    ],
                                ),
                            ),

                            ft.Container(
                                expand=True,
                                padding=16,
                                border_radius=10,
                                bgcolor=ft.Colors.with_opacity(
                                    0.06,
                                    STAT_BLUE
                                ),
                                content=ft.Column(
                                    spacing=7,
                                    controls=[
                                        ft.Icon(
                                            ft.Icons.VISIBILITY_OUTLINED,
                                            color=STAT_BLUE,
                                            size=22,
                                        ),
                                        ft.Text(
                                            "Visión",
                                            size=14,
                                            weight=ft.FontWeight.BOLD,
                                            color=STAT_BLUE,
                                        ),
                                        ft.Text(
                                            "Ser una empresa referente en "
                                            "México en el aprovechamiento de "
                                            "neumáticos reciclados y contribuir "
                                            "a una industria de construcción "
                                            "más sostenible.",
                                            size=12,
                                            color=TEXT_SECONDARY,
                                        ),
                                    ],
                                ),
                            ),
                        ],
                        spacing=12,
                    ),

                    # ─────────────────────────────────────────────────────
                    # SERVICIOS
                    # ─────────────────────────────────────────────────────
                    ft.Row(
                        controls=[
                            ft.Icon(
                                ft.Icons.SETTINGS_OUTLINED,
                                color=STAT_BLUE,
                                size=22,
                            ),
                            ft.Text(
                                "¿Qué hacemos?",
                                size=15,
                                weight=ft.FontWeight.BOLD,
                                color=TEXT_PRIMARY,
                            ),
                        ],
                        spacing=8,
                    ),

                    ft.Column(
                        spacing=8,
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Icon(
                                        ft.Icons.LOCAL_SHIPPING_OUTLINED,
                                        color=STAT_ORANGE,
                                        size=20,
                                    ),
                                    ft.Column(
                                        controls=[
                                            ft.Text(
                                                "Recolección",
                                                size=13,
                                                weight=ft.FontWeight.BOLD,
                                                color=TEXT_PRIMARY,
                                            ),
                                            ft.Text(
                                                "Recepción y traslado de neumáticos "
                                                "fuera de uso desde centros de "
                                                "acopio y empresas generadoras.",
                                                size=11,
                                                color=TEXT_SECONDARY,
                                            ),
                                        ],
                                        spacing=2,
                                        expand=True,
                                    ),
                                ],
                                spacing=10,
                            ),

                            ft.Row(
                                controls=[
                                    ft.Icon(
                                        ft.Icons.DELETE_SWEEP_OUTLINED,
                                        color=STAT_ORANGE,
                                        size=20,
                                    ),
                                    ft.Column(
                                        controls=[
                                            ft.Text(
                                                "Clasificación",
                                                size=13,
                                                weight=ft.FontWeight.BOLD,
                                                color=TEXT_PRIMARY,
                                            ),
                                            ft.Text(
                                                "Separación y clasificación de "
                                                "materiales según sus características "
                                                "y condiciones.",
                                                size=11,
                                                color=TEXT_SECONDARY,
                                            ),
                                        ],
                                        spacing=2,
                                        expand=True,
                                    ),
                                ],
                                spacing=10,
                            ),

                            ft.Row(
                                controls=[
                                    ft.Icon(
                                        ft.Icons.BUILD_OUTLINED,
                                        color=STAT_ORANGE,
                                        size=20,
                                    ),
                                    ft.Column(
                                        controls=[
                                            ft.Text(
                                                "Trituración",
                                                size=13,
                                                weight=ft.FontWeight.BOLD,
                                                color=TEXT_PRIMARY,
                                            ),
                                            ft.Text(
                                                "Procesamiento mecánico de los "
                                                "neumáticos para obtener caucho "
                                                "reciclado y otros materiales.",
                                                size=11,
                                                color=TEXT_SECONDARY,
                                            ),
                                        ],
                                        spacing=2,
                                        expand=True,
                                    ),
                                ],
                                spacing=10,
                            ),

                            ft.Row(
                                controls=[
                                    ft.Icon(
                                        ft.Icons.CONSTRUCTION_OUTLINED,
                                        color=STAT_ORANGE,
                                        size=20,
                                    ),
                                    ft.Column(
                                        controls=[
                                            ft.Text(
                                                "Distribución",
                                                size=13,
                                                weight=ft.FontWeight.BOLD,
                                                color=TEXT_PRIMARY,
                                            ),
                                            ft.Text(
                                                "Suministro de materiales reciclados "
                                                "a empresas constructoras y proyectos "
                                                "de infraestructura.",
                                                size=11,
                                                color=TEXT_SECONDARY,
                                            ),
                                        ],
                                        spacing=2,
                                        expand=True,
                                    ),
                                ],
                                spacing=10,
                            ),
                        ],
                    ),

                    # ─────────────────────────────────────────────────────
                    # PROCESO
                    # ─────────────────────────────────────────────────────
                    ft.Container(
                        padding=16,
                        border_radius=10,
                        bgcolor=ft.Colors.with_opacity(
                            0.04,
                            TEXT_PRIMARY
                        ),
                        content=ft.Column(
                            spacing=10,
                            controls=[
                                ft.Text(
                                    "Nuestro proceso",
                                    size=14,
                                    weight=ft.FontWeight.BOLD,
                                    color=TEXT_PRIMARY,
                                ),

                                ft.Row(
                                    controls=[
                                        ft.Column(
                                            controls=[
                                                ft.Icon(
                                                    ft.Icons.LOCAL_SHIPPING,
                                                    color=STAT_BLUE,
                                                    size=24,
                                                ),
                                                ft.Text(
                                                    "1. Recolección",
                                                    size=10,
                                                    color=TEXT_SECONDARY,
                                                ),
                                            ],
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=4,
                                        ),

                                        ft.Icon(
                                            ft.Icons.ARROW_FORWARD,
                                            color=DIVIDER,
                                            size=18,
                                        ),

                                        ft.Column(
                                            controls=[
                                                ft.Icon(
                                                    ft.Icons.INVENTORY_2_OUTLINED,
                                                    color=STAT_BLUE,
                                                    size=24,
                                                ),
                                                ft.Text(
                                                    "2. Recepción",
                                                    size=10,
                                                    color=TEXT_SECONDARY,
                                                ),
                                            ],
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=4,
                                        ),

                                        ft.Icon(
                                            ft.Icons.ARROW_FORWARD,
                                            color=DIVIDER,
                                            size=18,
                                        ),

                                        ft.Column(
                                            controls=[
                                                ft.Icon(
                                                    ft.Icons.CONTENT_CUT,
                                                    color=STAT_ORANGE,
                                                    size=24,
                                                ),
                                                ft.Text(
                                                    "3. Trituración",
                                                    size=10,
                                                    color=TEXT_SECONDARY,
                                                ),
                                            ],
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=4,
                                        ),

                                        ft.Icon(
                                            ft.Icons.ARROW_FORWARD,
                                            color=DIVIDER,
                                            size=18,
                                        ),

                                        ft.Column(
                                            controls=[
                                                ft.Icon(
                                                    ft.Icons.SCALE_OUTLINED,
                                                    color=STAT_ORANGE,
                                                    size=24,
                                                ),
                                                ft.Text(
                                                    "4. Pesaje",
                                                    size=10,
                                                    color=TEXT_SECONDARY,
                                                ),
                                            ],
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=4,
                                        ),

                                        ft.Icon(
                                            ft.Icons.ARROW_FORWARD,
                                            color=DIVIDER,
                                            size=18,
                                        ),

                                        ft.Column(
                                            controls=[
                                                ft.Icon(
                                                    ft.Icons.LOCAL_SHIPPING_OUTLINED,
                                                    color=STAT_BLUE,
                                                    size=24,
                                                ),
                                                ft.Text(
                                                    "5. Distribución",
                                                    size=10,
                                                    color=TEXT_SECONDARY,
                                                ),
                                            ],
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=4,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                            ],
                        ),
                    ),

                    # ─────────────────────────────────────────────────────
                    # VALORES
                    # ─────────────────────────────────────────────────────
                    ft.Row(
                        controls=[
                            ft.Icon(
                                ft.Icons.STARS_OUTLINED,
                                color=STAT_ORANGE,
                                size=22,
                            ),
                            ft.Text(
                                "Nuestros valores",
                                size=15,
                                weight=ft.FontWeight.BOLD,
                                color=TEXT_PRIMARY,
                            ),
                        ],
                        spacing=8,
                    ),

                    ft.Row(
                        controls=[
                            ft.Container(
                                expand=True,
                                padding=12,
                                border_radius=8,
                                bgcolor=ft.Colors.with_opacity(
                                    0.05,
                                    STAT_BLUE
                                ),
                                content=ft.Column(
                                    controls=[
                                        ft.Icon(
                                            ft.Icons.ECO_OUTLINED,
                                            color=STAT_BLUE,
                                            size=22,
                                        ),
                                        ft.Text(
                                            "Responsabilidad ambiental",
                                            size=11,
                                            weight=ft.FontWeight.BOLD,
                                            color=TEXT_PRIMARY,
                                        ),
                                    ],
                                    spacing=5,
                                ),
                            ),

                            ft.Container(
                                expand=True,
                                padding=12,
                                border_radius=8,
                                bgcolor=ft.Colors.with_opacity(
                                    0.05,
                                    STAT_ORANGE
                                ),
                                content=ft.Column(
                                    controls=[
                                        ft.Icon(
                                            ft.Icons.LIGHTBULB_OUTLINE,
                                            color=STAT_ORANGE,
                                            size=22,
                                        ),
                                        ft.Text(
                                            "Innovación",
                                            size=11,
                                            weight=ft.FontWeight.BOLD,
                                            color=TEXT_PRIMARY,
                                        ),
                                    ],
                                    spacing=5,
                                ),
                            ),

                            ft.Container(
                                expand=True,
                                padding=12,
                                border_radius=8,
                                bgcolor=ft.Colors.with_opacity(
                                    0.05,
                                    STAT_BLUE
                                ),
                                content=ft.Column(
                                    controls=[
                                        ft.Icon(
                                            ft.Icons.GROUP_OUTLINED,
                                            color=STAT_BLUE,
                                            size=22,
                                        ),
                                        ft.Text(
                                            "Trabajo en equipo",
                                            size=11,
                                            weight=ft.FontWeight.BOLD,
                                            color=TEXT_PRIMARY,
                                        ),
                                    ],
                                    spacing=5,
                                ),
                            ),

                            ft.Container(
                                expand=True,
                                padding=12,
                                border_radius=8,
                                bgcolor=ft.Colors.with_opacity(
                                    0.05,
                                    STAT_ORANGE
                                ),
                                content=ft.Column(
                                    controls=[
                                        ft.Icon(
                                            ft.Icons.VERIFIED_OUTLINED,
                                            color=STAT_ORANGE,
                                            size=22,
                                        ),
                                        ft.Text(
                                            "Calidad",
                                            size=11,
                                            weight=ft.FontWeight.BOLD,
                                            color=TEXT_PRIMARY,
                                        ),
                                    ],
                                    spacing=5,
                                ),
                            ),
                        ],
                        spacing=10,
                    ),

                    # ─────────────────────────────────────────────────────
                    # DATOS GENERALES
                    # ─────────────────────────────────────────────────────
                    ft.Container(
                        padding=16,
                        border_radius=10,
                        border=ft.Border.all(1, DIVIDER),
                        content=ft.Column(
                            spacing=8,
                            controls=[
                                ft.Text(
                                    "Datos generales",
                                    size=14,
                                    weight=ft.FontWeight.BOLD,
                                    color=TEXT_PRIMARY,
                                ),

                                ft.Row(
                                    controls=[
                                        ft.Icon(
                                            ft.Icons.CALENDAR_TODAY_OUTLINED,
                                            size=17,
                                            color=TEXT_SECONDARY,
                                        ),
                                        ft.Text(
                                            "Inicio de operaciones: 2018",
                                            size=12,
                                            color=TEXT_SECONDARY,
                                        ),
                                    ],
                                    spacing=8,
                                ),

                                ft.Row(
                                    controls=[
                                        ft.Icon(
                                            ft.Icons.LOCATION_ON_OUTLINED,
                                            size=17,
                                            color=TEXT_SECONDARY,
                                        ),
                                        ft.Text(
                                            "Zona de operaciones: Región Centro de México",
                                            size=12,
                                            color=TEXT_SECONDARY,
                                        ),
                                    ],
                                    spacing=8,
                                ),

                                ft.Row(
                                    controls=[
                                        ft.Icon(
                                            ft.Icons.RECYCLING_OUTLINED,
                                            size=17,
                                            color=TEXT_SECONDARY,
                                        ),
                                        ft.Text(
                                            "Especialidad: Reciclaje y aprovechamiento de neumáticos",
                                            size=12,
                                            color=TEXT_SECONDARY,
                                        ),
                                    ],
                                    spacing=8,
                                ),

                                ft.Row(
                                    controls=[
                                        ft.Icon(
                                            ft.Icons.BUSINESS_OUTLINED,
                                            size=17,
                                            color=TEXT_SECONDARY,
                                        ),
                                        ft.Text(
                                            "Clientes principales: Constructoras e industrias",
                                            size=12,
                                            color=TEXT_SECONDARY,
                                        ),
                                    ],
                                    spacing=8,
                                ),
                            ],
                        ),
                    ),

                    # ─────────────────────────────────────────────────────
                    # FRASE FINAL
                    # ─────────────────────────────────────────────────────
                    ft.Container(
                        padding=18,
                        border_radius=10,
                        bgcolor=ft.Colors.with_opacity(
                            0.08,
                            STAT_ORANGE
                        ),
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=6,
                            controls=[
                                ft.Icon(
                                    ft.Icons.ECO,
                                    color=STAT_ORANGE,
                                    size=26,
                                ),
                                ft.Text(
                                    "“Transformamos residuos en oportunidades.”",
                                    size=14,
                                    italic=True,
                                    weight=ft.FontWeight.BOLD,
                                    color=TEXT_PRIMARY,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                ft.Text(
                                    "Neusomic · Gestión responsable de materiales",
                                    size=11,
                                    color=TEXT_SECONDARY,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        ),

        actions=[
            ft.TextButton(
                "Cerrar",
                style=ft.ButtonStyle(
                    color=STAT_BLUE,
                ),
                on_click=close_about,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    return dialog



# ── Top bar ──────────────────────────────────────────────────────────────────
def topbar(page: ft.Page, active_route: str):
    #dialog = about_dialog(page)

    TITULOS = {
        "/dashboard_admin": "Dashboard",
        "/usuarios": "Empleados",
        "/neumaticos": "Monitor de transporte",
        "/desechos": "Desechos",
        "/reportes": "Reportes",
        "/transporte": "Transporte",
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

                ft.Text("Administrador", size=14, color="rgba(255,255,255,0.5"),
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
            stat_card("Ingreso neumáticos", "4,850", "+12% vs mes anterior", STAT_ORANGE),
            stat_card("Pedidos constructoras", "32", "Solicitudes recibidas", STAT_BLUE),
            stat_card("Volumen pavimento", "28,400 Kg", "Producción actual", STAT_TEAL),
            stat_card("Bajas de productos", "18", "Justificado por daño", STAT_PINK),
        ],
        spacing=12,
        expand=True,
    )


# ── Main dashboard view ──────────────────────────────────────────────────────
def dashboard_admin(page: ft.Page, on_navigate=None, on_logout=None):
    active_route = "/dashboard_admin"

    dialog = about_dialog(page)

    def open_about(e):
        print("CLICK EN INFO")

        page.overlay.append(dialog)
        dialog.open = True
        page.update()


    info_button = ft.Container(
        content=ft.Icon(
            ft.Icons.INFO_OUTLINE,
            color="#ffffff",
            size=18
        ),
        padding=8,
        border_radius=18,
        border=ft.Border.all(1, "#ffffff"),
        ink=True,
        tooltip="Saber más sobre nosotros",
        on_click=open_about,
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
        route="/dashboard_admin",
        padding=0,
        bgcolor=MAIN_BG,
        controls=[
            ft.Column(
                controls=[
                    topbar(page, active_route),
                    ft.Row(
                        controls=[
                            sidebar(active_route=active_route, on_navigate=on_navigate, on_logout = on_logout),
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
