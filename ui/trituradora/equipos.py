import asyncio
from datetime import date

import flet as ft

from dao.equipos_dao import EquiposDAO
from models.equipos import Equipos
from ui.colors import *

from ui.trituradora.dashboar_trituradora import sidebar, topbar

ACTIVE_ROUTE = "/maquinaria"

ESTADO_ICONO = {
    "En buen estado": (ft.Icons.CHECK_CIRCLE, STAT_BLUE),
    "En mantenimiento": (ft.Icons.BUILD, STAT_ORANGE),
    "Pendiente" : (ft.Icons.CHECK_CIRCLE, STAT_BLUE),
    "Fuera de servicio": (ft.Icons.CANCEL, "#e05353"),
}

ESTADOS_FILTRO = list(ESTADO_ICONO.keys())

ITEMS_POR_PAGINA = 6  # ← 2 filas x 3 columnas, igual que en el mockup


def color_eficiencia(eficiencia: float) -> str:
    if eficiencia >= 85:
        return STAT_BLUE
    if eficiencia >= 40:
        return STAT_ORANGE
    return "#e05353"


def texto_proxima_revision(valor):
    if not valor:
        return "—", TEXT_SECONDARY

    if isinstance(valor, date):
        return valor.strftime("%d/%m/%Y"), TEXT_PRIMARY

    valor_lower = str(valor).strip().lower()

    if valor_lower == "pendiente":
        return valor, "#e05353"

    if valor_lower == "en mantenimiento":
        return valor, STAT_ORANGE

    return valor, TEXT_PRIMARY




# ── Utilidades visuales de tarjeta ──────────────────────────────────────────
def badge_estado(estado: str):
    icono, color = ESTADO_ICONO.get(estado, (ft.Icons.HELP_OUTLINE, TEXT_SECONDARY))
    return ft.Container(
        width=30,
        height=30,
        border_radius=15,
        bgcolor=color,
        alignment=ft.Alignment.CENTER,
        content=ft.Icon(icono, size=16, color="#ffffff"),
    )


def boton_editar_flotante(equipo, on_editar=None):
    return ft.Container(
        width=30,
        height=30,
        border_radius=15,
        bgcolor=STAT_ORANGE,
        alignment=ft.Alignment.CENTER,
        ink=True,
        on_click=(lambda e: on_editar(equipo)) if on_editar else None,
        content=ft.Icon(ft.Icons.EDIT, size=15, color="#ffffff"),
    )


def tarjeta_equipo(equipo, on_ver_detalle=None, on_editar=None):
    icono_ref = ft.Ref[ft.Container]()

    def _hover(e):
        en_hover = e.data == "true"
        icono_normal, color_normal = ESTADO_ICONO.get(equipo.estado, (ft.Icons.HELP_OUTLINE, TEXT_SECONDARY))

        icono_ref.current.bgcolor = STAT_ORANGE if en_hover else color_normal
        icono_ref.current.content = ft.Icon(
            ft.Icons.EDIT if en_hover else icono_normal,
            size=15,
            color="#ffffff",
        )
        icono_ref.current.on_click = (lambda ev: on_editar(equipo)) if (en_hover and on_editar) else None
        icono_ref.current.update()

    revision_texto, revision_color = texto_proxima_revision(equipo.proxima_revision)

    return ft.Container(
        bgcolor=CARD_BG,
        border_radius=12,
        padding=18,
        ink=True,
        on_click=(lambda e: on_ver_detalle(equipo)) if on_ver_detalle else None,
        on_hover=_hover,
        content=ft.Column(
            spacing=10,
            controls=[
                ft.Row(
                    controls=[
                        ft.Column(
                            spacing=1,
                            expand=True,
                            controls=[
                                ft.Text(equipo.equipo_id, size=11, color=TEXT_SECONDARY),
                                ft.Text(equipo.nombre_equipo, size=14, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                            ],
                        ),
                        ft.Container(
                            ref=icono_ref,
                            width=30,
                            height=30,
                            border_radius=15,
                            bgcolor=ESTADO_ICONO.get(equipo.estado, (ft.Icons.HELP_OUTLINE, TEXT_SECONDARY))[1],
                            alignment=ft.Alignment.CENTER,
                            content=ft.Icon(
                                ESTADO_ICONO.get(equipo.estado, (ft.Icons.HELP_OUTLINE, TEXT_SECONDARY))[0],
                                size=16, color="#ffffff",
                            ),
                        ),
                    ],
                ),
                ft.Row(
                    controls=[
                        ft.Text("Eficiencia", size=11, color=TEXT_SECONDARY),
                        ft.Container(expand=True),
                        ft.Text(f"{float(equipo.eficiencia):.0f}%", size=11, color=TEXT_PRIMARY, weight=ft.FontWeight.W_600),
                    ],
                ),
                ft.ProgressBar(
                    value=max(0.0, min(1.0, equipo.eficiencia / 100)),
                    color=color_eficiencia(equipo.eficiencia),
                    bgcolor=ft.Colors.with_opacity(0.10, TEXT_PRIMARY),
                    height=6,
                    border_radius=3,
                ),
                ft.Row(
                    controls=[
                        ft.Column(
                            spacing=1,
                            controls=[
                                ft.Text("Horas de operación", size=10, color=TEXT_SECONDARY),
                                ft.Text(f"{equipo.horas_operacion:,}h", size=12, weight=ft.FontWeight.W_600, color=TEXT_PRIMARY),
                            ],
                        ),
                        ft.Container(expand=True),
                        ft.Column(
                            spacing=1,
                            horizontal_alignment=ft.CrossAxisAlignment.END,
                            controls=[
                                ft.Text("Próxima revisión", size=10, color=TEXT_SECONDARY),
                                ft.Text(revision_texto, size=12, weight=ft.FontWeight.W_600, color=revision_color),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    )


def buscador_equipo():
    return ft.TextField(
        hint_text="Buscar equipo",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=8,
        border_color=DIVIDER,
        bgcolor=CARD_BG,
        content_padding=ft.Padding.symmetric(horizontal=14, vertical=10),
        text_size=13,
        expand=True,
    )


def filtro_row(on_aplicar_filtro=None):
    dropdown = ft.Dropdown(
        hint_text="Filtrar por estado",
        width=200,
        border_radius=8,
        border_color=DIVIDER,
        text_size=13,
        options=[ft.dropdown.Option(e) for e in ESTADOS_FILTRO],
    )
    aplicar_btn = ft.ElevatedButton(
        "Aplicar",
        bgcolor=STAT_ORANGE,
        color="#fff",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=(lambda e: on_aplicar_filtro(dropdown.value)) if on_aplicar_filtro else None,
    )
    return ft.Row(controls=[dropdown, aplicar_btn], spacing=10)


def boton_agregar_equipo(on_click=None):
    return ft.ElevatedButton(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.ADD, size=16, color="#fff"),
                ft.Text("Agregar equipo", size=13, color="#fff", weight=ft.FontWeight.W_600),
            ],
            spacing=6,
            tight=True,
        ),
        bgcolor=STAT_BLUE,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=(lambda e: on_click(e)) if on_click else None,
    )


def paginacion(pagina_actual: int, total_paginas: int, on_cambiar_pagina=None):
    controles = [
        ft.IconButton(
            ft.Icons.CHEVRON_LEFT,
            icon_color=STAT_BLUE,
            on_click=(lambda e: on_cambiar_pagina(max(1, pagina_actual - 1))) if on_cambiar_pagina else None,
        )
    ]
    for n in range(1, total_paginas + 1):
        activo = n == pagina_actual
        controles.append(
            ft.Container(
                content=ft.Text(
                    str(n), size=13,
                    color=STAT_ORANGE if activo else TEXT_SECONDARY,
                    weight=ft.FontWeight.BOLD if activo else ft.FontWeight.NORMAL,
                ),
                padding=ft.Padding.symmetric(horizontal=6),
                ink=True,
                on_click=(lambda e, n=n: on_cambiar_pagina(n)) if on_cambiar_pagina else None,
            )
        )
    controles.append(
        ft.IconButton(
            ft.Icons.CHEVRON_RIGHT,
            icon_color=STAT_BLUE,
            on_click=(lambda e: on_cambiar_pagina(min(total_paginas, pagina_actual + 1))) if on_cambiar_pagina else None,
        )
    )
    return ft.Row(controls=controles, alignment=ft.MainAxisAlignment.CENTER, spacing=2)


def boton_informacion():
    # Mismo estilo que el info_button de dashboard_trituradora.py, para que
    # la vista de Maquinaria se vea consistente con el resto del panel.
    return ft.Container(
        content=ft.Container(
            content=ft.Icon(ft.Icons.INFO_OUTLINE, color="#ffffff", size=18),
            padding=8,
            border_radius=18,
            border=ft.Border.all(1, "#ffffff"),
            ink=True,
            tooltip="Saber más sobre nosotros",
        ),
        right=20,
        bottom=20,
    )


# ── Placeholder de imagen (⚠️ decorativo: la tabla `equipo` no tiene columna
# de foto todavía; no persiste nada hasta que se defina esa columna) ────────
def selector_imagen_placeholder(modo_editar: bool = False):
    return ft.Container(
        width=120,
        height=100,
        border_radius=10,
        bgcolor=ft.Colors.with_opacity(0.06, TEXT_PRIMARY),
        alignment=ft.Alignment.CENTER,
        tooltip="La foto del equipo aún no está en el esquema de BD (pendiente de definir columna)",
        content=ft.Stack(
            controls=[
                ft.Container(
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(ft.Icons.IMAGE_OUTLINED, size=34, color=TEXT_SECONDARY),
                ),
                ft.Container(
                    right=6,
                    bottom=6,
                    width=26,
                    height=26,
                    border_radius=13,
                    bgcolor="#1e1e1e",
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(
                        ft.Icons.EDIT if modo_editar else ft.Icons.ADD,
                        size=14,
                        color="#ffffff",
                    ),
                ),
            ],
        ),
    )


# ── Tarjeta de detalle (modal) ──────────────────────────────────────────────
def detalle_equipo_card(equipo, on_cerrar=None, on_editar=None, on_solicitar_revision=None):
    revision_texto, revision_color = texto_proxima_revision(equipo.proxima_revision)

    return ft.Container(
        width=460,
        bgcolor=CARD_BG,
        border_radius=14,
        padding=24,
        shadow=ft.BoxShadow(
            blur_radius=30,
            color=ft.Colors.with_opacity(0.35, "#000000"),
            offset=ft.Offset(0, 10),
        ),
        content=ft.Column(
            spacing=14,
            tight=True,
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Detalles del equipo", size=16, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                        ft.Container(expand=True),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            icon_color=TEXT_SECONDARY,
                            icon_size=18,
                            on_click=(lambda e: on_cerrar(e)) if on_cerrar else None,
                        ),
                    ],
                ),
                ft.Divider(height=1, color=DIVIDER),
                ft.Text("Nombre del equipo", size=12, color=TEXT_SECONDARY),
                ft.Container(
                    padding=ft.Padding.symmetric(horizontal=12, vertical=10),
                    border_radius=8,
                    border=ft.Border.all(1, DIVIDER),
                    content=ft.Text(equipo.nombre_equipo, size=13, color=TEXT_PRIMARY),
                ),
                ft.Row(
                    spacing=14,
                    controls=[
                        ft.Column(
                            expand=True,
                            spacing=4,
                            controls=[
                                ft.Text("Horas de operación", size=12, color=TEXT_SECONDARY),
                                ft.Container(
                                    padding=ft.Padding.symmetric(horizontal=12, vertical=10),
                                    border_radius=8,
                                    border=ft.Border.all(1, DIVIDER),
                                    content=ft.Text(f"{equipo.horas_operacion:,}h", size=13, color=TEXT_PRIMARY),
                                ),
                            ],
                        ),
                        ft.Column(
                            expand=True,
                            spacing=4,
                            controls=[
                                ft.Text("Próxima revisión", size=12, color=TEXT_SECONDARY),
                                ft.Container(
                                    padding=ft.Padding.symmetric(horizontal=12, vertical=10),
                                    border_radius=8,
                                    border=ft.Border.all(1, DIVIDER),
                                    content=ft.Text(revision_texto, size=13, color=revision_color),
                                ),
                            ],
                        ),
                    ],
                ),
                ft.Text("Estado", size=12, color=TEXT_SECONDARY),
                ft.Container(
                    padding=ft.Padding.symmetric(horizontal=12, vertical=10),
                    border_radius=8,
                    border=ft.Border.all(1, DIVIDER),
                    content=ft.Row(
                        controls=[
                            ft.Icon(
                                ESTADO_ICONO.get(equipo.estado, (ft.Icons.HELP_OUTLINE, TEXT_SECONDARY))[0],
                                size=15,
                                color=ESTADO_ICONO.get(equipo.estado, (ft.Icons.HELP_OUTLINE, TEXT_SECONDARY))[1],
                            ),
                            ft.Text(equipo.estado, size=13, color=TEXT_PRIMARY),
                        ],
                        spacing=8,
                    ),
                ),
                ft.Row(
                    controls=[
                        ft.Text("Eficiencia", size=12, color=TEXT_SECONDARY),
                        ft.Container(expand=True),
                        ft.Text(f"{float(equipo.eficiencia):.0f}%", size=12, color=TEXT_PRIMARY, weight=ft.FontWeight.W_600),
                    ],
                ),
                ft.ProgressBar(
                    value=max(0.0, min(1.0, equipo.eficiencia / 100)),
                    color=color_eficiencia(equipo.eficiencia),
                    bgcolor=ft.Colors.with_opacity(0.10, TEXT_PRIMARY),
                    height=8,
                    border_radius=4,
                ),
                ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[selector_imagen_placeholder()]),
                ft.Container(height=6),
                ft.Row(
                    controls=[
                        ft.OutlinedButton(
                            "Editar info",
                            style=ft.ButtonStyle(
                                color=STAT_ORANGE,
                                side=ft.BorderSide(1, STAT_ORANGE),
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                            on_click=(lambda e: on_editar(equipo)) if on_editar else None,
                        ),
                        ft.Container(expand=True),
                        ft.ElevatedButton(
                            "Solicitar revición de equipo",  # ← typo "revición" tal como en tu mockup
                            bgcolor=STAT_BLUE,
                            color="#fff",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                            on_click=(lambda e: on_solicitar_revision(equipo)) if on_solicitar_revision else None,
                        ),
                    ],
                ),
            ],
        ),
    )


# ── Formulario de edición (modal) ───────────────────────────────────────────
def campo_editable(label: str, value: str):
    return ft.TextField(
        label=label,
        value=value,
        expand=True,
        height=55,
        border_radius=8,
        border_color=DIVIDER,
        bgcolor=CARD_BG,
        text_size=13,
        label_style=ft.TextStyle(size=11, color=TEXT_SECONDARY),
        content_padding=ft.Padding.symmetric(horizontal=12, vertical=8),
    )


def formulario_editar_equipo(equipo, on_guardar=None, on_cancelar=None):
    nombre_field = campo_editable("Nombre del equipo", equipo.nombre_equipo)
    horas_field = campo_editable("Horas de operación", str(equipo.horas_operacion))
    revision_field = ft.TextField(
        label="Próxima revisión",
        hint_text="Ej: Pendiente, En mantenimiento o 30/07/2026",
        border_radius=8,
        border_color=DIVIDER,
        text_size=13,
    )
    estado_dropdown = ft.Dropdown(
        label="Estado",
        value=equipo.estado if equipo.estado in ESTADOS_FILTRO else None,
        border_radius=8,
        border_color=DIVIDER,
        text_size=13,
        label_style=ft.TextStyle(size=12, color=TEXT_SECONDARY),
        options=[ft.dropdown.Option(e) for e in ESTADOS_FILTRO],
    )

    eficiencia_field = campo_editable("Eficiencia (%)", str(equipo.eficiencia))

    error_text = ft.Text("", size=12, color="#e05353", visible=False)

    def _guardar(e):
        try:
            horas_val = int(horas_field.value)
            eficiencia_val = float(eficiencia_field.value)
        except (TypeError, ValueError):
            error_text.value = "Horas de operación y eficiencia deben ser numéricos."
            error_text.visible = True
            error_text.update()
            return

        datos_editados = {
            "equipo_id": equipo.equipo_id,
            "nombre_equipo": nombre_field.value,
            "horas_operacion": horas_val,
            "proxima_revision": revision_field.value,
            "estado": estado_dropdown.value or equipo.estado,
            "eficiencia": eficiencia_val,
        }
        if on_guardar:
            on_guardar(datos_editados)

    return ft.Container(
        width=520,
        bgcolor=CARD_BG,
        border_radius=14,
        padding=24,
        shadow=ft.BoxShadow(
            blur_radius=30,
            color=ft.Colors.with_opacity(0.35, "#000000"),
            offset=ft.Offset(0, 10),
        ),
        content=ft.Column(
            spacing=12,
            tight=True,
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Editar equipo", size=16, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                        ft.Container(expand=True),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            icon_color=TEXT_SECONDARY,
                            icon_size=18,
                            on_click=(lambda e: on_cancelar(e)) if on_cancelar else None,
                        ),
                    ],
                ),
                ft.Divider(height=1, color=DIVIDER),
                ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[selector_imagen_placeholder(modo_editar=True)]),
                nombre_field,
                ft.Row(controls=[horas_field, revision_field], spacing=10),
                ft.Row(controls=[estado_dropdown, eficiencia_field], spacing=10),
                error_text,
                ft.Container(height=6),
                ft.Row(
                    controls=[
                        ft.OutlinedButton(
                            "Cerrar",
                            style=ft.ButtonStyle(
                                color=STAT_ORANGE,
                                side=ft.BorderSide(1, STAT_ORANGE),
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                            on_click=(lambda e: on_cancelar(e)) if on_cancelar else None,
                        ),
                        ft.Container(expand=True),
                        ft.ElevatedButton(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.SAVE, size=16, color="#fff"),
                                    ft.Text("Guardar", size=13, color="#fff", weight=ft.FontWeight.W_600),
                                ],
                                spacing=6,
                                tight=True,
                            ),
                            bgcolor=STAT_BLUE,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                            on_click=_guardar,
                        ),
                    ],
                ),
            ],
        ),
    )


# ── Formulario de creación "Agregar equipo" (modal) ─────────────────────────
def formulario_nuevo_equipo(on_guardar=None, on_cancelar=None):
    nombre_field = campo_editable("Nombre del equipo", "")
    horas_field = campo_editable("Horas de operación", "0")
    revision_field = campo_editable("Próxima revisión", "")

    estado_dropdown = ft.Dropdown(
        label="Estado",
        border_radius=8,
        border_color=DIVIDER,
        text_size=13,
        label_style=ft.TextStyle(size=12, color=TEXT_SECONDARY),
        options=[ft.dropdown.Option(e) for e in ESTADOS_FILTRO],
    )

    eficiencia_field = campo_editable("Eficiencia (%)", "0")

    error_text = ft.Text("", size=12, color="#e05353", visible=False)

    def _guardar(e):
        if not all([nombre_field.value, estado_dropdown.value]):
            error_text.value = "Completa al menos nombre del equipo y estado."
            error_text.visible = True
            error_text.update()
            return
        try:
            horas_val = int(horas_field.value or 0)
            eficiencia_val = float(eficiencia_field.value or 0)
        except ValueError:
            error_text.value = "Horas de operación y eficiencia deben ser numéricos."
            error_text.visible = True
            error_text.update()
            return

        datos_nuevos = {
            "nombre_equipo": nombre_field.value,
            "horas_operacion": horas_val,
            "proxima_revision": revision_field.value or None,
            "estado": estado_dropdown.value,
            "eficiencia": eficiencia_val,
        }
        if on_guardar:
            on_guardar(datos_nuevos)

    return ft.Container(
        width=520,
        bgcolor=CARD_BG,
        border_radius=14,
        padding=24,
        shadow=ft.BoxShadow(
            blur_radius=30,
            color=ft.Colors.with_opacity(0.35, "#000000"),
            offset=ft.Offset(0, 10),
        ),
        content=ft.Column(
            spacing=12,
            tight=True,
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Agregar equipo", size=16, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                        ft.Container(expand=True),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            icon_color=STAT_ORANGE,
                            icon_size=18,
                            on_click=(lambda e: on_cancelar(e)) if on_cancelar else None,
                        ),
                    ],
                ),
                ft.Divider(height=1, color=DIVIDER),
                ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[selector_imagen_placeholder()]),
                nombre_field,
                ft.Row(controls=[horas_field, revision_field], spacing=10),
                ft.Row(controls=[estado_dropdown, eficiencia_field], spacing=10),
                error_text,
                ft.Container(height=6),
                ft.Row(
                    controls=[
                        ft.OutlinedButton(
                            "Cerrar",
                            style=ft.ButtonStyle(
                                color=STAT_ORANGE,
                                side=ft.BorderSide(1, STAT_ORANGE),
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                            on_click=(lambda e: on_cancelar(e)) if on_cancelar else None,
                        ),
                        ft.Container(expand=True),
                        ft.ElevatedButton(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.ADD, size=16, color="#fff"),
                                    ft.Text("Agregar equipo", size=13, color="#fff", weight=ft.FontWeight.W_600),
                                ],
                                spacing=6,
                                tight=True,
                            ),
                            bgcolor=STAT_BLUE,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                            on_click=_guardar,
                        ),
                    ],
                ),
            ],
        ),
    )


# ── Contenido de Equipos (área central + modal animado) ────────────────────
def equipos_content(page: ft.Page):
    todos_los_equipos = EquiposDAO().get_all()

    for equipo in todos_los_equipos:
        equipo.eficiencia = float(equipo.eficiencia)

    estado_pagina = {"pagina_actual": 1, "filtro_estado": None}

    modal_overlay_ref = ft.Ref[ft.Container]()
    modal_backdrop_ref = ft.Ref[ft.Container]()
    modal_card_ref = ft.Ref[ft.Container]()
    grid_wrapper_ref = ft.Ref[ft.Container]()
    paginacion_wrapper_ref = ft.Ref[ft.Container]()
    contador_ref = ft.Ref[ft.Text]()

    def _equipos_filtrados():
        if estado_pagina["filtro_estado"]:
            return [e for e in todos_los_equipos if e.estado == estado_pagina["filtro_estado"]]
        return todos_los_equipos

    def _total_paginas():
        equipos = _equipos_filtrados()
        return max(1, -(-len(equipos) // ITEMS_POR_PAGINA))  # ceil division

    def _equipos_pagina_actual():
        equipos = _equipos_filtrados()
        inicio = (estado_pagina["pagina_actual"] - 1) * ITEMS_POR_PAGINA
        return equipos[inicio: inicio + ITEMS_POR_PAGINA]

    def _grid():
        return ft.GridView(
            expand=True,
            runs_count=3,
            max_extent=260,
            child_aspect_ratio=1.35,
            spacing=20,
            run_spacing=20,
            controls=[
                tarjeta_equipo(eq, on_ver_detalle=abrir_detalle, on_editar=ir_a_editar)
                for eq in _equipos_pagina_actual()
            ],
        )

    def _refrescar_todo():
        nonlocal todos_los_equipos

        todos_los_equipos = EquiposDAO().get_all()

        for equipo in todos_los_equipos:
            equipo.eficiencia = float(equipo.eficiencia)

        estado_pagina["pagina_actual"] = min(
            estado_pagina["pagina_actual"],
            _total_paginas()
        )

        grid_wrapper_ref.current.content = _grid()
        grid_wrapper_ref.current.update()

    def cambiar_pagina(nueva_pagina):
        estado_pagina["pagina_actual"] = nueva_pagina
        _refrescar_todo()

    def aplicar_filtro(valor_estado):
        estado_pagina["filtro_estado"] = valor_estado
        estado_pagina["pagina_actual"] = 1
        _refrescar_todo()

    async def _swap_contenido(nuevo_control):
        modal_card_ref.current.opacity = 0
        modal_card_ref.current.update()
        await asyncio.sleep(0.15)
        modal_card_ref.current.content = nuevo_control
        modal_card_ref.current.opacity = 1
        modal_card_ref.current.update()

    async def _cerrar():
        modal_backdrop_ref.current.opacity = 0
        modal_card_ref.current.scale = 0.85
        modal_card_ref.current.opacity = 0
        modal_backdrop_ref.current.update()
        modal_card_ref.current.update()
        await asyncio.sleep(0.25)
        modal_overlay_ref.current.visible = False
        modal_overlay_ref.current.update()

    def cerrar_modal(e=None):
        page.run_task(_cerrar)

    def ir_a_editar(equipo):
        page.run_task(
            _swap_contenido,
            formulario_editar_equipo(equipo, on_guardar=guardar_edicion, on_cancelar=cerrar_modal),
        )

    def guardar_edicion(datos):
        equipo_actualizado = Equipos(
            equipo_id=datos["equipo_id"],
            nombre_equipo=datos["nombre_equipo"],
            horas_operacion=datos["horas_operacion"],
            proxima_revision=datos["proxima_revision"],
            estado=datos["estado"],
            eficiencia=datos["eficiencia"],
        )
        EquiposDAO().update(equipo_actualizado)
        _refrescar_todo()
        cerrar_modal()

    def solicitar_revision(equipo):
        # ⚠️ regla de negocio asumida: "solicitar revisión" marca el estado
        # como "En revisión". Confirmar si en realidad debe generar un
        # registro en Alertas u otra tabla en vez de solo tocar `equipo`.
        equipo.estado = "En revisión"
        EquiposDAO().update(equipo)
        _refrescar_todo()
        cerrar_modal()

    def guardar_nuevo(datos):
        nuevo = Equipos(
            equipo_id=EquiposDAO().generar_id(),
            nombre_equipo=datos["nombre_equipo"],
            horas_operacion=datos["horas_operacion"],
            proxima_revision=datos["proxima_revision"],
            estado=datos["estado"],
            eficiencia=datos["eficiencia"],
        )
        EquiposDAO().insert(nuevo)
        _refrescar_todo()
        cerrar_modal()

    def abrir_detalle(equipo):
        async def _abrir():
            tarjeta = detalle_equipo_card(
                equipo,
                on_cerrar=cerrar_modal,
                on_editar=ir_a_editar,
                on_solicitar_revision=solicitar_revision,
            )
            modal_card_ref.current.content = tarjeta
            modal_overlay_ref.current.visible = True
            modal_card_ref.current.scale = 0.85
            modal_card_ref.current.opacity = 0
            modal_backdrop_ref.current.opacity = 0
            modal_overlay_ref.current.update()

            await asyncio.sleep(0.02)
            modal_backdrop_ref.current.opacity = 1
            modal_card_ref.current.scale = 1
            modal_card_ref.current.opacity = 1
            modal_backdrop_ref.current.update()
            modal_card_ref.current.update()

        page.run_task(_abrir)

    def abrir_nuevo(e=None):
        async def _abrir():
            formulario = formulario_nuevo_equipo(on_guardar=guardar_nuevo, on_cancelar=cerrar_modal)
            modal_card_ref.current.content = formulario
            modal_overlay_ref.current.visible = True
            modal_card_ref.current.scale = 0.85
            modal_card_ref.current.opacity = 0
            modal_backdrop_ref.current.opacity = 0
            modal_overlay_ref.current.update()

            await asyncio.sleep(0.02)
            modal_backdrop_ref.current.opacity = 1
            modal_card_ref.current.scale = 1
            modal_card_ref.current.opacity = 1
            modal_backdrop_ref.current.update()
            modal_card_ref.current.update()

        page.run_task(_abrir)

    modal_overlay = ft.Container(
        ref=modal_overlay_ref,
        visible=False,
        expand=True,
        content=ft.Stack(
            controls=[
                ft.Container(
                    ref=modal_backdrop_ref,
                    expand=True,
                    bgcolor=ft.Colors.with_opacity(0.65, "#000000"),
                    blur=10,
                    opacity=0,
                    animate_opacity=ft.Animation(250, ft.AnimationCurve.EASE_OUT),
                    on_click=cerrar_modal,
                ),
                ft.Container(
                    expand=True,
                    alignment=ft.Alignment.CENTER,
                    on_click=lambda e: None,
                    content=ft.Container(
                        ref=modal_card_ref,
                        scale=0.85,
                        opacity=0,
                        animate_scale=ft.Animation(320, ft.AnimationCurve.EASE_OUT_BACK),
                        animate_opacity=ft.Animation(220, ft.AnimationCurve.EASE_OUT),
                    ),
                ),
            ],
        ),
    )

    return ft.Stack(
        controls=[
            ft.Container(
                expand=True,
                padding=20,
                bgcolor=MAIN_BG,
                content=ft.Column(
                    spacing=0,
                    expand=True,
                    controls=[
                        ft.Row(
                            controls=[buscador_equipo(), boton_agregar_equipo(abrir_nuevo)],
                            spacing=12,
                        ),
                        ft.Container(height=12),
                        filtro_row(on_aplicar_filtro=aplicar_filtro),
                        ft.Container(height=12),
                        ft.Row(
                            controls=[
                                ft.Container(expand=True),
                                ft.Text(
                                    f"{len(_equipos_filtrados())} elementos",
                                    size=12, color=TEXT_SECONDARY, ref=contador_ref,
                                ),
                            ],
                        ),
                        ft.Container(height=20),
                        ft.Container(
                            ref=grid_wrapper_ref,
                            expand=True,
                            content=_grid(),
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            "Ver más detalles de los equipos", size=12,
                            color=TEXT_SECONDARY, text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Container(height=8),
                        ft.Container(
                            ref=paginacion_wrapper_ref,
                            content=paginacion(
                                estado_pagina["pagina_actual"], _total_paginas(), on_cambiar_pagina=cambiar_pagina
                            ),
                        ),
                        ft.Container(height=10),
                    ],
                ),
            ),
            boton_informacion(),
            modal_overlay,
        ],
        expand=True,
    )


def equipos_triturador(page: ft.Page, on_navigate=None):
    return ft.View(
        route=ACTIVE_ROUTE,
        padding=0,
        bgcolor=MAIN_BG,
        controls=[
            ft.Column(
                controls=[
                    topbar(page, ACTIVE_ROUTE),
                    ft.Row(
                        controls=[
                            sidebar(active_route=ACTIVE_ROUTE, on_navigate=on_navigate),
                            ft.Container(content=equipos_content(page), expand=True),
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