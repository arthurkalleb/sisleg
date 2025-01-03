import flet as ft
from partials.logout import logout

def show_vereador(page):
    buttons = [
        ft.Text("Bem-vindo, Vereador!", size=24),
        ft.ElevatedButton("Voltar", on_click=lambda _: page.go("/")),
        ft.ElevatedButton("Logout", on_click=lambda _: logout(page)),
    ]
    page.views.append(
        ft.View(
            "/vereador",
            [
                ft.AppBar(title=ft.Text("Página do Vereador")),
                *buttons
            ]
        )
    )
    page.update()