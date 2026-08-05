import flet as ft


def login_view(page: ft.Page):

    page.title = "Neusomic"
    page.window_width = 1200
    page.window_height = 800
    page.bgcolor = "#091B3D"
    page.padding = 0

    # ----------------------------------------------------
    # Barra superior (Header)
    # ----------------------------------------------------
    header = ft.Container(
        bgcolor="#1E5BB8",
        height=70,
        padding=20,
        content=ft.Row(
            controls=[
                ft.Text(
                    "NEUSOMIC",
                    color="white",
                    size=28,
                    weight=ft.FontWeight.BOLD
                )
            ]
        )
    )

    # ----------------------------------------------------
    # Título dinámico de la Tarjeta
    # ----------------------------------------------------
    titulo = ft.Text(
        "Acceso Neusomic",
        size=24,
        weight=ft.FontWeight.BOLD,
        color="white"
    )

    # ----------------------------------------------------
    # EVENTO: Iniciar sesión / Navegar a Dashboard
    # ----------------------------------------------------
    def iniciar_sesion_click(e):
        # Importación local para evitar importación circular
        from ui.admin_view import admin_view
        
        # Aquí puedes agregar tus validaciones DAO con los campos:
        # usuario = txt_usuario.value
        # password = txt_password.value
        
        page.clean()
        admin_view(page)

    # ----------------------------------------------------
    # VISTAS (Formularios para cada pestaña)
    # ----------------------------------------------------

    # 1. Formulario de INGRESAR
    txt_usuario = ft.TextField(
        label="Usuario",
        width=330,
        prefix_icon=ft.Icons.PERSON,
    )
    txt_password = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        width=330,
        prefix_icon=ft.Icons.LOCK,
    )
    btn_ingresar = ft.ElevatedButton(
        content=ft.Text("Iniciar sesión", color="white", weight=ft.FontWeight.BOLD),
        width=330,
        height=45,
        bgcolor="#1E88E5",
        on_click=iniciar_sesion_click  # <--- Evento vinculado aquí
    )
    view_ingresar = [txt_usuario, txt_password, btn_ingresar]

    # 2. Formulario de RESTABLECER
    txt_correo_rest = ft.TextField(
        label="Correo electrónico",
        hint_text="usuario@neusomic.com",
        width=330,
        prefix_icon=ft.Icons.EMAIL,
    )
    btn_restablecer = ft.OutlinedButton(
        content=ft.Text("Restablecer contraseña", color="#FFA726", weight=ft.FontWeight.BOLD),
        width=330,
        height=45,
        style=ft.ButtonStyle(
            side=ft.BorderSide(1, "#FFA726")
        )
    )
    view_restablecer = [txt_correo_rest, btn_restablecer]

    # 3. Formulario de REGISTRARSE
    txt_nombres = ft.TextField(
        label="Nombres",
        hint_text="Nombre",
        width=330,
        prefix_icon=ft.Icons.PERSON
    )
    txt_app_paterno = ft.TextField(
        label="Apellido paterno",
        hint_text="Apellido paterno",
        width=330,
        prefix_icon=ft.Icons.PERSON
    )
    txt_app_materno = ft.TextField(
        label="Apellido materno",
        hint_text="Apellido materno",
        width=330,
        prefix_icon=ft.Icons.PERSON
    )
    txt_reg_correo = ft.TextField(
        label="Correo electrónico",
        hint_text="ejemplo01@neusomic.com",
        width=330,
        prefix_icon=ft.Icons.EMAIL
    )
    txt_reg_pass = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        width=330,
        prefix_icon=ft.Icons.LOCK
    )
    txt_confirm_pass = ft.TextField(
        label="Confirmar contraseña",
        password=True,
        can_reveal_password=True,
        width=330,
        prefix_icon=ft.Icons.LOCK
    )
    btn_registrarse = ft.ElevatedButton(
        content=ft.Text("Registrarse", color="white", weight=ft.FontWeight.BOLD),
        width=200,
        height=45,
        bgcolor="#1E88E5",
    )

    view_registrarse = [
        txt_nombres,
        txt_app_paterno,
        txt_app_materno,
        txt_reg_correo,
        txt_reg_pass,
        txt_confirm_pass,
        btn_registrarse
    ]

    # ----------------------------------------------------
    # Contenedor dinámico del formulario activo
    # ----------------------------------------------------
    form_container = ft.Column(
        controls=view_ingresar,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15,
    )

    # ----------------------------------------------------
    # Lógica de cambio de pestañas
    # ----------------------------------------------------
    def cambiar_pestana(e, opcion):
        tab_ingresar.color = "white70"
        tab_restablecer.color = "white70"
        tab_registrarse.color = "white70"

        if opcion == "ingresar":
            tab_ingresar.color = "#4EA8FF"
            titulo.value = "Acceso Neusomic"
            form_container.controls = view_ingresar
        elif opcion == "restablecer":
            tab_restablecer.color = "#FFA726"
            titulo.value = "Restablecer Neusomic"
            form_container.controls = view_restablecer
        elif opcion == "registrarse":
            tab_registrarse.color = "#4EA8FF"
            titulo.value = "Registro Neusomic"
            form_container.controls = view_registrarse

        page.update()

    # Controles de las Pestañas
    tab_ingresar = ft.Text("Ingresar", color="#4EA8FF", weight=ft.FontWeight.BOLD)
    tab_restablecer = ft.Text("Restablecer", color="white70", weight=ft.FontWeight.BOLD)
    tab_registrarse = ft.Text("Registrarse", color="white70", weight=ft.FontWeight.BOLD)

    pestañas = ft.Row(
        controls=[
            ft.Container(content=tab_ingresar, on_click=lambda e: cambiar_pestana(e, "ingresar"), ink=True),
            ft.Container(content=tab_restablecer, on_click=lambda e: cambiar_pestana(e, "restablecer"), ink=True),
            ft.Container(content=tab_registrarse, on_click=lambda e: cambiar_pestana(e, "registrarse"), ink=True),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=25,
    )

    # ----------------------------------------------------
    # Tarjeta Principal (Card)
    # ----------------------------------------------------
    card = ft.Container(
        width=450,
        bgcolor="#2D3E50",
        border_radius=10,
        padding=30,
        content=ft.Column(
            controls=[
                titulo,
                pestañas,
                ft.Divider(),
                form_container,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
        ),
    )

    # ----------------------------------------------------
    # Footer
    # ----------------------------------------------------
    footer = ft.Container(
        bgcolor="#0B2D63",
        height=55,
        alignment=ft.Alignment(0, 0),
        content=ft.Text(
            "© 2026 Neusomic Inc. Todos los derechos reservados.",
            color="white70",
        ),
    )

    # ----------------------------------------------------
    # Estructura Principal de la Página
    # ----------------------------------------------------
    page.add(
        ft.Column(
            controls=[
                header,
                ft.Container(
                    expand=True,
                    alignment=ft.Alignment(0, 0),
                    content=card,
                    padding=20,
                ),
                footer,
            ],
            expand=True,
            spacing=0,
        )
    )