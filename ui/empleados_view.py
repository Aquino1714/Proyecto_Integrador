import flet as ft
from dao.empleado_dao import EmpleadoDAO
from models.empleados import Empleado


def empleados_view(page: ft.Page):
    page.title = "Neusomic - Empleados"
    page.bgcolor = "#091B3D"
    page.padding = 0

    empleado_dao = EmpleadoDAO()

    # ----------------------------------------------------
    # NAVEGACIÓN ENTRE VISTAS
    # ----------------------------------------------------
    def navegar(e, vista):
        page.clean()
        if vista == "dashboard":
            from ui.admin_view import admin_view
            admin_view(page)
        elif vista == "empleados":
            empleados_view(page)

    sidebar = ft.Container(
        width=240,
        bgcolor="#0B1A30",
        padding=15,
        content=ft.Column(
            controls=[
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.DASHBOARD_OUTLINED, color="white70"),
                    title=ft.Text("Dashboard", color="white70"),
                    on_click=lambda e: navegar(e, "dashboard")
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.PEOPLE_ALT_OUTLINED, color="#FFA726"),
                    title=ft.Text("Empleados", color="#FFA726", weight=ft.FontWeight.BOLD),
                    on_click=lambda e: navegar(e, "empleados")
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.LOCAL_SHIPPING_OUTLINED, color="white70"),
                    title=ft.Text("Monitor transporte", color="white70"),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.DELETE_OUTLINED, color="white70"),
                    title=ft.Text("Reportes de residuos", color="white70"),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.BAR_CHART_OUTLINED, color="white70"),
                    title=ft.Text("Reportes", color="white70"),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.COMMUTE_OUTLINED, color="white70"),
                    title=ft.Text("Transportes", color="white70"),
                ),
                ft.Container(expand=True),
                ft.OutlinedButton(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.LOGOUT, color="#EF5350", size=18),
                            ft.Text("Cerrar sesión", color="#EF5350"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    style=ft.ButtonStyle(side=ft.BorderSide(1, "#EF5350")),
                    on_click=lambda e: cerrar_sesion(page)
                )
            ],
            spacing=10,
        )
    )

    header = ft.Container(
        height=65,
        bgcolor="#1E5BB8",
        padding=20,
        content=ft.Row(
            controls=[
                ft.Text("Empleados", color="white", size=24, weight=ft.FontWeight.BOLD),
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.NOTIFICATIONS, color="#FFA726"),
                        ft.Text("Administrador", color="white", weight=ft.FontWeight.BOLD),
                        ft.Icon(ft.Icons.ACCOUNT_CIRCLE, color="white", size=36),
                    ],
                    spacing=15
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
    )

    # ----------------------------------------------------
    # BADGE / CHIP PARA ROL
    # ----------------------------------------------------
    def crear_badge_rol(rol_nombre):
        rol_txt = str(rol_nombre or "Sin rol")
        color_fondo = "#1565C0" if "Almacén" in rol_txt or "trituración" in rol_txt else "#455A64"
        return ft.Container(
            content=ft.Text(rol_txt, color="white", size=12, weight=ft.FontWeight.BOLD),
            bgcolor=color_fondo,
            padding=ft.Padding(left=12, top=6, right=12, bottom=6),
            border_radius=5,
            alignment=ft.Alignment(0, 0)
        )

    # ----------------------------------------------------
    # TABLA DE EMPLEADOS
    # ----------------------------------------------------
    txt_contador = ft.Text("0 elementos", color="white70", size=12)

    tabla_empleados = ft.DataTable(
        bgcolor="#1A2634",
        border_radius=8,
        heading_row_color="#0F1722",
        show_checkbox_column=True,
        columns=[
            ft.DataColumn(ft.Text("ID", color="white", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Nombre completo", color="white", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Correo electrónico", color="white", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Rol", color="white", weight=ft.FontWeight.BOLD)),
        ],
        rows=[]
    )

    def cargar_empleados():
        tabla_empleados.rows.clear()
        try:
            lista_emp = empleado_dao.obtener_todos()
            txt_contador.value = f"{len(lista_emp)} elementos"
            
            def seleccionar_unica_fila(e, row_obj):
                estado_actual = row_obj.selected
                for r in tabla_empleados.rows:
                    r.selected = False
                row_obj.selected = not estado_actual
                page.update()

            for emp in lista_emp:
                nombre_completo = f"{emp.nombre} {emp.apellido_paterno} {emp.apellido_materno}".strip()
                id_formateado = f"EMP-{emp.empleado_id:03d}" if isinstance(emp.empleado_id, int) else str(emp.empleado_id)
                
                nueva_fila = ft.DataRow(
                    selected=False,
                    data=emp.empleado_id,
                )

                nueva_fila.on_select_change = lambda e, r=nueva_fila: seleccionar_unica_fila(e, r)

                nueva_fila.cells = [
                    ft.DataCell(ft.Text(id_formateado, color="white")),
                    ft.DataCell(ft.Text(nombre_completo, color="white")),
                    ft.DataCell(ft.Text(emp.correo, color="white70")),
                    ft.DataCell(crear_badge_rol(emp.rol)),
                ]
                
                tabla_empleados.rows.append(nueva_fila)

        except Exception as ex:
            print(f"Error al cargar empleados desde BD: {ex}")
        
        page.update()

    # ----------------------------------------------------
    # FORMULARIO "NUEVO EMPLEADO"
    # ----------------------------------------------------
    def crear_campo(label, hint="", password=False, read_only=False):
        return ft.TextField(
            label=label,
            hint_text=hint,
            border_color="#455A64",
            focused_border_color="#1E88E5",
            bgcolor="#1F2D40",
            label_style=ft.TextStyle(color="white70", size=12),
            border_radius=6,
            height=48,
            read_only=read_only,
            password=password,
            can_reveal_password=password,
            expand=True
        )

    txt_id = crear_campo("ID", hint="Autogenerado", read_only=True)
    txt_nom = crear_campo("Nombre(s)", hint="Nombre")
    txt_pat = crear_campo("Apellido paterno", hint="Apellido paterno")
    txt_mat = crear_campo("Apellido materno", hint="Apellido materno")
    txt_cor = crear_campo("Correo electrónico", hint="ejemplo@neusomic.com")
    txt_tel = crear_campo("Teléfono", hint="10 dígitos")
    txt_pas = crear_campo("Contraseña", hint="••••••••", password=True)

    drop_rol_modal = ft.Dropdown(
        label="Rol",
        bgcolor="#1F2D40",
        border_color="#455A64",
        focused_border_color="#1E88E5",
        label_style=ft.TextStyle(color="white70", size=12),
        border_radius=6,
        expand=True,
        options=[
            ft.dropdown.Option(key="1", text="Encargado Almacén"),
            ft.dropdown.Option(key="2", text="Chofer"),
            ft.dropdown.Option(key="3", text="Operario trituración"),
        ]
    )

    dialogo_agregar = ft.AlertDialog(
        bgcolor="#1A2634",
        shape=ft.RoundedRectangleBorder(radius=8),
        title=ft.Row(
            controls=[
                ft.Text("Nuevo empleado", color="#2196F3", size=18, weight=ft.FontWeight.BOLD),
                ft.IconButton(
                    icon=ft.Icons.CLOSE,
                    icon_color="#FFA726",
                    icon_size=20,
                    on_click=lambda e: cerrar_modal(e)
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        content=ft.Container(
            width=580,
            padding=10,
            content=ft.Column(
                controls=[
                    ft.Row(controls=[txt_id, txt_nom], spacing=15),
                    ft.Row(controls=[txt_pat, txt_mat], spacing=15),
                    ft.Row(controls=[txt_cor, txt_tel], spacing=15),
                    ft.Row(controls=[txt_pas, drop_rol_modal], spacing=15),
                ],
                spacing=15,
                tight=True
            )
        )
    )

    def cerrar_modal(e=None):
        dialogo_agregar.open = False
        page.update()

    def guardar_empleado_bd(e):
        try:
            nuevo_emp = Empleado(
                empleado_id=None,
                nombre=txt_nom.value,
                apellido_paterno=txt_pat.value,
                apellido_materno=txt_mat.value,
                correo=txt_cor.value,
                telefono=txt_tel.value or "0000000000",
                password=txt_pas.value or "123456",
                activo=True,
                id_rol=int(drop_rol_modal.value) if drop_rol_modal.value else 1,
                fecha_registro=None,
                fecha_baja=None,
                motivo_baja=None
            )

            empleado_dao.insertar(nuevo_emp)

            txt_nom.value = txt_pat.value = txt_mat.value = txt_cor.value = txt_tel.value = txt_pas.value = ""
            drop_rol_modal.value = None
            
            dialogo_agregar.open = False
            page.update()

            cargar_empleados()

        except Exception as ex:
            print(f"Error al insertar en la base de datos: {ex}")

    dialogo_agregar.actions = [
        ft.Row(
            controls=[
                ft.OutlinedButton(
                    content=ft.Text("Cancelar", color="#FFA726"),
                    height=42,
                    width=140,
                    style=ft.ButtonStyle(side=ft.BorderSide(1, "#FFA726")),
                    on_click=cerrar_modal
                ),
                ft.ElevatedButton(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.ADD, color="white", size=16),
                            ft.Text("Agregar empleado", color="white", weight=ft.FontWeight.BOLD)
                        ],
                        spacing=5
                    ),
                    bgcolor="#1E88E5",
                    height=42,
                    on_click=guardar_empleado_bd
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
    ]

    def abrir_modal_nuevo(e):
        if dialogo_agregar not in page.overlay:
            page.overlay.append(dialogo_agregar)
        dialogo_agregar.open = True
        page.update()

    # ----------------------------------------------------
    # COMPONENTES Y MODAL "VER DETALLES"
    # ----------------------------------------------------
    lbl_det_nombre_encabezado = ft.Text("", color="white", size=20, weight=ft.FontWeight.BOLD)
    lbl_det_rol = ft.Text("", color="white70", size=12)
    lbl_det_num_emp = ft.Text("", color="white70", size=13)
    lbl_det_nombre_completo = ft.Text("", color="white", size=14)
    lbl_det_correo = ft.Text("", color="#2196F3", size=14)
    lbl_det_estado = ft.Container(
        content=ft.Text("Activo", color="white", size=12, weight=ft.FontWeight.BOLD),
        bgcolor="#4CAF50",
        padding=ft.Padding(left=10, top=4, right=10, bottom=4),
        border_radius=4
    )
    lbl_det_fecha_nac = ft.Text("03/08/1995", color="white", size=14)

    dialogo_detalles = ft.AlertDialog(
        bgcolor="#1A2634",
        shape=ft.RoundedRectangleBorder(radius=8),
        title=ft.Row(
            controls=[
                ft.Text("Detalles empleado", color="#2196F3", size=16, weight=ft.FontWeight.BOLD),
                ft.IconButton(
                    icon=ft.Icons.CLOSE,
                    icon_color="#FFA726",
                    icon_size=20,
                    on_click=lambda e: cerrar_modal_detalles(e)
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        content=ft.Container(
            width=500,
            padding=15,
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.CircleAvatar(
                                content=ft.Icon(ft.Icons.PERSON, size=50, color="white70"),
                                radius=40,
                                bgcolor="#37474F"
                            ),
                            ft.Column(
                                controls=[
                                    lbl_det_nombre_encabezado,
                                    ft.Row(controls=[ft.Icon(ft.Icons.WORK_OUTLINED, size=14, color="white70"), lbl_det_rol]),
                                    ft.Text("No. empleado:", color="white70", size=12),
                                    lbl_det_num_emp
                                ],
                                spacing=3
                            )
                        ],
                        spacing=20
                    ),
                    ft.Divider(color="white12", height=20),
                    ft.Row(
                        controls=[
                            ft.Text("Nombre completo:", color="white70", width=180),
                            lbl_det_nombre_completo
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.Text("Dirección de correo electrónico:", color="white70", width=180),
                            lbl_det_correo
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.Text("Estado:", color="white70", width=180),
                            lbl_det_estado
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.Text("Fecha de nacimiento:", color="white70", width=180),
                            lbl_det_fecha_nac
                        ]
                    ),
                ],
                spacing=12,
                tight=True
            )
        ),
        actions=[
            ft.Row(
                controls=[
                    ft.OutlinedButton(
                        content=ft.Text("Dar de baja", color="#FFA726"),
                        height=40,
                        width=120,
                        style=ft.ButtonStyle(side=ft.BorderSide(1, "#FFA726")),
                        on_click=lambda e: cerrar_modal_detalles(e)
                    ),
                    ft.ElevatedButton(
                        content=ft.Text("Editar", color="white"),
                        bgcolor="#1E88E5",
                        height=40,
                        width=100,
                        on_click=lambda e: cerrar_modal_detalles(e)
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        ]
    )

    def cerrar_modal_detalles(e=None):
        dialogo_detalles.open = False
        page.update()

    def ver_detalles_seleccionado(e):
        id_seleccionado = None
        for row in tabla_empleados.rows:
            if row.selected:
                id_seleccionado = row.data
                break
        
        if id_seleccionado:
            todos = empleado_dao.obtener_todos()
            empleado_sel = next((emp for emp in todos if emp.empleado_id == id_seleccionado), None)
            
            if empleado_sel:
                lbl_det_nombre_encabezado.value = f"{empleado_sel.nombre} {empleado_sel.apellido_paterno}"
                lbl_det_rol.value = str(empleado_sel.rol or "Sin Rol")
                lbl_det_num_emp.value = f"EMP-{empleado_sel.empleado_id:03d}" if isinstance(empleado_sel.empleado_id, int) else str(empleado_sel.empleado_id)
                lbl_det_nombre_completo.value = f"{empleado_sel.nombre} {empleado_sel.apellido_paterno} {empleado_sel.apellido_materno}".strip()
                lbl_det_correo.value = empleado_sel.correo
                
                if dialogo_detalles not in page.overlay:
                    page.overlay.append(dialogo_detalles)
                dialogo_detalles.open = True
                page.update()
        else:
            print("Selecciona la casilla de un empleado primero.")

    # ----------------------------------------------------
    # ELIMINAR / DAR DE BAJA
    # ----------------------------------------------------
    def dar_baja_seleccionado(e):
        for row in tabla_empleados.rows:
            if row.selected and row.data:
                empleado_dao.eliminar(row.data)
        cargar_empleados()

    # ----------------------------------------------------
    # BARRA SUPERIOR DE BÚSQUEDA Y FILTROS
    # ----------------------------------------------------
    txt_buscar = ft.TextField(
        hint_text="Buscar Empleado",
        prefix_icon=ft.Icons.SEARCH,
        bgcolor="#1F2D40",
        border_radius=8,
        expand=True,
        height=45,
    )

    btn_nuevo = ft.ElevatedButton(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.ADD, color="white", size=18),
                ft.Text("Nuevo empleado", color="white", weight=ft.FontWeight.BOLD)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        bgcolor="#1E88E5",
        height=45,
        on_click=abrir_modal_nuevo
    )

    dropdown_filtro = ft.Dropdown(
        hint_text="Filtrar",
        width=200,
        bgcolor="#1F2D40",
        options=[
            ft.dropdown.Option("Encargado Almacén"),
            ft.dropdown.Option("Chofer"),
            ft.dropdown.Option("Operario trituración"),
        ],
    )

    btn_aplicar = ft.OutlinedButton(
        content=ft.Text("Aplicar", color="#FFA726"),
        height=40,
        style=ft.ButtonStyle(side=ft.BorderSide(1, "#FFA726"))
    )

    bar_busqueda = ft.Row(controls=[txt_buscar, btn_nuevo], spacing=15)
    bar_filtros = ft.Row(
        controls=[
            dropdown_filtro,
            btn_aplicar,
            ft.Container(expand=True),
            txt_contador
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    btn_baja = ft.OutlinedButton(
        content=ft.Text("Baja", color="#FFA726", weight=ft.FontWeight.BOLD),
        width=120,
        height=40,
        style=ft.ButtonStyle(side=ft.BorderSide(1, "#FFA726")),
        on_click=dar_baja_seleccionado
    )

    btn_detalles = ft.OutlinedButton(
        content=ft.Text("Ver detalles", color="white70"),
        width=130,
        height=40,
        style=ft.ButtonStyle(side=ft.BorderSide(1, "white30")),
        on_click=ver_detalles_seleccionado
    )

    acciones_inferiores = ft.Row(
        controls=[btn_baja, ft.Container(expand=True), btn_detalles],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    # ----------------------------------------------------
    # RENDER DE LA PANTALLA
    # ----------------------------------------------------
    contenido_principal = ft.Container(
        expand=True,
        padding=20,
        content=ft.Column(
            controls=[
                header,
                bar_busqueda,
                bar_filtros,
                ft.Container(
                    content=tabla_empleados,
                    bgcolor="#1A2634",
                    border_radius=8,
                    padding=10,
                    alignment=ft.Alignment(-1, -1)
                ),
                ft.Container(expand=True),
                acciones_inferiores
            ],
            spacing=15,
            scroll=ft.ScrollMode.AUTO
        )
    )

    page.add(
        ft.Row(
            controls=[sidebar, contenido_principal],
            expand=True,
            spacing=0
        )
    )

    cargar_empleados()


def cerrar_sesion(page: ft.Page):
    from ui.login_view import login_view
    page.clean()
    login_view(page)