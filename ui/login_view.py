from dao.user_dao import UserDAO
from models.user import User
from dao.empleado_dao import EmpleadoDAO
import hashlib
import asyncio


import flet as ft


COLOR_AZUL_OXFORD = "#001F4E"
COLOR_AZUL_COBALTO = "#0A2F8F"
COLOR_AZUL_MEDIO = "#1E88E5"
COLOR_NARANJA_AMBAR = "#FC8F1B"
COLOR_GRIS_OSCURO = "#333333"
COLOR_BLANCO = "#FFFFFF"
COLOR_AZUL_CIELO_INTENSO = "#E0FFFF"

AERO_BG = "rgba(255,255,255,0.55)"
AERO_BORDER = ft.Border(
    top=ft.BorderSide(1, "rgba(255,255,255,0.35)"),
    left=ft.BorderSide(1, "rgba(255,255,255,0.35)"),
    right=ft.BorderSide(1, "rgba(0,0,0,0.25)"),
    bottom=ft.BorderSide(1, "rgba(0,0,0,0.25)")
)

#Roles identificador
RUTAS_POR_ROL_EMPLEADO = {
    1: "/dashboard_admin",
    2: "/dashboard_chofer",
    3: "/dashboard_recepcion",
    4: "/dashboard_almacen",
    5: "/dashboard_trituracion",
    6: "/dashboard_distribucion",
}
def resolver_ruta_empleado(id_rol):
    return RUTAS_POR_ROL_EMPLEADO.get(id_rol)


RUTA_DASHBOARD_USUARIO = "ui.user.dashboard_user"

def login_view(page: ft.Page) -> ft.View:
    empleado_dao = EmpleadoDAO()
    user_dao = UserDAO()


    current_tab = 0

    # ------------------------------------------
    # COMPONENTES REUTILIZABLES
    # ------------------------------------------
    def build_textfield(label: str, hint: str, icon: str, is_password: bool = False):
        return ft.TextField(
            label=label,
            hint_text=hint,
            prefix_icon=icon,
            password=is_password,
            can_reveal_password=is_password,
            text_size=14,
            label_style=ft.TextStyle(color="#CBD5E1", size=13),
            hint_style=ft.TextStyle(color="#64748B", size=13),
            border_color="rgba(255,255,255,0.2)",
            focused_border_color=COLOR_AZUL_CIELO_INTENSO,
            bgcolor="rgba(15,23,42,0.5)",
            border_radius=8,
            cursor_color=COLOR_AZUL_CIELO_INTENSO,
            color=COLOR_BLANCO,
            dense=True,
            expand=True
        )

    # Campos Login
    txt_login_user = build_textfield("Usuario", "usuario01@example.com", ft.Icons.PERSON_OUTLINED)
    txt_login_pass = build_textfield("Contraseña", "********", ft.Icons.LOCK_OUTLINED, is_password=True)

    # Campos Restablecer
    txt_reset_email = build_textfield("Correo electrónico", "usuario@neusomic.com", ft.Icons.EMAIL_OUTLINED)

    # Campos Registro
    txt_reg_nombre = build_textfield("Nombres", "Nombre", ft.Icons.PERSON_OUTLINE)
    txt_reg_paterno = build_textfield("Apellido paterno", "Apellido paterno", ft.Icons.PERSON_OUTLINE)
    txt_reg_materno = build_textfield("Apellido materno", "Apellido materno", ft.Icons.PERSON_OUTLINE)
    txt_reg_user = build_textfield("User name", "ejemplo01", ft.Icons.ACCOUNT_CIRCLE_OUTLINED)
    txt_reg_phone = build_textfield("Teléfono","2221234567",ft.Icons.PHONE_OUTLINED)
    txt_reg_email = build_textfield("Correo","usuario@correo.com",ft.Icons.EMAIL_OUTLINED)

    txt_reg_pass = build_textfield("Contraseña", "********", ft.Icons.LOCK_OUTLINED, is_password=True)
    txt_reg_confirm = build_textfield("Confirmar contraseña", "********", ft.Icons.LOCK_OUTLINED, is_password=True)

    form_container = ft.Column(spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    title_text = ft.Text(size=24, weight=ft.FontWeight.BOLD, color=COLOR_BLANCO, text_align=ft.TextAlign.CENTER)
    # ------------------------------------------
    # NOTIFICACIONES FLOTANTES FLET 0.86.2
    # ------------------------------------------

    notification_layer = ft.Stack(
        controls=[],
        expand=True
    )

    async def mostrar_notificacion(mensaje, tipo="normal"):

        if tipo == "error":
            bgcolor = "#B91C1C"
            icon = ft.Icons.ERROR


        elif tipo == "warning":
            bgcolor = COLOR_NARANJA_AMBAR
            icon = ft.Icons.WARNING_AMBER_ROUNDED

        else:
            bgcolor = "#111111"
            icon = ft.Icons.INFO_OUTLINE

        toast = ft.Container(
            width=350,
            padding=15,
            bgcolor=bgcolor,
            border_radius=12,

            opacity=0,
            offset=ft.Offset(0, 0.5),

            shadow=ft.BoxShadow(
                blur_radius=18,
                spread_radius=2,
                color="#55000000",
                offset=ft.Offset(0, 5)
            ),

            animate_opacity=300,
            animate_offset=300,

            content=ft.Row(
                controls=[
                    ft.Icon(
                        icon,
                        color="white",
                        size=28
                    ),

                    ft.Text(
                        mensaje,
                        color="white",
                        size=14,
                        expand=True
                    )
                ]
            )
        )

        # Posición inferior derecha
        wrapper = ft.Container(
            content=toast,
            alignment=ft.Alignment(1, 1),
            padding=20
        )

        notification_layer.controls.append(wrapper)

        page.update()

        # Entrada animada
        toast.opacity = 1
        toast.offset = ft.Offset(0, 0)

        page.update()

        toast.opacity = 1
        toast.offset = ft.Offset(0, 0)
        page.update()

        await asyncio.sleep(3)

        toast.opacity = 0
        toast.offset = ft.Offset(0, 0.5)
        page.update()

        await asyncio.sleep(0.35)

        notification_layer.controls.remove(wrapper)
        page.update()

    # ------------------------------------------
    # EVENTOS
    # ------------------------------------------
    async def handle_login(e):
        identificador = txt_login_user.value
        pwd = txt_login_pass.value
        if not identificador or not pwd:
            await mostrar_notificacion(
                "Porfavor complete todos los campos",
                "error"
            )
            return
        try:
            empleado = empleado_dao.verify_login(identificador, pwd)
        except Exception as ex:
            print("ERROR LOGIN EMPLEADO:", ex)

            page.snack_bar = ft.SnackBar(
                content=ft.Text(str(ex)),
                bgcolor="#B81D24"
            )
            page.snack_bar.open = True
            page.update()
            return

        if empleado is not None:
            ruta_destino = resolver_ruta_empleado(empleado.id_rol)
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Bienvenido, {empleado.name}"),
                bgcolor="#B81D24"
            )
            page.snack_bar.open = True
            page.update()

            await page.push_route(ruta_destino)
            return

        try:
            user = user_dao.verify_login(identificador, pwd)
        except Exception as ex:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error: {ex}"),
                bgcolor="#B81D24"
            )
            page.snack_bar.open = True
            page.update()
            return

        if user is not None:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Bienvenido, {user.name}"),
                bgcolor=COLOR_AZUL_COBALTO
            )
            page.snack_bar.open = True
            page.update()

            await page.push_route(RUTA_DASHBOARD_USUARIO)
            return

        #Por si alguno de los dos no funciona
        await mostrar_notificacion(
            "Usuario o contraseña incorrectos",
            "error"
        )
    def handle_reset(e):
        email = txt_reset_email.value
        if email:
            page.open(ft.SnackBar(ft.Text(f"Solicitud enviada a: {email}"), bgcolor=COLOR_AZUL_MEDIO))
        else:
            page.open(ft.SnackBar(ft.Text("Ingrese su correo electrónico"), bgcolor="#B81D24"))

    async def handle_register(e):

        if txt_reg_pass.value != txt_reg_confirm.value:
            await mostrar_notificacion(
                "Las contraseñas no coinciden.",
                "error"
            )

        if (
                txt_reg_nombre.value == "" or
                txt_reg_paterno.value == "" or
                txt_reg_user.value == "" or
                txt_reg_email.value == ""
        ):
            await mostrar_notificacion(
                "Complete todos los campos obligatorios.",
                "error"
            )
            return

        try:

            password_hash = hashlib.sha256(
                txt_reg_pass.value.encode()
            ).hexdigest()

            nuevo_usuario = User(
                username=txt_reg_user.value,
                password_hash=password_hash,
                name=txt_reg_nombre.value,
                aPaterno=txt_reg_paterno.value,
                aMaterno=txt_reg_materno.value,
                phone=txt_reg_phone.value,
                email=txt_reg_email.value
            )

            dao = UserDAO()
            dao.insert(nuevo_usuario)

            await mostrar_notificacion(
                "Usuario registrado correctamente.",
                "success"
            )

            txt_reg_nombre.value = ""
            txt_reg_paterno.value = ""
            txt_reg_materno.value = ""
            txt_reg_user.value = ""
            txt_reg_phone.value = ""
            txt_reg_email.value = ""
            txt_reg_pass.value = ""
            txt_reg_confirm.value = ""

            page.update()

            switch_tab(0)

        except Exception as ex:

            await mostrar_notificacion(
                "Hubo un error al registrarse.",
                "error"
            )

    # ------------------------------------------
    # NAVEGACIÓN
    # ------------------------------------------
    def switch_tab(tab_index):
        nonlocal current_tab
        current_tab = tab_index
        form_container.controls.clear()

        if tab_index == 0:  # LOGIN
            title_text.value = "Acceso Neusomic"
            form_container.controls.extend([
                txt_login_user,
                txt_login_pass,
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(height=5),
                            ft.Row(
                                controls=[
                                    ft.Button(
                                        content=ft.Text("Iniciar sesión", size=14, weight=ft.FontWeight.BOLD,
                                                        color=COLOR_BLANCO),
                                        style=ft.ButtonStyle(
                                            bgcolor={"": COLOR_AZUL_COBALTO, "hovered": COLOR_AZUL_MEDIO},
                                            shape=ft.RoundedRectangleBorder(radius=6),
                                            padding=ft.Padding(24, 12, 24, 12)
                                        ),
                                        on_click=handle_login
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            ft.TextButton(
                                content=ft.Text("¿Olvidaste tu contraseña?", size=12, color=COLOR_NARANJA_AMBAR),
                                on_click=lambda _: switch_tab(1)
                            )
                        ],
                        alignment=ft.MainAxisAlignment.END,  # fuerza todo hacia abajo
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    alignment=ft.Alignment(0, 1)  # abajo y centrado
                ),
            ])
        elif tab_index == 1:  # RESTABLECER
            title_text.value = "Acceso Neusomic"
            form_container.controls.extend([
                txt_reset_email,
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(height=10),
                            ft.Row(
                                controls=[
                                    ft.OutlinedButton(
                                        content=ft.Text("Restablecer contraseña", size=14, color=COLOR_NARANJA_AMBAR),
                                        style=ft.ButtonStyle(
                                            side={"": ft.BorderSide(1, COLOR_NARANJA_AMBAR)},
                                            shape=ft.RoundedRectangleBorder(radius=6),
                                            padding=ft.Padding(20, 12, 20, 12)
                                        ),
                                        on_click=handle_reset
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            )
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    alignment=ft.Alignment(0, 1)
                )
            ])
        elif tab_index == 2:  # REGISTRO
            title_text.value = "Registro usuario"
            form_container.controls.extend([
                ft.Container(
                    content=ft.Column(
                        controls=[
                            txt_reg_nombre,
                            txt_reg_paterno,
                            txt_reg_materno,
                            txt_reg_user,
                            txt_reg_phone,
                            txt_reg_email,
                            txt_reg_pass,
                            txt_reg_confirm,
                            ft.Container(height=5),
                            ft.Row(
                                controls=[
                                    ft.Button(
                                        content=ft.Text("Registrarse", size=14, weight=ft.FontWeight.BOLD,
                                                        color=COLOR_BLANCO),
                                        style=ft.ButtonStyle(
                                            bgcolor={"": COLOR_AZUL_MEDIO, "hovered": COLOR_AZUL_COBALTO},
                                            shape=ft.RoundedRectangleBorder(radius=6),
                                            padding=ft.Padding(30, 12, 30, 12)
                                        ),
                                        on_click=handle_register
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            )
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    alignment=ft.Alignment(0, 1)
                )
            ])
        page.update()

    # Tabs
    btn_tab_ingresar = ft.TextButton("Ingresar", on_click=lambda _: switch_tab(0))
    btn_tab_restablecer = ft.TextButton("Restablecer", on_click=lambda _: switch_tab(1))
    btn_tab_registrar = ft.TextButton("Registrarse", on_click=lambda _: switch_tab(2))

    tabs_header = ft.Column([
        ft.Row(
            controls=[btn_tab_ingresar, btn_tab_restablecer, btn_tab_registrar],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY
        ),
        ft.Divider(height=1, color="rgba(255,255,255,0.2)")
    ], spacing=0)

    # TARJETA PRINCIPAL (MICA BLUR)
    # TARJETA PRINCIPAL (MUY PEQUEÑA)
    glass_card = ft.Container(
        content=ft.Column(
            controls=[
                title_text,
                ft.Container(height=10),
                tabs_header,
                ft.Container(height=10),
                ft.Container(
                    content=ft.Column(
                        controls=form_container.controls,
                        scroll=ft.ScrollMode.AUTO,
                        expand=True
                    ),
                    expand=True
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            tight=True,
            expand=True
        ),
        bgcolor="#1A1A1A",
        border=AERO_BORDER,
        border_radius=18,
        padding=20,  # menos padding para que se vea compacto
        width=400,  # ancho fijo
        height=400,  # alto fijo
        alignment=ft.Alignment.CENTER,
        shadow=ft.BoxShadow(
            blur_radius=15,
            spread_radius=1,
            color="rgba(0,0,0,0.5)",
            offset=ft.Offset(0, 6)
        )
    )

    # FONDO SIN DEGRADADO (color sólido)
    center_body = ft.Container(
        content=ft.Column(
            controls=[glass_card],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        expand=True,
        bgcolor=COLOR_AZUL_CIELO_INTENSO,  # fondo sólido en lugar de degradado
        alignment=ft.Alignment.CENTER,
        padding=20
    )

    # Header
    header = ft.Container(
        content=ft.Row([
            ft.Container(
                content=ft.Image(
                    src="assets/images/logo.png",
                    height=90,  # tamaño más grande del logo
                    fit=ft.BoxFit.CONTAIN
                ),
                expand=True,  # hace que el logo se adapte al ancho disponible
                alignment=ft.Alignment(-1, 0)
            )
        ]),
        bgcolor=COLOR_AZUL_OXFORD,
        padding=ft.Padding(left=20, top=12, right=20, bottom=12),
        width=page.width,
        height=90  # altura fija de la barra (no cambia aunque el logo sea más grande)
    )

    # Footer
    footer = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Column([
                    ft.Image(src="assets/images/logo.png", height=25, fit=ft.BoxFit.CONTAIN),
                    ft.Text(
                        "Solución logística e industrial para la gestión de pavimento asfáltico\n"
                        "ecológico a partir de mermas de neumáticos de desecho.",
                        size=10, color="#94A3B8"
                    )
                ], spacing=5, expand=True),
                ft.Column([
                    ft.Text("Contacto Técnico", size=11, weight=ft.FontWeight.BOLD, color="#94A3B8"),
                    ft.Text("Planta Trituradora Central: Zona Industrial Norte, Bodega 4.", size=10, color="#64748B")
                ], alignment=ft.MainAxisAlignment.END)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(height=10, color="rgba(255,255,255,0.1)"),
            ft.Text("© 2026 Neusomic Inc. Todos los derechos reservados.",
                    size=11, color="#64748B", text_align=ft.TextAlign.CENTER)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor="#020817",
        padding=15
    )

    # Zona Central con degradado sólido
    center_body = ft.Container(
        content=ft.Column(
            controls=[glass_card],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(0, -1),
            end=ft.Alignment(0, 1),
            colors=[COLOR_AZUL_COBALTO, COLOR_AZUL_MEDIO]  # degradado sólido
        ),
        alignment=ft.Alignment.CENTER,
        padding=20
    )

    # Layout final responsive
    switch_tab(0)

    return ft.View(
        route="/",
        controls=[
            ft.Stack(
                expand=True,
                controls=[

                    ft.Column(
                        controls=[
                            header,
                            center_body,
                            footer
                        ],
                        expand=True,
                        spacing=0
                    ),

                    notification_layer

                ]
            )
        ],
        padding=0
    )

    # Vista por defecto
    #switch_tab(0)


#ft.run(main)
