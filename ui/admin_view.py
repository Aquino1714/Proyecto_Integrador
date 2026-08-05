import flet as ft


def admin_view(page: ft.Page):
    page.title = "Neusomic - Dashboard"
    page.bgcolor = "#091B3D"
    page.padding = 0

    # ----------------------------------------------------
    # Función de navegación entre vistas
    # ----------------------------------------------------
    def navegar(e, vista):
        page.clean()
        if vista == "dashboard":
            admin_view(page)
        elif vista == "empleados":
            from ui.empleados_view import empleados_view
            empleados_view(page)

    # ----------------------------------------------------
    # 1. Sidebar (Menú Lateral Izquierdo)
    # ----------------------------------------------------
    sidebar = ft.Container(
        width=240,
        bgcolor="#0B1A30",
        padding=15,
        content=ft.Column(
            controls=[
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.DASHBOARD_OUTLINED, color="#FFA726"),
                    title=ft.Text("Dashboard", color="#FFA726", weight=ft.FontWeight.BOLD),
                    on_click=lambda e: navegar(e, "dashboard")
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.PEOPLE_ALT_OUTLINED, color="white70"),
                    title=ft.Text("Empleados", color="white70"),
                    on_click=lambda e: navegar(e, "empleados")  # <--- Evento vinculado correctamente
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

    # ----------------------------------------------------
    # 2. Header Superior del Dashboard
    # ----------------------------------------------------
    header_dashboard = ft.Container(
        height=65,
        bgcolor="#1E5BB8",
        padding=20,
        content=ft.Row(
            controls=[
                ft.Text("Dashboard", color="white", size=24, weight=ft.FontWeight.BOLD),
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
    # 3. Tarjetas KPI
    # ----------------------------------------------------
    def crear_kpi(titulo, valor, subtitulo, color_sub="#4CAF50"):
        return ft.Container(
            bgcolor="#2D3E50",
            border_radius=8,
            padding=15,
            expand=True,
            content=ft.Column(
                controls=[
                    ft.Text(titulo, color="white70", size=12),
                    ft.Text(valor, color="white", size=22, weight=ft.FontWeight.BOLD),
                    ft.Text(subtitulo, color=color_sub, size=11),
                ],
                spacing=5
            )
        )

    kpis = ft.Row(
        controls=[
            crear_kpi("Ingreso de neumáticos (mes)", "4,850 Pzas", "▲ +12% vs mes anterior"),
            crear_kpi("Pedidos de constructoras", "32 solicitudes", "Activas", color_sub="#FFA726"),
            crear_kpi("Volumen pavimento hecho", "28,400 Kg", "Procesado", color_sub="#2196F3"),
            crear_kpi("Bajas de productos", "18 Pzas", "Justificado por daño", color_sub="#EF5350"),
        ],
        spacing=15
    )

    # ----------------------------------------------------
    # 4. Áreas de Gráficas y Monitoreo
    # ----------------------------------------------------
    panel_graficas = ft.Row(
        controls=[
            ft.Container(
                bgcolor="#2D3E50",
                border_radius=8,
                padding=15,
                expand=True,
                content=ft.Column(
                    controls=[
                        ft.Text("Ingresos y despachos de neumáticos / volumen", color="white", weight=ft.FontWeight.BOLD),
                        ft.Container(
                            height=180,
                            bgcolor="#1A2634",
                            border_radius=5,
                            alignment=ft.Alignment(0, 0),
                            content=ft.Text("Gráfica de Barras", color="white54")
                        )
                    ]
                )
            ),
            ft.Container(
                bgcolor="#2D3E50",
                border_radius=8,
                padding=15,
                expand=True,
                content=ft.Column(
                    controls=[
                        ft.Text("Historial de Recolección por Transporte", color="white", weight=ft.FontWeight.BOLD),
                        ft.Container(
                            height=180,
                            bgcolor="#1A2634",
                            border_radius=5,
                            alignment=ft.Alignment(0, 0),
                            content=ft.Text("Gráfica Pastel", color="white54")
                        )
                    ]
                )
            )
        ],
        spacing=15
    )

    contenido_principal = ft.Container(
        expand=True,
        padding=20,
        content=ft.Column(
            controls=[
                header_dashboard,
                kpis,
                panel_graficas,
            ],
            spacing=20,
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


def cerrar_sesion(page: ft.Page):
    from ui.login_view import login_view
    page.clean()
    login_view(page)