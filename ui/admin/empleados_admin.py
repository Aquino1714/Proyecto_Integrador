import asyncio
from datetime import date

import flet as ft

from ui.colors import *
from dao.empleado_dao import EmpleadoDAO
from models.empleado import Empleado
from ui.admin.dashboard_admin import sidebar, topbar

ROLES_MAP = {
    1: "Administrador",
    2: "Chofer",
    3: "Recepcion",
    4: "Almacen",
    5: "Triturador",
    6: "Distribucion",
}

TURNOS = [
    "Matutino",
    "Vespertino",
    "Nocturno"
]


ROL_ID_MAP = {v: k for k, v in ROLES_MAP.items()}

ROLES_FILTRO = ["Administrador", "Chofer", "Recepcion", "Almacen", "Triturador", "Distribucion"]  # ← typo corregido

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


def buscador_empleado(on_buscar=None):
    return ft.TextField(
        hint_text="Buscar Empleado",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=8,
        border_color=DIVIDER,
        bgcolor=CARD_BG,
        content_padding=ft.Padding.symmetric(horizontal=14, vertical=10),
        text_size=13,
        expand=True,
        on_change=on_buscar
    )

def boton_nuevo_empleado(on_nuevo_empleado=None):
    return ft.ElevatedButton(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.ADD, size=16, color="#fff"),
                ft.Text("Nuevo empleado", size=13, color="#fff", weight=ft.FontWeight.W_600),
            ],
            spacing=6,
            tight=True,
        ),
        bgcolor=STAT_BLUE,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=lambda e: on_nuevo_empleado(e) if on_nuevo_empleado else None,
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


def tabla_empleados(empleados, on_ver_detalle=None):

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
                        fila_empleado(emp, on_ver_detalle)
                        for emp in empleados
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


def detalle_empleado_card(emp, on_cerrar=None, on_editar=None, on_dar_baja=None):
    nombre_completo = f"{emp.name} {emp.aPaterno} {emp.aMaterno}"
    rol_nombre = ROLES_MAP.get(emp.id_rol, "Sin rol asignado")
    id_display = f"EMP-{emp.empleado_id:03d}"
    estado = "Activo" if emp.active else "Inactivo"
    color_estado = STAT_BLUE if emp.active else "#9ca3af"

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
            spacing=6,
            tight=True,
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Detalles empleado", size=16, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
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
                ft.Container(height=10),
                ft.Row(
                    controls=[
                        ft.CircleAvatar(
                            content=ft.Icon(ft.Icons.PERSON, color=TEXT_SECONDARY, size=30),
                            bgcolor=ft.Colors.with_opacity(0.08, TEXT_PRIMARY),
                            radius=36,
                        ),
                        ft.Container(width=16),
                        ft.Column(
                            spacing=4,
                            controls=[
                                ft.Text(nombre_completo, size=17, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                                ft.Row(
                                    spacing=6,
                                    controls=[
                                        ft.Icon(ft.Icons.BADGE_OUTLINED, size=14, color=TEXT_SECONDARY),
                                        ft.Text(rol_nombre, size=12, color=TEXT_SECONDARY),
                                    ],
                                ),
                                ft.Text(f"No.empleado: {id_display}", size=12, color=TEXT_SECONDARY),
                            ],
                        ),
                    ],
                ),
                ft.Container(height=18),
                campo_detalle("Nombre completo:", nombre_completo),
                campo_detalle("Dirección de correo electrónico:", emp.email, color_valor=STAT_BLUE),
                campo_detalle("Estado:", estado, color_valor=color_estado),
                campo_detalle(
                    "Fecha de nacimiento:",
                    str(emp.fecha_nacimiento) if emp.fecha_nacimiento else "—",
                ),
                ft.Container(height=14),
                ft.Row(
                    controls=[
                        ft.OutlinedButton(
                            "Dar de baja",
                            style=ft.ButtonStyle(
                                color=STAT_ORANGE,
                                side=ft.BorderSide(1, STAT_ORANGE),
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                            on_click=(lambda e: on_dar_baja(emp)) if on_dar_baja else (lambda e: on_cerrar(e) if on_cerrar else None),
                        ),
                        ft.Container(expand=True),
                        ft.ElevatedButton(
                            "Editar",
                            bgcolor=STAT_BLUE,
                            color="#fff",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                            on_click=(lambda e: on_editar(emp)) if on_editar else (lambda e: on_cerrar(e) if on_cerrar else None),
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
        label_style=ft.TextStyle(
            size=11,
            color=TEXT_SECONDARY,
        ),
        content_padding=ft.Padding.symmetric(
            horizontal=12,
            vertical=8
        ),
    )


def formulario_editar_empleado(emp, on_guardar=None, on_cancelar=None):
    nombre_field = campo_editable("Nombre", emp.name)
    apaterno_field = campo_editable("Apellido paterno", emp.aPaterno)
    amaterno_field = campo_editable("Apellido materno", emp.aMaterno)

    fecha_nac_field = campo_editable(
        "Fecha de nacimiento",
        str(emp.fecha_nacimiento) if emp.fecha_nacimiento else "",
    )
    telefono_field = campo_editable("Teléfono", emp.phone or "")
    correo_field = campo_editable("Correo electrónico", emp.email)

    rol_dropdown = ft.Dropdown(
        label="Rol",
        value=ROLES_MAP.get(emp.id_rol),
        border_radius=8,
        border_color=DIVIDER,
        text_size=13,
        label_style=ft.TextStyle(size=12, color=TEXT_SECONDARY),
        options=[ft.dropdown.Option(r) for r in ROLES_FILTRO],
    )

    turno_dropdown = ft.Dropdown(
        label="Turno",
        value=emp.turno if emp.turno else None,
        expand=True,
        border_radius=8,
        border_color=DIVIDER,
        text_size=13,
        label_style=ft.TextStyle(
            size=11,
            color=TEXT_SECONDARY
        ),
        options=[
            ft.dropdown.Option(t)
            for t in TURNOS
        ],
    )

    activo_switch = ft.Switch(
        label="Activo",
        value=emp.active,
        label_text_style=ft.TextStyle(size=13, color=TEXT_PRIMARY),
    )

    def _guardar(e):
        datos_editados = {
            "empleado_id": emp.empleado_id,
            "name": nombre_field.value,
            "aPaterno": apaterno_field.value,
            "aMaterno": amaterno_field.value,
            "email": correo_field.value,
            "phone": telefono_field.value,
            "fecha_nacimiento": fecha_nac_field.value,
            "turno": turno_dropdown.value,
            "id_rol": ROL_ID_MAP.get(rol_dropdown.value, emp.id_rol),
            "active": activo_switch.value,
        }
        if on_guardar:
            on_guardar(datos_editados)

    return ft.Container(
        width=600,
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
                        ft.Text("Editar empleado", size=16, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
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
                ft.Row(controls=[nombre_field], spacing=10),
                ft.Row(controls=[apaterno_field, amaterno_field], spacing=10),
                ft.Row(controls=[fecha_nac_field, telefono_field], spacing=10),
                correo_field,
                ft.Row(controls=[rol_dropdown, turno_dropdown], spacing=10),
                activo_switch,
                ft.Container(height=6),
                ft.Row(
                    controls=[
                        ft.OutlinedButton(
                            "Cancelar",
                            style=ft.ButtonStyle(
                                color=STAT_ORANGE,  # ← ahora naranja
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


# ── Formulario de creación "Nuevo empleado" (modal) ─────────────────────────
def campo_nuevo(label: str, hint: str, password: bool = False):
    """Devuelve (field, layout): field para leer el valor, layout para insertar en la grilla."""
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


def formulario_nuevo_empleado(on_guardar=None, on_cancelar=None):
    nombre_field, nombre_box = campo_nuevo("Nombres:", "Nombre")
    apaterno_field, apaterno_box = campo_nuevo("Apellido paterno:", "Apellido paterno")
    amaterno_field, amaterno_box = campo_nuevo("Apellido materno:", "Apellido materno")
    correo_field, correo_box = campo_nuevo("Correo electrónico:", "ejemplo02@neusomic.com")
    # ⚠️ formato asumido DD/MM/AAAA como texto libre (igual que en el formulario de edición)
    fecha_nac_field, fecha_nac_box = campo_nuevo("Fecha de nacimiento:", "DD/MM/AAAA")
    telefono_field, telefono_box = campo_nuevo("Teléfono:", "10 dígitos")
    password_field, password_box = campo_nuevo("Contraseña:", "Contraseña", password=True)

    rol_dropdown = ft.Dropdown(
        label="Rol",
        expand=True,
        border_radius=8,
        border_color=DIVIDER,
        text_size=13,
        label_style=ft.TextStyle(size=12, color=TEXT_SECONDARY),
        options=[ft.dropdown.Option(r) for r in ROLES_FILTRO],
    )

    turno_dropdown = ft.Dropdown(
        label="Turno",
        expand=True,
        border_radius=8,
        border_color=DIVIDER,
        text_size=13,
        label_style=ft.TextStyle(size=12, color=TEXT_SECONDARY),
        options=[ft.dropdown.Option(t) for t in TURNOS],
    )

    error_text = ft.Text("", size=12, color=STAT_ORANGE, visible=False)

    def _guardar(e):
        campos_obligatorios = [
            nombre_field.value,
            apaterno_field.value,
            correo_field.value,
            password_field.value,
            rol_dropdown.value,
        ]
        if not all(campos_obligatorios):
            error_text.value = "Completa nombres, apellido paterno, correo, contraseña y rol."
            error_text.visible = True
            error_text.update()
            return

        datos_nuevos = {
            "name": nombre_field.value,
            "aPaterno": apaterno_field.value,
            "aMaterno": amaterno_field.value,
            "email": correo_field.value,
            "phone": telefono_field.value or None,
            "fecha_nacimiento": fecha_nac_field.value,
            "turno": turno_dropdown.value,
            "id_rol": ROL_ID_MAP.get(rol_dropdown.value),
            "password": password_field.value,
        }
        if on_guardar:
            on_guardar(datos_nuevos)

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
                        ft.Text("Nuevo empleado", size=16, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
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
                ft.Row(controls=[nombre_box, apaterno_box], spacing=14),
                ft.Row(controls=[amaterno_box, correo_box], spacing=14),
                ft.Row(controls=[fecha_nac_box, telefono_box], spacing=14),
                password_box,
                ft.Row(controls=[rol_dropdown, turno_dropdown], spacing=14),
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
                                    ft.Text("Agregar empleado", size=13, color="#fff", weight=ft.FontWeight.W_600),
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


# ── Diálogo de baja (modal) ─────────────────────────────────────────────────
def dialogo_dar_baja(emp, on_confirmar=None, on_cancelar=None):
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

    def _confirmar(e):
        if on_confirmar:
            on_confirmar(emp.empleado_id, motivo_field.value)

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
                        ft.Text("Dar de baja", size=16, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
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
                    f"Vas a dar de baja a {emp.name} {emp.aPaterno}. Este cambio se aplica de inmediato.",
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
                            "Confirmar baja",
                            bgcolor=STAT_ORANGE,
                            color="#fff",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                            on_click=_confirmar,
                        ),
                    ],
                ),
            ],
        ),
    )


# ── Contenido de Empleados (área central + modal animado) ──────────────────
def empleados_content(page: ft.Page, on_nuevo_empleado=None, on_ver_detalle=None):
    empleados = EmpleadoDAO().get_all()

    modal_overlay_ref = ft.Ref[ft.Container]()
    modal_backdrop_ref = ft.Ref[ft.Container]()
    modal_card_ref = ft.Ref[ft.Container]()
    tabla_wrapper_ref = ft.Ref[ft.Container]()
    contador_ref = ft.Ref[ft.Text]()

    busqueda_actual = ""
    rol_actual = None

    def actualizar_tabla():
        lista = EmpleadoDAO().get_all()

        if busqueda_actual:
            texto = busqueda_actual.lower()

            lista = [
                e for e in lista
                if texto in e.name.lower()
                   or texto in e.aPaterno.lower()
                   or texto in e.email.lower()
            ]

        if rol_actual:
            lista = [
                e for e in lista
                if ROLES_MAP.get(e.id_rol) == rol_actual
            ]

        tabla_wrapper_ref.current.content = tabla_empleados(
            lista,
            manejar_click_fila
        )

        tabla_wrapper_ref.current.update()

        contador_ref.current.value = f"{len(lista)} elementos"
        contador_ref.current.update()

    def _refrescar_lista():
        actualizar_tabla()
        nuevos = EmpleadoDAO().get_all()
        tabla_wrapper_ref.current.content = tabla_empleados(nuevos, manejar_click_fila)
        tabla_wrapper_ref.current.update()
        if contador_ref.current:
            contador_ref.current.value = f"{len(nuevos)} elementos"
            contador_ref.current.update()

    def buscar_empleado(e):
        nonlocal busqueda_actual

        busqueda_actual = e.control.value
        actualizar_tabla()

    def aplicar_filtro(rol):
        nonlocal rol_actual

        rol_actual = rol
        actualizar_tabla()

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

    def ir_a_editar(emp):
        page.run_task(
            _swap_contenido,
            formulario_editar_empleado(emp, on_guardar=guardar_edicion, on_cancelar=cerrar_modal),
        )

    def ir_a_baja(emp):
        page.run_task(
            _swap_contenido,
            dialogo_dar_baja(emp, on_confirmar=confirmar_baja, on_cancelar=cerrar_modal),
        )

    def guardar_edicion(datos):
        emp_actualizado = EmpleadoDAO().get_by_id(datos["empleado_id"])
        emp_actualizado.name = datos["name"]
        emp_actualizado.aPaterno = datos["aPaterno"]
        emp_actualizado.aMaterno = datos["aMaterno"]
        emp_actualizado.email = datos["email"]
        emp_actualizado.phone = datos["phone"]
        emp_actualizado.fecha_nacimiento = datos["fecha_nacimiento"]
        emp_actualizado.turno = datos["turno"]
        emp_actualizado.id_rol = datos["id_rol"]
        emp_actualizado.active = datos["active"]
        # ⚠️ password_hash se reenvía tal cual para no perder el password actual,
        # pero EmpleadoDAO.update() lo vuelve a hashear -> ROMPE EL LOGIN.
        # Pendiente resolver en el DAO (ver nota en mensajes anteriores).
        EmpleadoDAO().update(emp_actualizado)
        _refrescar_lista()
        cerrar_modal()

    def confirmar_baja(empleado_id, motivo):
        EmpleadoDAO().unsubscribe(empleado_id, motivo, date.today())
        _refrescar_lista()
        cerrar_modal()

    def guardar_nuevo(datos):
        # ⚠️ password_hash recibe el texto plano a propósito:
        # EmpleadoDAO.insert() lo hashea internamente (a diferencia de update()).
        nuevo = Empleado(
            empleado_id=None,
            name=datos["name"],
            aPaterno=datos["aPaterno"],
            aMaterno=datos["aMaterno"],
            email=datos["email"],
            phone=datos["phone"],
            password_hash=datos["password"],
            active=True,
            fecha_registro=date.today(),
            fecha_baja=None,
            motivo_baja=None,
            id_rol=datos["id_rol"],
            fecha_nacimiento=datos["fecha_nacimiento"],
            turno=datos["turno"],
        )
        EmpleadoDAO().insert(nuevo)
        _refrescar_lista()
        cerrar_modal()

    def abrir_detalle(emp):
        async def _abrir():
            tarjeta = detalle_empleado_card(
                emp,
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
            formulario = formulario_nuevo_empleado(on_guardar=guardar_nuevo, on_cancelar=cerrar_modal)
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
        if on_nuevo_empleado:
            on_nuevo_empleado(e)

    def manejar_click_fila(emp):
        abrir_detalle(emp)
        if on_ver_detalle:
            on_ver_detalle(emp)

    modal_overlay = ft.Container(
        ref=modal_overlay_ref,
        visible=False,
        expand=True,
        content=ft.Stack(
            controls=[
                ft.Container(
                    ref=modal_backdrop_ref,
                    expand=True,
                    bgcolor=ft.Colors.with_opacity(0.65, "#000000"),  # más opaco para resaltar la tarjeta
                    blur=10,  # efecto glass sobre el contenido de fondo
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
                                buscador_empleado(buscar_empleado),
                                boton_nuevo_empleado(manejar_click_nuevo)
                            ],
                            spacing=12,
                        ),
                        ft.Container(height=12),
                        filtro_row(aplicar_filtro),
                        ft.Container(height=12),
                        ft.Row(
                            controls=[
                                ft.Container(expand=True),
                                ft.Text(f"{len(empleados)} elementos", size=12, color=TEXT_SECONDARY, ref=contador_ref),
                            ],
                        ),
                        ft.Container(height=20),
                        ft.Container(
                            ref=tabla_wrapper_ref,
                            expand=True,
                            content=tabla_empleados(empleados, manejar_click_fila),
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


def empleados_admin(page: ft.Page, on_navigate=None, on_nuevo_empleado=None, on_ver_detalle=None, on_logout=None):
    active_route = "/usuarios"

    return ft.View(
        route="/usuarios",
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
                                content=empleados_content(page, on_nuevo_empleado, on_ver_detalle),
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
                            "ID",
                            weight=ft.FontWeight.BOLD,
                            color=TEXT_PRIMARY,
                        ),
                        expand=1,
                    ),

                    ft.Container(
                        ft.Text(
                            "Nombre",
                            weight=ft.FontWeight.BOLD,
                            color=TEXT_PRIMARY,
                        ),
                        expand=3,
                    ),

                    ft.Container(
                        ft.Text(
                            "Correo",
                            weight=ft.FontWeight.BOLD,
                            color=TEXT_PRIMARY,
                        ),
                        expand=4,
                    ),

                    ft.Container(
                        ft.Text(
                            "Rol",
                            weight=ft.FontWeight.BOLD,
                            color=TEXT_PRIMARY,
                        ),
                        expand=2,
                    ),
                ]
            ),
        )

def fila_empleado(emp, on_click=None):
        nombre = f"{emp.name} {emp.aPaterno} {emp.aMaterno}"

        return ft.Container(
            padding=15,
            border=ft.Border.only(
                bottom=ft.BorderSide(1, DIVIDER)
            ),
            ink=True,
            on_click=lambda e: on_click(emp) if on_click else None,
            content=ft.Row(
                controls=[

                    ft.Container(
                        ft.Text(
                            f"EMP-{emp.empleado_id:03d}",
                            color=TEXT_SECONDARY,
                        ),
                        expand=1,
                    ),

                    ft.Container(
                        ft.Text(
                            nombre,
                            color=TEXT_PRIMARY,
                        ),
                        expand=3,
                    ),

                    ft.Container(
                        ft.Text(
                            emp.email,
                            color=TEXT_SECONDARY,
                        ),
                        expand=4,
                    ),

                    ft.Container(
                        badge_rol(
                            ROLES_MAP.get(emp.id_rol, "")
                        ),
                        expand=2,
                    ),
                ]
            ),
        )