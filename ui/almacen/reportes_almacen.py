import asyncio
from datetime import date, datetime

import flet as ft

from ui.colors import *
from dao.reportesEmp_dao import ReportsEmpDAO
from models.reportesEmp import ReportsEmp
from ui.almacen.Dashboard_almacen import sidebar, topbar


ROL_TRITURACION = 4


ESTADO_PENDIENTE = "Pendiente"
ESTADO_COMPLETADO = "Completado"

ESTADO_COLORES = {
    ESTADO_PENDIENTE: STAT_ORANGE,
    ESTADO_COMPLETADO: STAT_TEAL,
}


def _formatear_fecha(valor) -> str:
    if valor is None:
        return "-"
    if isinstance(valor, (datetime, date)):
        return valor.strftime("%d/%m/%Y")
    texto = str(valor)
    for formato in ("%Y-%m-%d", "%d/%m/%Y", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(texto, formato).strftime("%d/%m/%Y")
        except ValueError:
            continue
    return texto


# ── Badge de estado ──────────────────────────────────────────────────────
def badge_estado(estado: str):
    color = ESTADO_COLORES.get(estado, STAT_ORANGE)
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(
                    ft.Icons.CHECK_CIRCLE_OUTLINE
                    if estado == ESTADO_COMPLETADO
                    else ft.Icons.SCHEDULE,
                    size=13,
                    color=color,
                ),
                ft.Text(estado, size=11, color=color, weight=ft.FontWeight.W_600),
            ],
            spacing=6,
            tight=True,
        ),
        padding=ft.Padding.symmetric(horizontal=10, vertical=4),
        border_radius=999,
        bgcolor=ft.Colors.with_opacity(0.12, color),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.5, color)),
    )


# ── Fila de la tabla ─────────────────────────────────────────────────────
def fila_reporte(rep, on_click=None, on_resolver=None):

    es_pendiente = rep.estado == ESTADO_PENDIENTE

    return ft.Container(
        padding=16,
        border_radius=10,
        bgcolor=CARD_BG,
        ink=True,
        border=ft.Border.all(
            1,
            STAT_ORANGE if es_pendiente else DIVIDER
        ),
        on_click=lambda e: on_click(rep) if on_click else None,

        content=ft.Column(
            spacing=8,
            controls=[

                ft.Row(
                    controls=[
                        badge_estado(rep.estado),
                        ft.Container(expand=True),
                        ft.Container(expand=True)
                    ]
                ),


                ft.Text(
                    rep.asunto,
                    size=14,
                    weight=ft.FontWeight.BOLD,
                    color=TEXT_PRIMARY
                ),


                ft.Text(
                    rep.descripcion or "",
                    size=12,
                    color=TEXT_SECONDARY,
                    max_lines=3
                ),


                ft.Text(
                    f"Fecha: {_formatear_fecha(rep.fecha_reporte)}",
                    size=11,
                    color=TEXT_SECONDARY
                )
            ]
        )
    )



# ── Modal: Redactar reporte ──────────────────────────────────────────────
def redactar_reporte_card(on_cancelar=None, on_enviar=None):
    campo_asunto = ft.TextField(
        label="Asunto",
        color=TEXT_PRIMARY,
        label_style=ft.TextStyle(color=TEXT_SECONDARY),
        bgcolor="#0f1a30",
        border_color=CARD_BORDER,
        focused_border_color=STAT_BLUE,
        border_radius=10,
        border=ft.InputBorder.OUTLINE,
    )
    campo_descripcion = ft.TextField(
        label="Descripción",
        color=TEXT_PRIMARY,
        label_style=ft.TextStyle(color=TEXT_SECONDARY),
        bgcolor="#0f1a30",
        border_color=CARD_BORDER,
        focused_border_color=STAT_BLUE,
        border_radius=10,
        border=ft.InputBorder.OUTLINE,
        multiline=True,
        min_lines=5,
        max_lines=8,
    )
    texto_error = ft.Text("", size=12, color=STAT_RED, visible=False)

    def _enviar(e):
        asunto = (campo_asunto.value or "").strip()
        descripcion = (campo_descripcion.value or "").strip()
        if not asunto or not descripcion:
            texto_error.value = "Asunto y descripción son obligatorios."
            texto_error.visible = True
            texto_error.update()
            return
        if on_enviar:
            on_enviar(asunto, descripcion)

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
                        ft.Text("Redactar reporte", size=16, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
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
                    "Este reporte se enviará como Pendiente a nombre del "
                    "operador del Almacen conectado.",
                    size=12,
                    color=TEXT_SECONDARY,
                ),
                ft.Container(height=4),
                campo_asunto,
                campo_descripcion,
                texto_error,
                ft.Container(height=4),
                ft.Row(
                    controls=[
                        ft.Container(expand=True),
                        ft.OutlinedButton(
                            "Cancelar",
                            style=ft.ButtonStyle(
                                color=TEXT_SECONDARY,
                                side=ft.BorderSide(1, DIVIDER),
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                            on_click=(lambda e: on_cancelar(e)) if on_cancelar else None,
                        ),
                        ft.Container(width=10),
                        ft.ElevatedButton(
                            "Enviar reporte",
                            icon=ft.Icons.SEND_ROUNDED,
                            bgcolor=STAT_ORANGE,
                            color="#ffffff",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                            on_click=_enviar,
                        ),
                    ],
                ),
            ],
        ),
    )


# ── Modal: Detalles del reporte ──────────────────────────────────────────
def detalle_reporte_card(rep: ReportsEmp, on_cerrar=None, on_eliminar=None, on_resolver=None):
    boton_principal = None


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
                ft.Row(
                    controls=[
                        ft.Text(f"Reporte #{rep.reporte_id}", size=14, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                        ft.Container(expand=True),
                        badge_estado(rep.estado),
                    ],
                ),
                ft.Container(height=6),
                ft.Text("Asunto:", size=12, color=TEXT_SECONDARY, weight=ft.FontWeight.W_600),
                ft.Text(rep.asunto, size=13, color=TEXT_PRIMARY, weight=ft.FontWeight.W_500),
                ft.Container(height=6),
                ft.Text("Descripción:", size=12, color=TEXT_SECONDARY, weight=ft.FontWeight.W_600),
                ft.Text(rep.descripcion or "—", size=13, color=TEXT_SECONDARY),
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
                            ft.Text(
                                _formatear_fecha(rep.fecha_reporte),
                                size=13,
                                color=TEXT_PRIMARY,
                                weight=ft.FontWeight.W_500,
                            ),
                        ],
                    ),
                ),
                ft.Container(height=6),
                ft.Row(controls=botones),
            ],
        ),
    )


# ── Modal: Confirmar eliminación ─────────────────────────────────────────
def dialogo_eliminar_reporte(rep: ReportsEmp, on_confirmar=None, on_cancelar=None):
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
                    f'¿Desea eliminar el reporte "{rep.asunto}" (#{rep.reporte_id})? '
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


# ── Contenido central: tabla + barra de herramientas + modal────────
def reportes_trituracion_content(page, empleado_id):

    dao = ReportsEmpDAO()

    reportes = dao.get_by_rol(ROL_TRITURACION)


    lista_ref = ft.Ref[ft.Column]()

    def abrir_detalle(rep):
        modal = detalle_reporte_card(
            rep,
            on_cerrar=lambda e: cerrar_dialogo(),
            on_eliminar=abrir_eliminar,
        )

        mostrar_modal(modal)

    def abrir_eliminar(rep):
        modal = dialogo_eliminar_reporte(
            rep,
            on_confirmar=eliminar_reporte,
            on_cancelar=lambda e: cerrar_dialogo()
        )

        mostrar_modal(modal)


    def eliminar_reporte(reporte_id):
        dao.delete(reporte_id)

        cerrar_dialogo()
        refrescar()

    def abrir_nuevo_reporte(e=None):
        print("Abriendo modal")

        modal = redactar_reporte_card(
            on_cancelar=lambda e: cerrar_dialogo(),
            on_enviar=guardar_reporte
        )

        mostrar_modal(modal)


    def cerrar_dialogo():
        page.overlay.clear()
        page.update()

    def guardar_reporte(asunto, descripcion):
        nuevo = ReportsEmp(
            reporte_id=None,
            asunto=asunto,
            descripcion=descripcion,
            fecha_reporte=datetime.now(),
            estado=ESTADO_PENDIENTE,
            empleado_id=empleado_id
        )

        dao.insert(nuevo)

        cerrar_dialogo()
        refrescar()

    def refrescar():
        if lista_ref.current is None:
            return

        nuevos = dao.get_by_rol(ROL_TRITURACION)

        lista_ref.current.controls = [
            fila_reporte(
                r,
                on_click=abrir_detalle,
                on_resolver=confirmar_resuelto
            )
            for r in nuevos
        ]
        lista_ref.current.update()
        lista_ref.current.update()

    def confirmar_resuelto(rep):
        dao.marcar_resuelto(rep.reporte_id)
        refrescar()

        lista_ref.current.update()

    def mostrar_modal(modal):
        contenedor_modal = ft.Container(
            expand=True,
            bgcolor=ft.Colors.with_opacity(0.45, "#000000"),
            alignment=ft.Alignment.CENTER,
            content=modal,
        )

        page.overlay.append(contenedor_modal)
        page.update()

    return ft.Stack(
        expand=True,
        controls=[

            ft.Container(
                expand=True,
                bgcolor=MAIN_BG,
                padding=20,

                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Container(expand=True),
                                ft.ElevatedButton(
                                    "Nuevo reporte",
                                    icon=ft.Icons.ADD,
                                    bgcolor=STAT_ORANGE,
                                    color="#ffffff",
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=8)
                                    ),
                                    on_click=abrir_nuevo_reporte
                                )
                            ]
                        ),

                        ft.Divider(
                            color=DIVIDER
                        ),

                        ft.Column(
                            ref=lista_ref,
                            spacing=12,
                            expand=True,
                            scroll=ft.ScrollMode.AUTO,

                            controls=[
                                fila_reporte(
                                    r,
                                    on_click=abrir_detalle,
                                    on_resolver=confirmar_resuelto
                                )
                                for r in reportes
                            ]
                        )

                    ],

                    expand=True
                )
            )
        ]
    )


# ── Vista completa (conectada a sidebar/topbar) ─────────────────────────────
def reportes_almacen(page: ft.Page, empleado_id, on_navigate=None, on_logout=None):

    active_route = "/reportes_almacen"

    return ft.View(
        route=active_route,
        padding=0,
        bgcolor=MAIN_BG,
        controls=[
            ft.Column(
                spacing=0,
                expand=True,
                controls=[
                    topbar(page, active_route),
                    ft.Row(
                        spacing=0,
                        expand=True,
                        controls=[
                            sidebar(active_route=active_route, on_navigate=on_navigate, on_logout=on_logout),
                            ft.Container(
                                content=reportes_trituracion_content(page, empleado_id),
                                expand=True,
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )