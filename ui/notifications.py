import asyncio
import flet as ft


class NotificationManager:

    def __init__(self, page: ft.Page):
        self.page = page
        self.layer = ft.Stack()


    def get_layer(self):
        return self.layer


    async def show(
        self,
        mensaje,
        tipo="normal"
    ):

        if tipo == "error":
            bgcolor = "#B91C1C"
            icon = ft.Icons.ERROR

        elif tipo == "success":
            bgcolor = "#059669"
            icon = ft.Icons.CHECK_CIRCLE

        elif tipo == "warning":
            bgcolor = "#D97706"
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
            offset=ft.Offset(0,0.5),

            shadow=ft.BoxShadow(
                blur_radius=18,
                spread_radius=2,
                color="#55000000",
                offset=ft.Offset(0,5)
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
            alignment=ft.Alignment(1,1),
            padding=20
        )


        self.layer.controls.append(wrapper)

        self.page.update()


        toast.opacity = 1
        toast.offset = ft.Offset(0,0)

        self.page.update()


        await asyncio.sleep(3)


        toast.opacity = 0
        toast.offset = ft.Offset(0,0.5)

        self.page.update()


        await asyncio.sleep(0.3)


        self.layer.controls.remove(wrapper)

        self.page.update()
