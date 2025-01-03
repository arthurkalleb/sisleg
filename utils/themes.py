import flet as ft

class AppTheme:
    light_theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.colors.BLUE_800,
            secondary=ft.colors.GREEN_800,
            background=ft.colors.GREY_100,
            surface=ft.colors.WHITE,
        ),
    )
    dark_theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.colors.BLUE_200,
            secondary=ft.colors.GREEN_200,
            background=ft.colors.GREY_900,
            surface=ft.colors.GREY_800,
        ),
    )