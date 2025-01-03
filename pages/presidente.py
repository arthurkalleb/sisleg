import flet as ft
from partials.logout import logout

def show_presidente(page):
    buttons = [
        ft.Text("Bem-vindo, Presidente!", size=24),
        ft.ElevatedButton("Voltar", on_click=lambda _: page.go("/")),
        ft.ElevatedButton("Logout", on_click=lambda _: logout(page)),
    ]
    page.views.append(
        ft.View(
            "/presidente",
            [
                ft.AppBar(
                    title=ft.Text("Página do Presidente"),
                    actions=[
                        ft.IconButton(ft.icons.LOGOUT, on_click=lambda _: logout(page)),
                    ],
                ),
                *buttons
            ]
        )
    )
    page.update()