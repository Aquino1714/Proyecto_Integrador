import flet as ft
from datetime import date, time

from ui.colors import *
from ui.admin.dashboard_admin import sidebar, topbar
from dao.transporte_dao import TransportDAO


# ── Colores por estado ───────────────────────────────────────────────────────
ESTADO_COLORS = {
    "Disponible": STAT_BLUE,
    "En viaje": STAT_ORANGE,
    "De regreso": STAT_TEAL,
    "Mantenimiento": "#9CA3AF",
    "Fuera de servicio": "#f87171",
}

FILTROS_ESTADO = ["Todos", "Disponible", "En viaje", "De regreso", "Mantenimiento", "Fuera de servicio"]


def estado_badge(estado: str):
    color = ESTADO_COLORS.get(estado, TEXT_SECONDARY)
    return ft.Container(
        content=ft.Text(estado, size=11, color=color, weight=ft.FontWeight.W_600),
        padding=ft.Padding.symmetric(horizontal=10, vertical=4),
        border=ft.Border.all(1, color),
        border_radius=6,
        bgcolor=ft.Colors.with_opacity(0.08, color),
    )


# ── Modal: Detalles del viaje ────────────────────────────────────────────────
def mostrar_detalle_chofer(page: ft.Page, chofer: dict, on_asignar_click):
    estado = chofer["estado"]
    color_estado = ESTADO_COLORS.get(estado, TEXT_SECONDARY)

    mapa_placeholder = ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(ft.Icons.MAP_OUTLINED, size=40, color="#9CA3AF"),
                ft.Text("Vista de mapa no disponible aún", size=12, color="#9CA3AF"),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=6,
        ),
        alignment=ft.alignment.center,
        bgcolor="#F3F4F6",
        border_radius=8,
        height=220,
        expand=True,
    )

    dialog = ft.AlertDialog(
        modal=True,
        bgcolor=CARD_BG,
        content=ft.Container(
            width=560,
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.CircleAvatar(
                                content=ft.Icon(ft.Icons.PERSON, size=34, color="#9CA3AF"),
                                bgcolor="#E5E7EB",
                                radius=34,
                            ),
                            ft.Container(width=14),
                            ft.Column(
                                controls=[
                                    ft.Text(chofer["nombre_completo"], size=16,
                                             weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                                    ft.Row(
                                        controls=[
                                            ft.Icon(ft.Icons.LOCAL_SHIPPING_OUTLINED, size=14, color=TEXT_SECONDARY),
                                            ft.Text(f"Transporte: {chofer['unidad_asignada']}",
                                                    size=12, color=TEXT_SECONDARY),
                                        ],
                                        spacing=6,
                                    ),
                                    ft.Text(f"Placas: {chofer['placas']}", size=12, color=TEXT_SECONDARY),
                                ],
                                spacing=2,
                            ),
                            ft.Container(expand=True),
                            ft.Column(
                                controls=[
                                    ft.Text("Estado de viaje", size=11, color=TEXT_SECONDARY),
                                    ft.Text(estado.upper(), size=13, weight=ft.FontWeight.BOLD, color=color_estado),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.END,
                                spacing=2,
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.START,
                    ),
                    ft.Container(height=16),
                    mapa_placeholder,
                    ft.Container(height=16),
                    ft.Row(
                        controls=[
                            ft.OutlinedButton(
                                "Regresar",
                                style=ft.ButtonStyle(color=STAT_ORANGE),
                                on_click=lambda e: page.close(dialog),
                            ),
                            ft.Container(expand=True),
                            ft.ElevatedButton(
                                "Asignar viaje",
                                bgcolor=STAT_BLUE,
                                color="#fff",
                                disabled=estado != "Disponible",
                                on_click=lambda e: (page.close(dialog), on_asignar_click(chofer)),
                            ),
                        ],
                    ),
                ],
                tight=True,
            ),
        ),
    )
    page.open(dialog)


# ── Modal: Asignar viaje ─────────────────────────────────────────────────────
def mostrar_asignar_viaje(page: ft.Page, chofer: dict, on_confirmado):
    estado = chofer["estado"]
    color_estado = ESTADO_COLORS.get(estado, TEXT_SECONDARY)

    fecha_ref = ft.Ref[ft.Text]()
    hora_ref = ft.Ref[ft.Text]()
    destino_field = ft.TextField(
        label="Destino",
        border_color="#D1D5DB",
        border_radius=8,
    )
    instrucciones_field = ft.TextField(
        label=None,
        hint_text="",
        multiline=True,
        min_lines=4,
        max_lines=6,
        border_color="#D1D5DB",
        border_radius=8,
    )

    estado_seleccion = {"fecha": date.today(), "hora": time(9, 0)}

    def fecha_elegida(e):
        if date_picker.value:
            estado_seleccion["fecha"] = date_picker.value
            fecha_texto.value = date_picker.value.strftime("%d/%m/%Y")
            fecha_texto.update()

    def hora_elegida(e):
        if time_picker.value:
            estado_seleccion["hora"] = time_picker.value
            hora_texto.value = time_picker.value.strftime("%I:%M %p")
            hora_texto.update()

    date_picker = ft.DatePicker(on_change=fecha_elegida)
    time_picker = ft.TimePicker(on_change=hora_elegida)
    page.overlay.extend([date_picker, time_picker])

    fecha_texto = ft.Text(estado_seleccion["fecha"].strftime("%d/%m/%Y"), size=12, color=TEXT_PRIMARY)
    hora_texto = ft.Text(estado_seleccion["hora"].strftime("%I:%M %p"), size=12, color=TEXT_PRIMARY)

    def confirmar_click(e):
        if not destino_field.value:
            destino_field.error_text = "El destino es obligatorio"
            destino_field.update()
            return
        TransportDAO.asignar_viaje(
            transporte_id=chofer["transporte_id"],
            fecha=estado_seleccion["fecha"],
            hora=estado_seleccion["hora"],
            destino=destino_field.value,
            instrucciones=instrucciones_field.value or "",
        )
        page.close(dialog)
        on_confirmado()

    dialog = ft.AlertDialog(
        modal=True,
        bgcolor=CARD_BG,
        content=ft.Container(
            width=520,
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("Asignar viaje", size=16, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                            ft.Container(expand=True),
                            ft.IconButton(
                                icon=ft.Icons.CLOSE,
                                icon_color=STAT_ORANGE,
                                on_click=lambda e: page.close(dialog),
                            ),
                        ],
                    ),
                    ft.Row(
                        controls=[
                            ft.CircleAvatar(
                                content=ft.Icon(ft.Icons.PERSON, size=28, color="#9CA3AF"),
                                bgcolor="#E5E7EB",
                                radius=28,
                            ),
                            ft.Container(width=12),
                            ft.Column(
                                controls=[
                                    ft.Text(chofer["nombre_completo"], size=14,
                                             weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                                    ft.Text(f"Transporte: {chofer['unidad_asignada']}", size=11, color=TEXT_SECONDARY),
                                    ft.Text(f"Placas: {chofer['placas']}", size=11, color=TEXT_SECONDARY),
                                ],
                                spacing=2,
                            ),
                            ft.Container(expand=True),
                            ft.Text(estado, size=13, weight=ft.FontWeight.BOLD, color=color_estado),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.START,
                    ),
                    ft.Divider(height=1, color=DIVIDER),
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text("Fecha:", size=12, color=TEXT_SECONDARY),
                                    ft.OutlinedButton(
                                        content=ft.Row(
                                            controls=[
                                                ft.Icon(ft.Icons.CALENDAR_TODAY, size=14),
                                                fecha_texto,
                                            ],
                                            spacing=6,
                                        ),
                                        on_click=lambda e: page.open(date_picker),
                                    ),
                                ],
                                spacing=4,
                            ),
                            ft.Container(width=24),
                            ft.Column(
                                controls=[
                                    ft.Text("Hora:", size=12, color=TEXT_SECONDARY),
                                    ft.OutlinedButton(
                                        content=ft.Row(
                                            controls=[
                                                ft.Icon(ft.Icons.ACCESS_TIME, size=14),
                                                hora_texto,
                                            ],
                                            spacing=6,
                                        ),
                                        on_click=lambda e: page.open(time_picker),
                                    ),
                                ],
                                spacing=4,
                            ),
                        ],
                    ),
                    ft.Container(height=8),
                    destino_field,
                    ft.Container(height=8),
                    ft.Text("Instrucciones:", size=12, color=TEXT_SECONDARY),
                    instrucciones_field,
                    ft.Container(height=12),
                    ft.Row(
                        controls=[
                            ft.OutlinedButton(
                                "Regresar",
                                style=ft.ButtonStyle(color=STAT_ORANGE),
                                on_click=lambda e: page.close(dialog),
                            ),
                            ft.Container(expand=True),
                            ft.ElevatedButton(
                                "Asignar viaje",
                                bgcolor=STAT_BLUE,
                                color="#fff",
                                on_click=confirmar_click,
                            ),
                        ],
                    ),
                ],
                tight=True,
            ),
        ),
    )
    page.open(dialog)


# ── Tabla ─────────────────────────────────────────────────────────────────
def _fila_tabla(chofer: dict, on_click):
    celda = lambda texto, expand=1: ft.Container(
        content=ft.Text(texto, size=12, color=TEXT_PRIMARY),
        expand=expand,
    )
    return ft.Container(
        on_click=lambda e: on_click(chofer),
        ink=True,
        padding=ft.Padding.symmetric(horizontal=16, vertical=12),
        tooltip="Ver más detalles del chofer",
        content=ft.Row(
            controls=[
                celda(f"CH-{chofer['transporte_id']:03d}"),
                celda(chofer["nombre_completo"], expand=2),
                celda(chofer["unidad_asignada"], expand=2),
                celda(chofer["placas"]),
                celda(f"{chofer['capacidad_carga_kg']:,}Kg"),
                ft.Container(
                    content=estado_badge(chofer["estado"]),
                    expand=1,
                    alignment=ft.Alignment(1, 0)
                ),
            ],
        ),
    )


def _encabezado_tabla():
    celda = lambda texto, expand=1: ft.Container(
        content=ft.Text(texto, size=12, color=TEXT_SECONDARY, weight=ft.FontWeight.W_600),
        expand=expand,
    )
    return ft.Container(
        padding=ft.Padding.symmetric(horizontal=16, vertical=10),
        bgcolor="#F9FAFB",
        content=ft.Row(
            controls=[
                celda("ID"),
                celda("Nombre", expand=2),
                celda("Unidad asignada", expand=2),
                celda("Placas"),
                celda("Capacidad Máxima"),
                ft.Container(
                    content=ft.Text(
                        "Estado",
                        size=12,
                        color=TEXT_SECONDARY,
                        weight=ft.FontWeight.W_600
                    ),
                    expand=1,
                    alignment=ft.Alignment(1, 0)
                ),
            ],
        ),
    )


# ── Vista principal ──────────────────────────────────────────────────────────
def monitor_transporte(page: ft.Page, on_navigate=None, on_logout=None):
    active_route = "/neumaticos"

    FILAS_POR_PAGINA = 5
    estado_vista = {"choferes": [], "busqueda": "", "filtro": None, "pagina": 1}

    tabla_container = ft.Ref[ft.Column]()
    paginacion_container = ft.Ref[ft.Row]()

    def abrir_detalle(chofer):
        mostrar_detalle_chofer(page, chofer, on_asignar_click=abrir_asignar)

    def abrir_asignar(chofer):
        mostrar_asignar_viaje(page, chofer, on_confirmado=cargar_datos)

    def cargar_datos():
        filtro = None if estado_vista["filtro"] in (None, "Todos") else estado_vista["filtro"]
        estado_vista["choferes"] = TransportDAO.obtener_choferes_transporte(
            busqueda=estado_vista["busqueda"] or None,
            filtro_estado=filtro,
        )
        estado_vista["pagina"] = 1
        redibujar()

    def redibujar():
        choferes = estado_vista["choferes"]
        total_paginas = max(1, -(-len(choferes) // FILAS_POR_PAGINA))
        pagina = min(estado_vista["pagina"], total_paginas)
        inicio = (pagina - 1) * FILAS_POR_PAGINA
        pagina_actual = choferes[inicio:inicio + FILAS_POR_PAGINA]

        filas = [_fila_tabla(c, abrir_detalle) for c in pagina_actual]
        if not filas:
            filas = [
                ft.Container(
                    padding=20,
                    content=ft.Text("No hay choferes que coincidan con la búsqueda/filtro.", size=12, color=TEXT_SECONDARY),
                )
            ]

        tabla_container.current.controls = [
            _encabezado_tabla(),
            ft.Column(controls=filas, spacing=0),
        ]
        if tabla_container.current.page:
            tabla_container.current.update()

        # ────Paginación─────────────────────────────────────────────
        def ir_a_pagina(n):
            estado_vista["pagina"] = n
            redibujar()

        botones_pagina = []
        for n in range(1, total_paginas + 1):
            es_actual = n == pagina
            botones_pagina.append(
                ft.TextButton(
                    str(n),
                    style=ft.ButtonStyle(
                        color=STAT_BLUE if es_actual else TEXT_SECONDARY,
                        overlay_color="transparent",
                    ),
                    on_click=lambda e, n=n: ir_a_pagina(n),
                )
            )

        paginacion_container.current.controls = [
            ft.IconButton(icon=ft.Icons.CHEVRON_LEFT, icon_size=16,
                           disabled=pagina <= 1,
                           on_click=lambda e: ir_a_pagina(pagina - 1)),
            *botones_pagina,
            ft.IconButton(icon=ft.Icons.CHEVRON_RIGHT, icon_size=16,
                          disabled=pagina >= total_paginas,
                          on_click=lambda e: ir_a_pagina(pagina + 1)),
        ]
        if paginacion_container.current.page:
            paginacion_container.current.update()

    def buscar_click(e):
        estado_vista["busqueda"] = buscador.value
        cargar_datos()

    def filtro_cambiado(e):
        estado_vista["filtro"] = e.control.value
        cargar_datos()

    buscador = ft.TextField(
        hint_text="Buscar chofer",
        prefix_icon=ft.Icons.SEARCH,
        border_color="#D1D5DB",
        border_radius=8,
        expand=True,
        on_submit=buscar_click,
    )

    filtro_dropdown = ft.Dropdown(
        hint_text="Filtrar",
        width=160,
        border_color="#D1D5DB",
        border_radius=8,
        options=[ft.dropdown.Option(f) for f in FILTROS_ESTADO],
    )

    filtro_dropdown.on_change = filtro_cambiado

    barra_busqueda = ft.Row(
        controls=[
            buscador,
            ft.ElevatedButton("Buscar", bgcolor=STAT_BLUE, color="#fff", on_click=buscar_click),
            filtro_dropdown,
        ],
        spacing=10,
    )

    tabla = ft.Column(ref=tabla_container, controls=[], spacing=0)
    paginacion = ft.Row(ref=paginacion_container, controls=[], alignment=ft.MainAxisAlignment.CENTER)

    info_button = ft.Container(
        content=ft.Icon(ft.Icons.INFO_OUTLINE, color="#ffffff", size=18),
        padding=8,
        border_radius=18,
        border=ft.Border.all(1, "#ffffff"),
        ink=True,
        tooltip="Más información sobre nosotros",
    )

    content_area = ft.Stack(
        controls=[
            ft.Container(
                expand=True,
                padding=20,
                bgcolor=MAIN_BG,
                content=ft.Column(
                    controls=[
                        barra_busqueda,
                        ft.Container(height=16),
                        ft.Container(
                            bgcolor=CARD_BG,
                            border_radius=10,
                            content=tabla,
                        ),
                        ft.Container(height=16),
                        paginacion,
                    ],
                    spacing=0,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                ),
            ),
            ft.Container(content=info_button, right=20, bottom=20),
        ],
        expand=True,
    )

    vista = ft.View(
        route=active_route,
        padding=0,
        bgcolor=MAIN_BG,
        controls=[
            ft.Column(
                controls=[
                    topbar(page, active_route),
                    ft.Row(
                        controls=[
                            sidebar(active_route=active_route, on_navigate=on_navigate, on_logout=on_logout),
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

    return vista
