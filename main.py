import flet as ft
from partials.routes import Routes
from utils.db import init_db

# Define o modo de depuração
DEBUG_MODE = False  

def main(page: ft.Page):
    # Inicializa o banco de dados
    init_db()

    # Configura a página
    page.title = "Sistema de Votação"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT  # Tema padrão

    # Inicializa o gerenciador de rotas
    routes = Routes(page)

    # Modo de depuração
    if DEBUG_MODE:
        # Define um usuário de teste na sessão (simulando login)
        page.session.set("user_id", 1)  # ID do usuário de teste
        page.session.set("username", "admin")  # Nome de usuário de teste
        page.session.set("role", "Administrador")  # Papel do usuário de teste

        # Redireciona para a rota de administrador (ou outra rota de teste)
        page.go("/admin")
    else:
        # Redireciona para a tela de login em modo normal
        page.go("/")

    page.update()

# Inicia a aplicação Flet
ft.app(target=main)