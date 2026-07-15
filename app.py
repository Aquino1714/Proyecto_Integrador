import flet as ft
from ui.login_view import login_view

def main(page: ft.Page):
    page.title = "Neusomic"
    page.padding = 0
    page.spacing = 0
    page.add(login_view(page))

ft.run(main)