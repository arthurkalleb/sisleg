import flet as ft
import base64  # Importação do módulo base64
from utils.db import get_vereadores, add_vereador, update_vereador, remove_vereador

def gerenciar_parlamentar(page):
    def load_vereadores():
        """
        Carrega a lista de vereadores e atualiza a interface.
        """
        vereadores = get_vereadores()
        lista_vereadores.controls.clear()  # Limpa a lista atual

        for vereador in vereadores:
            # Exibir a foto do vereador, se existir
            foto_vereador = ft.Image(
                src_base64=vereador["foto"] if vereador["foto"] else None,
                width=100,
                height=100,
                fit=ft.ImageFit.COVER,
                border_radius=ft.border_radius.all(10),
            )

            lista_vereadores.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.ListTile(
                                    leading=foto_vereador,
                                    title=ft.Text(vereador["nome"], size=18, weight=ft.FontWeight.BOLD),
                                    subtitle=ft.Text(f"Classificação: {vereador['classificacao']}"),
                                ),
                                ft.Row(
                                    [
                                        ft.ElevatedButton(
                                            "Editar",
                                            on_click=lambda e, id=vereador["id"]: editar_vereador(id),
                                            style=ft.ButtonStyle(
                                                bgcolor=ft.colors.BLUE_700,
                                                color=ft.colors.WHITE,
                                            ),
                                        ),
                                        ft.ElevatedButton(
                                            "Excluir",
                                            on_click=lambda e, id=vereador["id"]: excluir_vereador(id),
                                            style=ft.ButtonStyle(
                                                bgcolor=ft.colors.RED_700,
                                                color=ft.colors.WHITE,
                                            ),
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.END,
                                ),
                            ],
                            spacing=10,
                        ),
                        padding=15,
                    ),
                )
            )
        page.update()

    def adicionar_vereador(e):
        """
        Adiciona um novo vereador ao banco de dados.
        """
        nome = campo_nome.value
        classificacao = campo_classificacao.value
        senha = campo_senha.value
        foto = campo_foto.value  # Foto em base64

        if nome and classificacao and senha:
            add_vereador(nome, classificacao, senha, foto)
            limpar_campos()
            load_vereadores()  # Recarrega a lista de vereadores

    def editar_vereador(id):
        """
        Abre um formulário para editar um vereador existente.
        """
        vereador = next((v for v in get_vereadores() if v["id"] == id), None)
        if vereador:
            campo_nome.value = vereador["nome"]
            campo_classificacao.value = vereador["classificacao"]
            campo_senha.value = vereador["senha"]
            campo_foto.value = vereador["foto"]  # Carrega a foto em base64
            botao_salvar.text = "Salvar Edição"
            botao_salvar.on_click = lambda e: salvar_edicao(id)
            page.update()

    def salvar_edicao(id):
        """
        Salva as alterações de um vereador editado.
        """
        nome = campo_nome.value
        classificacao = campo_classificacao.value
        senha = campo_senha.value
        foto = campo_foto.value  # Foto em base64

        if nome and classificacao and senha:
            update_vereador(id, nome, classificacao, senha, foto)
            limpar_campos()
            load_vereadores()  # Recarrega a lista de vereadores

    def excluir_vereador(id):
        """
        Exclui um vereador do banco de dados.
        """
        remove_vereador(id)
        load_vereadores()  # Recarrega a lista de vereadores

    def limpar_campos():
        """
        Limpa os campos do formulário.
        """
        campo_nome.value = ""
        campo_classificacao.value = ""
        campo_senha.value = ""
        campo_foto.value = ""
        botao_salvar.text = "Adicionar Vereador"
        botao_salvar.on_click = adicionar_vereador
        page.update()

    def upload_foto(e: ft.FilePickerResultEvent):
        """
        Converte a foto selecionada para base64 e atualiza o campo de foto.
        """
        if e.files:
            file = e.files[0]
            with open(file.path, "rb") as image_file:
                foto_base64 = base64.b64encode(image_file.read()).decode("utf-8")
                campo_foto.value = foto_base64  # Armazena a foto em base64
                page.update()

    # Campos do formulário
    campo_nome = ft.TextField(label="Nome", autofocus=True, width=300)
    campo_classificacao = ft.Dropdown(
        label="Classificação",
        options=[
            ft.dropdown.Option("Presidente"),
            ft.dropdown.Option("Vice-Presidente"),
            ft.dropdown.Option("Primeiro Secretário"),
            ft.dropdown.Option("Segundo Secretário"),
            ft.dropdown.Option("Vereador"),
        ],
        width=300,
    )
    campo_senha = ft.TextField(label="Senha", password=True, width=300)
    campo_foto = ft.TextField(label="Foto (base64)", read_only=True, visible=False)  # Campo oculto para armazenar a foto em base64

    # FilePicker para upload de foto
    file_picker = ft.FilePicker(on_result=upload_foto)
    page.overlay.append(file_picker)

    # Botão de ação (Adicionar/Salvar Edição)
    botao_salvar = ft.ElevatedButton(
        "Adicionar Vereador",
        on_click=adicionar_vereador,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.GREEN_700,
            color=ft.colors.WHITE,
        ),
    )

    # Botão para selecionar foto
    botao_foto = ft.ElevatedButton(
        "Selecionar Foto",
        on_click=lambda _: file_picker.pick_files(),
        style=ft.ButtonStyle(
            bgcolor=ft.colors.BLUE_700,
            color=ft.colors.WHITE,
        ),
    )

    # Lista de vereadores
    lista_vereadores = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)

    # Layout do gerenciamento de parlamentares
    layout = ft.Column(
        [
            ft.Text("Gerenciar Parlamentares", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
            ft.Divider(height=10, color=ft.colors.GREY_400),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Adicionar/Editar Vereador", size=18, weight=ft.FontWeight.BOLD),
                        campo_nome,
                        campo_classificacao,
                        campo_senha,
                        ft.Row([botao_foto], alignment=ft.MainAxisAlignment.START),
                        ft.Row([botao_salvar], alignment=ft.MainAxisAlignment.END),
                        ft.Divider(height=10, color=ft.colors.GREY_400),
                        ft.Text("Lista de Vereadores", size=18, weight=ft.FontWeight.BOLD),
                        lista_vereadores,
                    ],
                    spacing=10,
                ),
                padding=20,
                border=ft.border.all(1, ft.colors.GREY_400),
                border_radius=10,
                expand=True,
            ),
        ],
        spacing=10,
        expand=True,
    )

    # Carrega a lista de vereadores ao abrir a página
    load_vereadores()

    # Retorna o layout para ser exibido no dashboard
    return layout