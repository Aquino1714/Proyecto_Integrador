import flet as ft
from ui.colors import *


def about_dialog(page: ft.Page):

    def close_about(e):
        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        modal=True,
        bgcolor=CARD_BG,
        title=ft.Text(
            "Sobre Neusomic",
            color=TEXT_PRIMARY,
            weight=ft.FontWeight.BOLD
        ),
        content=ft.Text(
            "Neusomic es la plataforma de gestión logística para recolección de "
            "neumáticos usados, control de inventario, trituración, pesaje de "
            "materia prima y distribución.",
            color=TEXT_SECONDARY,
            size=13,
        ),
        actions=[
            ft.TextButton(
                "Cerrar",
                style=ft.ButtonStyle(color=STAT_BLUE),
                on_click=close_about,
            ),
        ],
    )

    return dialog



def boton_informacion(page: ft.Page):

    dialog = about_dialog(page)

    def abrir(e):
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    return ft.Container(
        content=ft.Icon(
            ft.Icons.INFO_OUTLINE,
            color="#ffffff",
            size=18
        ),
        padding=8,
        border_radius=18,
        border=ft.Border.all(1, "#ffffff"),
        ink=True,
        tooltip="Saber más sobre nosotros",
        on_click=abrir,
    )
