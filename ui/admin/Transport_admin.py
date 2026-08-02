import asyncio
from datetime import date

import flet as ft

from ui.colors import *
from dao.transporte_dao import TransportDAO
from dao.empleado_dao import EmpleadoDAO
from models.transporte import Transport
from ui.admin.dashboard_admin import sidebar, topbar

ESTADOS = [
    "Disponible",
    "En viaje",
    "Mantenimiento",
    "Fuera de servicio"
]

MARCAS = ["Ford", "Toyota", "Chevrolet", "Freightliner", "Kenworth", "International", "Volvo", "Nissan", "Isuzu"]

MODELOS = ["Camión", "Camioneta", "Tráiler", "Pickup", "Van"]

ESTADO_COLORES = {
    "Disponible": STAT_BLUE,
    "En viaje": STAT_ORANGE,
    "Mantenimiento": "#9ca3af",
    "Fuera de servicio": "#ef4444",
}


CARD_WIDTH = 280
CARD_HEIGHT = 180
CARRUSEL_ANCHO_VISIBLE = 900
CARRUSEL_ALTO = 420


# ── Helpers de estilo ────────────────────────────────────────────────────────
def badge_estado(estado: str):
    color = ESTADO_COLORES.get(estado, STAT_BLUE)
    return ft.Container(
        content=ft.Text(estado, size=11, color=color, weight=ft.FontWeight.W_600),
        padding=ft.Padding.symmetric(horizontal=10, vertical=4),
        border_radius=6,
        bgcolor=ft.Colors.with_opacity(0.12, color),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.5, color)),
    )


def buscador_transporte():
    return ft.TextField(
        hint_text="Buscar transporte por nombre, modelo, placas",
        tooltip="Busca un transporte por placas, marca o modelo",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=8,
        border_color=DIVIDER,
        bgcolor=CARD_BG,
        content_padding=ft.Padding.symmetric(horizontal=14, vertical=10),
        text_size=13,
        expand=True,
    )


def boton_nuevo_transporte(on_nuevo_transporte=None):
    return ft.ElevatedButton(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.ADD, size=16, color="#fff"),
                ft.Text("Agregar transporte", size=13, color="#fff", weight=ft.FontWeight.W_600),
            ],
            spacing=6,
            tight=True,
        ),
        tooltip="Registrar un nuevo transporte en la flotilla",
        bgcolor=STAT_BLUE,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=lambda e: on_nuevo_transporte(e) if on_nuevo_transporte else None,
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

def imagen_placeholder():
    return ft.Container(
        bgcolor="#eef1f5",
        border_radius=10,
        alignment=ft.Alignment.CENTER,
        expand=True,
        content=ft.Icon(ft.Icons.IMAGE_OUTLINED, size=56, color="#6b7280"),
    )

def imagen_camion(file_path=None, editable=False, file_picker=None):

    def seleccionar(e):
        if file_picker:
            file_picker.pick_files(
                allow_multiple=False,
                allowed_extensions=["png", "jpg", "jpeg"],
            )

    if file_path:
        return ft.Container(
            width=240,
            height=170,
            bgcolor="#eef1f5",
            border_radius=10,
            alignment=ft.alignment.center,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            content=ft.Image(
                src=file_path,
                fit=ft.ImageFit.CONTAIN,
                width=220,
                height=150,
            ),
        )

    controles = [
        ft.Container(
            expand=True,
            alignment=ft.Alignment.CENTER,
            content=ft.Icon(
                ft.Icons.LOCAL_SHIPPING,
                size=72,
                color=STAT_BLUE,
            ),
        )
    ]

    if editable:
        controles.append(
            ft.Container(
                right=10,
                bottom=10,
                content=ft.IconButton(
                    icon=ft.Icons.ADD,
                    bgcolor="#111827",
                    icon_color="white",
                    on_click=seleccionar,
                ),
            )
        )

    return ft.Container(
        width=240,
        height=170,
        bgcolor="#eef1f5",
        border_radius=10,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        content=ft.Stack(
            expand=True,
            controls=controles,
        ),
    )
def campo_transporte(label: str, value: str = "", read_only: bool = False, tooltip: str = None, expand=True):
    return ft.TextField(
        label=label,
        value=value,
        read_only=read_only,
        expand=expand,
        height=55,
        border_radius=8,
        border_color=DIVIDER,
        bgcolor=CARD_BG,
        text_size=13,
        tooltip=tooltip,
        label_style=ft.TextStyle(size=11, color=TEXT_SECONDARY),
        content_padding=ft.Padding.symmetric(horizontal=12, vertical=8),
    )


def dropdown_transporte(label: str, opciones: list, valor=None, tooltip: str = None, expand=True):
    return ft.Dropdown(
        label=label,
        value=valor,
        expand=expand,
        border_radius=8,
        border_color=DIVIDER,
        text_size=13,
        tooltip=tooltip,
        label_style=ft.TextStyle(size=11, color=TEXT_SECONDARY),
        options=[ft.dropdown.Option(o) for o in opciones],
    )


def dropdown_chofer(valor_id=None):
    choferes = [emp for emp in EmpleadoDAO().get_all() if emp.id_rol == 2]
    return ft.Dropdown(
        label="Chofer asignado",
        value=str(valor_id) if valor_id else None,
        expand=True,
        border_radius=8,
        border_color=DIVIDER,
        text_size=13,
        tooltip="Chofer responsable de este transporte",
        label_style=ft.TextStyle(size=11, color=TEXT_SECONDARY),
        options=[ft.dropdown.Option(key=str(emp.empleado_id), text=f"{emp.name} {emp.aPaterno}") for emp in choferes],
    )


# ── Tarjeta del carrusel ─────────────────────────────────────────────────────
def tarjeta_transporte(t: Transport, es_centro: bool, on_ver_detalle=None, on_editar=None):
    acciones = (
        ft.Row(
            controls=[
                ft.OutlinedButton(
                    "Editar info",
                    tooltip="Editar los datos de este transporte",
                    style=ft.ButtonStyle(
                        color=STAT_ORANGE,
                        side=ft.BorderSide(1, STAT_ORANGE),
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                    on_click=(lambda e: on_editar(t)) if on_editar else None,
                ),
                ft.ElevatedButton(
                    "Ver detalles",
                    tooltip="Ver más detalles del transporte",
                    bgcolor=STAT_BLUE,
                    color="#fff",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                    on_click=(lambda e: on_ver_detalle(t)) if on_ver_detalle else None,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        if es_centro
        else ft.Container(height=0)
    )

    return ft.Container(
        width=CARD_WIDTH,
        height=CARD_HEIGHT,
        bgcolor=CARD_BG,
        border_radius=14,
        padding=14,
        ink=not es_centro,
        tooltip="Ver más detalles",
        on_click=(lambda e: on_ver_detalle(t))
        if on_ver_detalle
        else None,
        shadow=ft.BoxShadow(
            blur_radius=35 if es_centro else 15,
            spread_radius=2 if es_centro else 0,
            color=ft.Colors.with_opacity(
                0.28 if es_centro else 0.10,
                "#000000"
            ),
            offset=ft.Offset(
                0,
                12 if es_centro else 5
            ),
        ),
        content=ft.Row(
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=90,
                    height=90,
                    bgcolor="#eef1f5",
                    border_radius=12,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(
                        ft.Icons.LOCAL_SHIPPING,
                        size=45,
                        color=STAT_BLUE
                    ),
                ),

                ft.Column(
                    spacing=4,
                    expand=True,
                    controls=[
                        ft.Text(
                            t.placas,
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT_PRIMARY,
                        ),

                        ft.Text(
                            f"{t.marca} {t.modelo}",
                            size=12,
                            color=TEXT_SECONDARY,
                        ),

                        badge_estado(t.estado)
                    ],
                )
            ]
        )
    )


# ── Carrusel estilo "dock de macOS" ──────────────────────────────────────────
def carrusel_transportes(page: ft.Page, on_ver_detalle=None, on_editar=None):

    estado = {"transportes": TransportDAO().get_all(), "indice": 0}

    stack_ref = ft.Ref[ft.Stack]()
    paginador_ref = ft.Ref[ft.Container]()

    paso = CARD_WIDTH * 0.72

    def _construir_tarjetas():
        transportes = estado["transportes"]
        indice = estado["indice"]
        centro_x = (CARRUSEL_ANCHO_VISIBLE - CARD_WIDTH) / 2

        tarjetas = []
        for i, t in enumerate(transportes):
            distancia = i - indice
            if abs(distancia) > 2:
                continue

            es_centro = distancia == 0
            escala = {
                0: 1.22,
                1: 0.93,
                2: 0.74
            }.get(abs(distancia), 0.60)
            opacidad = {
                0: 1,
                1: 0.78,
                2: 0.32
            }.get(abs(distancia), 0)
            ajuste_escala = (CARD_WIDTH * (1 - escala)) / 2
            izquierda = centro_x + distancia * paso + ajuste_escala
            desplazamiento_y = {
                0: 0,
                1: 18,
                2: 35
            }.get(abs(distancia), 45)

            arriba = (
                    (CARD_HEIGHT - CARD_HEIGHT * escala) / 2
                    + desplazamiento_y
                    + 50
            )
            rotacion = {
                -2: -0.18,
                -1: -0.08,
                0: 0,
                1: 0.08,
                2: 0.18
            }.get(distancia, 0)
            tarjeta = ft.Container(
                left=izquierda,
                top=arriba,
                width=CARD_WIDTH,
                scale=escala,
                rotate=rotacion,
                opacity=opacidad,
                animate_position=ft.Animation(
                    650,
                    ft.AnimationCurve.EASE_IN_OUT_CUBIC
                ),
                animate_scale=ft.Animation(
                    650,
                    ft.AnimationCurve.FAST_OUT_SLOWIN
                ),
                animate_opacity=ft.Animation(
                    500,
                    ft.AnimationCurve.EASE_OUT
                ),
                content=tarjeta_transporte(t, es_centro, on_ver_detalle, on_editar),
            )
            tarjetas.append((abs(distancia), tarjeta))

        # La tarjeta central se dibuja al final para quedar por encima del resto.
        tarjetas.sort(key=lambda par: -par[0])
        return [tarjeta for _, tarjeta in tarjetas]

    def _construir_paginador():
        total = len(estado["transportes"])
        controles = []
        for n in range(1, total + 1):
            activo = n == estado["indice"] + 1
            controles.append(
                ft.Container(
                    content=ft.Text(
                        str(n),
                        size=13,
                        color=STAT_ORANGE if activo else TEXT_SECONDARY,
                        weight=ft.FontWeight.BOLD if activo else ft.FontWeight.NORMAL,
                    ),
                    padding=ft.Padding.symmetric(horizontal=6, vertical=2),
                    border=ft.Border(bottom=ft.BorderSide(2, STAT_ORANGE)) if activo else None,
                    tooltip=f"Ir al transporte {n}",
                    on_click=(lambda e, n=n: ir_a(n - 1)),
                )
            )
        return ft.Row(controls=controles, alignment=ft.MainAxisAlignment.CENTER, spacing=4)

    def _redibujar():
        stack_ref.current.controls.clear()
        stack_ref.current.controls = _construir_tarjetas()
        stack_ref.current.update()
        paginador_ref.current.content = _construir_paginador()
        paginador_ref.current.update()

    def ir_a(indice: int):
        total = len(estado["transportes"])
        if total == 0:
            return
        estado["indice"] = max(0, min(total - 1, indice))
        _redibujar()

    def anterior(e=None):
        ir_a(estado["indice"] - 1)

    def siguiente(e=None):
        ir_a(estado["indice"] + 1)

    def refrescar_datos():
        estado["transportes"] = TransportDAO().get_all()
        estado["indice"] = min(estado["indice"], max(0, len(estado["transportes"]) - 1))
        _redibujar()

    contenido = ft.Column(
        spacing=16,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.IconButton(
                        ft.Icons.CHEVRON_LEFT,
                        icon_color=STAT_BLUE,
                        icon_size=28,
                        tooltip="Transporte anterior",
                        on_click=anterior,
                    ),
                    ft.Container(
                        width=CARRUSEL_ANCHO_VISIBLE,
                        height=CARRUSEL_ALTO,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Stack(
                            ref=stack_ref,
                            controls=_construir_tarjetas(),
                        ),
                    ),
                    ft.IconButton(
                        ft.Icons.CHEVRON_RIGHT,
                        icon_color=STAT_BLUE,
                        icon_size=28,
                        tooltip="Siguiente transporte",
                        on_click=siguiente,
                    ),
                ],
            ),
            ft.Container(ref=paginador_ref, content=_construir_paginador(), alignment=ft.Alignment.CENTER),
        ],
    )

    return contenido, refrescar_datos, ir_a
# ── Tarjeta de detalle (modal) ───────────────────────────────────────────────
def detalle_transporte_card(t: Transport, on_cerrar=None, on_dar_baja=None, on_guardar=None):

    placas_field = campo_transporte(
        "Placas",
        t.placas,
        read_only=False,
    )

    modelo_field = campo_transporte(
        "Modelo",
        t.modelo,
        read_only=False,
    )

    marca_field = campo_transporte(
        "Marca",
        t.marca,
        read_only=False,
    )

    capacidad_field = campo_transporte(
        "Capacidad",
        str(t.capacidad_carga),
        read_only=False,
    )

    def guardar(e):
        datos = {
            "placas": placas_field.value,
            "modelo": modelo_field.value,
            "marca": marca_field.value,
            "capacidad_carga": capacidad_field.value,
            "estado": t.estado,
            "id_empleado": t.id_empleado,
        }

        if on_guardar:
            on_guardar(datos)

    return ft.Container(
        width=700,
        bgcolor=CARD_BG,
        border_radius=16,
        padding=24,
        shadow=ft.BoxShadow(
            blur_radius=35,
            color=ft.Colors.with_opacity(0.35, "#000000"),
            offset=ft.Offset(0, 10),
        ),
        content=ft.Column(
            tight=True,
            spacing=18,
            controls=[

                # ---------- Encabezado ----------
                ft.Row(
                    controls=[
                        ft.Text(
                            "Detalles del transporte",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT_PRIMARY,
                        ),
                        ft.Container(expand=True),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            icon_color=TEXT_SECONDARY,
                            tooltip="Cerrar",
                            on_click=(lambda e: on_cerrar(e))
                            if on_cerrar else None,
                        ),
                    ]
                ),

                ft.Divider(color=DIVIDER),

                # ---------- Contenido ----------
                ft.Row(
                    spacing=35,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[

                        ft.Column(
                            expand=True,
                            spacing=14,
                            controls=[
                                placas_field,
                                modelo_field,
                                marca_field,
                                capacidad_field,
                            ],
                        ),
                        ft.Container(
                            width=250,
                            content=ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=15,
                                controls=[

                                    imagen_camion(file_path=t.imagen),

                                    campo_transporte(
                                        "No. Serie",
                                        f"TR-{t.transporte_id:04d}"
                                        if t.transporte_id
                                        else "—",
                                        read_only=True,
                                        expand=False,
                                    ),

                                    badge_estado(t.estado),
                                ],
                            ),
                        ),
                    ],
                ),

                ft.Divider(color=DIVIDER),

                # ---------- Botones ----------
                ft.Row(
                    controls=[

                        ft.OutlinedButton(
                            "Cerrar",
                            style=ft.ButtonStyle(
                                color=TEXT_SECONDARY,
                                side=ft.BorderSide(1, DIVIDER),
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                            on_click=(lambda e: on_cerrar(e))
                            if on_cerrar else None,
                        ),

                        ft.Container(expand=True),

                        ft.ElevatedButton(
                            content=ft.Row(
                                tight=True,
                                spacing=8,
                                controls=[
                                    ft.Icon(
                                        ft.Icons.SAVE_OUTLINED,
                                        color="white",
                                        size=18,
                                    ),
                                    ft.Text(
                                        "Guardar cambios",
                                        color="white",
                                        weight=ft.FontWeight.W_600,
                                    ),
                                ],
                            ),
                            bgcolor=STAT_BLUE,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                            on_click=guardar,
                        ),

                        ft.ElevatedButton(
                            bgcolor=STAT_ORANGE,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                            on_click=(lambda e: on_dar_baja(t))
                            if on_dar_baja else None,
                            content=ft.Row(
                                tight=True,
                                spacing=8,
                                controls=[
                                    ft.Icon(
                                        ft.Icons.DELETE_OUTLINE,
                                        color="white",
                                        size=18,
                                    ),
                                    ft.Text(
                                        "Dar de baja",
                                        color="white",
                                        weight=ft.FontWeight.W_600,
                                    ),
                                ],
                            ),
                        ),
                    ]
                ),
            ],
        ),
    )

# ── Formulario de edición (modal) ───────────────────────────────────────────
def formulario_editar_transporte(t: Transport, on_guardar=None, on_cancelar=None):
    placas_field = campo_transporte("Placas", t.placas)
    modelo_dd = dropdown_transporte("Modelo", MODELOS, valor=t.modelo)
    marca_dd = dropdown_transporte("Marca", MARCAS, valor=t.marca)
    capacidad_field = campo_transporte("Capacidad", str(t.capacidad_carga))
    estado_dd = dropdown_transporte("Estado", ESTADOS, valor=t.estado)
    chofer_dd = dropdown_chofer(valor_id=t.id_empleado)

    error_text = ft.Text("", size=12, color=STAT_ORANGE, visible=False)

    def _guardar(e):
        datos = {
            "placas": placas_field.value,
            "modelo": modelo_dd.value,
            "marca": marca_dd.value,
            "capacidad_carga": capacidad_field.value,
            "estado": estado_dd.value,
            "id_empleado": int(chofer_dd.value) if chofer_dd.value else None,
            #"imagen": imagen_path,
        }
        if on_guardar:
            on_guardar(datos)

    return ft.Container(
        width=620,
        bgcolor=CARD_BG,
        border_radius=14,
        padding=24,
        shadow=ft.BoxShadow(blur_radius=30, color=ft.Colors.with_opacity(0.35, "#000000"), offset=ft.Offset(0, 10)),
        content=ft.Column(
            spacing=14,
            tight=True,
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Editar transporte", size=16, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                        ft.Container(expand=True),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            icon_color=TEXT_SECONDARY,
                            icon_size=18,
                            tooltip="Cancelar edición",
                            on_click=(lambda e: on_cancelar(e)) if on_cancelar else None,
                        ),
                    ],
                ),
                ft.Divider(height=1, color=DIVIDER),
                ft.Row(
                    spacing=20,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Column(expand=True, spacing=10,
                                  controls=[placas_field, modelo_dd, marca_dd, capacidad_field]),
                        ft.Column(
                            spacing=10,
                            width=760,
                            controls=[
                                imagen_camion(),
                                campo_transporte(
                                    "No.Serie",
                                    f"TR-{t.transporte_id:04d}" if t.transporte_id else "—",
                                    read_only=True,
                                    tooltip="El ID no se puede modificar",
                                ),
                            ],
                        ),
                    ],
                ),
                ft.Row(controls=[estado_dd, chofer_dd], spacing=14),
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
                                    ft.Icon(ft.Icons.SAVE_OUTLINED, size=16, color="#fff"),
                                    ft.Text("Guardar cambios", size=13, color="#fff", weight=ft.FontWeight.W_600),
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

# ── Formulario "Agregar Transporte" (modal) ─────────────────────────────────
def formulario_nuevo_transporte(on_guardar=None, on_cancelar=None, file_picker=None):

    imagen_path = None

    placas_field = campo_transporte("Placas", tooltip="Ej. ABC-1234")
    modelo_dd = dropdown_transporte("Modelo", MODELOS, tooltip="Tipo de vehículo")
    marca_dd = dropdown_transporte("Marca", MARCAS, tooltip="Fabricante del vehículo")
    capacidad_field = campo_transporte("Capacidad", tooltip="Ej. 16,000 kg")
    estado_dd = dropdown_transporte("Estado", ESTADOS, valor=ESTADOS[0])
    chofer_dd = dropdown_chofer()

    error_text = ft.Text(
        "",
        size=12,
        color=STAT_ORANGE,
        visible=False,
    )

    def _guardar(e):

        obligatorios = [
            placas_field.value,
            modelo_dd.value,
            marca_dd.value,
            capacidad_field.value,
        ]

        if not all(obligatorios):
            error_text.value = "Completa todos los campos obligatorios."
            error_text.visible = True
            error_text.update()
            return

        datos = {
            "placas": placas_field.value,
            "modelo": modelo_dd.value,
            "marca": marca_dd.value,
            "capacidad_carga": capacidad_field.value,
            "estado": estado_dd.value,
            "id_empleado": int(chofer_dd.value) if chofer_dd.value else None,
            "imagen": imagen_path,      # ← aunque sea None
        }

        if on_guardar:
            on_guardar(datos)

    return ft.Container(
        width=700,
        bgcolor=CARD_BG,
        border_radius=16,
        padding=24,
        shadow=ft.BoxShadow(
            blur_radius=30,
            color=ft.Colors.with_opacity(0.35, "#000000"),
            offset=ft.Offset(0, 10),
        ),
        content=ft.Column(
            spacing=18,
            tight=True,
            controls=[

                # Encabezado
                ft.Row(
                    controls=[
                        ft.Text(
                            "Agregar Transporte",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT_PRIMARY,
                        ),
                        ft.Container(expand=True),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            icon_color=TEXT_SECONDARY,
                            on_click=(lambda e: on_cancelar(e))
                            if on_cancelar else None,
                        ),
                    ]
                ),

                ft.Divider(color=DIVIDER),

                # Contenido
                ft.Row(
                    spacing=30,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[

                        ft.Column(
                            expand=True,
                            spacing=12,
                            controls=[
                                placas_field,
                                modelo_dd,
                                marca_dd,
                                capacidad_field,
                            ],
                        ),

                        ft.Container(
                            width=250,
                            content=ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=15,
                                controls=[

                                    imagen_camion(
                                        editable=True,
                                        file_picker=file_picker,
                                    ),

                                    campo_transporte(
                                        "No. Serie",
                                        "Se asigna automáticamente",
                                        read_only=True,
                                        expand=False,
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),

                ft.Row(
                    spacing=14,
                    controls=[
                        estado_dd,
                        chofer_dd,
                    ],
                ),

                error_text,

                ft.Divider(color=DIVIDER),

                ft.Row(
                    controls=[

                        ft.OutlinedButton(
                            "Cancelar",
                            style=ft.ButtonStyle(
                                color=STAT_ORANGE,
                                side=ft.BorderSide(1, STAT_ORANGE),
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                            on_click=(lambda e: on_cancelar(e))
                            if on_cancelar else None,
                        ),

                        ft.Container(expand=True),

                        ft.ElevatedButton(
                            bgcolor=STAT_BLUE,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                            on_click=_guardar,
                            content=ft.Row(
                                tight=True,
                                spacing=6,
                                controls=[
                                    ft.Icon(
                                        ft.Icons.ADD,
                                        color="white",
                                        size=18,
                                    ),
                                    ft.Text(
                                        "Agregar transporte",
                                        color="white",
                                        weight=ft.FontWeight.W_600,
                                    ),
                                ],
                            ),
                        ),
                    ]
                ),
            ],
        ),
    )

# ── Diálogo "Dar de baja" (eliminar) (modal) ────────────────────────────────
def dialogo_dar_baja_transporte(t: Transport, on_confirmar=None, on_cancelar=None):
    motivo_field = ft.TextField(
        label="Motivo de baja",
        tooltip="Explica por qué se da de baja este transporte",
        multiline=True,
        min_lines=3,
        max_lines=4,
        border_radius=8,
        border_color=DIVIDER,
        bgcolor=CARD_BG,
        text_size=13,
        label_style=ft.TextStyle(size=12, color=TEXT_SECONDARY),
    )

    def _confirmar(e):
        if on_confirmar:
            on_confirmar(t, motivo_field.value)

    return ft.Container(
        width=420,
        bgcolor=CARD_BG,
        border_radius=14,
        padding=24,
        shadow=ft.BoxShadow(blur_radius=30, color=ft.Colors.with_opacity(0.35, "#000000"), offset=ft.Offset(0, 10)),
        content=ft.Column(
            spacing=14,
            tight=True,
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Eliminar transporte", size=16, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                        ft.Container(expand=True),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            icon_color=TEXT_SECONDARY,
                            icon_size=18,
                            tooltip="Cancelar",
                            on_click=(lambda e: on_cancelar(e)) if on_cancelar else None,
                        ),
                    ],
                ),
                ft.Divider(height=1, color=DIVIDER),
                ft.Text(
                    "¿Deseas dar de baja este transporte? Una vez realizada, esta acción no podrá revertirse.",
                    size=12,
                    color=TEXT_SECONDARY,
                ),
                motivo_field,
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
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.DELETE_OUTLINE, size=16, color="#fff"),
                                    ft.Text("Dar de baja", size=13, color="#fff", weight=ft.FontWeight.W_600),
                                ],
                                spacing=6,
                                tight=True,
                            ),
                            tooltip="Esta acción no se puede deshacer",
                            bgcolor="#ef4444",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                            on_click=_confirmar,
                        ),
                    ],
                ),
            ],
        ),
    )


# ── Contenido de Transporte (área central + modal animado) ─────────────────
def transportes_content(page: ft.Page, on_nuevo_transporte=None, on_ver_detalle=None):
    modal_overlay_ref = ft.Ref[ft.Container]()
    modal_backdrop_ref = ft.Ref[ft.Container]()
    modal_card_ref = ft.Ref[ft.Container]()

    page.overlay.clear()

    #file_picker = ft.FilePicker()

    #page.overlay.append(file_picker)

    contenido_carrusel, refrescar_datos, ir_a = carrusel_transportes(
        page,
        on_ver_detalle=lambda t: manejar_ver_detalle(t),
        on_editar=lambda t: ir_a_editar(t),
    )

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

    def _abrir_con(control):
        async def _abrir():
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

        page.run_task(_abrir)

    def ir_a_editar(t: Transport):
        _abrir_con(
            formulario_editar_transporte(
                t,
                on_guardar=lambda datos: guardar_edicion(t, datos),
                on_cancelar=cerrar_modal
            )
        )

    def ir_a_baja(t: Transport):
        page.run_task(
            _swap_contenido,
            dialogo_dar_baja_transporte(t, on_confirmar=confirmar_baja, on_cancelar=cerrar_modal),
        )

    def guardar_edicion(t: Transport, datos):
        # ⚠️ Se reutiliza el objeto `t` ya cargado en memoria porque
        # TransportDAO no expone get_by_id().
        t.placas = datos["placas"]
        t.modelo = datos["modelo"]
        t.marca = datos["marca"]
        t.capacidad_carga = int(datos["capacidad_carga"])
        t.estado = datos["estado"]
        t.id_empleado = datos["id_empleado"]
        TransportDAO().update(t)
        refrescar_datos()
        cerrar_modal()

    def confirmar_baja(t: Transport, motivo: str):
        # ⚠️ TransportDAO.delete() borra el registro físicamente; el motivo
        # no se persiste porque no hay un método de baja lógica en el DAO.
        TransportDAO().delete(t.transporte_id)
        refrescar_datos()
        cerrar_modal()

    def guardar_nuevo(datos):
        nuevo = Transport(
            transporte_id=None,
            placas=datos["placas"],
            marca=datos["marca"],
            modelo=datos["modelo"],
            capacidad_carga=datos["capacidad_carga"],
            estado=datos["estado"],
            activo=True,
            fecra_registro=date.today(),
            fecha_baja=None,
            motivo_baja=None,
            id_empleado=datos["id_empleado"],
            imagen = datos["imagen"]
        )
        TransportDAO().insert(nuevo)
        refrescar_datos()
        cerrar_modal()

    def manejar_ver_detalle(t: Transport):
        _abrir_con(
            detalle_transporte_card(
                t,
                on_cerrar=cerrar_modal,
                on_dar_baja=ir_a_baja,
                on_guardar=lambda datos: guardar_edicion(t, datos)
            )
        )
        if on_ver_detalle:
            on_ver_detalle(t)

    def abrir_nuevo(e=None):
        _abrir_con(
            formulario_nuevo_transporte(
                on_guardar=guardar_nuevo,
                on_cancelar=cerrar_modal,
                #file_picker=file_picker
            )
        )

    def manejar_click_nuevo(e):
        abrir_nuevo(e)
        if on_nuevo_transporte:
            on_nuevo_transporte(e)

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
                        animate_scale=ft.Animation(320, ft.AnimationCurve.FAST_OUT_SLOWIN),
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
                            controls=[buscador_transporte(), boton_nuevo_transporte(manejar_click_nuevo)],
                            spacing=12,
                        ),
                        ft.Container(height=30),
                        ft.Container(content=contenido_carrusel, expand=True, alignment=ft.Alignment.CENTER),
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


def transportes_admin(page: ft.Page, on_navigate=None, on_nuevo_transporte=None, on_ver_detalle=None):
    active_route = "/transporte"

    return ft.View(
        route="/transporte",
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
                                content=transportes_content(page, on_nuevo_transporte, on_ver_detalle),
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

