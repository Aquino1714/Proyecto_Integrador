import asyncio

import flet as ft

from ui.colors import *
from dao.solicitudes_servicio_dao import SolicitudesServicioDAO
from ui.vulcanizadora.dashboard_vulcanizadora import sidebar, topbar

ESTADO_COLORES = {
    "Pendiente": STAT_ORANGE,
    "Atendido": STAT_TEAL,
    "En proceso": STAT_BLUE,
    "Cancelado": "#f87171",
}


# ── Badges ────────────────────────────────────────────────────────────────
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

def badge_servicio(tipo_servicio):
    return ft.Container(
        content=ft.Text(
            tipo_servicio,
            size=11,
            color=STAT_BLUE,
            weight=ft.FontWeight.W_600,
        ),
        padding=ft.Padding.symmetric(horizontal=10, vertical=4),
        border_radius=6,
        bgcolor=ft.Colors.with_opacity(0.12, STAT_BLUE),
        border=ft.Border.all(
            1,
            ft.Colors.with_opacity(0.5, STAT_BLUE)
        ),
    )

# ── Acción del lado derecho de la tarjeta ────────────────────────────────────
def accion_reporte(rep, on_resolver=None):
    if rep.estado == "Pendiente":
        return ft.ElevatedButton(
            "Marcar como resuelto",
            bgcolor=STAT_BLUE,
            color="#fff",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
            on_click=(lambda e: on_resolver(rep)) if on_resolver else None,
        )
    return ft.Row(
        controls=[
            ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, size=16, color=STAT_TEAL),
            ft.Text("Resuelto", size=12, color=STAT_TEAL, weight=ft.FontWeight.W_600),
        ],
        spacing=6,
    )


# ── Tarjeta individual de reporte ────────────────────────────────────────────
def tarjeta_solicitud(rep, on_click=None, on_resolver=None):
    es_pendiente = rep.estado == "Pendiente"

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
                ft.Row(
                    controls=[
                        badge_estado(rep.estado),
                        badge_servicio(rep.tipo_servicio)
                    ],
                    spacing=8
                ),
                ft.Row(
                    controls=[
                        ft.Column(
                            spacing=2,
                            expand=True,
                            controls=[
                                ft.Text(
                                    f"Solicitud #{rep.solicitud_id} - {rep.tipo_servicio}",
                                    size=14,
                                    weight=ft.FontWeight.BOLD,
                                    color=TEXT_PRIMARY,
                                ),
                                ft.Text(
                                    (rep.notas or "")[:120]
                                    + ("..." if rep.notas and len(rep.notas) > 120 else ""),
                                    size=12,
                                    color=TEXT_SECONDARY,
                                ),
                                ft.Text(
                                    f"Fecha Reporte: {rep.fecha_solicitud}",
                                    size=11,
                                    color=TEXT_SECONDARY,
                                ),
                            ],
                        ),
                        accion_reporte(rep, on_resolver),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
        ),
    )


# ── Modal: detalle del reporte ───────────────────────────────────────────────
def detalle_reporte_card(rep, on_cerrar=None, on_eliminar=None, on_resolver=None):
    boton_principal = None
    if rep.estado == "Pendiente":
        boton_principal = ft.ElevatedButton(
            "Marcar como resuelto",
            bgcolor=STAT_BLUE,
            color="#fff",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
            on_click=(lambda e: on_resolver(rep)) if on_resolver else None,
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
                        ft.Text("Detalles de solicitud", size=16, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
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
                ft.Row(
                    controls=[
                        ft.Text(
                            f"Usuario ID: {rep.usuario_id}",
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT_PRIMARY,
                        ),
                        ft.Container(expand=True),
                        #badge_rol(rep.rol_nombre),
                    ],
                ),
                ft.Container(height=6),
                ft.Text("Asunto:", size=12, color=TEXT_SECONDARY, weight=ft.FontWeight.W_600),
                ft.Text(rep.tipo_servicio, size=13, color=TEXT_PRIMARY, weight=ft.FontWeight.W_500),
                ft.Container(height=6),
                ft.Text("Descripción:", size=12, color=TEXT_SECONDARY, weight=ft.FontWeight.W_600),
                ft.Text(rep.notas or "Sin notas", size=13, color=TEXT_SECONDARY),
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
                            ft.Text(str(rep.fecha_solicitud), size=13, color=TEXT_PRIMARY, weight=ft.FontWeight.W_500),
                        ],
                    ),
                ),
                ft.Container(height=6),
                ft.Row(controls=botones),
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
                    f"¿Eliminar la solicitud #{rep.solicitud_id}? "
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
                            on_click=(lambda e: on_confirmar(rep.solicitud_id)) if on_confirmar else None,
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
def solicitudes_servicio_content(page):
    solicitudes = SolicitudesServicioDAO().get_all()

    modal_overlay_ref = ft.Ref[ft.Container]()
    modal_backdrop_ref = ft.Ref[ft.Container]()
    modal_card_ref = ft.Ref[ft.Container]()
    lista_wrapper_ref = ft.Ref[ft.Column]()

    def _refrescar():
        nuevos = SolicitudesServicioDAO().get_all()
        lista_wrapper_ref.current.controls = [
            tarjeta_solicitud(r, on_click=abrir_detalle, on_resolver=confirmar_resuelto)
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
            on_resolver=confirmar_resuelto,
        )
        page.run_task(_abrir_con_contenido, tarjeta)

    def confirmar_resuelto(rep):
        SolicitudesServicioDAO().marcar_atendida(rep.solicitud_id)
        _refrescar()
        cerrar_modal()

    def abrir_eliminar(rep):
        page.run_task(
            _swap_contenido,
            dialogo_eliminar_reporte(rep, on_confirmar=confirmar_eliminar, on_cancelar=cerrar_modal),
        )

    def confirmar_eliminar(solicitud_id):
        SolicitudesServicioDAO().delete(solicitud_id)
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
                                    "Bandeja de Solicitudes de Servicio",
                                    size=17,
                                    weight=ft.FontWeight.BOLD,
                                    color=TEXT_PRIMARY,
                                ),
                            ],
                            spacing=8,
                        ),
                        ft.Text(
                            "Solicitudes de servicio recibidas.",
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
                                tarjeta_solicitud(r, on_click=abrir_detalle, on_resolver=confirmar_resuelto)
                                for r in solicitudes
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
def solicitud_apoyo(page: ft.Page, on_navigate=None, on_logout=None):
    active_route = "/apollo"

    return ft.View(
        route="/apollo",
        padding=0,
        bgcolor=MAIN_BG,
        controls=[
            ft.Column(
                controls=[
                    topbar(page, active_route),
                    ft.Row(
                        controls=[
                            sidebar(active_route=active_route, on_navigate=on_navigate, on_logout=on_logout),
                            ft.Container(
                                content=solicitudes_servicio_content(page),
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