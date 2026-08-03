import flet as ft
from ui.colors import *

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
        expand=True,
        tooltip=f"Ingrese {label.lower()}"
    )


# ── Campos del login ──────────────────────────────────────────────────────
txt_login_user = build_textfield("Usuario", "usuario01@example.com", ft.Icons.PERSON_OUTLINED)
txt_login_pass = build_textfield("Contraseña", "********", ft.Icons.LOCK_OUTLINED, is_password=True)

# ── Caqmpos del area de restablecer ──────────────────────────────────────────────────────
txt_reset_email = build_textfield("Correo electrónico", "usuario@neusomic.com", ft.Icons.EMAIL_OUTLINED)

# ── Campos del registro ──────────────────────────────────────────────────────
txt_reg_nombre = build_textfield("Nombre(s)", "Nombre", ft.Icons.PERSON_OUTLINE)
txt_reg_paterno = build_textfield("Apellido paterno", "Apellido paterno", ft.Icons.PERSON_OUTLINE)
txt_reg_materno = build_textfield("Apellido materno", "Apellido materno", ft.Icons.PERSON_OUTLINE)
txt_reg_user = build_textfield("User name", "ejemplo01", ft.Icons.ACCOUNT_CIRCLE_OUTLINED)
txt_reg_phone = build_textfield("Teléfono", "2221234567", ft.Icons.PHONE_OUTLINED)
txt_reg_email = build_textfield("Correo", "usuario@correo.com", ft.Icons.EMAIL_OUTLINED)

txt_reg_pass = build_textfield("Contraseña", "********", ft.Icons.LOCK_OUTLINED, is_password=True)
txt_reg_confirm = build_textfield("Confirmar contraseña", "********", ft.Icons.LOCK_OUTLINED, is_password=True)

# ── Campos registro vulcanizadora ─────────────────────
txt_vul_nombre = build_textfield("Nombre vulcanizadora", "Vulcanizadora El Sol", ft.Icons.BUSINESS_OUTLINED)

txt_vul_telefono = build_textfield("Teléfono", "2221234567", ft.Icons.PHONE_OUTLINED)

txt_vul_correo = build_textfield("Correo", "correo@vulcanizadora.com", ft.Icons.EMAIL_OUTLINED)

txt_vul_responsable = build_textfield("Responsable", "Nombre encargado", ft.Icons.PERSON_OUTLINE)

txt_vul_direccion = build_textfield("Dirección", "Dirección completa", ft.Icons.LOCATION_ON_OUTLINED)

txt_vul_pass = build_textfield("Contraseña", "********", ft.Icons.LOCK_OUTLINED, is_password=True)

txt_vul_confirm = build_textfield("Confirmar contraseña", "********", ft.Icons.LOCK_OUTLINED, is_password=True)

form_container = ft.Column(spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

title_text = ft.Text(size=24, weight=ft.FontWeight.BOLD, color=COLOR_BLANCO, text_align=ft.TextAlign.CENTER)

notification_layer = ft.Stack(
    controls=[],
    expand=True
)