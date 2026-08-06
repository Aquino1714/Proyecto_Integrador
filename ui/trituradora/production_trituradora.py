import asyncio
from datetime import date

import flet as ft
from datetime import datetime


from ui.colors import *
from dao.empleado_dao import EmpleadoDAO
from models.empleado import Empleado
from dao.lote_production_dao import ProductionloteDAO
from models.lote_producc import Productionlote
from ui.trituradora.dashboar_trituradora import sidebar, topbar

ROLES_MAP = {
    1: "Administrador",
    2: "Chofer",
    3: "Recepcion",
    4: "Almacen",
    5: "Triturador",
    6: "Distribucion",
}

ESTADOS = {
    "En preparación",
    "En trituración",
    "Finalizado",
}

TURNOS = [
    "Matutino",
    "Vespertino",
    "Nocturno"
]


ROL_ID_MAP = {v: k for k, v in ROLES_MAP.items()}

ROLES_FILTRO = ["Completado", "En proceso", "Pendiente"]

ROL_COLORES = {
    "Administrador": STAT_BLUE,
    "Chofer": "#9ca3af",
    "Recepcion": "#ffaa00",
    "Almacen": "#ffaa00",
    "Triturador": "#ffaa00",
    "Distribucion": "#ffaa00",
}


def badge_rol(rol: str):
    color = ROL_COLORES.get(rol, STAT_BLUE)
    return ft.Container(
        content=ft.Text(rol, size=11, color=color, weight=ft.FontWeight.W_600),
        padding=ft.Padding.symmetric(horizontal=10, vertical=4),
        border_radius=6,
        bgcolor=ft.Colors.with_opacity(0.12, color),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.5, color)),
    )


def buscador_producto():
    return ft.TextField(
        hint_text="Buscar por Producto u Operador....",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=8,
        border_color=DIVIDER,
        bgcolor=CARD_BG,
        content_padding=ft.Padding.symmetric(horizontal=14, vertical=10),
        text_size=13,
        expand=True,
    )

def boton_nuevo_lote(on_nuevo_lote=None):
    return ft.ElevatedButton(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.ADD, size=16, color="#fff"),
                ft.Text(
                    "Nuevo lote",
                    size=13,
                    color="#fff",
                    weight=ft.FontWeight.W_600,
                ),
            ],
            spacing=6,
            tight=True,
        ),
        bgcolor=STAT_BLUE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8)
        ),
        on_click=lambda e: on_nuevo_lote(e) if on_nuevo_lote else None,
    )

def filtro_row(on_aplicar_filtro=None):
    dropdown = ft.Dropdown(
        hint_text="Filtrar",
        width=180,
        border_radius=8,
        border_color=DIVIDER,
        text_size=13,
        options=[ft.dropdown.Option(r) for r in ROLES_FILTRO],
    )
    aplicar_btn = ft.ElevatedButton(
        "Aplicar",
        bgcolor=STAT_ORANGE,
        color="#fff",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=lambda e: on_aplicar_filtro(dropdown.value) if on_aplicar_filtro else None,
    )
    return ft.Row(controls=[dropdown, aplicar_btn], spacing=10)
def cambiar_hover(e):

    e.control.bgcolor = (
        ft.Colors.with_opacity(0.04, STAT_BLUE)
        if e.data == "true"
        else CARD_BG
    )

    e.control.update()


def tabla_lotes(lotes, on_ver_detalle=None):

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

                encabezado_tabla(),

                ft.Divider(height=1),

                ft.ListView(
                    expand=True,
                    spacing=0,
                    controls=[
                        fila_lote(lot, on_ver_detalle)
                        for lot in lotes
                    ]
                ),
            ]
        ),
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
    return ft.Row(controles, alignment=ft.MainAxisAlignment.CENTER, spacing=2) if False else ft.Row(controls=controles, alignment=ft.MainAxisAlignment.CENTER, spacing=2)


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
                side=ft.BorderSide(
                    width=2,
                    color="#ffffff"
                ),
            ),
        ),
        right=20,
        bottom=20,
    )


# ── Tarjeta de detalle (modal) ──────────────────────────────────────────────
def campo_detalle(etiqueta: str, valor: str, color_valor=None):
    return ft.Container(
        padding=ft.Padding.symmetric(vertical=6),
        content=ft.Column(
            controls=[
                ft.Text(etiqueta, size=12, color=TEXT_SECONDARY),
                ft.Text(valor, size=13, color=color_valor or TEXT_PRIMARY, weight=ft.FontWeight.W_500),
            ],
            spacing=2,
        ),
    )


def detalle_lote_card(lote, on_cerrar=None, on_editar=None, on_dar_baja=None):

    botones = []

    if on_editar:
        botones.append(
            ft.ElevatedButton(
                expand=True,
                height=44,
                bgcolor=STAT_ORANGE,
                color="#fff",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8)
                ),
                content=ft.Text(
                    "Editar registro",
                    weight=ft.FontWeight.W_600
                ),
                on_click=lambda e: on_editar(lote)
            )
        )

    if on_dar_baja:
        botones.append(
            ft.OutlinedButton(
                expand=True,
                height=44,
                style=ft.ButtonStyle(
                    color=TEXT_PRIMARY,
                    side=ft.BorderSide(1, DIVIDER),
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
                content=ft.Text(
                    "Dar de baja",
                    weight=ft.FontWeight.W_600
                ),
                on_click=lambda e: on_dar_baja(lote)
            )
        )

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
                        ft.Container(
                            width=42,
                            height=42,
                            border_radius=10,
                            bgcolor=ft.Colors.with_opacity(
                                0.15,
                                STAT_ORANGE
                            ),
                            alignment=ft.Alignment.CENTER,
                            content=ft.Icon(
                                ft.Icons.INVENTORY_2_ROUNDED,
                                color=STAT_ORANGE,
                                size=20
                            ),
                        ),

                        ft.Column(
                            spacing=0,
                            controls=[
                                ft.Text(
                                    "Detalle del lote",
                                    size=15,
                                    weight=ft.FontWeight.BOLD,
                                    color=TEXT_PRIMARY
                                ),
                                ft.Text(
                                    f"L-{lote.lote_id:04d}",
                                    size=12,
                                    color=TEXT_SECONDARY
                                ),
                            ],
                        ),

                        ft.Container(expand=True),

                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            icon_color=TEXT_SECONDARY,
                            icon_size=18,
                            on_click=(
                                lambda e: on_cerrar(e)
                            ) if on_cerrar else None,
                        ),
                    ],
                ),

                ft.Row(
                    controls=[
                        campo_detalle(
                            "# ID del lote",
                            f"LOT-{lote.lote_id:04d}"
                        ),
                        campo_detalle(
                            "Producto",
                            lote.producto
                        ),
                    ],
                    spacing=12,
                ),

                ft.Row(
                    controls=[
                        campo_detalle(
                            "Operador",
                            lote.operador
                        ),
                        campo_detalle(
                            "Turno",
                            lote.turno
                        ),
                    ],
                    spacing=12,
                ),

                campo_detalle(
                    "Cantidad",
                    f"{lote.cantidad_kg} kg"
                ),

                campo_detalle(
                    "Estado",
                    lote.estado
                ),

                ft.Row(
                    controls=botones,
                    spacing=10,
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
        label_style=ft.TextStyle(
            size=11,
            color=TEXT_SECONDARY,
        ),
        content_padding=ft.Padding.symmetric(
            horizontal=12,
            vertical=8
        ),
    )

def formulario_editar_lote(lote, on_guardar=None, on_cancelar=None):

    cantidad_field = ft.TextField(
        value=str(lote.cantidad_kg),
        width=150,
        text_align=ft.TextAlign.CENTER,
        border_radius=8,
        border_color=DIVIDER,
        bgcolor=CARD_BG,
        text_size=13,
    )


    def cambiar_cantidad(valor):
        try:
            actual = float(cantidad_field.value)
        except:
            actual = 0

        actual += valor

        if actual < 0:
            actual = 0

        cantidad_field.value = str(int(actual))
        cantidad_field.update()


    cantidad_box = ft.Row(
        controls=[

            ft.IconButton(
                icon=ft.Icons.REMOVE,
                bgcolor=ft.Colors.with_opacity(
                    0.15,
                    STAT_ORANGE
                ),
                icon_color=STAT_ORANGE,
                on_click=lambda e: cambiar_cantidad(-100),
            ),

            cantidad_field,

            ft.IconButton(
                icon=ft.Icons.ADD,
                bgcolor=ft.Colors.with_opacity(
                    0.15,
                    STAT_BLUE
                ),
                icon_color=STAT_BLUE,
                on_click=lambda e: cambiar_cantidad(100),
            ),
        ],
        spacing=5,
    )


    producto_field = ft.TextField(
        label="Producto",
        value=lote.producto,
        expand=True,
        border_radius=8,
        border_color=DIVIDER,
        bgcolor=CARD_BG,
        text_size=13,
        label_style=ft.TextStyle(
            size=12,
            color=TEXT_SECONDARY
        ),
        content_padding=ft.Padding.symmetric(
            horizontal=12,
            vertical=10
        ),
    )


    estado_dropdown = ft.Dropdown(
        label="Estado",
        value=lote.estado,
        expand=True,
        border_radius=8,
        border_color=DIVIDER,
        text_size=13,
        options=[
            ft.dropdown.Option(e)
            for e in ESTADOS
        ],
    )


    turno_dropdown = ft.Dropdown(
        label="Turno",
        value=lote.turno,
        expand=True,
        border_radius=8,
        border_color=DIVIDER,
        text_size=13,
        options=[
            ft.dropdown.Option(t)
            for t in TURNOS
        ],
    )


    # Solo lectura
    hora_inicio_field = ft.TextField(
        label="Hora de inicio",
        value=str(lote.hora_inicio),
        read_only=True,
        expand=True,
        border_radius=8,
        border_color=DIVIDER,
        prefix_icon=ft.Icons.ACCESS_TIME,
    )


    def _guardar(e):

        datos_editados = {

            "lote_id": lote.lote_id,

            "empleado_id": lote.empleado_id,

            "cantidad_kg": float(
                cantidad_field.value
            ),

            "estado": estado_dropdown.value,

            "producto": producto_field.value,

            "turno": turno_dropdown.value,

            # conserva la original
            "hora_inicio": lote.hora_inicio,
        }


        if on_guardar:
            on_guardar(datos_editados)



    return ft.Container(

        width=560,

        bgcolor=CARD_BG,

        border_radius=14,

        padding=24,

        shadow=ft.BoxShadow(
            blur_radius=30,
            color=ft.Colors.with_opacity(
                0.35,
                "#000000"
            ),
            offset=ft.Offset(
                0,
                10
            ),
        ),

        content=ft.Column(
            spacing=14,
            tight=True,
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            width=46,
                            height=46,
                            border_radius=12,
                            bgcolor=ft.Colors.with_opacity(
                                .12,
                                STAT_BLUE
                            ),
                            alignment=ft.Alignment.CENTER,
                            content=ft.Icon(
                                ft.Icons.EDIT,
                                color=STAT_BLUE,
                                size=24,
                            ),
                        ),

                        ft.Column(
                            spacing=2,
                            controls=[
                                ft.Text(
                                    "Editar lote",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=TEXT_PRIMARY,
                                ),

                                ft.Text(
                                    "Actualiza la información del lote de producción",
                                    size=12,
                                    color=TEXT_SECONDARY,
                                ),
                            ],
                        ),

                        ft.Container(
                            expand=True
                        ),

                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            icon_color=TEXT_SECONDARY,
                            on_click=on_cancelar,
                        )
                    ]
                ),

                ft.Divider(
                    height=1,
                    color=DIVIDER
                ),

                campo_detalle(
                    "Operador:",
                    lote.operador
                ),

                ft.Row(
                    controls=[
                        cantidad_box,
                        producto_field,
                    ],
                    spacing=14,
                ),

                ft.Row(
                    controls=[
                        estado_dropdown,
                        turno_dropdown,
                    ],
                    spacing=14,
                ),

                ft.Row(
                    controls=[
                        hora_inicio_field,
                    ],
                ),

                ft.Container(
                    height=6
                ),

                ft.Row(
                    controls=[

                        ft.OutlinedButton(
                            "Cancelar",
                            style=ft.ButtonStyle(
                                color=STAT_ORANGE,
                                side=ft.BorderSide(
                                    1,
                                    STAT_ORANGE
                                ),
                                shape=ft.RoundedRectangleBorder(
                                    radius=8
                                ),
                            ),
                            on_click=on_cancelar,
                        ),

                        ft.Container(
                            expand=True
                        ),

                        ft.ElevatedButton(
                            height=46,
                            bgcolor=STAT_BLUE,
                            color="white",

                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(
                                    radius=10
                                ),
                                elevation=4,
                            ),

                            on_click=_guardar,

                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Icon(
                                        ft.Icons.SAVE,
                                        size=18
                                    ),
                                    ft.Text(
                                        "Guardar cambios",
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                ],
                            ),
                        ),
                    ]
                ),
            ],
        ),
    )

# ── Formulario de creación "Nuevo lote" (modal) ─────────────────────────
def campo_nuevo(label: str, hint: str, password: bool = False):

    field = ft.TextField(
        hint_text=hint,
        password=password,
        can_reveal_password=password,
        border_radius=8,
        border_color=DIVIDER,
        bgcolor=CARD_BG,
        text_size=13,
        content_padding=ft.Padding.symmetric(horizontal=12, vertical=10),
        expand=True,
    )
    layout = ft.Column(
        spacing=4,
        expand=True,
        controls=[
            ft.Text(label, size=12, color=TEXT_SECONDARY),
            field,
        ],
    )
    return field, layout

def formulario_nuevo_lote(
    operadores,
    on_guardar=None,
    on_cancelar=None,
):
    cantidad_field = ft.TextField(
        value="0",
        width=150,
        text_align=ft.TextAlign.CENTER,
        border_radius=8,
        border_color=DIVIDER,
        bgcolor=CARD_BG,
        text_size=13,
    )

    def cambiar_cantidad(valor):
        try:
            actual = float(cantidad_field.value)
        except:
            actual = 0

        actual += valor

        if actual < 0:
            actual = 0

        cantidad_field.value = str(int(actual))
        cantidad_field.update()

    cantidad_box = ft.Row(
        controls=[
            ft.IconButton(
                icon=ft.Icons.REMOVE,
                bgcolor=ft.Colors.with_opacity(0.15, STAT_ORANGE),
                icon_color=STAT_ORANGE,
                on_click=lambda e: cambiar_cantidad(-100),
            ),

            cantidad_field,

            ft.IconButton(
                icon=ft.Icons.ADD,
                bgcolor=ft.Colors.with_opacity(0.15, STAT_BLUE),
                icon_color=STAT_BLUE,
                on_click=lambda e: cambiar_cantidad(100),
            ),
        ],
        spacing=5,
    )

    operador_dropdown = ft.Dropdown(
        label="Operador",
        border_radius=8,
        border_color=DIVIDER,
        text_size=13,
        options=[
            ft.dropdown.Option(
                key=str(op["id"]),
                text=op["nombre"]
            )
            for op in operadores
        ],
    )
    producto_field = ft.TextField(
        label="Producto",
        expand=True,
        border_radius=8,
        border_color=DIVIDER,
        bgcolor=CARD_BG,
        text_size=13,
        label_style=ft.TextStyle(size=12, color=TEXT_SECONDARY),
        content_padding=ft.Padding.symmetric(horizontal=12, vertical=10),
    )

    estado_dropdown = ft.Dropdown(
        label="Estado",
        expand=True,
        border_radius=8,
        border_color=DIVIDER,
        text_size=13,
        options=[
            ft.dropdown.Option(e)
            for e in ESTADOS
        ],
    )

    turno_dropdown = ft.Dropdown(
        label="Turno",
        expand=True,
        border_radius=8,
        border_color=DIVIDER,
        text_size=13,
        options=[
            ft.dropdown.Option(t)
            for t in TURNOS
        ],
    )

    error_text = ft.Text(
        "",
        size=12,
        color=STAT_ORANGE,
        visible=False,
    )

    hora_picker = ft.TimePicker()

    hora_inicio_field = ft.TextField(
        label="Hora de inicio",
        value=datetime.now().strftime("%H:%M"),
        read_only=True,
        expand=True,
        border_radius=8,
        border_color=DIVIDER,
        prefix_icon=ft.Icons.ACCESS_TIME,
    )

    def hora_seleccionada(e):
        if hora_picker.value:
            hora_inicio_field.value = hora_picker.value.strftime("%H:%M")
            hora_inicio_field.update()

    hora_picker.on_change = hora_seleccionada

    def _guardar(e):
        if not all([
            operador_dropdown.value,
            cantidad_field.value,
            producto_field.value,
            estado_dropdown.value,
            turno_dropdown.value,
        ]):
            error_text.value = "Completa todos los campos."
            error_text.visible = True
            error_text.update()
            return

        try:
            cantidad = float(cantidad_field.value)
        except ValueError:
            error_text.value = "La cantidad debe ser numérica."
            error_text.visible = True
            error_text.update()
            return

        datos = {
            "lote_id": None,
            "empleado_id": int(operador_dropdown.value),
            "cantidad_kg": cantidad,
            "estado": estado_dropdown.value,
            "producto": producto_field.value,
            "turno": turno_dropdown.value,
            "hora_inicio": hora_inicio_field.value,
        }

        if on_guardar:
            on_guardar(datos)

    return ft.Container(
        width=560,
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
                        ft.Container(
                            width=46,
                            height=46,
                            border_radius=12,
                            bgcolor=ft.Colors.with_opacity(.12, STAT_BLUE),
                            alignment=ft.Alignment.CENTER,
                            content=ft.Icon(
                                ft.Icons.INVENTORY_2_ROUNDED,
                                color=STAT_BLUE,
                                size=24,
                            ),
                        ),
                        ft.Column(
                            spacing=2,
                            controls=[
                                ft.Text(
                                    "Nuevo lote",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=TEXT_PRIMARY,
                                ),
                                ft.Text(
                                    "Registra un nuevo lote de producción",
                                    size=12,
                                    color=TEXT_SECONDARY,
                                ),
                            ],
                        ),
                        ft.Container(expand=True),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            icon_color=TEXT_SECONDARY,
                            on_click=on_cancelar,
                        )
                    ]
                ),

                ft.Divider(height=1, color=DIVIDER),

                operador_dropdown,

                ft.Row(
                    controls=[
                        cantidad_box,
                        producto_field,
                    ],
                    spacing=14,
                ),

                ft.Row(
                    controls=[
                        estado_dropdown,
                        turno_dropdown,
                    ],
                    spacing=14,
                ),

                ft.Row(
                    controls=[
                        hora_inicio_field,
                    ],
                ),

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
                            on_click=on_cancelar,
                        ),

                        ft.Container(expand=True),

                        ft.ElevatedButton(
                            height=46,
                            bgcolor=STAT_BLUE,
                            color="white",
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                elevation=4,
                            ),
                            on_click=_guardar,
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Icon(ft.Icons.CHECK, size=18),
                                    ft.Text(
                                        "Crear lote",
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                ],
                            ),
                        ),
                    ]
                ),
            ],
        ),
    )



# ── Diálogo de baja (modal) ─────────────────────────────────────────────────
def dialogo_dar_baja(lote, on_confirmar=None, on_cancelar=None):

    def _confirmar(e):
        if on_confirmar:
            on_confirmar(lote.lote_id)


    return ft.Container(
        width=420,
        bgcolor=CARD_BG,
        border_radius=14,
        padding=24,

        shadow=ft.BoxShadow(
            blur_radius=30,
            color=ft.Colors.with_opacity(
                0.35,
                "#000000"
            ),
            offset=ft.Offset(
                0,
                10
            ),
        ),

        content=ft.Column(
            spacing=14,
            tight=True,

            controls=[


                ft.Row(
                    controls=[

                        ft.Text(
                            "Eliminar lote",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT_PRIMARY
                        ),

                        ft.Container(
                            expand=True
                        ),

                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            icon_color=TEXT_SECONDARY,
                            icon_size=18,

                            on_click=(
                                lambda e: on_cancelar(e)
                            ) if on_cancelar else None,
                        ),
                    ],
                ),


                ft.Divider(
                    height=1,
                    color=DIVIDER
                ),


                ft.Text(
                    f"¿Estás seguro de eliminar el lote LOT-{lote.lote_id:03d}?",
                    size=13,
                    color=TEXT_PRIMARY,
                ),


                ft.Text(
                    f"Producto: {lote.producto}\n"
                    f"Cantidad: {lote.cantidad_kg} kg\n"
                    f"Operador: {lote.operador}",
                    size=12,
                    color=TEXT_SECONDARY,
                ),


                ft.Row(
                    controls=[


                        ft.OutlinedButton(
                            "Cancelar",

                            style=ft.ButtonStyle(

                                color=TEXT_SECONDARY,

                                side=ft.BorderSide(
                                    1,
                                    DIVIDER
                                ),

                                shape=ft.RoundedRectangleBorder(
                                    radius=8
                                ),
                            ),

                            on_click=(
                                lambda e: on_cancelar(e)
                            ) if on_cancelar else None,
                        ),


                        ft.Container(
                            expand=True
                        ),


                        ft.ElevatedButton(

                            "Eliminar",

                            bgcolor=STAT_ORANGE,

                            color="#fff",

                            style=ft.ButtonStyle(

                                shape=ft.RoundedRectangleBorder(
                                    radius=8
                                )
                            ),

                            on_click=_confirmar,
                        ),
                    ],
                ),
            ],
        ),
    )

# ────────────────── Contenido de Lotes ──────────────────

def lotes_content(page: ft.Page, on_nuevo_lote=None, on_ver_detalle_lote=None):

        lotes = ProductionloteDAO().get_all_con_operador()

        modal_overlay_ref = ft.Ref[ft.Container]()
        modal_backdrop_ref = ft.Ref[ft.Container]()
        modal_card_ref = ft.Ref[ft.Container]()
        tabla_wrapper_ref = ft.Ref[ft.Container]()
        contador_ref = ft.Ref[ft.Text]()

        def _refrescar_lista():
            nuevos = ProductionloteDAO().get_all_con_operador()

            tabla_wrapper_ref.current.content = tabla_lotes(
                nuevos,
                manejar_click_fila
            )

            tabla_wrapper_ref.current.update()

            if contador_ref.current:
                contador_ref.current.value = f"{len(nuevos)} lotes"
                contador_ref.current.update()

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

        def ir_a_editar(lote):

            page.run_task(
                _swap_contenido,
                formulario_editar_lote(
                    lote,
                    on_guardar=guardar_edicion,
                    on_cancelar=cerrar_modal
                )
            )

        def ir_a_baja(lote):

            page.run_task(
                _swap_contenido,
                dialogo_dar_baja(
                    lote,
                    on_confirmar=confirmar_eliminar,
                    on_cancelar=cerrar_modal
                )
            )

        def guardar_edicion(datos):

            lote = Productionlote(
                lote_id=datos["lote_id"],
                empleado_id=datos["empleado_id"],
                cantidad_kg=datos["cantidad_kg"],
                estado=datos["estado"],
                producto=datos["producto"],
                turno=datos["turno"],
                hora_inicio=datos["hora_inicio"],
            )

            ProductionloteDAO().update(lote)

            _refrescar_lista()
            cerrar_modal()

        def confirmar_eliminar(lote_id):

            ProductionloteDAO().delete(lote_id)

            _refrescar_lista()
            cerrar_modal()

        def guardar_nuevo(datos):

            nuevo_lote = Productionlote(
                lote_id=None,
                empleado_id=datos["empleado_id"],
                cantidad_kg=datos["cantidad_kg"],
                estado=datos["estado"],
                producto=datos["producto"],
                turno=datos["turno"],
                hora_inicio=datos["hora_inicio"],
            )

            ProductionloteDAO().insert(nuevo_lote)

            _refrescar_lista()
            cerrar_modal()

        def abrir_detalle(lote):

            async def _abrir():
                tarjeta = detalle_lote_card(
                    lote,
                    on_cerrar=cerrar_modal,
                    on_editar=ir_a_editar,
                    on_dar_baja=ir_a_baja,
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
                operadores = EmpleadoDAO().get_operadores()

                formulario = formulario_nuevo_lote(
                    operadores=operadores,
                    on_guardar=guardar_nuevo,
                    on_cancelar=cerrar_modal
                )

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

        def manejar_click_nuevo(e):

            abrir_nuevo(e)

            if on_nuevo_lote:
                on_nuevo_lote(e)

        def manejar_click_fila(lote):

            abrir_detalle(lote)

            if on_ver_detalle_lote:
                on_ver_detalle_lote(lote)

        modal_overlay = ft.Container(
            ref=modal_overlay_ref,
            visible=False,
            expand=True,
            content=ft.Stack(
                controls=[
                    ft.Container(
                        ref=modal_backdrop_ref,
                        expand=True,
                        bgcolor=ft.Colors.with_opacity(
                            0.65,
                            "#000000"
                        ),
                        blur=10,
                        opacity=0,
                        animate_opacity=ft.Animation(
                            250,
                            ft.AnimationCurve.EASE_OUT
                        ),
                        on_click=cerrar_modal,
                    ),

                    ft.Container(
                        alignment=ft.Alignment.CENTER,
                        on_click=lambda e: None,
                        content=ft.Container(
                            ref=modal_card_ref,
                            scale=0.85,
                            opacity=0,
                            animate_scale=ft.Animation(
                                320,
                                ft.AnimationCurve.EASE_OUT_BACK
                            ),
                            animate_opacity=ft.Animation(
                                220,
                                ft.AnimationCurve.EASE_OUT
                            ),
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
                                controls=[buscador_producto(), boton_nuevo_lote(manejar_click_nuevo)],
                                spacing=12,
                            ),
                            ft.Container(height=12),
                            filtro_row(),
                            ft.Container(height=12),
                            ft.Row(
                                controls=[
                                    ft.Container(expand=True),
                                    ft.Text(f"{len(lotes)} elementos", size=12, color=TEXT_SECONDARY, ref=contador_ref),
                                ],
                            ),
                            ft.Container(height=20),
                            ft.Container(
                                ref=tabla_wrapper_ref,
                                expand=True,
                                content=tabla_lotes(lotes, manejar_click_fila),
                            ),
                            ft.Row(
                                controls=[paginacion(pagina_actual=1, total_paginas=6)],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            ft.Container(height=10),
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


def production_trituradora(page: ft.Page, on_navigate=None, on_nuevo_lote=None, on_ver_detalle=None, on_logout=None):
    active_route = "/produccion"

    return ft.View(
        route="/produccion",
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
                                content=lotes_content(page, on_nuevo_lote, on_ver_detalle),
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

def encabezado_tabla():
    return ft.Container(
        padding=15,
        bgcolor=ft.Colors.with_opacity(0.04, TEXT_PRIMARY),
        border_radius=10,
        content=ft.Row(
            controls=[

                ft.Container(
                    ft.Text(
                        "Lote",
                        weight=ft.FontWeight.BOLD,
                        color=TEXT_PRIMARY,
                    ),
                    expand=1,
                ),

                ft.Container(
                    ft.Text(
                        "Producto",
                        weight=ft.FontWeight.BOLD,
                        color=TEXT_PRIMARY,
                    ),
                    expand=3,
                ),

                ft.Container(
                    ft.Text(
                        "Cantidad (kg/t)",
                        weight=ft.FontWeight.BOLD,
                        color=TEXT_PRIMARY,
                    ),
                    expand=2,
                ),

                ft.Container(
                    ft.Text(
                        "Turno",
                        weight=ft.FontWeight.BOLD,
                        color=TEXT_PRIMARY,
                    ),
                    expand=2,
                ),

                ft.Container(
                    ft.Text(
                        "Operador",
                        weight=ft.FontWeight.BOLD,
                        color=TEXT_PRIMARY,
                    ),
                    expand=3,
                ),

                ft.Container(
                    ft.Text(
                        "Estado",
                        weight=ft.FontWeight.BOLD,
                        color=TEXT_PRIMARY,
                    ),
                    expand=2,
                ),
            ]
        ),
    )

def fila_lote(lote, on_click=None):

    return ft.Container(
        padding=15,

        border=ft.Border.only(
            bottom=ft.BorderSide(1, DIVIDER)
        ),

        ink=True,

        on_click=lambda e: on_click(lote) if on_click else None,

        content=ft.Row(
            controls=[

                ft.Container(
                    ft.Text(
                        f"LOT-{lote.lote_id:03d}",
                        color=TEXT_SECONDARY,
                    ),
                    expand=1,
                ),

                ft.Container(
                    ft.Text(
                        lote.producto,
                        color=TEXT_PRIMARY,
                    ),
                    expand=3,
                ),

                ft.Container(
                    ft.Text(
                        f"{lote.cantidad_kg} kg",
                        color=TEXT_SECONDARY,
                    ),
                    expand=2,
                ),

                ft.Container(
                    ft.Text(
                        lote.turno,
                        color=TEXT_SECONDARY,
                    ),
                    expand=2,
                ),

                ft.Container(
                    ft.Text(
                        lote.operador,
                        color=TEXT_PRIMARY,
                    ),
                    expand=3,
                ),

                ft.Container(
                    ft.Text(
                        lote.estado,
                        color=TEXT_SECONDARY,
                    ),
                    expand=2,
                ),

            ]
        ),
    )
