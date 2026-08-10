from models.user import User
from utils.security import Security
import asyncio
import re
from ui.campos_login import *
from dao import *

import flet as ft

AERO_BG = "rgba(255,255,255,0.55)"
AERO_BORDER = ft.Border(
    top=ft.BorderSide(1, "rgba(255,255,255,0.35)"),
    left=ft.BorderSide(1, "rgba(255,255,255,0.35)"),
    right=ft.BorderSide(1, "rgba(0,0,0,0.25)"),
    bottom=ft.BorderSide(1, "rgba(0,0,0,0.25)")
)

# ── Roles identificables ──────────────────────────────────────────────────────
RUTAS_POR_ROL_EMPLEADO = {
    1: "/dashboard_admin",
    2: "/dashboard_chofer",
    3: "/dashboard_recepcion",
    4: "/dashboard_almacen",
    5: "/dashboard_trituradora",
    6: "/dashboard_distribucion",
}
def resolver_ruta_empleado(id_rol):
    return RUTAS_POR_ROL_EMPLEADO.get(id_rol)


RUTA_DASHBOARD_USUARIO = "ui.user.dashboard_user"
RUTA_DASHBOARD_VULCANIZADORA = "/dashboard_vulcanizadora"

def es_correo_valido(correo):
    patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(patron, correo) is not None


def login_view(page: ft.Page) -> ft.View:
    empleado_dao = EmpleadoDAO()
    user_dao = UserDAO()
    vulcanizadora_dao = VulcanizadoraDAO()


    current_tab = 0

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

        wrapper = ft.Container(
            content=toast,
            alignment=ft.Alignment(1, 1),
            padding=20
        )

        notification_layer.controls.append(wrapper)

        page.update()

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
            empleado = None

        if empleado is not None:
            page.empleado_id = empleado.empleado_id
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
            vulcanizadora = vulcanizadora_dao.verify_login(identificador, pwd)
        except Exception as ex:
            print("ERROR LOGIN VULCANIZADORA:", ex)
            vulcanizadora = None

        if vulcanizadora is not None:
            page.vulcanizadora_id = vulcanizadora.vulcanizadora_id

            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Bienvenido, {vulcanizadora.nombre}"),
                bgcolor=COLOR_AZUL_COBALTO
            )
            page.snack_bar.open = True
            page.update()

            await page.push_route(RUTA_DASHBOARD_VULCANIZADORA)
            return

        try:
            user = user_dao.verify_login(identificador, pwd)
        except Exception as ex:
            print("ERROR LOGIN USUARIO:", ex)
            user = None

        if user is not None:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Bienvenido, {user.name}"),
                bgcolor=COLOR_AZUL_COBALTO
            )
            page.snack_bar.open = True
            page.update()

            await page.push_route(RUTA_DASHBOARD_USUARIO)
            return




        # ── Por si no se identifica el campo ──────────────────────────────────────────────────────
        await mostrar_notificacion(
            "Usuario y contraseña incorrectos",
            "error"
        )
        return
    async def handle_reset(e):
        email = txt_reset_email.value
        if email:
            await mostrar_notificacion("Lo sentimos esta función aun no esta disponible")
            #await mostrar_notificacion(
            #    f"Solicitud enviada a: {email}",
            #    "success"
            #)
        else:
            await mostrar_notificacion("Ingrese su correo electrónico", "error")


    async def handle_register(e):

        if txt_reg_pass.value != txt_reg_confirm.value:
            await mostrar_notificacion(
                "Las contraseñas no coinciden.",
                "error"
            )
            return

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

        if not es_correo_valido(txt_reg_email.value):
            await mostrar_notificacion(
                "Ingrese un correo electrónico válido.",
                "error"
            )
            return

        try:

            password_hash = Security.hash_password(
                txt_reg_pass.value
            )

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

    async def handle_register_vulcanizadora(e):

        if txt_vul_pass.value != txt_vul_confirm.value:
            await mostrar_notificacion(
                "Las contraseñas no coinciden.",
                "error"
            )
            return

        campos = [
            txt_vul_nombre.value,
            txt_vul_telefono.value,
            txt_vul_correo.value,
            txt_vul_responsable.value,
            txt_vul_direccion.value,
            txt_vul_pass.value
        ]

        if any(c == "" for c in campos):
            await mostrar_notificacion(
                "Complete todos los campos obligatorios.",
                "error"
            )
            return

        if not es_correo_valido(txt_vul_correo.value):
            await mostrar_notificacion(
                "Ingrese un correo válido.",
                "error"
            )
            return

        try:

            nueva_vulcanizadora = VulcanizadoraDAO(
                nombre=txt_vul_nombre.value,
                telefono=txt_vul_telefono.value,
                correo=txt_vul_correo.value,
                responsable=txt_vul_responsable.value,
                direccion=txt_vul_direccion.value,
                activo=True,
                password_hash=txt_vul_pass.value
            )

            vulcanizadora_dao.insert(
                nueva_vulcanizadora
            )

            await mostrar_notificacion(
                "Vulcanizadora registrada correctamente.",
                "success"
            )

            txt_vul_nombre.value = ""
            txt_vul_telefono.value = ""
            txt_vul_correo.value = ""
            txt_vul_responsable.value = ""
            txt_vul_direccion.value = ""
            txt_vul_pass.value = ""
            txt_vul_confirm.value = ""

            page.update()

            switch_tab(0)

        except Exception as ex:

            print("ERROR REGISTRO VULCANIZADORA:", ex)

            await mostrar_notificacion(
                "Error al registrar vulcanizadora.",
                "error"
            )

    def actualizar_tabs(tab_index):
        color_inactivo = "#94A3B8"
        fondo_inactivo = "transparent"

        # ── Colores de cada sección ─────────────────────────────
        color_ingresar = COLOR_AZUL_COBALTO
        color_restablecer = COLOR_NARANJA_AMBAR
        color_registrarse = COLOR_AZUL_CIELO_INTENSO

        fondo_ingresar = "rgba(37, 99, 235, 0.18)"
        fondo_restablecer = "rgba(245, 158, 11, 0.18)"
        fondo_registrarse = "rgba(56, 189, 248, 0.18)"

        # ── Ingresar ────────────────────────────────────────────
        btn_tab_ingresar.style = ft.ButtonStyle(
            color={
                "": color_ingresar if tab_index == 0 else color_inactivo,
                "hovered": color_ingresar
            },
            bgcolor={
                "": fondo_ingresar if tab_index == 0 else fondo_inactivo,
                "hovered": "rgba(37, 99, 235, 0.12)"
            },
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=ft.Padding(15, 8, 15, 8)
        )

        # ── Restablecer ─────────────────────────────────────────
        btn_tab_restablecer.style = ft.ButtonStyle(
            color={
                "": color_restablecer if tab_index == 1 else color_inactivo,
                "hovered": color_restablecer
            },
            bgcolor={
                "": fondo_restablecer if tab_index == 1 else fondo_inactivo,
                "hovered": "rgba(245, 158, 11, 0.12)"
            },
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=ft.Padding(15, 8, 15, 8)
        )

        # ── Registrarse ─────────────────────────────────────────
        btn_tab_registrar.style = ft.ButtonStyle(
            color={
                "": color_registrarse if tab_index in (2, 3) else color_inactivo,
                "hovered": color_registrarse
            },
            bgcolor={
                "": fondo_registrarse if tab_index in (2, 3) else fondo_inactivo,
                "hovered": "rgba(56, 189, 248, 0.12)"
            },
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=ft.Padding(15, 8, 15, 8)
        )

    def switch_tab(tab_index):
        nonlocal current_tab
        current_tab = tab_index

        identificadores = {
            0: "login",
            1: "restablecer",
            2: "registro",
            3: "registro_vulcanizadora"
        }

        page.login_section = identificadores.get (
            tab_index,
            "desconocido"
        )

        actualizar_tabs(tab_index)

        form_container.controls.clear()
        # ── Login ──────────────────────────────────────────────────────
        if tab_index == 0:
            title_text.value = "Acceso al sistema Neusomic"
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
                                        content=ft.Text("Iniciar sesión", size=14, weight=ft.FontWeight.BOLD, color=COLOR_BLANCO),
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
                        alignment=ft.MainAxisAlignment.END,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    alignment=ft.Alignment(0, 1)
                ),
            ])
        # ── Restablecer ──────────────────────────────────────────────────────
        elif tab_index == 1:
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
        # ── Registrar ──────────────────────────────────────────────────────
        elif tab_index == 2:
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
                                    ),
                                    ft.TextButton(
                                        content=ft.Text(
                                            "¿Registrar una vulcanizadora?",
                                            size=12,
                                            color=COLOR_NARANJA_AMBAR
                                        ),
                                        on_click=lambda _: switch_tab(3)
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

        elif tab_index == 3:

            title_text.value = "Registro vulcanizadora"

            form_container.controls.extend([

                txt_vul_nombre,
                txt_vul_telefono,
                txt_vul_correo,
                txt_vul_responsable,
                txt_vul_direccion,
                txt_vul_pass,
                txt_vul_confirm,

                ft.Row(
                    controls=[
                        ft.Button(
                            content=ft.Text(
                                "Registrar vulcanizadora",
                                color=COLOR_BLANCO
                            ),
                            style=ft.ButtonStyle(
                                bgcolor={
                                    "": COLOR_AZUL_MEDIO,
                                    "hovered": COLOR_AZUL_COBALTO
                                }
                            ),
                            on_click=handle_register_vulcanizadora
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),

                ft.TextButton(
                    content=ft.Text(
                        "Registrar usuario normal",
                        size=12,
                        color=COLOR_NARANJA_AMBAR
                    ),
                    on_click=lambda _: switch_tab(2)
                )

            ])

        page.update()

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

    glass_card = ft.Container(
        key="login",
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
        padding=20,
        width=400,
        height=400,
        alignment=ft.Alignment.CENTER,
        shadow=ft.BoxShadow(
            blur_radius=15,
            spread_radius=1,
            color="rgba(0,0,0,0.5)",
            offset=ft.Offset(0, 6)
        )
    )

    center_body = ft.Container(
        content=ft.Column(
            controls=[glass_card],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        expand=True,
        bgcolor=COLOR_AZUL_CIELO_INTENSO,
        alignment=ft.Alignment.CENTER,
        padding=20
    )

    # Header
    header = ft.Container(
        content=ft.Row([
            ft.Container(
                content=ft.Image(
                    src="assets/images/logo.png",
                    height=90,
                    fit=ft.BoxFit.CONTAIN
                ),
                expand=True,
                alignment=ft.Alignment(-1, 0)
            )
        ]),
        bgcolor=COLOR_AZUL_OXFORD,
        padding=ft.Padding(left=20, top=12, right=20, bottom=12),
        width=page.width,
        height=90
    )

    # ── Footer ──────────────────────────────────────────────────────
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