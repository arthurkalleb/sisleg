import flet as ft
from partials.logout import logout
from partials.gerenciar_parlamentar import gerenciar_parlamentar

def show_admin(page):
    # Verifica se o usuário está logado e é um administrador
    if not page.session.contains_key("user_id") or page.session.get("role") != "Administrador":
        page.go("/")  # Redireciona para a tela de login se o usuário não estiver logado ou não for administrador
        return

    # Layout do gerenciamento de parlamentares
    gerenciar_parlamentar_layout = gerenciar_parlamentar(page)

    # Barra de título personalizada (substituindo o AppBar)
    title_bar = ft.Container(
        content=ft.Row(
            [
                ft.Text("Página do Administrador", size=20, weight=ft.FontWeight.BOLD, expand=True),
                ft.IconButton(ft.icons.LOGOUT, on_click=lambda _: logout(page)),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=10,  # Adiciona padding ao Container
        bgcolor=ft.colors.BLUE_700,
        border_radius=ft.border_radius.all(10),
    )

    # Container para organizar o dashboard do admin
    dashboard_container = ft.Container(
        content=ft.Column(
            [
                ft.Text("Dashboard do Administrador", size=24, weight=ft.FontWeight.BOLD),
                gerenciar_parlamentar_layout,
            ],
            spacing=20,
            expand=True,
        ),
        padding=20,
        border=ft.border.all(1, ft.colors.GREY_400),
        border_radius=10,
        expand=True,
    )

    # Layout principal da página de admin
    layout = ft.Column(
        [
            title_bar,  # Barra de título personalizada
            dashboard_container,
        ],
        expand=True,
    )

    # Adiciona o layout à página
    page.views.append(
        ft.View(
            "/admin",
            [layout],
        )
    )
    page.update()