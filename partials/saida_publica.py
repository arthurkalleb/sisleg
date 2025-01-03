import flet as ft
from utils.db import get_vereadores_com_status
import websockets
import asyncio
import threading

def show_saida_publica(page):
    def load_vereadores():
        vereadores = get_vereadores_com_status()
        lista_vereadores.controls.clear()
        for vereador in vereadores:
            cor_indicador = ft.colors.GREEN if vereador["logado"] else ft.colors.RED
            status = "Presente" if vereador["logado"] else "Ausente"
            lista_vereadores.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Row(
                            [
                                ft.CircleAvatar(
                                    foreground_image_url=vereador["foto"],
                                    radius=30,
                                ),
                                ft.Column(
                                    [
                                        ft.Text(vereador["nome"], size=16, weight=ft.FontWeight.BOLD),
                                        ft.Text(status, color=cor_indicador),
                                    ],
                                    spacing=5,
                                ),
                            ],
                            spacing=20,
                        ),
                        padding=15,
                    ),
                )
            )
        page.update()

    async def listen_for_updates():
        async with websockets.connect("ws://localhost:8765") as websocket:
            while True:
                message = await websocket.recv()
                if message == "update":
                    load_vereadores()

    def start_websocket_listener():
        asyncio.run(listen_for_updates())

    lista_vereadores = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)

    layout = ft.Container(
        content=ft.Column(
            [
                ft.Text("Lista de Presença", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                lista_vereadores,
            ],
            spacing=20,
            expand=True,
        ),
        padding=20,
        expand=True,
    )

    load_vereadores()
    threading.Thread(target=start_websocket_listener, daemon=True).start()

    page.views.append(
        ft.View(
            "/saida_publica",
            [
                ft.AppBar(title=ft.Text("Tela de Saída Pública")),
                layout,
            ],
        )
    )
    page.update()