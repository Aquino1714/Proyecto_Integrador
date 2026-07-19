import flet as ft

# ---------- PALETA ----------
AZUL = "#1E6FD9"
AZUL_OSCURO = "#1550A0"
NARANJA = "#FF9800"
NARANJA_OSCURO = "#C96E00"
AZUL_CLARO = "#5AA9FF"
AZUL_CLARO_OSCURO = "#2D7FE0"

# Fondo claro, azulado, como en la imagen de referencia
BG_CLARO = "#EAF1FF"
NAVBAR_BG = "#1550A0"
FOOTER_BG = "#0B1B3A"

VIDRIO = ft.Colors.with_opacity(0.55, ft.Colors.WHITE)
BORDER_VIDRIO = ft.Colors.with_opacity(0.6, ft.Colors.WHITE)
VIDRIO_CAMPO = ft.Colors.with_opacity(0.35, ft.Colors.WHITE)
BORDER_CAMPO = ft.Colors.with_opacity(0.5, AZUL)

# Ancho de tarjeta: mínimo y máximo para el cálculo responsive
TARJETA_MIN = 300
TARJETA_MAX = 420


def main(page: ft.Page):
    page.title = "Neusomic - Acceso"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = BG_CLARO
    page.padding = 0
    page.window.width = 1100
    page.window.height = 750
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    tab_activa = ["ingresar"]
    panel_formulario = ft.Container()

    # ---------- COMPONENTES REUTILIZABLES ----------
    def campo_glass(icon, etiqueta, password=False):
        # Campo con floating label NATIVO de Material (label + border OUTLINE):
        # Flutter anima y alinea el label automáticamente -- incluye el "corte"
        # en el borde que se ve en la referencia -- sin necesidad de un Stack
        # manual (que era la causa de los íconos desfasados y el texto fijo).
        return ft.Container(
            bgcolor=VIDRIO_CAMPO,
            border_radius=12,
            margin=ft.Margin.symmetric(vertical=4),
            blur=ft.Blur(14, 14, ft.BlurTileMode.MIRROR),
            shadow=ft.BoxShadow(
                blur_radius=16,
                color=ft.Colors.with_opacity(0.12, "#000000"),
                offset=ft.Offset(0, 4),
            ),
            content=ft.TextField(
                label=etiqueta.upper(),
                prefix_icon=icon,
                password=password,
                can_reveal_password=password,
                border=ft.InputBorder.OUTLINE,
                border_radius=12,
                border_color=ft.Colors.with_opacity(0.35, AZUL_OSCURO),
                focused_border_color=AZUL_OSCURO,
                bgcolor=ft.Colors.TRANSPARENT,
                text_style=ft.TextStyle(color="#0B1B3A", size=14, weight=ft.FontWeight.W_600),
                label_style=ft.TextStyle(
                    color=ft.Colors.with_opacity(0.6, "#0B1B3A"),
                    size=11,
                    weight=ft.FontWeight.BOLD,
                    letter_spacing=1.0,
                ),
                focused_border_width=1.5,
                content_padding=ft.Padding.symmetric(horizontal=14, vertical=12),
            ),
        )

    def boton_glass(texto, color_1, color_2, on_click=None):
        return ft.Container(
            content=ft.Text(texto, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=15),
            alignment=ft.Alignment.CENTER,
            padding=14,
            border_radius=12,
            margin=ft.Margin.symmetric(vertical=4),
            gradient=ft.LinearGradient(colors=[color_1, color_2]),
            shadow=ft.BoxShadow(
                blur_radius=18,
                color=ft.Colors.with_opacity(0.45, color_1),
                offset=ft.Offset(0, 6),
            ),
            on_click=on_click,
            ink=True,
        )

    # ---------- FORMULARIOS (3 SECCIONES / TABS) ----------
    def form_ingresar():
        return ft.Column(
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                campo_glass(ft.Icons.PERSON_OUTLINE, "Usuario"),
                campo_glass(ft.Icons.LOCK_OUTLINE, "Contraseña", password=True),
                boton_glass("Iniciar sesión", AZUL, AZUL_OSCURO,
                            on_click=lambda e: None),
                ft.Container(
                    content=ft.Text(
                        "¿Olvidaste tu contraseña?",
                        color=NARANJA, size=12,
                        weight=ft.FontWeight.W_600,
                    ),
                    alignment=ft.Alignment.CENTER,
                    on_click=lambda e: cambiar_tab("restablecer"),
                ),
            ],
        )

    def form_restablecer():
        return ft.Column(
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                campo_glass(ft.Icons.MAIL_OUTLINE, "Correo electrónico"),
                boton_glass("Enviar enlace de restablecimiento", NARANJA, NARANJA_OSCURO),
            ],
        )

    def form_registrarse():
        return ft.Column(
            spacing=8,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                campo_glass(ft.Icons.PERSON_OUTLINE, "Nombre(s)"),
                campo_glass(ft.Icons.PERSON_OUTLINE, "Apellido Paterno"),
                campo_glass(ft.Icons.PERSON_OUTLINE, "Apellido Materno"),
                campo_glass(ft.Icons.PERSON_OUTLINE, "Nombre de usuario"),
                campo_glass(ft.Icons.MAIL_OUTLINE, "Correo electrónico"),
                campo_glass(ft.Icons.LOCK_OUTLINE, "Contraseña", password=True),
                boton_glass("Crear cuenta", AZUL_CLARO, AZUL_CLARO_OSCURO),
            ],
        )

    FORMULARIOS = {
        "ingresar": form_ingresar,
        "restablecer": form_restablecer,
        "registrarse": form_registrarse,
    }

    def tab_item(nombre, etiqueta):
        activa = tab_activa[0] == nombre
        return ft.Container(
            content=ft.Text(
                etiqueta,
                color=AZUL_OSCURO if activa else ft.Colors.with_opacity(0.55, "#0B1B3A"),
                weight=ft.FontWeight.BOLD if activa else ft.FontWeight.W_500,
                size=13,
            ),
            alignment=ft.Alignment.CENTER,
            padding=ft.Padding.only(bottom=8),
            border=ft.Border(bottom=ft.BorderSide(2, AZUL_OSCURO)) if activa else None,
            expand=True,
            on_click=lambda e, n=nombre: cambiar_tab(n),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        )

    barra_tabs = ft.Row(spacing=6)

    def construir_tabs():
        barra_tabs.controls = [
            tab_item("ingresar", "Ingresar"),
            tab_item("restablecer", "Restablecer"),
            tab_item("registrarse", "Registrarse"),
        ]

    def cambiar_tab(nombre):
        tab_activa[0] = nombre
        construir_tabs()
        panel_formulario.content = FORMULARIOS[nombre]()
        page.update()

    construir_tabs()
    panel_formulario.content = form_ingresar()

    # ---------- SECCIÓN 1: NAVBAR ----------
    navbar = ft.Container(
        bgcolor=NAVBAR_BG,
        padding=ft.Padding.symmetric(horizontal=24, vertical=14),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.RECYCLING, color=NARANJA, size=28),
                ft.Text("Neusomic", color=ft.Colors.WHITE, size=20, weight=ft.FontWeight.BOLD),
            ],
        ),
    )

    # ---------- SECCIÓN 2: TARJETA CENTRAL (LIQUID GLASS, RESPONSIVE) ----------
    tarjeta_glass = ft.Container(
        width=TARJETA_MAX,
        padding=28,
        border_radius=22,
        bgcolor=VIDRIO,
        border=ft.Border.all(1, BORDER_VIDRIO),
        blur=ft.Blur(24, 24, ft.BlurTileMode.MIRROR),
        shadow=ft.BoxShadow(
            blur_radius=40,
            color=ft.Colors.with_opacity(0.20, "#000000"),
            offset=ft.Offset(0, 12),
        ),
        content=ft.Column(
            spacing=18,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Text(
                    "Acceso Neusomic",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color="#0B1B3A",
                    text_align=ft.TextAlign.CENTER,
                ),
                barra_tabs,
                ft.Divider(height=1, color=ft.Colors.with_opacity(0.3, AZUL_OSCURO)),
                panel_formulario,
            ],
        ),
    )

    cuerpo = ft.Container(
        expand=True,
        padding=20,
        alignment=ft.Alignment.CENTER,
        gradient=ft.RadialGradient(
            center=ft.Alignment.TOP_LEFT,
            radius=1.3,
            colors=[
                ft.Colors.with_opacity(0.25, AZUL_CLARO),
                BG_CLARO,
                BG_CLARO,
            ],
        ),
        content=tarjeta_glass,
    )

    # Ajusta el ancho de la tarjeta y el padding del cuerpo según el ancho
    # de la ventana/navegador, para que se vea bien en móvil, tablet y escritorio.
    def ajustar_responsive(e=None):
        ancho_disponible = page.width or TARJETA_MAX
        nuevo_ancho = max(TARJETA_MIN, min(TARJETA_MAX, ancho_disponible - 40))
        tarjeta_glass.width = nuevo_ancho
        tarjeta_glass.padding = 20 if ancho_disponible < 480 else 28
        navbar.padding = ft.Padding.symmetric(
            horizontal=16 if ancho_disponible < 480 else 24, vertical=14
        )
        footer.padding = ft.Padding.symmetric(
            horizontal=16 if ancho_disponible < 480 else 24, vertical=16
        )
        page.update()

    page.on_resized = ajustar_responsive

    # ---------- SECCIÓN 3: FOOTER ----------
    footer = ft.Container(
        bgcolor=FOOTER_BG,
        padding=ft.Padding.symmetric(horizontal=24, vertical=16),
        content=ft.ResponsiveRow(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Column(
                    col={"xs": 12, "sm": 6},
                    spacing=2,
                    controls=[
                        ft.Row(
                            spacing=8,
                            controls=[
                                ft.Icon(ft.Icons.RECYCLING, color=NARANJA, size=18),
                                ft.Text("Neusomic", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=14),
                            ],
                        ),
                        ft.Text(
                            "Solución logística e industrial para la gestión de pavimento "
                            "asfáltico ecológico a partir de mermas de neumáticos de desecho.",
                            color=ft.Colors.with_opacity(0.7, ft.Colors.WHITE),
                            size=11,
                        ),
                    ],
                ),
                ft.Column(
                    col={"xs": 12, "sm": 6},
                    spacing=2,
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                    controls=[
                        ft.Text("Contacto Técnico", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=12),
                        ft.Text("Planta Trituradora Central: Zona Industrial Norte,",
                                color=ft.Colors.with_opacity(0.7, ft.Colors.WHITE), size=11),
                        ft.Text("Bodega 6.", color=ft.Colors.with_opacity(0.7, ft.Colors.WHITE), size=11),
                    ],
                ),
            ],
        ),
    )

    footer_legal = ft.Container(
        bgcolor="#000000",
        padding=ft.Padding.symmetric(vertical=8),
        content=ft.Text(
            "© 2026 Neusomic Inc. Todos los derechos reservados.",
            color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE),
            size=10,
            text_align=ft.TextAlign.CENTER,
        ),
        alignment=ft.Alignment.CENTER,
    )

    page.add(
        ft.Column(
            spacing=0,
            expand=True,
            controls=[
                navbar,
                cuerpo,
                footer,
                footer_legal,
            ],
        )
    )

    ajustar_responsive()


if __name__ == "__main__":
    ft.app(target=main)