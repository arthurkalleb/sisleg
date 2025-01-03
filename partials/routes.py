import flet as ft
from pages.vereador import show_vereador
from pages.presidente import show_presidente
from pages.admin import show_admin
from partials.saida import show_saida
from partials.pautas import show_pautas
from utils.db import verify_login, get_roles

class Routes:
    def __init__(self, page):
        self.page = page
        self.page.on_route_change = self.handle_route_change
        self.username = ft.TextField(label="Nome de usuário", autofocus=True, border_radius=10, border_color=ft.colors.BLUE_800)
        self.password = ft.TextField(label="Senha", password=True, border_radius=10, border_color=ft.colors.BLUE_800)
        self.role = ft.Dropdown(
            label="Categoria",
            options=[ft.dropdown.Option(role) for role in get_roles()],
            border_radius=10,
            border_color=ft.colors.BLUE_800,
        )
        self.error_message = ft.Text(color=ft.colors.RED)

    def handle_route_change(self, route):
        self.page.views.clear()

        # Rotas públicas (não requerem login)
        if self.page.route == "/saida":
            show_saida(self.page)
        elif self.page.route == "/pautas":
            show_pautas(self.page)
        else:
            # Rotas que requerem autenticação
            if not self.page.session.contains_key("user_id"):  # Verifica se o usuário está logado
                self.show_login()
            else:
                if self.page.route == "/vereador":
                    show_vereador(self.page)
                elif self.page.route == "/presidente":
                    show_presidente(self.page)
                elif self.page.route == "/admin":
                    show_admin(self.page)
                else:
                    self.show_login()  # Redireciona para o login se a rota não for reconhecida
        self.page.update()

    def show_login(self):
        login_container = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Bem-vindo ao Sistema de Votação!", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_800),
                    self.username,
                    self.password,
                    self.role,
                    ft.ElevatedButton(
                        "Entrar",
                        on_click=self.validate_login,
                        style=ft.ButtonStyle(
                            bgcolor=ft.colors.BLUE_800,
                            color=ft.colors.WHITE,
                            padding=20,
                            shape=ft.RoundedRectangleBorder(radius=10),
                        ),
                    ),
                    self.error_message,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            padding=40,
            border_radius=20,
            bgcolor=ft.colors.WHITE,
            width=400,
            height=500,
            alignment=ft.alignment.center,
        )

        background = ft.Container(
            content=login_container,
            alignment=ft.alignment.center,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.colors.BLUE_50, ft.colors.BLUE_100],
            ),
            expand=True,
        )

        self.page.views.append(
            ft.View(
                "/",
                [background],
                padding=0,
                spacing=0,
            )
        )
        self.page.update()

    def validate_login(self, e):
        user = verify_login(self.username.value, self.password.value, self.role.value)
        if user:
            self.page.session.set("user_id", user["id"])
            self.page.session.set("username", user["username"])
            self.page.session.set("role", user["role"])
            if user["role"] == "Administrador":
                self.page.go("/admin")  # Redireciona para a rota /admin
            elif user["role"] == "Presidente":
                self.page.go("/presidente")
            elif user["role"] == "Vereador":
                self.page.go("/vereador")
            self.page.update()  # Atualiza a página após o redirecionamento
        else:
            self.error_message.value = "Credenciais inválidas!"
            self.page.update()