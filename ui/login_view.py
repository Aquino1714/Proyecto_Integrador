import flet as ft



def login_view(page) :
    page.padding = 0
    page.margin = 0

    header = ft.Container (
        content =  ft.Row (
            [
                ft.Image (
                    src = "assets/image/logo.png",
                    width = 42,
                    height = 42,
                    #fit = ft.ImageFit.CONTAIN
                )
            ],
            spacing = 10
        ),
        bgcolor = "#114BA4",
        padding = 15,
        width = float("inf")
    )

    custom_tabs = ft.Row (
        spacing = 25,
        alignment = ft.MainAxisAlignment.CENTER,
        controls = [
            ft.Container (
                content = ft.Column (
                    [
                        ft.Text (
                            "Ingresar",
                            color = "#42A5F5",
                            weight = ft.FontWeight.BOLD,
                        ),
                        ft.Container ( height = 5)
                    ],
                    spacing = 0
                ),
                border = ft.Border (
                    bottom = ft.BorderSide (2, "#0D47A1")
                ),
            ),
            ft.Container (
                content = ft.Column (
                    [
                        ft.Text (
                            "Restablecer",
                            color = "#B3FFFFFF"
                        ),
                        ft.Container (height = 5)
                    ],
                    spacing = 0
                )
            ),
            
            ft.Container (
                content = ft.Column (
                    [
                        ft.Text (
                            "Registrarse",
                            color = "#8093A6"
                        ),
                        ft.Container(height = 5)
                    ],
                    spacing = 0
                )
            ),
        ]
    )

# ------Logo -------
    logo_container = ft.Container (
        width = 50,
        height = 50,
        border_radius = 18,
        bgcolor = "#1AFFFFFF",
        border = ft.Border (
            top = ft.BorderSide (1, "#40FFFFFF"),
            bottom = ft.BorderSide (1, "#40FFFFFF"),
            left = ft.BorderSide (1, "#40FFFFFF"),
            right = ft.BorderSide (1, "#40FFFFFF")
        ),
        alignment = ft.Alignment (0, 0),
        shadow = ft.BoxShadow (
            blur_radius = 20,
            color = "#661E40AF",
            offset = ft.Offset (0, 6)
        ),
        content = ft.Image (
            src = "assets/image/logo.png",
            width = 36,
            height = 36,
            #fit = ft.ImageFit.CONTAIN
        )
    )

    login_card = ft.Container (
        width = 400,
        height = 500,
        padding = 40,
        bgcolor = "#B3FFFFFF",
        blur = ft.Blur(30, 30, ft.BlurTileMode.CLAMP),
        border_radius = 30,

        border = ft.Border (
            top = ft.BorderSide (2, "#80FFFFFF"),
            bottom = ft.BorderSide (2, "#80FFFFFF"),
            left = ft.BorderSide (2, "#80FFFFFF"),
            right = ft.BorderSide (2, "#80FFFFFF")
        ),

        shadow = ft.BoxShadow (
            blur_radius = 40,
            color = "#1A0D47A1",
            offset = ft.Offset(0, 15),
        ),
        
        content = ft.Column (
            [
                logo_container,

                ft.Container (height = 6),

                ft.Text (
                    "Acceso Neusomic",
                    size = 24,
                    weight = ft.FontWeight.BOLD,
                    color = "white"
                ),

                custom_tabs,

                ft.Container(height = 10),

                ft.TextField (
                    label = "Usuario",
                    hint_text =  "Usuario@example.com",
                    label_style = ft.TextStyle (
                        color = "#5A6B7D"
                    ),
                    hint_style = ft.TextStyle (
                        color = "#FFFFFF"
                    ),
                    color = "white",
                    border_color = "#4D0D47A1",
                    focused_border_color = "#42A5F5",
                    border_radius = 12,
                    prefix_icon = ft.Icons.PERSON_OUTLINE,
                    width = 320
                ),

                ft.TextField (
                    label = "Contraseña",
                    password = True,
                    can_reveal_password = True,
                    label_style = ft.TextStyle (
                        color = "#5A6B7D"
                    ),
                    color = "0D2C54",
                    border_color = "#4D0D47A1",
                    focused_border_color = "#42A5F5",
                    border_radius = 12,
                    prefix_icon = ft.Icons.LOCK_OUTLINE,
                    width = 320
                ),

                ft.Container(
                    content = ft.TextButton (
                        content = ft.Text (
                            "¿Olvidaste tu contraseña?",
                            color = "#FC8F1B",
                            size = 13,
                        ),
                    ),
                    alignment = ft.Alignment ( 1, 0),
                    width = 320
                ),

                ft.Container (
                    content = ft.ElevatedButton (
                        "Iniciar sesión",
                        color = "white",
                        bgcolor = "#1E40AF",
                        style = ft.ButtonStyle (
                            shape = ft.RoundedRectangleBorder (
                                radius = 14
                            ),
                        ),
                        width = 320,
                        height = 50
                    ),
                    shadow = ft.BoxShadow (
                        blur_radius = 200,
                        color = "#661E40AF",
                        offset = ft.Offset (0, 4)
                    )
                )
            ],
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            spacing = 15
        )
    )

    foother = ft.Container (
        bgcolor = "#0B!B#A",
        padding = 20,
        width = float ("inf"),
        content = ft.Text (
            "© 2026 Neusomic Inc. Todos los derechos reservados.",
            color = "#B3FFFFFF",
            size = 12,
            text_align = ft.TextAlign.CENTER
        )
    )

    blob_1 = ft.Container (
        width = 420,
        height = 420,
        border_radius = 1000,
        blur = ft.Blur (80, 80, ft.BlurTileMode.CLAMP),
        gradient = ft.RadialGradient (
            colors = ["#6D5CFF", "#006D5CFF"]
        ),
        top = -120,
        left = -100,
        opacity = 0.55
    )

    blob_2 = ft.Container (
        width = 380,
        height = 380,
        border_radius = 1000,
        blur = ft.Blur (80, 80, ft.BlurTileMode.CLAMP),
        gradient = ft.RadialGradient (
            colors = ["#FF5CA8", "#00FF5CA8"]
        ),
        bottom = -120,
        right = -100,
        opacity = 0.5
    )

    blob_3 = ft.Container (
        width = 320,
        height = 320,
        border_radius = 1000,
        blur = ft.Blur (80, 80, ft.BlurTileMode.CLAMP),
        gradient = ft.RadialGradient (
            colors = ["#33D6FF", "#0033D6FF"]
        ),
        bottom = 40,
        left = 20,
        opacity = 0.4
    )

    center_stage = ft.Stack (
        [
            ft.Container (
                expand = True,
                gradient = ft.LinearGradient (
                    begin = ft.Alignment (-1, -1),
                    end = ft.Alignment (1, 1),
                    colors = [
                        "#130924",
                        "#0B132B",
                        "#081C24",
                    ],
                    stops = [
                        0.1,
                        0.5,
                        0.9
                    ]
                )
            ),
            blob_1,
            blob_2,
            blob_3,
            ft.Container (
                content = login_card,
                expand = True,
                alignment = ft.Alignment(0, 0)
            )
        ],
        expand = True
    )

    return ft.Column (
        [
            header,
            center_stage,
            foother
        ],
        expand = True,
        spacing = 0
    )