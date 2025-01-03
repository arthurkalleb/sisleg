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