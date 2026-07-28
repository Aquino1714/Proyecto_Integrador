import flet as ft
from ui.colors import *


def glass_card(content, padding=16, expand=False, width=None, height=None):
    return ft.Container(
        content=content,
        padding=padding,
        expand=expand,
        width=width,
        height=height,
        bgcolor=CARD_BG,
        border=ft.Border.all(1, GLASS_BORDER),
        border_radius=12,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=20,
            color="rgba(0,0,0,0.35)",
            offset=ft.Offset(0, 4),
        ),
    )


def stat_card(title: str, value: str, subtitle: str, value_color: str, expand=True):
    return ft.Container(
        expand=expand,
        content=ft.Column(
            controls=[
                ft.Text(title, size=11, color=TEXT_MUTED, weight=ft.FontWeight.W_500),
                ft.Text(value, size=26, color=value_color, weight=ft.FontWeight.BOLD),
                ft.Text(subtitle, size=11, color=TEXT_SECONDARY),
            ],
            spacing=6,
        ),
        padding=ft.Padding.all(18),
        bgcolor=CARD_BG,
        border=ft.Border.all(1, GLASS_BORDER),
        border_radius=12,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=18,
            color="rgba(0,0,0,0.4)",
            offset=ft.Offset(0, 4),
        ),
    )



def bar_chart_widget():
    months = ["Nov", "Dic", "Ene", "Feb", "Abr"]
    blue_vals = [13000, 5000, 8000, 9000, 7000]
    green_vals = [14000, 7000, 18000, 16000, 22000]
    max_val = 28000

    def bar_pair(label, b, g):
        bh = max(2, int(b / max_val * 110))
        gh = max(2, int(g / max_val * 110))
        return ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(width=14, height=bh, bgcolor="#3b82f6", border_radius=3),
                        ft.Container(width=14, height=gh, bgcolor="#22c55e", border_radius=3),
                    ],
                    spacing=3,
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.END,
                ),
                ft.Text(label, size=9, color=TEXT_MUTED, text_align=ft.TextAlign.CENTER),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
        )

    bars = ft.Row(
        controls=[bar_pair(months[i], blue_vals[i], green_vals[i]) for i in range(5)],
        spacing=16,
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.END,
    )

    legend = ft.Row(
        controls=[
            ft.Row(controls=[ft.Container(width=10, height=10, bgcolor="#3b82f6", border_radius=2), ft.Text("Ingresos", size=10, color=TEXT_SECONDARY)], spacing=4),
            ft.Row(controls=[ft.Container(width=10, height=10, bgcolor="#22c55e", border_radius=2), ft.Text("Despachos", size=10, color=TEXT_SECONDARY)], spacing=4),
        ],
        spacing=16,
    )

    return glass_card(
        ft.Column(
            controls=[
                ft.Text("Ingresos y despachos de neumáticos / volumen", size=13, color=TEXT_PRIMARY, weight=ft.FontWeight.W_600),
                ft.Container(height=8),
                bars,
                ft.Container(height=6),
                legend,
            ],
            spacing=0,
        ),
        padding=20,
        expand=True,
        height=230,
    )


# ── Radial chart (ProgressRing-based) ────────────────────────────────────────
def pie_chart_widget():
    ring = ft.Stack(
        controls=[
            ft.ProgressRing(value=1.0, stroke_width=14, color="#1e40af", width=120, height=120),
            ft.ProgressRing(value=0.65, stroke_width=14, color="#3b82f6", width=120, height=120),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("65%", size=20, color="#fff", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        ft.Text("Camión", size=9, color=TEXT_SECONDARY, text_align=ft.TextAlign.CENTER),
                    ],
                    spacing=0,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                width=120,
                height=120,
                alignment=ft.Alignment.CENTER,
            ),
        ],
        width=120,
        height=120,
    )

    legend = ft.Column(
        controls=[
            ft.Row(controls=[ft.Container(width=10, height=10, bgcolor="#3b82f6", border_radius=2), ft.Text("Camión Pesado  65%", size=10, color=TEXT_SECONDARY)], spacing=6),
            ft.Row(controls=[ft.Container(width=10, height=10, bgcolor="#1e40af", border_radius=2), ft.Text("Veh. Particular  35%", size=10, color=TEXT_SECONDARY)], spacing=6),
        ],
        spacing=8,
    )

    return glass_card(
        ft.Column(
            controls=[
                ft.Text("Historial de Recolección por Transporte", size=13, color=TEXT_PRIMARY, weight=ft.FontWeight.W_600),
                ft.Container(height=8),
                ft.Row(
                    controls=[
                        ft.Container(content=ring, width=130, height=130),
                        legend,
                    ],
                    spacing=16,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            spacing=0,
        ),
        padding=20,
        expand=True,
        height=230,
    )



def orders_table_widget():
    rows = [
        ("Constructora Alpha S.A  (pedido: #PAV-98)", "12,000 Kg (En espera)", "#f97316"),
        ("Pavimentos del Bajío", "8,500 Kg (Despachado)", "#22c55e"),
    ]

    def order_row(label, status, color):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(label, size=12, color=TEXT_PRIMARY, expand=True),
                    ft.Text(status, size=11, color=color, weight=ft.FontWeight.W_600),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=ft.Padding.symmetric(vertical=10, horizontal=12),
            bgcolor="rgba(255,255,255,0.03)",
            border=ft.Border.all(1, GLASS_BORDER),
            border_radius=8,
        )

    return glass_card(
        ft.Column(
            controls=[
                ft.Text("Monitoreo de pedidos", size=13, color=TEXT_PRIMARY, weight=ft.FontWeight.W_600),
                ft.Container(height=8),
                *[order_row(*r) for r in rows],
            ],
            spacing=8,
        ),
        padding=20,
        expand=True,
    )


def waste_reports_widget():
    return glass_card(
        ft.Column(
            controls=[
                ft.Text("Reportes de desechos para trituración", size=13, color=TEXT_PRIMARY, weight=ft.FontWeight.W_600),
                ft.Container(height=8),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.TIRE_REPAIR, color=TEXT_SECONDARY, size=18),
                            ft.Column(
                                controls=[
                                    ft.Text("Vulcanizadora San Ángel", size=12, color=TEXT_PRIMARY),
                                    ft.Text("65 neumáticos para trituración", size=10, color=TEXT_MUTED),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            ft.Icon(ft.Icons.STARS_OUTLINED, color=TEXT_SECONDARY, size=18),
                        ],
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=ft.Padding.symmetric(vertical=10, horizontal=12),
                    bgcolor="rgba(255,255,255,0.03)",
                    border=ft.Border.all(1, GLASS_BORDER),
                    border_radius=8,
                ),
            ],
            spacing=8,
        ),
        padding=20,
        expand=True,
    )
