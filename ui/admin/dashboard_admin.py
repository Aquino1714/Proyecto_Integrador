from datetime import date

import flet as ft

from ui.colors import *
from ui.notifications import NotificationManager
from ui.admin.components import (
    stat_card,
    grafica_barras,
    grafica_pastel,
    lista_actividad_reciente,
)

from dao.empleado_dao import EmpleadoDAO
from dao.transporte_dao import TransportDAO          # ← AJUSTAR si el path real es distinto
from dao.reporteVul_dao import ReportVulDAO
from dao.reportesEmp_dao import ReportsEmpDAO


# ── Catálogos locales (duplicados a propósito, mismo patrón que el resto de
#    los módulos admin, para evitar imports circulares con dashboard_admin) ──
ROLES_MAP = {
    1: "Administrador",
    2: "Chofer",
    3: "Recepcion",
    4: "Almacen",
    5: "Triturador",
    6: "Distribucion",
}

ROL_COLORES = {
    "Administrador": STAT_BLUE,
    "Chofer": STAT_TEAL,
    "Recepcion": STAT_ORANGE,
    "Almacen": "#a855f7",
    "Triturador": "#ef4444",
    "Distribucion": "#eab308",
}

ESTADO_TRANSPORTE_COLORES = {
    "Disponible": STAT_BLUE,
    "En viaje": STAT_ORANGE,
    "Mantenimiento": "#9ca3af",
    "Fuera de servicio": "#ef4444",
}

ESTADO_DESECHO_COLORES = {
    "Pendiente": STAT_ORANGE,
    "Asignado": STAT_BLUE,
    "Completado": STAT_TEAL,
    "Cancelado": "#9ca3af",
}

ESTADO_EMP_COLORES = {
    "Pendiente": STAT_ORANGE,
    "Resuelto": STAT_TEAL,
}


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


def boton_informacion(on_click=None):
    return ft.Container(
        content=ft.IconButton(
            icon=ft.Icons.INFO_OUTLINE,
            icon_color="#ffffff",
            icon_size=18,
            tooltip="Saber más sobre nosotros",
            style=ft.ButtonStyle(
                bgcolor="transparent",
                shape=ft.RoundedRectangleBorder(radius=50),
                side=ft.BorderSide(width=2, color="#ffffff"),
            ),
            on_click=on_click,
        ),
        right=20,
        bottom=20,
    )


# ── Obtención y agregación de datos ─────────────────────────────────────────
def _obtener_metricas():
    """
    Consulta los DAOs y agrega la información necesaria para el dashboard.
    Devuelve un dict con listas/contadores listos para renderizar.
    Si alguna consulta falla, esa sección regresa vacía (no tumba el dashboard).
    """
    empleados, transportes, reportes_desecho, reportes_emp = [], [], [], []
    errores = []

    try:
        empleados = EmpleadoDAO().get_all()
    except Exception as ex:
        errores.append(f"Empleados: {ex}")

    try:
        transportes = TransportDAO().get_all()
    except Exception as ex:
        errores.append(f"Transporte: {ex}")

    try:
        reportes_desecho = ReportVulDAO().get_all_admin()
    except Exception as ex:
        errores.append(f"Reportes de desecho: {ex}")

    try:
        reportes_emp = ReportsEmpDAO().get_all_admin()
    except Exception as ex:
        errores.append(f"Reportes de empleados: {ex}")

    # ── Empleados ──
    empleados_activos = [e for e in empleados if getattr(e, "active", False)]
    empleados_inactivos = len(empleados) - len(empleados_activos)

    conteo_por_rol = {rol: 0 for rol in ROLES_MAP.values()}
    for e in empleados_activos:
        rol = ROLES_MAP.get(getattr(e, "id_rol", None))
        if rol:
            conteo_por_rol[rol] += 1

    # ── Transporte ──
    conteo_transporte = {estado: 0 for estado in ESTADO_TRANSPORTE_COLORES}
    for t in transportes:
        estado = getattr(t, "estado", None)
        if estado in conteo_transporte:
            conteo_transporte[estado] += 1

    # ── Reportes de desecho (vulcanizadoras) ──
    conteo_desecho = {estado: 0 for estado in ESTADO_DESECHO_COLORES}
    for r in reportes_desecho:
        estado = getattr(r, "estado", None)
        if estado in conteo_desecho:
            conteo_desecho[estado] += 1

    # ── Reportes internos de empleados ──
    conteo_emp = {estado: 0 for estado in ESTADO_EMP_COLORES}
    for r in reportes_emp:
        estado = getattr(r, "estado", None)
        if estado in conteo_emp:
            conteo_emp[estado] += 1

    return {
        "empleados": empleados,
        "empleados_activos": len(empleados_activos),
        "empleados_inactivos": empleados_inactivos,
        "conteo_por_rol": conteo_por_rol,
        "transportes": transportes,
        "conteo_transporte": conteo_transporte,
        "reportes_desecho": reportes_desecho,
        "conteo_desecho": conteo_desecho,
        "reportes_emp": reportes_emp,
        "conteo_emp": conteo_emp,
        "errores": errores,
    }


def _mas_recientes(lista, campo_fecha="fecha_reporte", estado_prioritario="Pendiente", limite=5):
    """Ordena priorizando el estado indicado y luego por fecha descendente."""
    try:
        prioritarios = [x for x in lista if getattr(x, "estado", None) == estado_prioritario]
        resto = [x for x in lista if getattr(x, "estado", None) != estado_prioritario]

        clave = lambda x: getattr(x, campo_fecha, None) or date.min
        prioritarios = sorted(prioritarios, key=clave, reverse=True)
        resto = sorted(resto, key=clave, reverse=True)
        return (prioritarios + resto)[:limite]
    except Exception:
        return list(lista)[:limite]


# ── Construcción del contenido del dashboard ────────────────────────────────
def _construir_kpis(m: dict):
    total_transportes = len(m["transportes"])
    disponibles = m["conteo_transporte"].get("Disponible", 0)
    en_viaje = m["conteo_transporte"].get("En viaje", 0)
    mantenimiento = m["conteo_transporte"].get("Mantenimiento", 0)

    pendientes_desecho = m["conteo_desecho"].get("Pendiente", 0)
    asignados_desecho = m["conteo_desecho"].get("Asignado", 0)
    completados_desecho = m["conteo_desecho"].get("Completado", 0)

    pendientes_emp = m["conteo_emp"].get("Pendiente", 0)
    resueltos_emp = m["conteo_emp"].get("Resuelto", 0)

    return ft.Row(
        spacing=14,
        controls=[
            stat_card(
                titulo="Empleados activos",
                valor=str(m["empleados_activos"]),
                subtitulo=f"{m['empleados_inactivos']} dados de baja",
                color=STAT_BLUE,
                icon=ft.Icons.BADGE_OUTLINED,
            ),
            stat_card(
                titulo="Flotilla disponible",
                valor=f"{disponibles}/{total_transportes}",
                subtitulo=f"{en_viaje} en viaje · {mantenimiento} en mantenimiento",
                color=STAT_TEAL,
                icon=ft.Icons.LOCAL_SHIPPING_OUTLINED,
            ),
            stat_card(
                titulo="Reportes de desecho pendientes",
                valor=str(pendientes_desecho),
                subtitulo=f"{asignados_desecho} asignados · {completados_desecho} completados",
                color=STAT_ORANGE,
                icon=ft.Icons.DELETE_OUTLINED,
            ),
            stat_card(
                titulo="Reportes internos pendientes",
                valor=str(pendientes_emp),
                subtitulo=f"{resueltos_emp} resueltos",
                color="#ef4444",
                icon=ft.Icons.ANALYTICS_OUTLINED,
            ),
        ],
    )


def _construir_graficas(m: dict, ir_a_transporte, ir_a_desechos):
    categorias_rol = list(m["conteo_por_rol"].keys())
    valores_rol = [m["conteo_por_rol"][r] for r in categorias_rol]
    colores_rol = [ROL_COLORES.get(r, STAT_PINK) for r in categorias_rol]

    grafica_empleados = grafica_barras(
        titulo="Plantilla por rol",
        subtitulo="Empleados activos",
        categorias=categorias_rol,
        valores=valores_rol,
        colores=colores_rol,
        icon=ft.Icons.GROUPS_OUTLINED,
        icon_color=STAT_BLUE,
    )

    secciones_transporte = [
        (estado, m["conteo_transporte"].get(estado, 0), color)
        for estado, color in ESTADO_TRANSPORTE_COLORES.items()
    ]
    grafica_transporte = grafica_pastel(
        titulo="Estado de la flotilla",
        subtitulo="Distribución actual",
        secciones=secciones_transporte,
        icon=ft.Icons.LOCAL_SHIPPING_OUTLINED,
        icon_color=STAT_TEAL,
    )

    secciones_desecho = [
        (estado, m["conteo_desecho"].get(estado, 0), color)
        for estado, color in ESTADO_DESECHO_COLORES.items()
    ]
    grafica_desecho = grafica_pastel(
        titulo="Reportes de desecho",
        subtitulo="Por estatus",
        secciones=secciones_desecho,
        icon=ft.Icons.RECYCLING_OUTLINED,
        icon_color=STAT_ORANGE,
    )

    return ft.Row(
        spacing=14,
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[grafica_empleados, grafica_transporte, grafica_desecho],
    )


def _construir_actividad(m: dict, ir_a_desechos, ir_a_reportes):
    recientes_desecho = _mas_recientes(m["reportes_desecho"], "fecha_reporte", "Pendiente")
    items_desecho = [
        {
            "titulo": f"{getattr(r, 'vulcanizadora_nombre', '—')} · "
                      f"{getattr(r, 'cantidad_llantas', 0)} neumáticos",
            "subtitulo": f"Reportado: {getattr(r, 'fecha_reporte', '—')}",
            "estado": getattr(r, "estado", "—"),
            "color_estado": ESTADO_DESECHO_COLORES.get(getattr(r, "estado", None), STAT_ORANGE),
        }
        for r in recientes_desecho
    ]

    recientes_emp = _mas_recientes(m["reportes_emp"], "fecha_reporte", "Pendiente")
    items_emp = [
        {
            "titulo": f"{getattr(r, 'asunto', '—')} — {getattr(r, 'empleado_nombre', '—')}",
            "subtitulo": f"{getattr(r, 'rol_nombre', '—') or '—'} · {getattr(r, 'fecha_reporte', '—')}",
            "estado": getattr(r, "estado", "—"),
            "color_estado": ESTADO_EMP_COLORES.get(getattr(r, "estado", None), STAT_ORANGE),
        }
        for r in recientes_emp
    ]

    lista_desecho = lista_actividad_reciente(
        titulo="Reportes de desecho recientes",
        subtitulo="Vulcanizadoras · prioriza pendientes",
        items=items_desecho,
        icon=ft.Icons.DELETE_OUTLINED,
        icon_color=STAT_ORANGE,
        on_click_item=lambda item: ir_a_desechos(),
        on_ver_todos=lambda e: ir_a_desechos(),
        texto_vacio="No hay reportes de desecho registrados.",
    )

    lista_emp = lista_actividad_reciente(
        titulo="Reportes internos recientes",
        subtitulo="Choferes, recepción, almacén y trituración",
        items=items_emp,
        icon=ft.Icons.ANALYTICS_OUTLINED,
        icon_color="#ef4444",
        on_click_item=lambda item: ir_a_reportes(),
        on_ver_todos=lambda e: ir_a_reportes(),
        texto_vacio="No hay reportes internos registrados.",
    )

    return ft.Row(spacing=14, controls=[lista_desecho, lista_emp])


# ── Contenido principal del dashboard ───────────────────────────────────────
def dashboard_content(page: ft.Page, on_navigate=None):
    notify = NotificationManager(page)

    contenido_ref = ft.Ref[ft.Column]()

    def ir_a(ruta):
        if on_navigate:
            page.run_task(on_navigate, ruta)

    def ir_a_transporte():
        ir_a("/transporte")

    def ir_a_desechos():
        ir_a("/desechos")

    def ir_a_reportes():
        ir_a("/reportes")

    def _construir():
        m = _obtener_metricas()

        if m["errores"]:
            page.run_task(
                notify.show,
                "No se pudieron cargar algunos datos del dashboard.",
                "warning",
            )

        return [
            _construir_kpis(m),
            _construir_graficas(
                m,
                ir_a_transporte,
                ir_a_desechos,
            ),
            _construir_actividad(
                m,
                ir_a_desechos,
                ir_a_reportes,
            ),
            ft.Container(height=6),
        ]

    def actualizar(e=None):
        contenido_ref.current.controls = _construir()
        contenido_ref.current.update()

    encabezado = ft.Row(
        controls=[
            ft.Column(
                spacing=1,
                tight=True,
                controls=[
                    ft.Text(
                        "Resumen general",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=TEXT_PRIMARY,
                    ),
                    ft.Text(
                        "Vista consolidada de operaciones de Neusomic",
                        size=12,
                        color=TEXT_SECONDARY,
                    ),
                ],
            ),
            ft.Container(expand=True),
            ft.OutlinedButton(
                content=ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.REFRESH,
                            size=16,
                            color=STAT_BLUE,
                        ),
                        ft.Text(
                            "Actualizar",
                            size=12,
                            color=STAT_BLUE,
                            weight=ft.FontWeight.W_600,
                        ),
                    ],
                    spacing=6,
                    tight=True,
                ),
                style=ft.ButtonStyle(
                    color=STAT_BLUE,
                    side=ft.BorderSide(1, STAT_BLUE),
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
                on_click=actualizar,
            ),
        ],
    )

    contenido = ft.Column(
        ref=contenido_ref,
        spacing=16,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        controls=_construir(),
    )

    return ft.Column(
        spacing=16,
        expand=True,
        controls=[
            encabezado,
            contenido,
        ],
    )



# ── Vista completa (Stack con botón de info + modal) ────────────────────────
def dashboard_admin(page: ft.Page, on_navigate=None, on_logout=None):
    active_route = "/dashboard_admin"

    dialog = about_dialog(page)

    def open_about(e):
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    content_area = ft.Stack(
        controls=[
            ft.Container(
                expand=True,
                padding=20,
                bgcolor=MAIN_BG,
                content=dashboard_content(page, on_navigate=on_navigate),
            ),
            boton_informacion(on_click=open_about),
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
                            sidebar(active_route=active_route, on_navigate=on_navigate, on_logout=on_logout),
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