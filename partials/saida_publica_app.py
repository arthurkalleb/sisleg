import flet as ft
from saida_publica import show_saida_publica

def main(page: ft.Page):
    show_saida_publica(page)

ft.app(target=main)