import flet as ft
import flet_charts as fch

from ui.colors import *
from dao.inventario_dao import InventarioDAO
from dao.reporteVul_dao import ReportVulDAO


ESTADO_COLORES_REPORTE = {
    "Pendiente": STAT_ORANGE,
    "Asignado": STAT_BLUE,
    "Completado": STAT_TEAL,
    "Cancelado": "#9ca3af",
}


# ── Sidebar ──────────────────────────────────────────────────────────────────
def sidebar(
    active_route: str = "/dashboard_vulcanizadora",
    on_navigate=None,
    on_logout=None,
):
    items = [
        (
            "/dashboard_vulcanizadora",
            "Panel principal",
            ft.Icons.DASHBOARD_ROUNDED,
            True,
        ),
        (
            "/inventarioV",
            "Inventario de \n neumáticos",
            ft.Icons.CAR_REPAIR,
            False,
        ),
        (
            "/solicitudes",
            "Mis Solicitudes",
            ft.Icons.RECEIPT_LONG_ROUNDED,
            False,
        ),
        (
            "/perfil",
            "Mi perfil",
            ft.Icons.PERSON_ROUNDED,
            False,
        ),
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
                        color=(
                            SIDEBAR_ACTIVE
                            if is_active
                            else SIDEBAR_TEXT
                        ),
                        size=18,
                    ),
                    ft.Text(
                        label,
                        size=12,
                        color=(
                            SIDEBAR_TEXT_ACTIVE
                            if is_active
                            else SIDEBAR_TEXT
                        ),
                    ),
                ],
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding.symmetric(
                horizontal=24,
                vertical=16,
            ),
            border_radius=8,
            bgcolor=(
                ft.Colors.with_opacity(
                    0.18,
                    SIDEBAR_ACTIVE,
                )
                if is_active
                else None
            ),
            border=(
                ft.Border(
                    left=ft.BorderSide(
                        3,
                        SIDEBAR_ACTIVE,
                    )
                )
                if is_active
                else None
            ),
        )

    async def logout_click(e):
        if on_logout:
            await on_logout()

    return ft.Container(
        width=220,
        bgcolor=SIDEBAR_BG,
        padding=ft.Padding.only(
            left=10,
            right=10,
            top=18,
            bottom=14,
        ),
        content=ft.Column(
            controls=[
                ft.Divider(
                    height=1,
                    color=DIVIDER,
                ),

                ft.Container(height=10),

                *[nav_item(*it) for it in items],

                ft.Container(expand=True),

                ft.Divider(
                    height=1,
                    color=DIVIDER,
                ),

                ft.Container(height=10),

                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(
                                ft.Icons.LOGOUT,
                                color="#f87171",
                                size=16,
                            ),
                            ft.Text(
                                "Cerrar sesión",
                                size=12,
                                color="#f87171",
                            ),
                        ],
                        spacing=8,
                    ),
                    padding=ft.Padding.symmetric(
                        horizontal=12,
                        vertical=9,
                    ),
                    border=ft.Border.all(
                        1,
                        "#f87171",
                    ),
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
    dialog = ft.AlertDialog(
        modal=True,
        bgcolor=CARD_BG,
        title=ft.Text(
            "Sobre Neusomic",
            color=TEXT_PRIMARY,
            weight=ft.FontWeight.BOLD,
        ),
        content=ft.Text(
            "Neusomic es la plataforma de gestión logística para "
            "recolección de neumáticos usados, control de inventario, "
            "trituración, pesaje de materia prima (caucho limpio) "
            "y distribución de pavimento asfáltico modificado a "
            "empresas constructoras.",
            color=TEXT_SECONDARY,
            size=13,
        ),
        actions=[
            ft.TextButton(
                "Cerrar",
                style=ft.ButtonStyle(
                    color=STAT_BLUE,
                ),
                on_click=lambda e: page.close(dialog),
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    return dialog


# ── Top bar ──────────────────────────────────────────────────────────────────
def topbar(
    page: ft.Page,
    active_route: str,
    on_refrescar=None,
):
    TITULOS = {
        "/dashboard_vulcanizadora": "Panel principal",
        "/inventarioV": "Inventario de neumáticos",
        "/solicitudes": "Mis solicitudes",
        "/perfil": "Mi perfil",
    }

    titulo = TITULOS.get(
        active_route,
        "Panel principal",
    )

    logo = ft.Image(
        src="assets/images/logo.png",
        width=100,
        height=90,
        fit=ft.BoxFit.CONTAIN,
    )

    acciones = []

    if on_refrescar:
        acciones.append(
            ft.Container(
                content=ft.IconButton(
                    icon=ft.Icons.REFRESH_ROUNDED,
                    icon_color="#f97316",
                    icon_size=18,
                    tooltip="Actualizar estadísticas",
                    on_click=on_refrescar,
                ),
                padding=0,
            )
        )
    else:
        acciones.append(
            ft.Container(
                content=ft.Icon(
                    ft.Icons.NOTIFICATIONS_NONE,
                    color="#f97316",
                    size=18,
                ),
                padding=6,
            )
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

                *acciones,

                ft.Text(
                    "vulcanizadora",
                    size=14,
                    color="rgba(255,255,255,0.5)",
                ),

                ft.Text(
                    "|",
                    size=14,
                    color="rgba(255,255,255,0.5)",
                ),

                ft.Container(
                    content=ft.Icon(
                        ft.Icons.ACCOUNT_CIRCLE,
                        color="#fff",
                        size=28,
                    ),
                    padding=6,
                    bgcolor="rgba(255,255,255,0.15)",
                    border_radius=20,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        padding=ft.Padding.symmetric(
            horizontal=24,
            vertical=3,
        ),
        bgcolor=TOPBAR_BG,
    )


# ── Estadísticas reales ───────────────────────────────────────────────────────
def _calcular_stats(vulcanizadora_id):
    """
    Consulta InventarioDAO y ReportVulDAO para armar el panel
    con datos reales de esta vulcanizadora.
    """

    resumen_inv = {}
    reportes = []

    try:
        resumen_inv = (
            InventarioDAO()
            .resumen_por_vulcanizadora(
                vulcanizadora_id
            )
            or {}
        )
    except Exception as ex:
        print(
            f"Error al obtener resumen de inventario: {ex}"
        )

    try:
        reportes = (
            ReportVulDAO()
            .get_by_vulcanizadora_admin(
                vulcanizadora_id
            )
            or []
        )
    except Exception as ex:
        print(
            f"Error al obtener reportes de desecho: {ex}"
        )

    reportes_recientes = sorted(
        reportes,
        key=lambda r: r.fecha_reporte,
        reverse=True,
    )[:5]

    return {
        "inventario_total": resumen_inv.get(
            "total",
            0,
        ),
        "inventario_bueno": resumen_inv.get(
            "bueno",
            0,
        ),
        "inventario_usado": resumen_inv.get(
            "usado",
            0,
        ),
        "inventario_desecho": resumen_inv.get(
            "para_desecho",
            0,
        ),
        "reportes_total": len(reportes),
        "reportes_pendientes": sum(
            1
            for r in reportes
            if r.estado == "Pendiente"
        ),
        "reportes_asignados": sum(
            1
            for r in reportes
            if r.estado == "Asignado"
        ),
        "reportes_completados": sum(
            1
            for r in reportes
            if r.estado == "Completado"
        ),
        "reportes_recientes": reportes_recientes,
    }


# ── Stat cards ────────────────────────────────────────────────────────────────
def stat_card(
    titulo: str,
    valor,
    icono,
    color,
):
    return ft.Container(
        expand=True,
        bgcolor=CARD_BG,
        border_radius=12,
        padding=16,
        border=ft.Border.all(
            1,
            DIVIDER,
        ),
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(
                            titulo,
                            size=12,
                            color=TEXT_SECONDARY,
                        ),
                        ft.Text(
                            str(valor),
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT_PRIMARY,
                        ),
                    ],
                    spacing=4,
                    expand=True,
                ),

                ft.Container(
                    content=ft.Icon(
                        icono,
                        color=color,
                        size=20,
                    ),
                    width=40,
                    height=40,
                    bgcolor=ft.Colors.with_opacity(
                        0.12,
                        color,
                    ),
                    border_radius=10,
                    alignment=ft.Alignment(0, 0),
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )


def stat_row(stats: dict):
    return ft.Row(
        controls=[
            stat_card(
                "Neumáticos en inventario",
                stats["inventario_total"],
                ft.Icons.TIRE_REPAIR,
                STAT_BLUE,
            ),

            stat_card(
                "En buen estado",
                stats["inventario_bueno"],
                ft.Icons.CHECK_CIRCLE_OUTLINE,
                STAT_TEAL,
            ),

            stat_card(
                "Para desecho",
                stats["inventario_desecho"],
                ft.Icons.DELETE_OUTLINE,
                STAT_RED,
            ),

            stat_card(
                "Reportes pendientes",
                stats["reportes_pendientes"],
                ft.Icons.PENDING_ACTIONS_ROUNDED,
                STAT_ORANGE,
            ),
        ],
        spacing=12,
        expand=True,
    )


# ── Leyenda ───────────────────────────────────────────────────────────────────
def _punto_leyenda(
    texto,
    color,
):
    return ft.Row(
        controls=[
            ft.Container(
                width=8,
                height=8,
                border_radius=4,
                bgcolor=color,
            ),

            ft.Text(
                texto,
                size=11,
                color=TEXT_SECONDARY,
            ),
        ],
        spacing=6,
    )


# ── Gráfica de pastel ─────────────────────────────────────────────────────────
def pie_chart_widget(stats: dict):
    bueno = stats["inventario_bueno"]
    usado = stats["inventario_usado"]
    desecho = stats["inventario_desecho"]

    total = bueno + usado + desecho

    if total == 0:

        secciones = [
            fch.PieChartSection(
                value=1,
                title="Sin datos",
                color=DIVIDER,
                radius=60,
                title_style=ft.TextStyle(
                    size=11,
                    color=TEXT_SECONDARY,
                ),
            )
        ]

    else:

        secciones = [
            fch.PieChartSection(
                value=bueno,
                title=str(bueno),
                title_position=0.55,
                color=STAT_TEAL,
                radius=60,
                title_style=ft.TextStyle(
                    size=12,
                    color="#fff",
                    weight=ft.FontWeight.BOLD,
                ),
            ),

            fch.PieChartSection(
                value=usado,
                title=str(usado),
                title_position=0.55,
                color=STAT_ORANGE,
                radius=60,
                title_style=ft.TextStyle(
                    size=12,
                    color="#fff",
                    weight=ft.FontWeight.BOLD,
                ),
            ),

            fch.PieChartSection(
                value=desecho,
                title=str(desecho),
                title_position=0.55,
                color=STAT_RED,
                radius=60,
                title_style=ft.TextStyle(
                    size=12,
                    color="#fff",
                    weight=ft.FontWeight.BOLD,
                ),
            ),
        ]

    return ft.Container(
        expand=True,
        bgcolor=CARD_BG,
        border_radius=12,
        padding=16,
        border=ft.Border.all(
            1,
            DIVIDER,
        ),
        content=ft.Column(
            controls=[
                ft.Text(
                    "Composición del inventario",
                    size=14,
                    weight=ft.FontWeight.BOLD,
                    color=TEXT_PRIMARY,
                ),

                ft.Container(height=6),

                ft.Container(
                    height=180,
                    content=fch.PieChart(
                        sections=secciones,
                        sections_space=2,
                        center_space_radius=36,
                        expand=True,
                    ),
                ),

                ft.Container(height=8),

                ft.Row(
                    controls=[
                        _punto_leyenda(
                            "Bueno",
                            STAT_TEAL,
                        ),
                        _punto_leyenda(
                            "Usado",
                            STAT_ORANGE,
                        ),
                        _punto_leyenda(
                            "Desecho",
                            STAT_RED,
                        ),
                    ],
                    spacing=14,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            spacing=0,
        ),
    )


# ── Gráfica de barras: reportes de desecho por estatus ───────────────────────
def bar_chart_widget(stats: dict):
    valores = [
        (
            "Pendiente",
            stats["reportes_pendientes"],
            STAT_ORANGE,
        ),
        (
            "Asignado",
            stats["reportes_asignados"],
            STAT_BLUE,
        ),
        (
            "Completado",
            stats["reportes_completados"],
            STAT_TEAL,
        ),
    ]

    max_valor = max(
        (v for _, v, _ in valores),
        default=0,
    ) or 1

    grupos = []
    etiquetas = []

    for i, (nombre, valor, color) in enumerate(valores):

        grupos.append(
            fch.BarChartGroup(
                x=i,
                rods=[
                    fch.BarChartRod(
                        from_y=0,
                        to_y=valor,
                        width=28,
                        color=color,
                        border_radius=6,
                        tooltip=f"{nombre}: {valor}",
                    )
                ],
            )
        )

        etiquetas.append(
            fch.ChartAxisLabel(
                value=i,
                label=ft.Container(
                    content=ft.Text(
                        nombre,
                        size=10,
                        color=TEXT_SECONDARY,
                    ),
                    padding=ft.Padding.only(
                        top=6,
                    ),
                ),
            )
        )

    return ft.Container(
        expand=True,
        bgcolor=CARD_BG,
        border_radius=12,
        padding=16,
        border=ft.Border.all(
            1,
            DIVIDER,
        ),
        content=ft.Column(
            controls=[
                ft.Text(
                    "Reportes de desecho por estatus",
                    size=14,
                    weight=ft.FontWeight.BOLD,
                    color=TEXT_PRIMARY,
                ),

                ft.Container(height=10),

                ft.Container(
                    height=180,
                    content=fch.BarChart(
                        groups=grupos,

                        border=ft.Border.all(
                            1,
                            DIVIDER,
                        ),

                        left_axis=fch.ChartAxis(
                            label_size=28,
                        ),

                        bottom_axis=fch.ChartAxis(
                            labels=etiquetas,
                            label_size=28,
                        ),

                        horizontal_grid_lines=fch.ChartGridLines(
                            color=DIVIDER,
                            width=1,
                        ),

                        max_y=max_valor + 1,

                        interactive=True,

                        expand=True,
                    ),
                ),
            ],
            spacing=0,
        ),
    )


# ── Badge de estado ───────────────────────────────────────────────────────────
def _badge_estado_reporte(
    estado: str,
):
    color = ESTADO_COLORES_REPORTE.get(
        estado,
        STAT_ORANGE,
    )

    return ft.Container(
        content=ft.Text(
            estado,
            size=11,
            color=color,
            weight=ft.FontWeight.W_600,
        ),

        padding=ft.Padding.symmetric(
            horizontal=10,
            vertical=4,
        ),

        border_radius=6,

        bgcolor=ft.Colors.with_opacity(
            0.12,
            color,
        ),

        border=ft.Border.all(
            1,
            ft.Colors.with_opacity(
                0.5,
                color,
            ),
        ),
    )


# ── Reportes recientes ────────────────────────────────────────────────────────
def reportes_recientes_widget(
    stats: dict,
    on_ver_todos=None,
):
    reportes = stats["reportes_recientes"]

    if not reportes:

        filas = [
            ft.Container(
                padding=24,
                alignment=ft.Alignment(0, 0),
                content=ft.Text(
                    "Sin reportes de desecho registrados todavía.",
                    size=12,
                    color=TEXT_SECONDARY,
                ),
            )
        ]

    else:

        filas = []

        for rep in reportes:

            filas.append(
                ft.Container(
                    padding=ft.Padding.symmetric(
                        horizontal=4,
                        vertical=10,
                    ),

                    border=ft.Border.only(
                        bottom=ft.BorderSide(
                            1,
                            DIVIDER,
                        )
                    ),

                    content=ft.Row(
                        controls=[
                            ft.Column(
                                spacing=2,
                                expand=True,
                                controls=[
                                    ft.Text(
                                        f"{rep.cantidad_llantas} neumáticos",
                                        size=13,
                                        color=TEXT_PRIMARY,
                                        weight=ft.FontWeight.W_600,
                                    ),

                                    ft.Text(
                                        f"Fecha: {rep.fecha_reporte}",
                                        size=11,
                                        color=TEXT_SECONDARY,
                                    ),
                                ],
                            ),

                            _badge_estado_reporte(
                                rep.estado
                            ),
                        ],

                        vertical_alignment=(
                            ft.CrossAxisAlignment.CENTER
                        ),
                    ),
                )
            )

    return ft.Container(
        expand=True,
        bgcolor=CARD_BG,
        border_radius=12,
        padding=16,

        border=ft.Border.all(
            1,
            DIVIDER,
        ),

        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(
                            "Reportes de desecho recientes",
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT_PRIMARY,
                        ),

                        ft.Container(
                            expand=True
                        ),

                        ft.TextButton(
                            "Ver todos",

                            style=ft.ButtonStyle(
                                color=STAT_BLUE
                            ),

                            on_click=(
                                lambda e: on_ver_todos(e)
                            )
                            if on_ver_todos
                            else None,
                        ),
                    ],
                ),

                ft.Divider(
                    height=1,
                    color=DIVIDER,
                ),

                ft.Column(
                    controls=filas,
                    spacing=0,
                ),
            ],

            spacing=8,
        ),
    )


# ── Main dashboard view ──────────────────────────────────────────────────────
def dashboard_vulcanizadora(
    page: ft.Page,
    vulcanizadora_id,
    on_navigate=None,
    on_logout=None,
):

    active_route = "/dashboard_vulcanizadora"

    columna_ref = ft.Ref[ft.Column]()

    def _construir_controles(stats):

        def ir_a_solicitudes(e=None):
            if on_navigate:
                page.run_task(
                    on_navigate,
                    "/solicitudes",
                )

        return [
            stat_row(stats),

            ft.Container(height=12),

            ft.Row(
                controls=[
                    pie_chart_widget(stats),
                    bar_chart_widget(stats),
                ],
                spacing=12,
                expand=True,
            ),

            ft.Container(height=12),

            reportes_recientes_widget(
                stats,
                on_ver_todos=ir_a_solicitudes,
            ),
        ]

    def refrescar(e=None):

        nuevos_stats = _calcular_stats(
            vulcanizadora_id
        )

        columna_ref.current.controls = (
            _construir_controles(
                nuevos_stats
            )
        )

        columna_ref.current.update()

    stats_iniciales = _calcular_stats(
        vulcanizadora_id
    )

    info_button = ft.Container(
        content=ft.Icon(
            ft.Icons.INFO_OUTLINE,
            color="#ffffff",
            size=18,
        ),

        padding=8,

        border_radius=18,

        border=ft.Border.all(
            1,
            "#ffffff",
        ),

        ink=True,

        tooltip="Saber más sobre nosotros",

        on_click=lambda e: page.open(
            about_dialog(page)
        ),
    )

    content_area = ft.Stack(
        controls=[
            ft.Container(
                expand=True,
                padding=20,
                bgcolor=MAIN_BG,

                content=ft.Column(
                    ref=columna_ref,

                    controls=_construir_controles(
                        stats_iniciales
                    ),

                    spacing=0,

                    scroll=ft.ScrollMode.AUTO,

                    expand=True,
                ),
            ),

            ft.Container(
                content=info_button,
                right=20,
                bottom=20,
            ),
        ],

        expand=True,
    )

    return ft.View(
        route="/dashboard_vulcanizadora",

        padding=0,

        bgcolor=MAIN_BG,

        controls=[
            ft.Column(
                controls=[
                    topbar(
                        page,
                        active_route,
                        on_refrescar=refrescar,
                    ),

                    ft.Row(
                        controls=[
                            sidebar(
                                active_route=active_route,
                                on_navigate=on_navigate,
                                on_logout=on_logout,
                            ),

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
