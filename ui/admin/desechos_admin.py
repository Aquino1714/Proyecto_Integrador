import asyncio

import flet as ft

from ui.colors import *
from dao.reporteVul_dao import ReportVulDAO
from ui.admin.dashboard_admin import sidebar, topbar

ESTADO_COLORES = {
    "Pendiente": STAT_ORANGE,
    "Asignado": STAT_BLUE,
    "Completado": STAT_TEAL,
    "Cancelado": "#9ca3af",
}


# ── Badge de estado ──────────────────────────────────────────────────────────
def badge_estado(estado: str):
    color = ESTADO_COLORES.get(estado, STAT_ORANGE)
    return ft.Container(
        content=ft.Text(
            f"Estatus: {estado.lower()}",
            size=11,
            color=color,
            weight=ft.FontWeight.W_600,
        ),
        padding=ft.Padding.symmetric(horizontal=10, vertical=4),
        border_radius=6,
        bgcolor=ft.Colors.with_opacity(0.12, color),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.5, color)),
    )


# ── Acción del lado derecho de la tarjeta, según estado ─────────────────────
def accion_reporte(rep, on_asignar=None):
    if rep.estado == "Pendiente":
        return ft.ElevatedButton(
            "Asignar Chofer Cercano",
            bgcolor=STAT_BLUE,
            color="#fff",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
            on_click=(lambda e: on_asignar(rep)) if on_asignar else None,
        )
    if rep.estado == "Asignado":
        return ft.Row(
            controls=[
                ft.Icon(ft.Icons.LOCAL_SHIPPING_OUTLINED, size=16, color=STAT_BLUE),
                ft.Text(
                    f"Asignado a {rep.empleado_nombre or '—'}",
                    size=12,
                    color=STAT_BLUE,
                    weight=ft.FontWeight.W_600,
                ),
            ],
            spacing=6,
        )
    if rep.estado == "Completado":
        return ft.Row(
            controls=[
                ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, size=16, color=STAT_TEAL),
                ft.Text("Completado", size=12, color=STAT_TEAL, weight=ft.FontWeight.W_600),
            ],
            spacing=6,
        )
    # Cancelado (histórico; el flujo nuevo ya no genera este estado desde la UI)
    return ft.Text("Cancelado", size=12, color="#9ca3af", weight=ft.FontWeight.W_600)


# ── Tarjeta individual de reporte ────────────────────────────────────────────
def tarjeta_reporte(rep, on_click=None, on_asignar=None):
    es_pendiente = rep.estado == "Pendiente"
    id_display = f"VULC-{rep.vulcanizadora_id:02d}"

    return ft.Container(
        padding=16,
        border_radius=10,
        bgcolor=CARD_BG,
        ink=True,
        border=ft.Border.all(1, STAT_ORANGE if es_pendiente else DIVIDER),
        on_click=(lambda e: on_click(rep)) if on_click else None,
        content=ft.Column(
            spacing=8,
            controls=[
                badge_estado(rep.estado),
                ft.Row(
                    controls=[
                        ft.Column(
                            spacing=2,
                            expand=True,
                            controls=[
                                ft.Text(
                                    f"{rep.vulcanizadora_nombre} (ID: {id_display})",
                                    size=14,
                                    weight=ft.FontWeight.BOLD,
                                    color=TEXT_PRIMARY,
                                ),
                                ft.Text(
                                    f"Volumen reportado para trituración: "
                                    f"{rep.cantidad_llantas} neumáticos",
                                    size=12,
                                    color=TEXT_SECONDARY,
                                ),
                                ft.Text(
                                    f"Fecha Reporte: {rep.fecha_reporte}",
                                    size=11,
                                    color=TEXT_SECONDARY,
                                ),
                            ],
                        ),
                        accion_reporte(rep, on_asignar),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
        ),
    )


# ── Descripción del reporte (para el modal de detalle) ──────────────────────
def _descripcion_reporte(rep):
    if rep.detalles and rep.detalles.strip():
        texto = rep.detalles
    else:
        texto = (
            f"Se informa que durante la jornada del día se generó un volumen "
            f"total de {rep.cantidad_llantas} neumáticos de desecho listos "
            f"para trituración. Aún no se ha registrado una descripción "
            f"detallada por parte de la vulcanizadora."
        )
    return ft.Text(texto, size=13, color=TEXT_SECONDARY)


# ── Modal: detalle del reporte ───────────────────────────────────────────────
def detalle_reporte_card(rep, on_cerrar=None, on_eliminar=None, on_accion_principal=None):
    id_display = f"VULC-{rep.vulcanizadora_id:02d}"

    boton_principal = None
    if rep.estado == "Pendiente":
        boton_principal = ft.ElevatedButton(
            "Asignar chofer",
            bgcolor=STAT_BLUE,
            color="#fff",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
            on_click=(lambda e: on_accion_principal(rep)) if on_accion_principal else None,
        )
    elif rep.estado == "Asignado":
        boton_principal = ft.ElevatedButton(
            "Marcar completado",
            bgcolor=STAT_TEAL,
            color="#fff",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
            on_click=(lambda e: on_accion_principal(rep)) if on_accion_principal else None,
        )

    botones = [
        ft.OutlinedButton(
            "Eliminar",
            style=ft.ButtonStyle(
                color="#f87171",
                side=ft.BorderSide(1, "#f87171"),
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            on_click=(lambda e: on_eliminar(rep)) if on_eliminar else None,
        ),
        ft.Container(expand=True),
        ft.OutlinedButton(
            "Cerrar",
            style=ft.ButtonStyle(
                color=TEXT_SECONDARY,
                side=ft.BorderSide(1, DIVIDER),
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            on_click=(lambda e: on_cerrar(e)) if on_cerrar else None,
        ),
    ]
    if boton_principal:
        botones.append(ft.Container(width=10))
        botones.append(boton_principal)

    return ft.Container(
        width=480,
        bgcolor=CARD_BG,
        border_radius=14,
        padding=24,
        shadow=ft.BoxShadow(
            blur_radius=30,
            color=ft.Colors.with_opacity(0.35, "#000000"),
            offset=ft.Offset(0, 10),
        ),
        content=ft.Column(
            spacing=10,
            tight=True,
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Detalles del reporte", size=16, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
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
                ft.Text(
                    f"{rep.vulcanizadora_nombre} (ID: {id_display})",
                    size=14,
                    weight=ft.FontWeight.BOLD,
                    color=TEXT_PRIMARY,
                ),
                ft.Container(height=6),
                ft.Text("Reporte:", size=12, color=TEXT_SECONDARY, weight=ft.FontWeight.W_600),
                _descripcion_reporte(rep),
                ft.Container(height=6),
                ft.Container(
                    padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                    border_radius=8,
                    bgcolor=ft.Colors.with_opacity(0.04, TEXT_PRIMARY),
                    border=ft.Border.all(1, DIVIDER),
                    content=ft.Row(
                        controls=[
                            ft.Text("Fecha de Reporte:", size=12, color=TEXT_SECONDARY),
                            ft.Container(expand=True),
                            ft.Text(str(rep.fecha_reporte), size=13, color=TEXT_PRIMARY, weight=ft.FontWeight.W_500),
                        ],
                    ),
                ),
                ft.Container(height=6),
                ft.Row(controls=botones),
            ],
        ),
    )


# ── Modal: seleccionar chofer para asignar ──────────────────────────────────
def formulario_asignar_chofer(rep, choferes, on_confirmar=None, on_cancelar=None):
    dropdown = ft.Dropdown(
        label="Chofer disponible",
        border_radius=8,
        border_color=DIVIDER,
        text_size=13,
        label_style=ft.TextStyle(size=12, color=TEXT_SECONDARY),
        options=[ft.dropdown.Option(str(c["empleado_id"]), c["nombre"]) for c in choferes],
    )
    error_text = ft.Text("", size=12, color=STAT_ORANGE, visible=False)

    def _confirmar(e):
        if not dropdown.value:
            error_text.value = "Selecciona un chofer para continuar."
            error_text.visible = True
            error_text.update()
            return
        if on_confirmar:
            on_confirmar(rep.reporte_id, int(dropdown.value))

    return ft.Container(
        width=420,
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
                        ft.Text("Asignar chofer", size=16, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
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
                ft.Text(
                    f"Reporte de {rep.vulcanizadora_nombre}: "
                    f"{rep.cantidad_llantas} neumáticos.",
                    size=12,
                    color=TEXT_SECONDARY,
                ),
                dropdown,
                error_text,
                ft.Row(
                    controls=[
                        ft.OutlinedButton(
                            "Cancelar",
                            style=ft.ButtonStyle(
                                color=TEXT_SECONDARY,
                                side=ft.BorderSide(1, DIVIDER),
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                            on_click=(lambda e: on_cancelar(e)) if on_cancelar else None,
                        ),
                        ft.Container(expand=True),
                        ft.ElevatedButton(
                            "Confirmar asignación",
                            bgcolor=STAT_BLUE,
                            color="#fff",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                            on_click=_confirmar,
                        ),
                    ],
                ),
            ],
        ),
    )


# ── Modal: confirmar eliminación ────────────────────────────────────────────
def dialogo_eliminar_reporte(rep, on_confirmar=None, on_cancelar=None):
    return ft.Container(
        width=400,
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
                        ft.Text("Eliminar reporte", size=16, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
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
                ft.Text(
                    f"¿Eliminar el reporte de {rep.vulcanizadora_nombre}? "
                    "Esta acción no se puede deshacer.",
                    size=12,
                    color=TEXT_SECONDARY,
                ),
                ft.Row(
                    controls=[
                        ft.OutlinedButton(
                            "Cancelar",
                            style=ft.ButtonStyle(
                                color=TEXT_SECONDARY,
                                side=ft.BorderSide(1, DIVIDER),
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                            on_click=(lambda e: on_cancelar(e)) if on_cancelar else None,
                        ),
                        ft.Container(expand=True),
                        ft.ElevatedButton(
                            "Eliminar",
                            bgcolor="#f87171",
                            color="#fff",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                            on_click=(lambda e: on_confirmar(rep.reporte_id)) if on_confirmar else None,
                        ),
                    ],
                ),
            ],
        ),
    )


def boton_informacion():
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
        ),
        right=20,
        bottom=20,
    )


# ── Contenido central: bandeja + modal animado (estilo Mac, blur cristalino) ─
def desechos_content(page: ft.Page):
    reportes = ReportVulDAO().get_all_admin()

    modal_overlay_ref = ft.Ref[ft.Container]()
    modal_backdrop_ref = ft.Ref[ft.Container]()
    modal_card_ref = ft.Ref[ft.Container]()
    lista_wrapper_ref = ft.Ref[ft.Column]()

    def _refrescar():
        nuevos = ReportVulDAO().get_all_admin()
        lista_wrapper_ref.current.controls = [
            tarjeta_reporte(r, on_click=abrir_detalle, on_asignar=abrir_asignar)
            for r in nuevos
        ]
        lista_wrapper_ref.current.update()

    async def _swap_contenido(nuevo_control):
        modal_card_ref.current.opacity = 0
        modal_card_ref.current.update()
        await asyncio.sleep(0.15)
        modal_card_ref.current.content = nuevo_control
        modal_card_ref.current.opacity = 1
        modal_card_ref.current.update()

    async def _abrir_con_contenido(control):
        modal_card_ref.current.content = control
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

    def abrir_detalle(rep):
        tarjeta = detalle_reporte_card(
            rep,
            on_cerrar=cerrar_modal,
            on_eliminar=abrir_eliminar,
            on_accion_principal=manejar_accion_principal,
        )
        page.run_task(_abrir_con_contenido, tarjeta)

    def abrir_asignar(rep):
        choferes = ReportVulDAO().get_choferes_disponibles()
        formulario = formulario_asignar_chofer(
            rep, choferes, on_confirmar=confirmar_asignacion, on_cancelar=cerrar_modal
        )
        page.run_task(_abrir_con_contenido, formulario)

    def confirmar_asignacion(reporte_id, empleado_id):
        ReportVulDAO().asignar_chofer(reporte_id, empleado_id)
        _refrescar()
        cerrar_modal()

    def manejar_accion_principal(rep):
        if rep.estado == "Pendiente":
            page.run_task(
                _swap_contenido,
                formulario_asignar_chofer(
                    rep,
                    ReportVulDAO().get_choferes_disponibles(),
                    on_confirmar=confirmar_asignacion,
                    on_cancelar=cerrar_modal,
                ),
            )
        elif rep.estado == "Asignado":
            ReportVulDAO().marcar_completado(rep.reporte_id)
            _refrescar()
            cerrar_modal()

    def abrir_eliminar(rep):
        page.run_task(
            _swap_contenido,
            dialogo_eliminar_reporte(rep, on_confirmar=confirmar_eliminar, on_cancelar=cerrar_modal),
        )

    def confirmar_eliminar(reporte_id):
        ReportVulDAO().delete(reporte_id)
        _refrescar()
        cerrar_modal()

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
                    blur=10,  # cristal esmerilado sobre el fondo
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
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.RADIO_BUTTON_CHECKED, color=STAT_ORANGE, size=18),
                                ft.Text(
                                    "Bandeja de Reportes de Desecho Entrantes",
                                    size=17,
                                    weight=ft.FontWeight.BOLD,
                                    color=TEXT_PRIMARY,
                                ),
                            ],
                            spacing=8,
                        ),
                        ft.Text(
                            "Alertas y solicitudes de recolección.",
                            size=12,
                            color=TEXT_SECONDARY,
                        ),
                        ft.Container(height=6),
                        ft.Divider(height=1, color=DIVIDER),
                        ft.Container(height=12),
                        ft.Column(
                            ref=lista_wrapper_ref,
                            spacing=12,
                            scroll=ft.ScrollMode.AUTO,
                            expand=True,
                            controls=[
                                tarjeta_reporte(r, on_click=abrir_detalle, on_asignar=abrir_asignar)
                                for r in reportes
                            ],
                        ),
                    ],
                    spacing=6,
                    expand=True,
                ),
            ),
            boton_informacion(),
            modal_overlay,
        ],
        expand=True,
    )


# ── Vista completa (conectada a sidebar/topbar) ─────────────────────────────
def desechos_admin(page: ft.Page, on_navigate=None):
    active_route = "/desechos"

    return ft.View(
        route="/desechos",
        padding=0,
        bgcolor=MAIN_BG,
        controls=[
            ft.Column(
                controls=[
                    topbar(page, active_route),
                    ft.Row(
                        controls=[
                            sidebar(active_route=active_route, on_navigate=on_navigate),
                            ft.Container(
                                content=desechos_content(page),
                                expand=True,
                            ),
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