import asyncio
from datetime import date

import flet as ft

from ui.colors import *
from dao import *
from models import *
from ui.almacen.Dashboard_almacen import sidebar, topbar


# ── Badges de estado ─────────────────────────────────────────────────────
def badge_estado_stock(cantidad_disponible_kg, stock_minimo, stock_maximo):
    if cantidad_disponible_kg <= stock_minimo:
        label, color = "Bajo", STAT_ORANGE
    elif stock_maximo and cantidad_disponible_kg >= stock_maximo:
        label, color = "Alto", STAT_TEAL
    else:
        label, color = "Normal", STAT_BLUE

    return ft.Container(
        content=ft.Text(label, size=11, color=color, weight=ft.FontWeight.W_600),
        padding=ft.Padding.symmetric(horizontal=10, vertical=4),
        border_radius=6,
        bgcolor=ft.Colors.with_opacity(0.12, color),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.5, color)),
    )


def campo_busqueda(hint_text: str):
    return ft.TextField(
        hint_text=hint_text,
        prefix_icon=ft.Icons.SEARCH,
        border_radius=8,
        border_color=DIVIDER,
        bgcolor=CARD_BG,
        content_padding=ft.Padding.symmetric(horizontal=14, vertical=10),
        text_size=13,
        expand=True,
    )


def boton_accion(texto: str, on_click=None, bgcolor=None):
    return ft.ElevatedButton(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.ADD, size=16, color="#fff"),
                ft.Text(texto, size=13, color="#fff", weight=ft.FontWeight.W_600),
            ],
            spacing=6,
            tight=True,
        ),
        bgcolor=bgcolor or STAT_BLUE,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=lambda e: on_click(e) if on_click else None,
    )


def cambiar_hover(e):

    e.control.bgcolor = (
        ft.Colors.with_opacity(0.04, STAT_BLUE)
        if e.data == "true"
        else CARD_BG
    )

    e.control.update()


def encabezado_columnas(columnas):
    return ft.Container(
        padding=15,
        bgcolor=ft.Colors.with_opacity(0.04, TEXT_PRIMARY),
        border_radius=10,
        content=ft.Row(
            controls=[
                ft.Container(
                    ft.Text(texto, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                    expand=exp,
                )
                for texto, exp in columnas
            ]
        ),
    )


def fila_valores(valores, on_click=None):
    celdas = []
    for valor, exp, color in valores:
        contenido = valor if isinstance(valor, ft.Control) else ft.Text(valor, color=color or TEXT_SECONDARY)
        celdas.append(ft.Container(contenido, expand=exp))

    return ft.Container(
        padding=15,
        border=ft.Border.only(bottom=ft.BorderSide(1, DIVIDER)),
        ink=True,
        on_click=(lambda e: on_click(e)) if on_click else None,
        content=ft.Row(controls=celdas),
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
    return ft.Row(controles=controles, alignment=ft.MainAxisAlignment.CENTER, spacing=2) if False else ft.Row(controls=controles, alignment=ft.MainAxisAlignment.CENTER, spacing=2)


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


# ── Tarjetas de estadísticas ─────────────────────────────────────────────
def tarjeta_estadistica(titulo: str, valor: str, color):
    return ft.Container(
        expand=True,
        bgcolor=CARD_BG,
        border_radius=10,
        padding=16,
        content=ft.Column(
            spacing=4,
            controls=[
                ft.Text(titulo, size=12, color=TEXT_SECONDARY),
                ft.Text(valor, size=22, weight=ft.FontWeight.BOLD, color=color),
            ],
        ),
    )


def fila_estadisticas(stock):
    total_productos = len(stock)
    total_kg = sum(s.cantidad_disponible_kg for s in stock)
    en_alerta = sum(1 for s in stock if s.cantidad_disponible_kg <= s.stock_minimo)

    return ft.Row(
        spacing=14,
        controls=[
            tarjeta_estadistica("Productos en stock", str(total_productos), STAT_BLUE),
            tarjeta_estadistica("Kg totales en almacén", f"{total_kg:,.0f} kg", STAT_TEAL),
            tarjeta_estadistica("Productos en alerta", str(en_alerta), STAT_ORANGE),
        ],
    )


# ── Campo editable genérico (mismo patrón que empleados_admin.py) ──────────
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


# ── Formulario: editar stock (stock_minimo / stock_maximo) ──────────────────
def formulario_editar_stock(item, on_guardar=None, on_cancelar=None):
    material_field = campo_editable("Material (ID)", str(item.material_id))
    cantidad_field = campo_editable("Cantidad disponible (kg)", str(item.cantidad_disponible_kg))
    minimo_field = campo_editable("Stock mínimo (kg)", str(item.stock_minimo))
    maximo_field = campo_editable("Stock máximo (kg)", str(item.stock_maximo))

    def _guardar(e):
        datos_editados = {
            "stock_producto_id": item.stock_producto_id,
            "material_id": material_field.value,
            "cantidad_disponible_kg": cantidad_field.value,
            "stock_minimo": minimo_field.value,
            "stock_maximo": maximo_field.value,
        }
        if on_guardar:
            on_guardar(datos_editados)

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
            spacing=12,
            tight=True,
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Editar stock", size=16, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
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
                material_field,
                ft.Row(controls=[minimo_field, maximo_field], spacing=10),
                cantidad_field,
                ft.Container(height=6),
                ft.Row(
                    controls=[
                        ft.OutlinedButton(
                            "Cancelar",
                            style=ft.ButtonStyle(
                                color=STAT_ORANGE,
                                side=ft.BorderSide(1, STAT_ORANGE),
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                            on_click=(lambda e: on_cancelar(e)) if on_cancelar else None,
                        ),
                        ft.Container(expand=True),
                        ft.ElevatedButton(
                            "Guardar cambios",
                            bgcolor=STAT_BLUE,
                            color="#fff",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                            on_click=_guardar,
                        ),
                    ],
                ),
            ],
        ),
    )


# ── Formulario: nueva entrada de inventario ─────────────────────────────────
def formulario_nueva_entrada(on_guardar=None, on_cancelar=None):
    neumatico_field = campo_editable("Neumático (ID)", "")
    ubicacion_field = campo_editable("Ubicación (ID)", "")

    fecha_field = campo_editable("Fecha de ingreso", "DD/MM/AAAA")

    error_text = ft.Text("", size=12, color=STAT_ORANGE, visible=False)

    def _guardar(e):
        if not all([neumatico_field.value, ubicacion_field.value, fecha_field.value]):
            error_text.value = "Completa neumático, ubicación y fecha de ingreso."
            error_text.visible = True
            error_text.update()
            return

        datos_nuevos = {
            "neumatico_id": neumatico_field.value,
            "ubicacion_id": ubicacion_field.value,
            "fecha_ingreso": fecha_field.value,
        }
        if on_guardar:
            on_guardar(datos_nuevos)

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
            spacing=12,
            tight=True,
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Nueva entrada", size=16, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
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
                neumatico_field,
                ubicacion_field,
                fecha_field,
                error_text,
                ft.Container(height=6),
                ft.Row(
                    controls=[
                        ft.OutlinedButton(
                            "Cancelar",
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
                                    ft.Text("Registrar entrada", size=13, color="#fff", weight=ft.FontWeight.W_600),
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


# ── Formulario: nueva baja de inventario ────────────────────────────────────
def formulario_nueva_baja(on_guardar=None, on_cancelar=None):
    producto_field = campo_editable("Producto en stock (ID)", "")
    cantidad_field = ft.TextField(
        label="Cantidad (kg)",
        keyboard_type=ft.KeyboardType.NUMBER,
        border_radius=8,
        border_color=DIVIDER,
        bgcolor=CARD_BG,
        text_size=13,
        label_style=ft.TextStyle(size=11, color=TEXT_SECONDARY),
        content_padding=ft.Padding.symmetric(horizontal=12, vertical=8),
    )
    motivo_field = ft.TextField(
        label="Motivo de baja",
        multiline=True,
        min_lines=3,
        max_lines=4,
        border_radius=8,
        border_color=DIVIDER,
        bgcolor=CARD_BG,
        text_size=13,
        label_style=ft.TextStyle(size=12, color=TEXT_SECONDARY),
    )

    error_text = ft.Text("", size=12, color=STAT_ORANGE, visible=False)

    def _guardar(e):
        if not all([producto_field.value, cantidad_field.value, motivo_field.value]):
            error_text.value = "Completa producto, cantidad y motivo de la baja."
            error_text.visible = True
            error_text.update()
            return

        datos_nuevos = {
            "stock_producto_id": producto_field.value,
            "cantidad_kg": cantidad_field.value,
            "motivo": motivo_field.value,
            "fecha_baja": date.today(),
        }
        if on_guardar:
            on_guardar(datos_nuevos)

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
            spacing=12,
            tight=True,
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Registrar baja", size=16, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
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
                producto_field,
                cantidad_field,
                motivo_field,
                error_text,
                ft.Container(height=6),
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
                            "Confirmar baja",
                            bgcolor=STAT_ORANGE,
                            color="#fff",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                            on_click=_guardar,
                        ),
                    ],
                ),
            ],
        ),
    )


# ── Tabla: Stock de productos ───────────────────────────────────────────────
COLUMNAS_STOCK = [
    ("ID", 1),
    ("Material", 3),
    ("Disponible (kg)", 2),
    ("Mínimo / Máximo", 2),
    ("Estado", 2),
    ("Actualizado", 2),
]


def fila_stock(item, on_click=None):
    return fila_valores(
        [
            (f"STK-{item.stock_producto_id:03d}", 1, TEXT_SECONDARY),
            (f"Material {item.material_id}", 3, TEXT_PRIMARY),
            (f"{item.cantidad_disponible_kg:,.0f} kg", 2, TEXT_PRIMARY),
            (f"{item.stock_minimo:,.0f} / {item.stock_maximo:,.0f} kg", 2, TEXT_SECONDARY),
            (badge_estado_stock(item.cantidad_disponible_kg, item.stock_minimo, item.stock_maximo), 2, None),
            (str(item.fecha_actualizacion) if item.fecha_actualizacion else "—", 2, TEXT_SECONDARY),
        ],
        on_click=(lambda e: on_click(item)) if on_click else None,
    )


def tabla_stock(items, on_click=None):
    return ft.Container(
        expand=True,
        bgcolor=CARD_BG,
        ink=True,
        on_hover=lambda e: cambiar_hover(e),
        border_radius=10,
        padding=15,
        content=ft.Column(
            spacing=0,
            controls=[
                encabezado_columnas(COLUMNAS_STOCK),
                ft.Divider(height=1),
                ft.ListView(
                    expand=True,
                    spacing=0,
                    controls=[fila_stock(item, on_click) for item in items],
                ),
            ],
        ),
    )


# ── Tabla: Entradas de inventario ───────────────────────────────────────────
COLUMNAS_ENTRADA = [
    ("ID", 1),
    ("Neumático", 3),
    ("Ubicación", 3),
    ("Fecha de ingreso", 3),
]


def fila_entrada(item):
    return fila_valores(
        [
            (f"ENT-{item.inventario_id:03d}", 1, TEXT_SECONDARY),
            (f"Neumático {item.neumatico_id}", 3, TEXT_PRIMARY),
            (f"Ubicación {item.ubicacion_id}", 3, TEXT_SECONDARY),
            (str(item.fecha_ingreso) if item.fecha_ingreso else "—", 3, TEXT_SECONDARY),
        ],
    )


def tabla_entradas(items):
    return ft.Container(
        expand=True,
        bgcolor=CARD_BG,
        ink=True,
        on_hover=lambda e: cambiar_hover(e),
        border_radius=10,
        padding=15,
        content=ft.Column(
            spacing=0,
            controls=[
                encabezado_columnas(COLUMNAS_ENTRADA),
                ft.Divider(height=1),
                ft.ListView(
                    expand=True,
                    spacing=0,
                    controls=[fila_entrada(item) for item in items],
                ),
            ],
        ),
    )


# ── Tabla: Bajas de inventario ──────────────────────────────────────────────
COLUMNAS_BAJA = [
    ("ID", 1),
    ("Producto", 2),
    ("Cantidad (kg)", 2),
    ("Motivo", 4),
    ("Fecha de baja", 2),
]


def fila_baja(item):
    return fila_valores(
        [
            (f"BJ-{item.baja_inventario_id:03d}", 1, TEXT_SECONDARY),
            (f"STK-{item.stock_producto_id:03d}", 2, TEXT_PRIMARY),
            (f"{item.cantidad_kg:,.0f} kg", 2, STAT_ORANGE),
            (item.motivo or "—", 4, TEXT_SECONDARY),
            (str(item.fecha_baja) if item.fecha_baja else "—", 2, TEXT_SECONDARY),
        ],
    )


def tabla_bajas(items):
    return ft.Container(
        expand=True,
        bgcolor=CARD_BG,
        ink=True,
        on_hover=lambda e: cambiar_hover(e),
        border_radius=10,
        padding=15,
        content=ft.Column(
            spacing=0,
            controls=[
                encabezado_columnas(COLUMNAS_BAJA),
                ft.Divider(height=1),
                ft.ListView(
                    expand=True,
                    spacing=0,
                    controls=[fila_baja(item) for item in items],
                ),
            ],
        ),
    )


# ── Contenido de Almacén ─────────────────────────────────────────────────
def almacen_content(page: ft.Page):
    stock_items = StockProductosDAO().get_all()
    entrada_items = InventarioEntradaDAO().get_all()
    baja_items = BajasInventarioDAO().get_all()

    modal_overlay_ref = ft.Ref[ft.Container]()
    modal_backdrop_ref = ft.Ref[ft.Container]()
    modal_card_ref = ft.Ref[ft.Container]()
    tabs_ref = ft.Ref[ft.Tabs]()
    stats_ref = ft.Ref[ft.Row]()
    stock_wrapper_ref = ft.Ref[ft.Container]()
    entradas_wrapper_ref = ft.Ref[ft.Container]()
    bajas_wrapper_ref = ft.Ref[ft.Container]()

    def _refrescar_stock():
        nuevos = StockProductosDAO().get_all()
        stock_wrapper_ref.current.content = tabla_stock(nuevos, abrir_editar_stock)
        stock_wrapper_ref.current.update()
        stats_ref.current.controls = fila_estadisticas(nuevos).controls
        stats_ref.current.update()

    def _refrescar_entradas():
        nuevos = InventarioEntradaDAO().get_all()
        entradas_wrapper_ref.current.content = tabla_entradas(nuevos)
        entradas_wrapper_ref.current.update()

    def _refrescar_bajas():
        nuevos = BajasInventarioDAO().get_all()
        bajas_wrapper_ref.current.content = tabla_bajas(nuevos)
        bajas_wrapper_ref.current.update()

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

    def _abrir_modal(contenido):
        async def _abrir():
            modal_card_ref.current.content = contenido
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

    # -- Materiales --

    def guardar_nuevo_material(datos):
        nuevo = materiales(
            material_id=None,
            nombre=datos["nombre"],
            descripcion=datos["descripcion"],
            unidad=datos["unidad"]
        )

        MaterialesDAO().insert(nuevo)

        cerrar_modal()

    def abrir_nuevo_material(e=None):
        _abrir_modal(
            formulario_nuevo_material(
                on_guardar=guardar_nuevo_material,
                on_cancelar=cerrar_modal
            )
        )
    # -- Stock --
    def guardar_edicion_stock(datos):
        item_actualizado = StockProductosDAO().get_by_id(datos["stock_producto_id"])
        item_actualizado.material_id = datos["material_id"]
        item_actualizado.cantidad_disponible_kg = datos["cantidad_disponible_kg"]
        item_actualizado.stock_minimo = datos["stock_minimo"]
        item_actualizado.stock_maximo = datos["stock_maximo"]
        item_actualizado.fecha_actualizacion = date.today()
        StockProductosDAO().update(item_actualizado)
        _refrescar_stock()
        cerrar_modal()

    def abrir_editar_stock(item):
        _abrir_modal(formulario_editar_stock(item, on_guardar=guardar_edicion_stock, on_cancelar=cerrar_modal))

    # -- Entradas --
    def guardar_nueva_entrada(datos):
        nueva = inventario_entrada(
            inventario_id=None,
            neumatico_id=datos["neumatico_id"],
            ubicacion_id=datos["ubicacion_id"],
            fecha_ingreso=datos["fecha_ingreso"],
        )
        InventarioEntradaDAO().insert(nueva)
        _refrescar_entradas()
        cerrar_modal()

    def abrir_nueva_entrada(e=None):
        _abrir_modal(formulario_nueva_entrada(on_guardar=guardar_nueva_entrada, on_cancelar=cerrar_modal))

    # -- Bajas --
    def guardar_nueva_baja(datos):
        nueva = bajas_inventario(
            baja_inventario_id=None,
            stock_producto_id=datos["stock_producto_id"],
            cantidad_kg=datos["cantidad_kg"],
            motivo=datos["motivo"],
            fecha_baja=datos["fecha_baja"],
        )
        BajasInventarioDAO().insert(nueva)
        _refrescar_bajas()
        _refrescar_stock()
        cerrar_modal()

    def abrir_nueva_baja(e=None):
        _abrir_modal(formulario_nueva_baja(on_guardar=guardar_nueva_baja, on_cancelar=cerrar_modal))

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

    pestana_stock = ft.Container(
        padding=ft.Padding.only(top=16),
        content=ft.Column(
            spacing=12,
            expand=True,
            controls=[
                ft.Row(
                    controls=[
                        campo_busqueda("Buscar por material"),
                        boton_accion(
                            "Agregar material",
                            abrir_nuevo_material
                        )
                    ],
                    spacing=12,
                ),
                ft.Container(
                    ref=stock_wrapper_ref,
                    expand=True,
                    content=tabla_stock(stock_items, abrir_editar_stock),
                ),
                ft.Row(controls=[paginacion(1, 1)], alignment=ft.MainAxisAlignment.CENTER),
            ],
        ),
    )

    pestana_entradas = ft.Container(
        padding=ft.Padding.only(top=16),
        content=ft.Column(
            spacing=12,
            expand=True,
            controls=[
                ft.Row(
                    controls=[campo_busqueda("Buscar por neumático o ubicación"), boton_accion("Registrar entrada", abrir_nueva_entrada)],
                    spacing=12,
                ),
                ft.Container(
                    ref=entradas_wrapper_ref,
                    expand=True,
                    content=tabla_entradas(entrada_items),
                ),
                ft.Row(controls=[paginacion(1, 1)], alignment=ft.MainAxisAlignment.CENTER),
            ],
        ),
    )

    pestana_bajas = ft.Container(
        padding=ft.Padding.only(top=16),
        content=ft.Column(
            spacing=12,
            expand=True,
            controls=[
                ft.Row(
                    controls=[campo_busqueda("Buscar por producto o motivo"), boton_accion("Registrar baja", abrir_nueva_baja, bgcolor=STAT_ORANGE)],
                    spacing=12,
                ),
                ft.Container(
                    ref=bajas_wrapper_ref,
                    expand=True,
                    content=tabla_bajas(baja_items),
                ),
                ft.Row(controls=[paginacion(1, 1)], alignment=ft.MainAxisAlignment.CENTER),
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
                        ft.Row(ref=stats_ref, controls=fila_estadisticas(stock_items).controls, spacing=14),
                        ft.Container(height=16),
                        ft.Tabs(
                            content=ft.Column(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Tab("Stock de productos"),
                                            ft.Tab("Entradas de inventario"),
                                            ft.Tab("Bajas de inventario"),
                                        ]
                                    ),
                                    ft.Container(
                                        content=pestana_stock,
                                        expand=True,
                                    ),
                                ],
                                expand=True,
                            ),
                            length=3,
                            selected_index=0,
                            expand=True,
                        )
                    ],
                    spacing=0,
                    expand=True,
                ),
            ),
            boton_informacion(),
            modal_overlay,
        ],
        expand=True,
    )


def formulario_nuevo_material(on_guardar=None, on_cancelar=None):

    nombre_field = campo_editable("Nombre del material", "")
    descripcion_field = campo_editable("Descripción", "")
    unidad_field = campo_editable("Unidad de medida", "kg")

    def _guardar(e):

        if not nombre_field.value:
            return

        datos = {
            "nombre": nombre_field.value,
            "descripcion": descripcion_field.value,
            "unidad": unidad_field.value,
        }

        if on_guardar:
            on_guardar(datos)

    return ft.Container(
        width=460,
        bgcolor=CARD_BG,
        border_radius=14,
        padding=24,

        content=ft.Column(
            spacing=12,
            tight=True,

            controls=[

                ft.Row(
                    controls=[
                        ft.Text(
                            "Nuevo material",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT_PRIMARY
                        ),

                        ft.Container(expand=True),

                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            on_click=(
                                lambda e: on_cancelar(e)
                            ) if on_cancelar else None
                        )
                    ]
                ),

                ft.Divider(),

                nombre_field,
                descripcion_field,
                unidad_field,

                ft.Row(
                    controls=[

                        ft.OutlinedButton(
                            "Cancelar",
                            on_click=(
                                lambda e: on_cancelar(e)
                            ) if on_cancelar else None
                        ),

                        ft.Container(expand=True),

                        ft.ElevatedButton(
                            "Guardar",
                            bgcolor=STAT_BLUE,
                            color="white",
                            on_click=_guardar
                        )

                    ]
                )
            ]
        )
    )


def panel_inventario(page: ft.Page, on_navigate=None, on_logout=None):
    active_route = "/inventario"

    return ft.View(
        route="/inventario",
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
                                content=almacen_content(page),
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