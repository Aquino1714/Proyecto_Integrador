import flet as ft

from flet_charts import (
    BarChart,
    BarChartGroup,
    BarChartRod,
    PieChart,
    PieChartSection,
    ChartAxis,
    ChartAxisLabel,
    ChartGridLines,
)

from ui.colors import *


# =============================================================================
# HELPERS / CONTENEDORES
# =============================================================================

def _card_container(
    content,
    expand=True,
    padding=20,
    height=None,
    width=None,
):
    """
    Contenedor principal de tarjetas.
    Combina el estilo profesional del primer código
    con el efecto glass del segundo.
    """
    return ft.Container(
        expand=expand,
        width=width,
        height=height,
        padding=padding,
        bgcolor=CARD_BG,
        border=ft.Border.all(1, GLASS_BORDER),
        border_radius=14,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=18,
            color=ft.Colors.with_opacity(0.10, "#000000"),
            offset=ft.Offset(0, 4),
        ),
        content=content,
    )


def glass_card(
    content,
    padding=16,
    expand=False,
    width=None,
    height=None,
):
    """
    Alias compatible con el segundo código.
    """
    return _card_container(
        content=content,
        padding=padding,
        expand=expand,
        width=width,
        height=height,
    )


def _encabezado_card(
    titulo: str,
    subtitulo: str = None,
    icon=None,
    icon_color=None,
):
    controles = []

    color_icono = icon_color or STAT_BLUE

    if icon:
        controles.append(
            ft.Container(
                width=34,
                height=34,
                border_radius=9,
                alignment=ft.Alignment.CENTER,
                bgcolor=ft.Colors.with_opacity(0.12, color_icono),
                content=ft.Icon(
                    icon,
                    size=17,
                    color=color_icono,
                ),
            )
        )

        controles.append(ft.Container(width=10))

    textos = [
        ft.Text(
            titulo,
            size=14,
            weight=ft.FontWeight.BOLD,
            color=TEXT_PRIMARY,
        )
    ]

    if subtitulo:
        textos.append(
            ft.Text(
                subtitulo,
                size=11,
                color=TEXT_SECONDARY,
            )
        )

    controles.append(
        ft.Column(
            controls=textos,
            spacing=1,
            tight=True,
            expand=True,
        )
    )

    return ft.Row(
        controls=controles,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


# =============================================================================
# KPI / STAT CARD
# =============================================================================

def stat_card(
    titulo: str = None,
    valor: str = None,
    subtitulo: str = "",
    color=STAT_BLUE,
    icon=ft.Icons.INSIGHTS_OUTLINED,
    tendencia: float = None,
    on_click=None,

    # Compatibilidad con el segundo código
    title: str = None,
    value: str = None,
    subtitle: str = None,
    value_color: str = None,
    expand: bool = True,
):
    """
    Tarjeta KPI unificada.

    Compatible con ambos estilos:

    stat_card(
        titulo="Ingresos",
        valor="$120,000",
        subtitulo="Este mes",
        color=STAT_BLUE,
        tendencia=12.5,
    )

    También acepta:

    stat_card(
        title="Ingresos",
        value="$120,000",
        subtitle="Este mes",
        value_color=STAT_BLUE,
    )
    """

    titulo = titulo or title or ""
    valor = valor or value or ""
    subtitulo = subtitulo or subtitle or ""
    color = value_color or color

    chip_tendencia = None

    if tendencia is not None:
        positivo = tendencia >= 0

        color_tendencia = (
            STAT_TEAL
            if positivo
            else "#ef4444"
        )

        icono_tendencia = (
            ft.Icons.TRENDING_UP
            if positivo
            else ft.Icons.TRENDING_DOWN
        )

        chip_tendencia = ft.Container(
            padding=ft.Padding.symmetric(
                horizontal=8,
                vertical=3,
            ),
            border_radius=20,
            bgcolor=ft.Colors.with_opacity(
                0.12,
                color_tendencia,
            ),
            content=ft.Row(
                controls=[
                    ft.Icon(
                        icono_tendencia,
                        size=12,
                        color=color_tendencia,
                    ),
                    ft.Text(
                        f"{tendencia:+.1f}%",
                        size=11,
                        weight=ft.FontWeight.W_600,
                        color=color_tendencia,
                    ),
                ],
                spacing=3,
                tight=True,
            ),
        )

    return ft.Container(
        expand=expand,
        padding=18,
        bgcolor=CARD_BG,
        border_radius=14,
        ink=on_click is not None,
        on_click=(
            lambda e: on_click(e)
            if on_click
            else None
        ),
        border=ft.Border.all(
            1,
            GLASS_BORDER,
        ),
        shadow=ft.BoxShadow(
            blur_radius=18,
            color=ft.Colors.with_opacity(
                0.08,
                "#000000",
            ),
            offset=ft.Offset(0, 4),
        ),
        content=ft.Column(
            spacing=10,
            tight=True,
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            width=40,
                            height=40,
                            border_radius=10,
                            alignment=ft.Alignment.CENTER,
                            bgcolor=ft.Colors.with_opacity(
                                0.12,
                                color,
                            ),
                            content=ft.Icon(
                                icon,
                                size=20,
                                color=color,
                            ),
                        ),
                        ft.Container(expand=True),

                        chip_tendencia
                        if chip_tendencia
                        else ft.Container(),
                    ],
                ),

                ft.Text(
                    valor,
                    size=26,
                    weight=ft.FontWeight.BOLD,
                    color=color,
                ),

                ft.Text(
                    titulo,
                    size=12,
                    color=TEXT_SECONDARY,
                    weight=ft.FontWeight.W_600,
                ),

                (
                    ft.Text(
                        subtitulo,
                        size=11,
                        color=TEXT_SECONDARY,
                    )
                    if subtitulo
                    else ft.Container(height=0)
                ),
            ],
        ),
    )


# =============================================================================
# GRÁFICA DE BARRAS GENÉRICA
# =============================================================================

def grafica_barras(
    titulo: str,
    categorias: list,
    valores: list,
    colores: list,
    subtitulo: str = None,
    icon=ft.Icons.BAR_CHART_OUTLINED,
    icon_color=STAT_BLUE,
    altura: int = 230,
):
    """
    Gráfica de barras reutilizable.

    categorias = ["Ene", "Feb", "Mar"]
    valores = [100, 200, 150]
    colores = ["#3b82f6", "#22c55e", "#f97316"]
    """

    if not categorias or not valores or not any(valores):
        return _card_container(
            ft.Column(
                spacing=14,
                controls=[
                    _encabezado_card(
                        titulo,
                        subtitulo,
                        icon,
                        icon_color,
                    ),
                    ft.Container(
                        height=altura,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Text(
                            "Sin datos disponibles",
                            size=12,
                            color=TEXT_SECONDARY,
                        ),
                    ),
                ],
            )
        )

    max_valor = max(valores)

    tope_y = max(
        1,
        int(max_valor * 1.25),
    )

    grupos = []
    etiquetas_eje = []

    for i, (cat, val, color) in enumerate(
        zip(categorias, valores, colores)
    ):
        grupos.append(
            BarChartGroup(
                x=i,
                rods=[
                    BarChartRod(
                        from_y=0,
                        to_y=val,
                        width=26,
                        color=color,
                        border_radius=ft.BorderRadius.only(
                            top_left=6,
                            top_right=6,
                        ),
                        tooltip=f"{cat}: {val}",
                    )
                ],
            )
        )

        etiquetas_eje.append(
            ChartAxisLabel(
                value=i,
                label=ft.Text(
                    cat,
                    size=10,
                    color=TEXT_SECONDARY,
                ),
            )
        )

    chart = BarChart(
        groups=grupos,
        interactive=True,
        max_y=tope_y,
        group_spacing=26,
        border=ft.Border.only(
            bottom=ft.BorderSide(
                1,
                DIVIDER,
            )
        ),
        horizontal_grid_lines=ChartGridLines(
            color=DIVIDER,
            width=1,
        ),
        left_axis=ChartAxis(
            label_size=32,
            show_labels=True,
        ),
        bottom_axis=ChartAxis(
            labels=etiquetas_eje,
            label_size=28,
        ),
        top_axis=ChartAxis(
            show_labels=False,
        ),
        right_axis=ChartAxis(
            show_labels=False,
        ),
        expand=True,
    )

    return _card_container(
        ft.Column(
            spacing=14,
            expand=True,
            controls=[
                _encabezado_card(
                    titulo,
                    subtitulo,
                    icon,
                    icon_color,
                ),
                ft.Container(
                    height=altura,
                    content=chart,
                ),
            ],
        )
    )


# =============================================================================
# GRÁFICA DE BARRAS - INGRESOS Y DESPACHOS
# =============================================================================

def bar_chart_widget():
    """
    Widget específico para ingresos y despachos
    de neumáticos.
    """

    months = [
        "Nov",
        "Dic",
        "Ene",
        "Feb",
        "Abr",
    ]

    blue_vals = [
        13000,
        5000,
        8000,
        9000,
        7000,
    ]

    green_vals = [
        14000,
        7000,
        18000,
        16000,
        22000,
    ]

    max_val = 28000

    def bar_pair(label, blue, green):

        blue_height = max(
            2,
            int(blue / max_val * 110),
        )

        green_height = max(
            2,
            int(green / max_val * 110),
        )

        return ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            width=14,
                            height=blue_height,
                            bgcolor="#3b82f6",
                            border_radius=3,
                        ),

                        ft.Container(
                            width=14,
                            height=green_height,
                            bgcolor="#22c55e",
                            border_radius=3,
                        ),
                    ],
                    spacing=3,
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.END,
                ),

                ft.Text(
                    label,
                    size=9,
                    color=TEXT_MUTED,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
        )

    bars = ft.Row(
        controls=[
            bar_pair(
                months[i],
                blue_vals[i],
                green_vals[i],
            )
            for i in range(len(months))
        ],
        spacing=16,
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.END,
    )

    legend = ft.Row(
        controls=[
            ft.Row(
                controls=[
                    ft.Container(
                        width=10,
                        height=10,
                        bgcolor="#3b82f6",
                        border_radius=2,
                    ),
                    ft.Text(
                        "Ingresos",
                        size=10,
                        color=TEXT_SECONDARY,
                    ),
                ],
                spacing=4,
            ),

            ft.Row(
                controls=[
                    ft.Container(
                        width=10,
                        height=10,
                        bgcolor="#22c55e",
                        border_radius=2,
                    ),
                    ft.Text(
                        "Despachos",
                        size=10,
                        color=TEXT_SECONDARY,
                    ),
                ],
                spacing=4,
            ),
        ],
        spacing=16,
    )

    return glass_card(
        ft.Column(
            controls=[
                _encabezado_card(
                    "Ingresos y despachos",
                    "Neumáticos / volumen",
                    ft.Icons.BAR_CHART_OUTLINED,
                    STAT_BLUE,
                ),

                ft.Container(height=8),

                bars,

                ft.Container(height=6),

                legend,
            ],
            spacing=0,
        ),
        padding=20,
        expand=True,
        height=230,
    )


# =============================================================================
# GRÁFICA DE PASTEL GENÉRICA
# =============================================================================

def _item_leyenda(
    color,
    etiqueta,
    valor,
):
    return ft.Row(
        controls=[
            ft.Container(
                width=9,
                height=9,
                border_radius=5,
                bgcolor=color,
            ),

            ft.Text(
                etiqueta,
                size=12,
                color=TEXT_SECONDARY,
                expand=True,
            ),

            ft.Text(
                str(valor),
                size=12,
                weight=ft.FontWeight.W_600,
                color=TEXT_PRIMARY,
            ),
        ],
        spacing=8,
    )


def grafica_pastel(
    titulo: str,
    secciones: list,
    subtitulo: str = None,
    icon=ft.Icons.PIE_CHART_OUTLINE,
    icon_color=STAT_ORANGE,
    altura: int = 190,
):
    """
    secciones:

    [
        ("Camión pesado", 65, "#3b82f6"),
        ("Vehículo particular", 35, "#1e40af"),
    ]
    """

    total = sum(
        valor
        for _, valor, _ in secciones
    )

    if total <= 0:
        return _card_container(
            ft.Column(
                spacing=14,
                controls=[
                    _encabezado_card(
                        titulo,
                        subtitulo,
                        icon,
                        icon_color,
                    ),

                    ft.Container(
                        height=altura,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Text(
                            "Sin datos disponibles",
                            size=12,
                            color=TEXT_SECONDARY,
                        ),
                    ),
                ],
            )
        )

    pie_sections = [
        PieChartSection(
            value=valor,
            color=color,
            radius=52,
            title=(
                f"{round(valor / total * 100)}%"
                if valor > 0
                else ""
            ),
            title_style=ft.TextStyle(
                size=11,
                weight=ft.FontWeight.BOLD,
                color="#ffffff",
            ),
        )

        for etiqueta, valor, color in secciones

        if valor > 0
    ]

    chart = PieChart(
        sections=pie_sections,
        sections_space=2,
        center_space_radius=34,
        expand=True,
    )

    leyenda = ft.Column(
        spacing=8,
        controls=[
            _item_leyenda(
                color,
                etiqueta,
                valor,
            )
            for etiqueta, valor, color in secciones
        ],
    )

    return _card_container(
        ft.Column(
            spacing=14,
            expand=True,
            controls=[
                _encabezado_card(
                    titulo,
                    subtitulo,
                    icon,
                    icon_color,
                ),

                ft.Row(
                    spacing=18,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            width=altura,
                            height=altura,
                            content=chart,
                        ),

                        ft.Container(
                            expand=True,
                            content=leyenda,
                        ),
                    ],
                ),
            ],
        )
    )


# =============================================================================
# RADIAL CHART - HISTORIAL DE RECOLECCIÓN
# =============================================================================

def pie_chart_widget():

    ring = ft.Stack(
        controls=[
            ft.ProgressRing(
                value=1.0,
                stroke_width=14,
                color="#1e40af",
                width=120,
                height=120,
            ),

            ft.ProgressRing(
                value=0.65,
                stroke_width=14,
                color="#3b82f6",
                width=120,
                height=120,
            ),

            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "65%",
                            size=20,
                            color="#ffffff",
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                        ),

                        ft.Text(
                            "Camión",
                            size=9,
                            color=TEXT_SECONDARY,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    spacing=0,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                width=120,
                height=120,
                alignment=ft.Alignment.CENTER,
            ),
        ],
        width=120,
        height=120,
    )

    legend = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Container(
                        width=10,
                        height=10,
                        bgcolor="#3b82f6",
                        border_radius=2,
                    ),
                    ft.Text(
                        "Camión Pesado  65%",
                        size=10,
                        color=TEXT_SECONDARY,
                    ),
                ],
                spacing=6,
            ),

            ft.Row(
                controls=[
                    ft.Container(
                        width=10,
                        height=10,
                        bgcolor="#1e40af",
                        border_radius=2,
                    ),
                    ft.Text(
                        "Veh. Particular  35%",
                        size=10,
                        color=TEXT_SECONDARY,
                    ),
                ],
                spacing=6,
            ),
        ],
        spacing=8,
    )

    return glass_card(
        ft.Column(
            controls=[
                _encabezado_card(
                    "Historial de recolección",
                    "Por tipo de transporte",
                    ft.Icons.PIE_CHART_OUTLINE,
                    STAT_BLUE,
                ),

                ft.Container(height=8),

                ft.Row(
                    controls=[
                        ft.Container(
                            content=ring,
                            width=130,
                            height=130,
                        ),

                        legend,
                    ],
                    spacing=16,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            spacing=0,
        ),
        padding=20,
        expand=True,
        height=230,
    )


# =============================================================================
# BADGE DE ESTADO
# =============================================================================

def _badge_estado(
    texto: str,
    color,
):
    return ft.Container(
        content=ft.Text(
            texto,
            size=10,
            color=color,
            weight=ft.FontWeight.W_600,
        ),

        padding=ft.Padding.symmetric(
            horizontal=8,
            vertical=3,
        ),

        border_radius=6,

        bgcolor=ft.Colors.with_opacity(
            0.12,
            color,
        ),
    )


# =============================================================================
# ACTIVIDAD RECIENTE
# =============================================================================

def _fila_actividad(
    item: dict,
    on_click=None,
):
    return ft.Container(
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

        ink=on_click is not None,

        on_click=(
            lambda e: on_click(item)
            if on_click
            else None
        ),

        content=ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,

            controls=[
                ft.Column(
                    expand=True,
                    spacing=2,
                    tight=True,

                    controls=[
                        ft.Text(
                            item.get(
                                "titulo",
                                "",
                            ),
                            size=12,
                            weight=ft.FontWeight.W_600,
                            color=TEXT_PRIMARY,
                            max_lines=1,
                            overflow=ft.TextOverflow.ELLIPSIS,
                        ),

                        ft.Text(
                            item.get(
                                "subtitulo",
                                "",
                            ),
                            size=11,
                            color=TEXT_SECONDARY,
                            max_lines=1,
                            overflow=ft.TextOverflow.ELLIPSIS,
                        ),
                    ],
                ),

                _badge_estado(
                    item.get(
                        "estado",
                        "",
                    ),
                    item.get(
                        "color_estado",
                        STAT_BLUE,
                    ),
                ),
            ],

            spacing=10,
        ),
    )


def lista_actividad_reciente(
    titulo: str,
    items: list,
    subtitulo: str = None,
    icon=ft.Icons.NOTIFICATIONS_ACTIVE_OUTLINED,
    icon_color=STAT_ORANGE,
    on_click_item=None,
    on_ver_todos=None,
    texto_vacio="Sin actividad reciente.",
    altura: int = 260,
):
    encabezado = _encabezado_card(
        titulo,
        subtitulo,
        icon,
        icon_color,
    )

    if on_ver_todos:
        contenido_boton = ft.TextButton(
            content=ft.Row(
                controls=[
                    ft.Text(
                        "Ver todos",
                        size=12,
                        color=STAT_BLUE,
                        weight=ft.FontWeight.W_600,
                    ),

                    ft.Icon(
                        ft.Icons.ARROW_FORWARD,
                        size=14,
                        color=STAT_BLUE,
                    ),
                ],
                spacing=4,
                tight=True,
            ),
            on_click=on_ver_todos,
        )
    else:
        contenido_boton = ft.Container()

    if not items:
        cuerpo = ft.Container(
            height=min(
                altura,
                120,
            ),
            alignment=ft.Alignment.CENTER,
            content=ft.Text(
                texto_vacio,
                size=12,
                color=TEXT_SECONDARY,
            ),
        )

    else:
        cuerpo = ft.Container(
            height=altura,

            content=ft.Column(
                spacing=0,
                scroll=ft.ScrollMode.AUTO,

                controls=[
                    _fila_actividad(
                        item,
                        on_click_item,
                    )
                    for item in items
                ],
            ),
        )

    fila_header = ft.Row(
        controls=[
            ft.Container(
                expand=True,
                content=encabezado,
            ),

            contenido_boton,
        ],

        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return _card_container(
        ft.Column(
            spacing=14,
            expand=True,

            controls=[
                fila_header,

                ft.Divider(
                    height=1,
                    color=DIVIDER,
                ),

                cuerpo,
            ],
        )
    )


# =============================================================================
# TABLA / MONITOREO DE PEDIDOS
# =============================================================================

def orders_table_widget():

    rows = [
        (
            "Constructora Alpha S.A  (pedido: #PAV-98)",
            "12,000 Kg (En espera)",
            "#f97316",
        ),

        (
            "Pavimentos del Bajío",
            "8,500 Kg (Despachado)",
            "#22c55e",
        ),
    ]

    def order_row(
        label,
        status,
        color,
    ):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(
                        label,
                        size=12,
                        color=TEXT_PRIMARY,
                        expand=True,
                    ),

                    ft.Text(
                        status,
                        size=11,
                        color=color,
                        weight=ft.FontWeight.W_600,
                    ),
                ],

                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),

            padding=ft.Padding.symmetric(
                vertical=10,
                horizontal=12,
            ),

            bgcolor="rgba(255,255,255,0.03)",

            border=ft.Border.all(
                1,
                GLASS_BORDER,
            ),

            border_radius=8,
        )

    return glass_card(
        ft.Column(
            controls=[
                _encabezado_card(
                    "Monitoreo de pedidos",
                    "Estado de pedidos actuales",
                    ft.Icons.LOCAL_SHIPPING_OUTLINED,
                    STAT_BLUE,
                ),

                ft.Container(height=8),

                *[
                    order_row(*row)
                    for row in rows
                ],
            ],

            spacing=8,
        ),

        padding=20,
        expand=True,
    )


# =============================================================================
# REPORTES DE DESECHOS
# =============================================================================

def waste_reports_widget():

    return glass_card(
        ft.Column(
            controls=[
                _encabezado_card(
                    "Reportes de desechos",
                    "Neumáticos destinados a trituración",
                    ft.Icons.RECYCLING_OUTLINED,
                    STAT_ORANGE,
                ),

                ft.Container(height=8),

                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(
                                ft.Icons.TIRE_REPAIR,
                                color=TEXT_SECONDARY,
                                size=18,
                            ),

                            ft.Column(
                                controls=[
                                    ft.Text(
                                        "Vulcanizadora San Ángel",
                                        size=12,
                                        color=TEXT_PRIMARY,
                                    ),

                                    ft.Text(
                                        "65 neumáticos para trituración",
                                        size=10,
                                        color=TEXT_MUTED,
                                    ),
                                ],

                                spacing=2,
                                expand=True,
                            ),

                            ft.Icon(
                                ft.Icons.STARS_OUTLINED,
                                color=TEXT_SECONDARY,
                                size=18,
                            ),
                        ],

                        spacing=10,

                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),

                    padding=ft.Padding.symmetric(
                        vertical=10,
                        horizontal=12,
                    ),

                    bgcolor="rgba(255,255,255,0.03)",

                    border=ft.Border.all(
                        1,
                        GLASS_BORDER,
                    ),

                    border_radius=8,
                ),
            ],

            spacing=8,
        ),

        padding=20,
        expand=True,
    )
