import asyncio
import flet as ft

from ui.colors import *
from ui.vulcanizadora.dashboard_vulcanizadora import sidebar
from dao.inventario_dao import InventarioDAO
from models.inventario_neumatico import (
    InventarioNeumaticoNuevo,
    ESTADOS_VALIDOS,
)


dao = InventarioDAO()


ESTADO_LABELS = {
    "bueno": "Bueno",
    "usado": "Usado",
    "para_desecho": "Para desecho",
}

ESTADO_COLORS = {
    "bueno": STAT_TEAL,
    "usado": STAT_ORANGE,
    "para_desecho": STAT_RED,
}

def _topbar_inventario(page: ft.Page):
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
                    "Inventario de neumáticos",
                    size=20,
                    color="#fff",
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Container(expand=True),

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


def _stat_card(titulo: str, valor: str, color: str):
    return ft.Container(
        bgcolor=CARD_BG,
        border_radius=12,
        padding=16,
        expand=True,
        content=ft.Column(
            controls=[
                ft.Text(
                    titulo,
                    size=12,
                    color=TEXT_SECONDARY,
                ),

                ft.Text(
                    str(valor),
                    size=24,
                    color=color,
                    weight=ft.FontWeight.BOLD,
                ),
            ],
            spacing=4,
        ),
    )


def badge_estado(estado: str):
    color = ESTADO_COLORS.get(
        estado,
        STAT_BLUE,
    )

    return ft.Container(
        content=ft.Text(
            ESTADO_LABELS.get(
                estado,
                estado,
            ),
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

def campo_inventario(
    label: str,
    value: str = "",
    tooltip: str = None,
    expand=True,
):
    return ft.TextField(
        label=label,
        value=value,
        expand=expand,
        height=55,
        border_radius=8,
        border_color=DIVIDER,
        bgcolor=CARD_BG,
        text_size=13,
        tooltip=tooltip,
        label_style=ft.TextStyle(
            size=11,
            color=TEXT_SECONDARY,
        ),
        content_padding=ft.Padding.symmetric(
            horizontal=12,
            vertical=8,
        ),
    )

def cambiar_hover(e):
    e.control.bgcolor = (
        ft.Colors.with_opacity(
            0.04,
            STAT_BLUE,
        )
        if e.data == "true"
        else CARD_BG
    )

    e.control.update()


def fila_inventario(
    item,
    on_ver_detalle=None,
    on_eliminar=None,
):
    return ft.Container(
        padding=15,
        bgcolor=CARD_BG,
        border=ft.Border.only(
            bottom=ft.BorderSide(
                1,
                DIVIDER,
            )
        ),
        ink=True,
        tooltip="Click para ver más detalles",
        on_hover=cambiar_hover,
        on_click=(
            lambda e: on_ver_detalle(item)
            if on_ver_detalle
            else None
        ),

        content=ft.Row(
            controls=[

                ft.Container(
                    content=ft.Text(
                        item.tipo_neumatico,
                        color=TEXT_PRIMARY,
                        size=13,
                    ),
                    expand=2,
                ),

                ft.Container(
                    content=ft.Text(
                        item.medida,
                        color=TEXT_PRIMARY,
                        size=13,
                    ),
                    expand=2,
                ),

                ft.Container(
                    content=ft.Text(
                        item.marca,
                        color=TEXT_PRIMARY,
                        size=13,
                    ),
                    expand=2,
                ),

                ft.Container(
                    content=ft.Text(
                        str(item.cantidad),
                        color=TEXT_PRIMARY,
                        size=13,
                    ),
                    expand=1,
                ),

                ft.Container(
                    content=badge_estado(
                        item.estado
                    ),
                    expand=2,
                ),

                ft.Container(
                    content=ft.Text(
                        str(item.fecha_ingreso),
                        color=TEXT_SECONDARY,
                        size=12,
                    ),
                    expand=2,
                ),

                ft.Container(
                    width=45,
                    content=ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_color="#f87171",
                        icon_size=18,
                        tooltip="Eliminar neumático",
                        on_click=(
                            lambda e, iid=item.inventario_id:
                            on_eliminar(iid)
                            if on_eliminar
                            else None
                        ),
                    ),
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )


def encabezado_inventario():
    return ft.Container(
        padding=15,
        bgcolor=ft.Colors.with_opacity(
            0.04,
            TEXT_PRIMARY,
        ),
        border_radius=10,

        content=ft.Row(
            controls=[

                ft.Container(
                    ft.Text(
                        "Tipo",
                        weight=ft.FontWeight.BOLD,
                        color=TEXT_PRIMARY,
                        size=12,
                    ),
                    expand=2,
                ),

                ft.Container(
                    ft.Text(
                        "Medida",
                        weight=ft.FontWeight.BOLD,
                        color=TEXT_PRIMARY,
                        size=12,
                    ),
                    expand=2,
                ),

                ft.Container(
                    ft.Text(
                        "Marca",
                        weight=ft.FontWeight.BOLD,
                        color=TEXT_PRIMARY,
                        size=12,
                    ),
                    expand=2,
                ),

                ft.Container(
                    ft.Text(
                        "Cantidad",
                        weight=ft.FontWeight.BOLD,
                        color=TEXT_PRIMARY,
                        size=12,
                    ),
                    expand=1,
                ),

                ft.Container(
                    ft.Text(
                        "Estado",
                        weight=ft.FontWeight.BOLD,
                        color=TEXT_PRIMARY,
                        size=12,
                    ),
                    expand=2,
                ),

                ft.Container(
                    ft.Text(
                        "Ingreso",
                        weight=ft.FontWeight.BOLD,
                        color=TEXT_PRIMARY,
                        size=12,
                    ),
                    expand=2,
                ),

                ft.Container(
                    width=45,
                ),
            ]
        ),
    )

def formulario_nuevo_inventario(
    on_guardar=None,
    on_cancelar=None,
    on_error=None,
):

    tipo_field = campo_inventario(
        "Tipo",
        tooltip="Ej. Auto, camioneta, camión",
    )

    medida_field = campo_inventario(
        "Medida",
        tooltip="Ej. 195/65 R15",
    )

    marca_field = campo_inventario(
        "Marca",
        tooltip="Ej. Michelin",
    )

    cantidad_field = campo_inventario(
        "Cantidad",
        tooltip="Cantidad de neumáticos",
    )

    estado_field = ft.Dropdown(
        label="Estado",
        expand=True,
        border_radius=8,
        border_color=DIVIDER,
        text_size=13,
        tooltip="Selecciona el estado del neumático",
        label_style=ft.TextStyle(
            size=11,
            color=TEXT_SECONDARY,
        ),
        options=[
            ft.dropdown.Option(
                key=e,
                text=ESTADO_LABELS[e],
            )
            for e in ESTADOS_VALIDOS
        ],
        value="bueno",
    )

    observaciones_field = ft.TextField(
        label="Observaciones",
        multiline=True,
        min_lines=3,
        max_lines=4,
        border_radius=8,
        border_color=DIVIDER,
        bgcolor=CARD_BG,
        text_size=13,
        tooltip="Observaciones adicionales",
        label_style=ft.TextStyle(
            size=11,
            color=TEXT_SECONDARY,
        ),
        content_padding=ft.Padding.symmetric(
            horizontal=12,
            vertical=8,
        ),
    )

    def guardar(e):

        if not tipo_field.value:
            if on_error:
                on_error(
                    "El tipo de neumático es obligatorio."
                )
            return

        if not medida_field.value:
            if on_error:
                on_error(
                    "La medida es obligatoria."
                )
            return

        if not marca_field.value:
            if on_error:
                on_error(
                    "La marca es obligatoria."
                )
            return

        try:
            cantidad = int(
                cantidad_field.value
                or 0
            )

            if cantidad < 0:
                raise ValueError

        except (TypeError, ValueError):

            cantidad_field.error_text = (
                "Ingresa una cantidad válida."
            )

            cantidad_field.update()

            if on_error:
                on_error(
                    "La cantidad debe ser un número entero válido."
                )

            return

        cantidad_field.error_text = None

        datos = InventarioNeumaticoNuevo(
            vulcanizadora_id=None,
            tipo_neumatico=(
                tipo_field.value.strip()
            ),
            medida=(
                medida_field.value.strip()
            ),
            marca=(
                marca_field.value.strip()
            ),
            cantidad=cantidad,
            estado=estado_field.value,
            observaciones=(
                observaciones_field.value.strip()
                or None
            ),
        )

        if on_guardar:
            on_guardar(datos)

    return ft.Container(
        width=560,
        bgcolor=CARD_BG,
        border_radius=14,
        padding=24,

        shadow=ft.BoxShadow(
            blur_radius=30,
            color=ft.Colors.with_opacity(
                0.35,
                "#000000",
            ),
            offset=ft.Offset(
                0,
                10,
            ),
        ),

        content=ft.Column(
            spacing=14,
            tight=True,

            controls=[

                ft.Row(
                    controls=[
                        ft.Text(
                            "Nuevo inventario",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT_PRIMARY,
                        ),

                        ft.Container(
                            expand=True
                        ),

                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            icon_color=TEXT_SECONDARY,
                            icon_size=18,
                            tooltip="Cerrar",
                            on_click=(
                                lambda e:
                                on_cancelar(e)
                                if on_cancelar
                                else None
                            ),
                        ),
                    ],
                ),

                ft.Divider(
                    height=1,
                    color=DIVIDER,
                ),

                ft.Row(
                    controls=[
                        tipo_field,
                        medida_field,
                    ],
                    spacing=14,
                ),

                ft.Row(
                    controls=[
                        marca_field,
                        cantidad_field,
                    ],
                    spacing=14,
                ),

                ft.Row(
                    controls=[
                        estado_field,
                    ],
                ),

                observaciones_field,

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
                                    STAT_ORANGE,
                                ),
                                shape=ft.RoundedRectangleBorder(
                                    radius=8
                                ),
                            ),
                            on_click=(
                                lambda e:
                                on_cancelar(e)
                                if on_cancelar
                                else None
                            ),
                        ),

                        ft.Container(
                            expand=True
                        ),

                        ft.ElevatedButton(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(
                                        ft.Icons.ADD,
                                        size=16,
                                        color="#fff",
                                    ),
                                    ft.Text(
                                        "Agregar inventario",
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
                                shape=ft.RoundedRectangleBorder(
                                    radius=8
                                )
                            ),
                            on_click=guardar,
                        ),
                    ],
                ),
            ],
        ),
    )


def detalle_inventario(
    item,
    on_cerrar=None,
):

    return ft.Container(
        width=460,
        bgcolor=CARD_BG,
        border_radius=14,
        padding=24,

        shadow=ft.BoxShadow(
            blur_radius=30,
            color=ft.Colors.with_opacity(
                0.35,
                "#000000",
            ),
            offset=ft.Offset(
                0,
                10,
            ),
        ),

        content=ft.Column(
            spacing=10,
            tight=True,

            controls=[

                ft.Row(
                    controls=[

                        ft.Text(
                            "Detalles del neumático",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT_PRIMARY,
                        ),

                        ft.Container(
                            expand=True
                        ),

                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            icon_color=TEXT_SECONDARY,
                            icon_size=18,
                            tooltip="Cerrar",
                            on_click=(
                                lambda e:
                                on_cerrar(e)
                                if on_cerrar
                                else None
                            ),
                        ),
                    ],
                ),

                ft.Divider(
                    height=1,
                    color=DIVIDER,
                ),

                ft.Container(
                    height=10
                ),

                ft.Row(
                    controls=[

                        ft.CircleAvatar(
                            content=ft.Icon(
                                ft.Icons.TIRE_REPAIR,
                                color=TEXT_SECONDARY,
                                size=30,
                            ),
                            bgcolor=ft.Colors.with_opacity(
                                0.08,
                                TEXT_PRIMARY,
                            ),
                            radius=36,
                        ),

                        ft.Container(
                            width=16
                        ),

                        ft.Column(
                            spacing=4,
                            controls=[

                                ft.Text(
                                    item.marca,
                                    size=17,
                                    weight=ft.FontWeight.BOLD,
                                    color=TEXT_PRIMARY,
                                ),

                                ft.Text(
                                    item.medida,
                                    size=12,
                                    color=TEXT_SECONDARY,
                                ),

                                ft.Text(
                                    item.tipo_neumatico,
                                    size=12,
                                    color=TEXT_SECONDARY,
                                ),
                            ],
                        ),
                    ],
                ),

                ft.Container(
                    height=14
                ),

                campo_detalle(
                    "Tipo:",
                    item.tipo_neumatico,
                ),

                campo_detalle(
                    "Medida:",
                    item.medida,
                ),

                campo_detalle(
                    "Marca:",
                    item.marca,
                ),

                campo_detalle(
                    "Cantidad:",
                    str(item.cantidad),
                ),

                ft.Container(
                    padding=ft.Padding.symmetric(
                        vertical=6
                    ),
                    content=ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text(
                                "Estado:",
                                size=12,
                                color=TEXT_SECONDARY,
                            ),
                            badge_estado(
                                item.estado
                            ),
                        ],
                    ),
                ),

                campo_detalle(
                    "Fecha de ingreso:",
                    str(item.fecha_ingreso),
                ),

                campo_detalle(
                    "Observaciones:",
                    getattr(
                        item,
                        "observaciones",
                        None,
                    )
                    or "—",
                ),

                ft.Container(
                    height=10
                ),

                ft.Row(
                    controls=[

                        ft.Container(
                            expand=True
                        ),

                        ft.ElevatedButton(
                            "Cerrar",
                            bgcolor=STAT_BLUE,
                            color="#fff",
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(
                                    radius=8
                                )
                            ),
                            on_click=(
                                lambda e:
                                on_cerrar(e)
                                if on_cerrar
                                else None
                            ),
                        ),
                    ],
                ),
            ],
        ),
    )


def campo_detalle(
    etiqueta: str,
    valor: str,
    color_valor=None,
):

    return ft.Container(
        padding=ft.Padding.symmetric(
            vertical=5
        ),

        content=ft.Column(
            controls=[

                ft.Text(
                    etiqueta,
                    size=12,
                    color=TEXT_SECONDARY,
                ),

                ft.Text(
                    valor,
                    size=13,
                    color=(
                        color_valor
                        or TEXT_PRIMARY
                    ),
                    weight=ft.FontWeight.W_500,
                ),
            ],
            spacing=2,
        ),
    )


def dialogo_eliminar(
    item,
    on_confirmar=None,
    on_cancelar=None,
):

    return ft.Container(
        width=420,
        bgcolor=CARD_BG,
        border_radius=14,
        padding=24,

        shadow=ft.BoxShadow(
            blur_radius=30,
            color=ft.Colors.with_opacity(
                0.35,
                "#000000",
            ),
            offset=ft.Offset(
                0,
                10,
            ),
        ),

        content=ft.Column(
            spacing=14,
            tight=True,

            controls=[

                ft.Row(
                    controls=[

                        ft.Text(
                            "Eliminar inventario",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT_PRIMARY,
                        ),

                        ft.Container(
                            expand=True
                        ),

                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            icon_color=TEXT_SECONDARY,
                            icon_size=18,
                            tooltip="Cerrar",
                            on_click=(
                                lambda e:
                                on_cancelar(e)
                                if on_cancelar
                                else None
                            ),
                        ),
                    ],
                ),

                ft.Divider(
                    height=1,
                    color=DIVIDER,
                ),

                ft.Text(
                    (
                        f"¿Seguro que deseas eliminar "
                        f"el registro de {item.marca} "
                        f"{item.medida}?"
                    ),
                    size=13,
                    color=TEXT_PRIMARY,
                ),

                ft.Text(
                    "Esta acción no se puede deshacer.",
                    size=12,
                    color=TEXT_SECONDARY,
                ),

                ft.Container(
                    height=5
                ),

                ft.Row(
                    controls=[

                        ft.OutlinedButton(
                            "Cancelar",
                            style=ft.ButtonStyle(
                                color=TEXT_SECONDARY,
                                side=ft.BorderSide(
                                    1,
                                    DIVIDER,
                                ),
                                shape=ft.RoundedRectangleBorder(
                                    radius=8
                                ),
                            ),
                            on_click=(
                                lambda e:
                                on_cancelar(e)
                                if on_cancelar
                                else None
                            ),
                        ),

                        ft.Container(
                            expand=True
                        ),

                        ft.ElevatedButton(
                            "Eliminar",
                            bgcolor=STAT_RED,
                            color="#fff",
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(
                                    radius=8
                                )
                            ),
                            on_click=(
                                lambda e:
                                on_confirmar(
                                    item.inventario_id
                                )
                                if on_confirmar
                                else None
                            ),
                        ),
                    ],
                ),
            ],
        ),
    )
def inventario_view(
    page: ft.Page,
    vulcanizadora_id: int,
    on_navigate=None,
    on_logout=None,
):

    active_route = "/inventarioV"


    modal_overlay_ref = ft.Ref[ft.Container]()
    modal_backdrop_ref = ft.Ref[ft.Container]()
    modal_card_ref = ft.Ref[ft.Container]()

    tabla_wrapper_ref = ft.Ref[ft.Container]()
    contador_ref = ft.Ref[ft.Text]()

    resumen_row = ft.Row(
        spacing=12,
        expand=True,
    )

    async def cerrar_modal_async():

        if not modal_backdrop_ref.current:
            return

        modal_backdrop_ref.current.opacity = 0
        modal_card_ref.current.scale = 0.85
        modal_card_ref.current.opacity = 0

        modal_backdrop_ref.current.update()
        modal_card_ref.current.update()

        await asyncio.sleep(0.25)

        modal_overlay_ref.current.visible = False
        modal_overlay_ref.current.update()

    def cerrar_modal(e=None):
        page.run_task(
            cerrar_modal_async
        )

    async def mostrar_modal_async(
        contenido,
        width=560,
    ):

        modal_card_ref.current.width = width
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

    def mostrar_modal(
        contenido,
        width=560,
    ):
        page.run_task(
            mostrar_modal_async,
            contenido,
            width,
        )

    def abrir_detalle(item):

        contenido = detalle_inventario(
            item,
            on_cerrar=cerrar_modal,
        )

        mostrar_modal(
            contenido,
            width=460,
        )

    def confirmar_eliminacion(
        inventario_id,
    ):

        try:

            dao.eliminar(
                inventario_id
            )

            cerrar_modal()
            refrescar(
                actualizar_ui=True
            )

        except Exception as ex:

            print(
                f"Error al eliminar inventario: {ex}"
            )

    def abrir_confirmacion_eliminar(
        item,
    ):

        contenido = dialogo_eliminar(
            item,
            on_confirmar=confirmar_eliminacion,
            on_cancelar=cerrar_modal,
        )

        mostrar_modal(
            contenido,
            width=420,
        )

    def construir_tabla():

        items = dao.listar_por_vulcanizadora(
            vulcanizadora_id
        )

        controles = [
            encabezado_inventario()
        ]

        for item in items:

            controles.append(
                fila_inventario(
                    item,
                    on_ver_detalle=abrir_detalle,
                    on_eliminar=(
                        lambda iid:
                        abrir_confirmacion_eliminar(
                            next(
                                (
                                    x
                                    for x in items
                                    if x.inventario_id == iid
                                ),
                                None,
                            )
                        )
                        if next(
                            (
                                x
                                for x in items
                                if x.inventario_id == iid
                            ),
                            None,
                        )
                        else None
                    ),
                )
            )

        return ft.Container(
            expand=True,
            bgcolor=CARD_BG,
            border_radius=10,
            padding=15,

            content=ft.Column(
                spacing=0,
                controls=[
                    ft.ListView(
                        expand=True,
                        spacing=0,
                        controls=controles,
                    ),
                ],
            ),
        )

    def refrescar(
        actualizar_ui=True
    ):

        resumen = dao.resumen_por_vulcanizadora(
            vulcanizadora_id
        )

        resumen_row.controls = [

            _stat_card(
                "Total en inventario",
                resumen["total"],
                STAT_BLUE,
            ),

            _stat_card(
                "Bueno",
                resumen["bueno"],
                STAT_TEAL,
            ),

            _stat_card(
                "Usado",
                resumen["usado"],
                STAT_ORANGE,
            ),

            _stat_card(
                "Para desecho",
                resumen["para_desecho"],
                STAT_RED,
            ),
        ]

        items = dao.listar_por_vulcanizadora(
            vulcanizadora_id
        )

        contador_ref.current.value = (
            f"{len(items)} elementos"
        )

        tabla_wrapper_ref.current.content = (
            construir_tabla()
        )

        if actualizar_ui:

            resumen_row.update()

            contador_ref.current.update()

            tabla_wrapper_ref.current.update()


    def guardar_nuevo(
        datos,
    ):

        try:

            datos.vulcanizadora_id = (
                vulcanizadora_id
            )

            dao.crear(
                datos
            )

            cerrar_modal()

            refrescar(
                actualizar_ui=True
            )

        except Exception as ex:

            import traceback

            traceback.print_exc()

            print(
                f"Error al guardar inventario: {ex}"
            )

    def abrir_nuevo(e=None):

        formulario = formulario_nuevo_inventario(
            on_guardar=guardar_nuevo,
            on_cancelar=cerrar_modal,
            on_error=lambda mensaje: print(
                mensaje
            ),
        )

        mostrar_modal(
            formulario,
            width=560,
        )


    modal_overlay = ft.Container(
        ref=modal_overlay_ref,
        visible=False,
        expand=True,

        content=ft.Stack(
            controls=[

                # Fondo oscuro
                ft.Container(
                    ref=modal_backdrop_ref,
                    expand=True,

                    bgcolor=ft.Colors.with_opacity(
                        0.65,
                        "#000000",
                    ),

                    blur=10,

                    opacity=0,

                    animate_opacity=ft.Animation(
                        250,
                        ft.AnimationCurve.EASE_OUT,
                    ),

                    on_click=cerrar_modal,
                ),

                # Contenedor centrado
                ft.Container(
                    expand=True,

                    alignment=ft.Alignment.CENTER,

                    on_click=lambda e: None,

                    content=ft.Container(
                        ref=modal_card_ref,

                        width=560,

                        scale=0.85,
                        opacity=0,

                        animate_scale=ft.Animation(
                            320,
                            ft.AnimationCurve.EASE_OUT_BACK,
                        ),

                        animate_opacity=ft.Animation(
                            220,
                            ft.AnimationCurve.EASE_OUT,
                        ),
                    ),
                ),
            ],
        ),
    )


    tabla_card = ft.Container(
        bgcolor=CARD_BG,
        border_radius=12,
        padding=20,
        expand=True,

        content=ft.Column(
            controls=[

                ft.Row(
                    controls=[

                        ft.Text(
                            "Stock actual",
                            size=14,
                            color=TEXT_PRIMARY,
                            weight=ft.FontWeight.BOLD,
                        ),

                        ft.Container(
                            expand=True
                        ),

                        ft.ElevatedButton(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(
                                        ft.Icons.ADD,
                                        size=16,
                                        color="#fff",
                                    ),
                                    ft.Text(
                                        "Agregar",
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
                                shape=ft.RoundedRectangleBorder(
                                    radius=8
                                )
                            ),

                            on_click=abrir_nuevo,
                        ),
                    ],
                ),

                ft.Container(
                    height=10
                ),

                ft.Row(
                    controls=[
                        ft.Container(
                            expand=True,
                            ref=tabla_wrapper_ref,
                        ),
                    ],
                    expand=True,
                ),
            ],
            expand=True,
        ),
    )

    content_area = ft.Container(
        expand=True,
        padding=20,
        bgcolor=MAIN_BG,

        content=ft.Column(
            controls=[

                resumen_row,

                ft.Container(
                    height=12
                ),

                ft.Row(
                    controls=[
                        ft.Container(
                            expand=True
                        ),

                        ft.Text(
                            "0 elementos",
                            size=12,
                            color=TEXT_SECONDARY,
                            ref=contador_ref,
                        ),
                    ],
                ),

                ft.Container(
                    height=12
                ),

                tabla_card,
            ],

            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        ),
    )

    view = ft.View(
        route="/inventarioV",
        padding=0,
        bgcolor=MAIN_BG,

        controls=[

            ft.Column(
                controls=[

                    _topbar_inventario(
                        page
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

    refrescar(
        actualizar_ui=False
    )

    page.overlay.append(
        modal_overlay
    )

    return view
