import flet as ft
import bcrypt  # BCRYPT

from ui.colors import *
from ui.vulcanizadora.dashboard_vulcanizadora import sidebar
from dao.vulcanizadora_dao import VulcanizadoraDAO
from models.vulcanizadora import Vulcanizadora

dao = VulcanizadoraDAO()


# ── Topbar local (mismo look que dashboard.py, título correcto) ─────────────
def _topbar_perfil(page: ft.Page):
    logo = ft.Image(
        src="assets/images/logo.png",
        width=100,
        height=90,
        fit=ft.BoxFit.CONTAIN,
    )
    return ft.Container(
        content=ft.Row(
            controls=[
                logo,
                ft.Container(width=20),
                ft.Text("Mi perfil", size=20, color="#fff", weight=ft.FontWeight.BOLD),
                ft.Container(expand=True),
                ft.Text("vulcanizadora", size=14, color="rgba(255,255,255,0.5)"),
                ft.Text("|", size=14, color="rgba(255,255,255,0.5)"),
                ft.Container(
                    content=ft.Icon(ft.Icons.ACCOUNT_CIRCLE, color="#fff", size=28),
                    padding=6,
                    bgcolor="rgba(255,255,255,0.15)",
                    border_radius=20,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        padding=ft.Padding.symmetric(horizontal=24, vertical=3),
        bgcolor=TOPBAR_BG,
    )


# ── Campo de solo lectura ────────────────────────────────────────────────────
def _read_only_field(label: str, value: str):
    return ft.Column(
        controls=[
            ft.Text(label, size=11, color=TEXT_SECONDARY),
            ft.Text(value or "—", size=14, color=TEXT_PRIMARY, weight=ft.FontWeight.W_500),
        ],
        spacing=2,
    )


# ── Vista principal ──────────────────────────────────────────────────────────
def perfil_view(page: ft.Page, vulcanizadora_id: int, on_navigate=None, on_logout=None):
    active_route = "/perfil"

    vulca = dao.get_by_id(vulcanizadora_id)

    # Campos editables
    nombre_field = ft.TextField(label="Nombre", value=vulca.nombre if vulca else "", expand=True)
    telefono_field = ft.TextField(label="Teléfono", value=vulca.telefono if vulca else "", expand=True)
    correo_field = ft.TextField(label="Correo", value=vulca.correo if vulca else "", expand=True)
    responsable_field = ft.TextField(label="Responsable", value=vulca.responsable if vulca else "", expand=True)
    direccion_field = ft.TextField(label="Dirección", value=vulca.direccion if vulca else "", expand=True)
    #ciudad_field = ft.TextField(label="Ciudad", value=vulca.ciudad if vulca else "", expand=True)

    feedback_text = ft.Text("", size=12)

    #edit_mode = ft.Ref[bool]()
    edit_mode = False

    campos_editables = [nombre_field, telefono_field, correo_field,
                        responsable_field, direccion_field]

    def set_disabled(disabled: bool):
        for f in campos_editables:
            f.disabled = disabled

    set_disabled(True)

    async def toggle_edit(e):
        nonlocal edit_mode

        edit_mode = not edit_mode

        set_disabled(not edit_mode)

        edit_btn.text = "Cancelar" if edit_mode else "Editar"
        guardar_btn.visible = edit_mode

        if not edit_mode and vulca:
            nombre_field.value = vulca.nombre
            telefono_field.value = vulca.telefono
            correo_field.value = vulca.correo
            responsable_field.value = vulca.responsable
            direccion_field.value = vulca.direccion

        if hasattr(page, "update_async"):
            await page.update_async()
        else:
            page.update()

    async def guardar_click(e):
        nonlocal edit_mode

        if not vulca:
            feedback_text.value = "No se encontró la vulcanizadora."
            feedback_text.color = "#f87171"
            page.update()
            return

        # Guardar los valores actuales de los campos
        nombre = nombre_field.value.strip()
        telefono = telefono_field.value.strip()
        correo = correo_field.value.strip()
        responsable = responsable_field.value.strip()
        direccion = direccion_field.value.strip()

        # Actualizar el objeto
        vulca.nombre = nombre
        vulca.telefono = telefono
        vulca.correo = correo
        vulca.responsable = responsable
        vulca.direccion = direccion

        # Actualizar base de datos
        ok = dao.update(vulca)

        if ok:
            feedback_text.value = "Perfil actualizado correctamente."
            feedback_text.color = STAT_TEAL

            # edit_mode es un bool, por eso NO lleva .current
            edit_mode = False

            set_disabled(True)
            edit_btn.text = "Editar"
            guardar_btn.visible = False

        else:
            feedback_text.value = "No se pudo actualizar el perfil."
            feedback_text.color = "#f87171"

        page.update()

    edit_btn = ft.OutlinedButton("Editar", on_click=toggle_edit)
    guardar_btn = ft.ElevatedButton(
        "Guardar cambios",
        bgcolor=STAT_BLUE,
        color="#fff",
        visible=False,
        on_click=guardar_click,
    )

    # ── Diálogo de cambio de contraseña ─────────────────────────────
    actual_pw = ft.TextField(label="Contraseña actual", password=True, can_reveal_password=True)
    nueva_pw = ft.TextField(label="Contraseña nueva", password=True, can_reveal_password=True)
    confirmar_pw = ft.TextField(label="Confirmar contraseña nueva", password=True, can_reveal_password=True)
    pw_feedback = ft.Text("", size=12)

    async def cambiar_password_click(e):
        stored_hash = dao.get_password_hash(vulcanizadora_id)
        if not stored_hash or not bcrypt.checkpw(  # BCRYPT
                actual_pw.value.encode(), stored_hash.encode()
        ):
            pw_feedback.value = "La contraseña actual no es correcta."
            pw_feedback.color = "#f87171"
            page.update()
            return

        if len(nueva_pw.value or "") < 8:
            pw_feedback.value = "La nueva contraseña debe tener al menos 8 caracteres."
            pw_feedback.color = "#f87171"
            page.update()
            return

        if nueva_pw.value != confirmar_pw.value:
            pw_feedback.value = "Las contraseñas nuevas no coinciden."
            pw_feedback.color = "#f87171"
            page.update()
            return

        nuevo_hash = bcrypt.hashpw(nueva_pw.value.encode(), bcrypt.gensalt()).decode()  # BCRYPT
        ok = dao.update_password(vulcanizadora_id, nuevo_hash)
        pw_feedback.value = "Contraseña actualizada." if ok else "No se pudo actualizar la contraseña."
        pw_feedback.color = STAT_TEAL if ok else "#f87171"
        if ok:
            actual_pw.value = nueva_pw.value = confirmar_pw.value = ""
        page.update()

    password_dialog = ft.AlertDialog(
        modal=True,
        bgcolor=CARD_BG,
        title=ft.Text("Cambiar contraseña", color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
        content=ft.Column(
            controls=[actual_pw, nueva_pw, confirmar_pw, pw_feedback],
            spacing=10,
            tight=True,
            width=320,
        ),
        actions=[
            ft.TextButton("Cerrar", on_click=lambda e: page.close(password_dialog)),
            ft.ElevatedButton(
                "Actualizar",
                bgcolor=STAT_BLUE,
                color="#fff",
                on_click=cambiar_password_click,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    async def abrir_password_dialog(e):
        page.open(password_dialog) if hasattr(page, "open") else page.dialog.__setattr__("open", True)
        page.update()

    # ── Tarjeta de datos de la vulcanizadora (solo lectura) ─────────
    solo_lectura_card = ft.Container(
        bgcolor=CARD_BG,
        border_radius=12,
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Estado de la cuenta", size=14, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                ft.Container(height=8),
                ft.Row(
                    controls=[
                        _read_only_field("Activo", "Sí" if (vulca and vulca.activo) else "No"),
                        _read_only_field(
                            "Fecha de registro",
                            str(vulca.fecha_registro) if vulca else "",
                        ),
                    ],
                    spacing=40,
                ),
            ],
        ),
    )

    datos_card = ft.Container(
        bgcolor=CARD_BG,
        border_radius=12,
        padding=20,
        expand=True,
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Datos del negocio", size=14, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                        ft.Container(expand=True),
                        edit_btn,
                        guardar_btn,
                    ],
                ),
                ft.Container(height=10),
                ft.Row(controls=[nombre_field, responsable_field], spacing=16),
                ft.Row(controls=[telefono_field, correo_field], spacing=16),
                feedback_text,
            ],
            spacing=12,
        ),
    )

    seguridad_card = ft.Container(
        bgcolor=CARD_BG,
        border_radius=12,
        padding=20,
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text("Seguridad", size=14, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                        ft.Text(
                            "Cambia tu contraseña de acceso. Se te pedirá la actual.",
                            size=12,
                            color=TEXT_SECONDARY,
                        ),
                    ],
                    spacing=4,
                    expand=True,
                ),
                ft.OutlinedButton("Cambiar contraseña", on_click=abrir_password_dialog),
            ],
        ),
    )

    content_area = ft.Container(
        expand=True,
        padding=20,
        bgcolor=MAIN_BG,
        content=ft.Column(
            controls=[
                datos_card,
                ft.Container(height=12),
                solo_lectura_card,
                ft.Container(height=12),
                seguridad_card,
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        ),
    )

    return ft.View(
        route="/perfil",
        padding=0,
        bgcolor=MAIN_BG,
        controls=[
            ft.Column(
                controls=[
                    _topbar_perfil(page),
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
