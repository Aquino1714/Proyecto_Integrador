import flet as ft


def login_view(page: ft.Page):

    page.title = "Neusomic"
    page.window_width = 1200
    page.window_height = 700
    page.bgcolor = "#091B3D"
    page.padding = 0

    # ------------------------
    # Barra superior
    # ------------------------

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

    # ------------------------
    # Título
    # ------------------------

    titulo = ft.Text(
        "Acceso Neusomic",
        size=24,
        weight=ft.FontWeight.BOLD,
        color="white"
    )

    # ------------------------
    # Pestañas
    # ------------------------

    pestañas = ft.Row(
        controls=[
            ft.Text("Ingresar", color="#4EA8FF"),
            ft.Text("Restablecer", color="white70"),
            ft.Text("Registrarse", color="white70"),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=30,
    )

    # ------------------------
    # Campos
    # ------------------------

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

    # ------------------------
    # Botón
    # ------------------------

    boton = ft.ElevatedButton(
        text="Iniciar sesión",
        width=330,
        height=45,
        bgcolor="#1E88E5",
        color="white"
    )

    # ------------------------
    # Tarjeta
    # ------------------------

    card = ft.Container(
        width=420,
        bgcolor="#2D3E50",
        border_radius=10,
        padding=30,
        content=ft.Column(
            controls=[
                titulo,
                pestañas,
                ft.Divider(),
                txt_usuario,
                txt_password,
                boton,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
    )

    # ------------------------
    # Footer
    # ------------------------

    footer = ft.Container(
        bgcolor="#0B2D63",
        height=55,
        alignment=ft.alignment.center,
        content=ft.Text(
            "© 2026 Neusomic Inc. Todos los derechos reservados.",
            color="white70",
        ),
    )

    # ------------------------
    # Página
    # ------------------------

    page.add(
        ft.Column(
            controls=[
                header,
                ft.Container(
                    expand=True,
                    alignment=ft.alignment.center,
                    content=card,
                ),
                footer,
            ],
            expand=True,
            spacing=0,
        )
    )