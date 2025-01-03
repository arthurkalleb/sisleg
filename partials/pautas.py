import flet as ft

def show_pautas(page):
    pautas = [
        "Pauta 1: Discussão sobre o orçamento municipal.",
        "Pauta 2: Projeto de lei para reforma da educação.",
        "Pauta 3: Aprovação de novos contratos públicos.",
    ]

    layout = ft.Container(
        content=ft.Column(
            [
                ft.Text("Pautas da Sessão", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                *[ft.Text(pauta, size=16) for pauta in pautas],
            ],
            spacing=20,
            expand=True,
        ),
        padding=20,
        expand=True,
    )

    page.views.append(
        ft.View(
            "/pautas",
            [
                ft.AppBar(title=ft.Text("Pautas da Sessão")),
                layout,
            ],
        )
    )
    page.update()