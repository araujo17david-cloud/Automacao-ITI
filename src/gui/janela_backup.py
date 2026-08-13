import customtkinter as ctk

from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox

from PIL import Image

from src.api.download import baixar_dados
from src.excel.excel import criar_excel
from src.services.tratamento import (
    filtrar_por_mes,
    filtrar_por_regiao,
    obter_certificados
)
from src.utils.meses import MESES


PASTA_PROJETO = Path(__file__).resolve().parents[2]

CAMINHO_LOGO = (
    PASTA_PROJETO
    / "assets"
    / "logo.png"
)

CAMINHO_ICONE = (
    PASTA_PROJETO
    / "assets"
    / "logo.ico"
)


def iniciar():
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("blue")

    janela = ctk.CTk()

    janela.title("Automação ITI v2.0")
    janela.geometry("1100x720")
    janela.minsize(1000, 680)

    if CAMINHO_ICONE.exists():
        try:
            janela.iconbitmap(
                str(CAMINHO_ICONE)
            )
        except Exception as erro_icone:
            print(
                "Não foi possível carregar o ícone:",
                erro_icone
            )

    janela.grid_columnconfigure(
        1,
        weight=1
    )

    janela.grid_rowconfigure(
        0,
        weight=1
    )

    # ==================================
    # MENU LATERAL
    # ==================================

    menu_lateral = ctk.CTkFrame(
        janela,
        width=230,
        corner_radius=0,
        fg_color="#123B2A"
    )

    menu_lateral.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    menu_lateral.grid_propagate(
        False
    )

    # Logo do menu
    if CAMINHO_LOGO.exists():
        try:
            imagem_original = Image.open(
                CAMINHO_LOGO
            )

            imagem_logo = ctk.CTkImage(
                light_image=imagem_original,
                dark_image=imagem_original,
                size=(180, 70)
            )

            logo = ctk.CTkLabel(
                menu_lateral,
                text="",
                image=imagem_logo
            )

            logo.pack(
                pady=(30, 20)
            )

        except Exception as erro_logo:
            print(
                "Não foi possível carregar a logo:",
                erro_logo
            )

    titulo_menu = ctk.CTkLabel(
        menu_lateral,
        text="AUTOMAÇÃO ITI",
        font=("Segoe UI", 20, "bold"),
        text_color="white"
    )

    titulo_menu.pack(
        pady=(5, 30)
    )

    botao_relatorios = ctk.CTkButton(
        menu_lateral,
        text="Relatórios",
        height=42,
        corner_radius=8,
        fg_color="#1D6B47",
        hover_color="#24875A",
        anchor="w",
        font=("Segoe UI", 14, "bold")
    )

    botao_relatorios.pack(
        fill="x",
        padx=18,
        pady=6
    )

    botao_configuracoes = ctk.CTkButton(
        menu_lateral,
        text="Configurações",
        height=42,
        corner_radius=8,
        fg_color="transparent",
        hover_color="#1D6B47",
        anchor="w",
        font=("Segoe UI", 14)
    )

    botao_configuracoes.pack(
        fill="x",
        padx=18,
        pady=6
    )

    botao_sobre = ctk.CTkButton(
        menu_lateral,
        text="Sobre",
        height=42,
        corner_radius=8,
        fg_color="transparent",
        hover_color="#1D6B47",
        anchor="w",
        font=("Segoe UI", 14)
    )

    botao_sobre.pack(
        fill="x",
        padx=18,
        pady=6
    )

    versao = ctk.CTkLabel(
        menu_lateral,
        text="INCD\nAutomação ITI v2.0",
        font=("Segoe UI", 11),
        text_color="#D2E8DC"
    )

    versao.pack(
        side="bottom",
        pady=24
    )

    # ==================================
    # ÁREA PRINCIPAL
    # ==================================

    area_principal = ctk.CTkFrame(
        janela,
        corner_radius=0,
        fg_color="#F4F6F8"
    )

    area_principal.grid(
        row=0,
        column=1,
        sticky="nsew"
    )

    area_principal.grid_columnconfigure(
        0,
        weight=1
    )

    area_principal.grid_rowconfigure(
        0,
        weight=1
    )

    # ==================================
    # PÁGINA DE RELATÓRIOS
    # ==================================

    pagina_relatorios = ctk.CTkFrame(
        area_principal,
        corner_radius=0,
        fg_color="#F4F6F8"
    )

    pagina_relatorios.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    pagina_relatorios.grid_columnconfigure(
        0,
        weight=1
    )

    pagina_relatorios.grid_rowconfigure(
        4,
        weight=1
    )

    # Cabeçalho
    cabecalho = ctk.CTkFrame(
        pagina_relatorios,
        height=90,
        corner_radius=0,
        fg_color="white"
    )

    cabecalho.grid(
        row=0,
        column=0,
        sticky="ew"
    )

    cabecalho.grid_propagate(
        False
    )

    titulo = ctk.CTkLabel(
        cabecalho,
        text="Relatórios de Certificados",
        font=("Segoe UI", 26, "bold"),
        text_color="#1D2939"
    )

    titulo.pack(
        anchor="w",
        padx=35,
        pady=(18, 2)
    )

    descricao = ctk.CTkLabel(
        cabecalho,
        text=(
            "Gere relatórios por mês e região "
            "com resumo e dashboard."
        ),
        font=("Segoe UI", 13),
        text_color="#667085"
    )

    descricao.pack(
        anchor="w",
        padx=35
    )

    # ==================================
    # CARTÕES
    # ==================================

    area_cartoes = ctk.CTkFrame(
        pagina_relatorios,
        fg_color="transparent"
    )

    area_cartoes.grid(
        row=1,
        column=0,
        sticky="ew",
        padx=30,
        pady=(25, 10)
    )

    for coluna in range(3):
        area_cartoes.grid_columnconfigure(
            coluna,
            weight=1
        )

    def criar_cartao(
        coluna,
        titulo_cartao,
        valor,
        descricao_cartao
    ):
        cartao = ctk.CTkFrame(
            area_cartoes,
            height=115,
            corner_radius=12,
            fg_color="white",
            border_width=1,
            border_color="#E4E7EC"
        )

        cartao.grid(
            row=0,
            column=coluna,
            sticky="ew",
            padx=8
        )

        cartao.grid_propagate(
            False
        )

        ctk.CTkLabel(
            cartao,
            text=titulo_cartao,
            font=("Segoe UI", 12),
            text_color="#667085"
        ).pack(
            anchor="w",
            padx=18,
            pady=(14, 2)
        )

        ctk.CTkLabel(
            cartao,
            text=valor,
            font=("Segoe UI", 24, "bold"),
            text_color="#123B2A"
        ).pack(
            anchor="w",
            padx=18
        )

        ctk.CTkLabel(
            cartao,
            text=descricao_cartao,
            font=("Segoe UI", 10),
            text_color="#98A2B3"
        ).pack(
            anchor="w",
            padx=18,
            pady=(2, 8)
        )

    criar_cartao(
        0,
        "Formato",
        "Excel",
        "Dashboard, resumo e dados detalhados"
    )

    criar_cartao(
        1,
        "Filtros",
        "Mês e região",
        "Seleção personalizada dos dados"
    )

    criar_cartao(
        2,
        "Fonte",
        "Portal ITI",
        "Dados baixados automaticamente"
    )

    # ==================================
    # FORMULÁRIO
    # ==================================

    painel_formulario = ctk.CTkFrame(
        pagina_relatorios,
        corner_radius=12,
        fg_color="white",
        border_width=1,
        border_color="#E4E7EC"
    )

    painel_formulario.grid(
        row=2,
        column=0,
        sticky="ew",
        padx=38,
        pady=15
    )

    painel_formulario.grid_columnconfigure(
        0,
        weight=1
    )

    painel_formulario.grid_columnconfigure(
        1,
        weight=1
    )

    ctk.CTkLabel(
        painel_formulario,
        text="Configuração do relatório",
        font=("Segoe UI", 17, "bold"),
        text_color="#1D2939"
    ).grid(
        row=0,
        column=0,
        columnspan=2,
        sticky="w",
        padx=25,
        pady=(20, 18)
    )

    ctk.CTkLabel(
        painel_formulario,
        text="Mês",
        font=("Segoe UI", 12, "bold")
    ).grid(
        row=1,
        column=0,
        sticky="w",
        padx=(25, 12)
    )

    ctk.CTkLabel(
        painel_formulario,
        text="Região",
        font=("Segoe UI", 12, "bold")
    ).grid(
        row=1,
        column=1,
        sticky="w",
        padx=(12, 25)
    )

    meses = [
        "Todos os meses",
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro"
    ]

    combo_mes = ctk.CTkComboBox(
        painel_formulario,
        values=meses,
        height=40
    )

    combo_mes.grid(
        row=2,
        column=0,
        sticky="ew",
        padx=(25, 12),
        pady=(7, 20)
    )

    combo_mes.set(
        "Todos os meses"
    )

    regioes = [
        "Todas",
        "Norte",
        "Nordeste",
        "Centro Oeste",
        "Centro-Oeste",
        "Sudeste",
        "Sul",
        "Exterior",
        "Exceções",
        "Outros"
    ]

    combo_regiao = ctk.CTkComboBox(
        painel_formulario,
        values=regioes,
        height=40
    )

    combo_regiao.grid(
        row=2,
        column=1,
        sticky="ew",
        padx=(12, 25),
        pady=(7, 20)
    )

    combo_regiao.set(
        "Todas"
    )

    # ==================================
    # STATUS
    # ==================================

    status = ctk.CTkLabel(
        pagina_relatorios,
        text="Status: pronto",
        font=("Segoe UI", 12),
        text_color="#475467"
    )

    status.grid(
        row=3,
        column=0,
        pady=(8, 3)
    )

    progresso = ctk.CTkProgressBar(
        pagina_relatorios,
        height=12,
        progress_color="#1D6B47"
    )

    progresso.grid(
        row=4,
        column=0,
        sticky="new",
        padx=90,
        pady=(3, 12)
    )

    progresso.set(0)

    # ==================================
    # CAIXA DE LOG
    # ==================================

    caixa_log = ctk.CTkTextbox(
        pagina_relatorios,
        height=110,
        corner_radius=10,
        border_width=1,
        border_color="#E4E7EC",
        fg_color="white"
    )

    caixa_log.grid(
        row=5,
        column=0,
        sticky="ew",
        padx=38,
        pady=(5, 12)
    )

    caixa_log.insert(
        "end",
        "Sistema pronto para gerar o relatório.\n"
    )

    caixa_log.configure(
        state="disabled"
    )

    def registrar_log(mensagem):
        caixa_log.configure(
            state="normal"
        )

        horario = datetime.now().strftime(
            "%H:%M:%S"
        )

        caixa_log.insert(
            "end",
            f"[{horario}] {mensagem}\n"
        )

        caixa_log.see(
            "end"
        )

        caixa_log.configure(
            state="disabled"
        )

    # ==================================
    # PÁGINA SOBRE
    # ==================================

    pagina_sobre = ctk.CTkFrame(
        area_principal,
        corner_radius=0,
        fg_color="#F4F6F8"
    )

    pagina_sobre.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    pagina_sobre.grid_columnconfigure(
        0,
        weight=1
    )

    cabecalho_sobre = ctk.CTkFrame(
        pagina_sobre,
        height=90,
        corner_radius=0,
        fg_color="white"
    )

    cabecalho_sobre.grid(
        row=0,
        column=0,
        sticky="ew"
    )

    cabecalho_sobre.grid_propagate(
        False
    )

    ctk.CTkLabel(
        cabecalho_sobre,
        text="Sobre o sistema",
        font=("Segoe UI", 26, "bold"),
        text_color="#1D2939"
    ).pack(
        anchor="w",
        padx=35,
        pady=(18, 2)
    )

    ctk.CTkLabel(
        cabecalho_sobre,
        text="Informações da aplicação e do projeto.",
        font=("Segoe UI", 13),
        text_color="#667085"
    ).pack(
        anchor="w",
        padx=35
    )

    cartao_sobre = ctk.CTkFrame(
        pagina_sobre,
        corner_radius=14,
        fg_color="white",
        border_width=1,
        border_color="#E4E7EC"
    )

    cartao_sobre.grid(
        row=1,
        column=0,
        sticky="ew",
        padx=80,
        pady=60
    )

    if CAMINHO_LOGO.exists():
        try:
            imagem_sobre_original = Image.open(
                CAMINHO_LOGO
            )

            imagem_sobre = ctk.CTkImage(
                light_image=imagem_sobre_original,
                dark_image=imagem_sobre_original,
                size=(220, 85)
            )

            ctk.CTkLabel(
                cartao_sobre,
                text="",
                image=imagem_sobre
            ).pack(
                pady=(30, 15)
            )

        except Exception as erro_logo_sobre:
            print(
                "Não foi possível carregar a logo:",
                erro_logo_sobre
            )

    ctk.CTkLabel(
        cartao_sobre,
        text="Automação ITI",
        font=("Segoe UI", 24, "bold"),
        text_color="#123B2A"
    ).pack(
        pady=(5, 4)
    )

    ctk.CTkLabel(
        cartao_sobre,
        text="Versão 2.0",
        font=("Segoe UI", 13, "bold"),
        text_color="#1D6B47"
    ).pack(
        pady=4
    )

    texto_sobre = (
        "Aplicação desenvolvida para extrair dados do Portal ITI, "
        "aplicar filtros por mês e região e gerar relatórios "
        "profissionais em Excel.\n\n"
        "O arquivo gerado contém Dashboard, Resumo "
        "e dados detalhados."
    )

    ctk.CTkLabel(
        cartao_sobre,
        text=texto_sobre,
        font=("Segoe UI", 13),
        text_color="#475467",
        justify="center",
        wraplength=580
    ).pack(
        padx=45,
        pady=(15, 10)
    )

    ctk.CTkLabel(
        cartao_sobre,
        text="Desenvolvido por David de Araujo",
        font=("Segoe UI", 11),
        text_color="#98A2B3"
    ).pack(
        pady=(10, 30)
    )

    # ==================================
    # PÁGINA CONFIGURAÇÕES
    # ==================================

    pagina_configuracoes = ctk.CTkFrame(
        area_principal,
        corner_radius=0,
        fg_color="#F4F6F8"
    )

    pagina_configuracoes.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    pagina_configuracoes.grid_columnconfigure(
        0,
        weight=1
    )

    cabecalho_configuracoes = ctk.CTkFrame(
        pagina_configuracoes,
        height=90,
        corner_radius=0,
        fg_color="white"
    )

    cabecalho_configuracoes.grid(
        row=0,
        column=0,
        sticky="ew"
    )

    cabecalho_configuracoes.grid_propagate(
        False
    )

    ctk.CTkLabel(
        cabecalho_configuracoes,
        text="Configurações",
        font=("Segoe UI", 26, "bold"),
        text_color="#1D2939"
    ).pack(
        anchor="w",
        padx=35,
        pady=(18, 2)
    )

    ctk.CTkLabel(
        cabecalho_configuracoes,
        text="Preferências visuais e opções da aplicação.",
        font=("Segoe UI", 13),
        text_color="#667085"
    ).pack(
        anchor="w",
        padx=35
    )

    painel_configuracoes = ctk.CTkFrame(
        pagina_configuracoes,
        corner_radius=14,
        fg_color="white",
        border_width=1,
        border_color="#E4E7EC"
    )

    painel_configuracoes.grid(
        row=1,
        column=0,
        sticky="ew",
        padx=80,
        pady=60
    )

    painel_configuracoes.grid_columnconfigure(
        0,
        weight=1
    )

    ctk.CTkLabel(
        painel_configuracoes,
        text="Tema da aplicação",
        font=("Segoe UI", 15, "bold"),
        text_color="#1D2939"
    ).grid(
        row=0,
        column=0,
        sticky="w",
        padx=30,
        pady=(30, 8)
    )

    combo_tema = ctk.CTkComboBox(
        painel_configuracoes,
        values=[
            "Claro",
            "Escuro",
            "Sistema"
        ],
        height=40
    )

    combo_tema.grid(
        row=1,
        column=0,
        sticky="ew",
        padx=30,
        pady=(0, 30)
    )

    combo_tema.set(
        "Claro"
    )

    def alterar_tema(tema):
        temas = {
            "Claro": "Light",
            "Escuro": "Dark",
            "Sistema": "System"
        }

        ctk.set_appearance_mode(
            temas.get(
                tema,
                "Light"
            )
        )

    combo_tema.configure(
        command=alterar_tema
    )

    # ==================================
    # FUNÇÕES DE NAVEGAÇÃO
    # ==================================

    def mostrar_relatorios():
        pagina_relatorios.tkraise()

        botao_relatorios.configure(
            fg_color="#1D6B47"
        )

        botao_configuracoes.configure(
            fg_color="transparent"
        )

        botao_sobre.configure(
            fg_color="transparent"
        )

    def mostrar_configuracoes():
        pagina_configuracoes.tkraise()

        botao_relatorios.configure(
            fg_color="transparent"
        )

        botao_configuracoes.configure(
            fg_color="#1D6B47"
        )

        botao_sobre.configure(
            fg_color="transparent"
        )

    def mostrar_sobre():
        pagina_sobre.tkraise()

        botao_relatorios.configure(
            fg_color="transparent"
        )

        botao_configuracoes.configure(
            fg_color="transparent"
        )

        botao_sobre.configure(
            fg_color="#1D6B47"
        )

    # ==================================
    # GERAÇÃO DO RELATÓRIO
    # ==================================

    def gerar_relatorio():
        botao_gerar.configure(
            state="disabled",
            text="GERANDO..."
        )

        progresso.set(0.05)

        status.configure(
            text=(
                "Status: aguardando local "
                "para salvar..."
            )
        )

        registrar_log(
            "Geração do relatório iniciada."
        )

        janela.update_idletasks()

        try:
            data_atual = datetime.now().strftime(
                "%Y-%m-%d"
            )

            nome_sugerido = (
                f"Relatorio_ITI_{data_atual}.xlsx"
            )

            caminho_arquivo = (
                filedialog.asksaveasfilename(
                    title="Salvar relatório",
                    defaultextension=".xlsx",
                    initialfile=nome_sugerido,
                    filetypes=[
                        (
                            "Arquivo Excel",
                            "*.xlsx"
                        )
                    ]
                )
            )

            if not caminho_arquivo:
                progresso.set(0)

                status.configure(
                    text=(
                        "Status: operação cancelada."
                    )
                )

                registrar_log(
                    "Operação cancelada pelo usuário."
                )

                return

            progresso.set(0.15)

            status.configure(
                text="Status: baixando dados..."
            )

            registrar_log(
                "Baixando os dados do Portal ITI."
            )

            janela.update_idletasks()

            dados = baixar_dados()

            progresso.set(0.40)

            registrar_log(
                "Dados baixados com sucesso."
            )

            status.configure(
                text="Status: tratando dados..."
            )

            janela.update_idletasks()

            certificados = obter_certificados(
                dados
            )

            progresso.set(0.60)

            mes_escolhido = combo_mes.get()

            if mes_escolhido != "Todos os meses":
                codigo_mes = MESES[
                    mes_escolhido
                ]

                certificados = filtrar_por_mes(
                    certificados,
                    codigo_mes
                )

            regiao_escolhida = (
                combo_regiao.get()
            )

            certificados = filtrar_por_regiao(
                certificados,
                regiao_escolhida
            )

            progresso.set(0.80)

            registrar_log(
                "Filtros aplicados aos dados."
            )

            if not certificados:
                progresso.set(0)

                status.configure(
                    text=(
                        "Status: nenhum registro "
                        "encontrado."
                    )
                )

                registrar_log(
                    "Nenhum registro encontrado."
                )

                messagebox.showwarning(
                    "Aviso",
                    (
                        "Nenhum registro encontrado "
                        "para os filtros selecionados."
                    )
                )

                return

            status.configure(
                text="Status: criando Excel..."
            )

            progresso.set(0.90)

            registrar_log(
                "Criando o arquivo Excel."
            )

            janela.update_idletasks()

            caminho = criar_excel(
                certificados,
                caminho_arquivo
            )

            progresso.set(1)

            status.configure(
                text=(
                    "Status: relatório concluído."
                )
            )

            registrar_log(
                f"Relatório salvo em: {caminho}"
            )

            janela.update_idletasks()

            messagebox.showinfo(
                "Sucesso",
                (
                    "Relatório gerado com sucesso!\n\n"
                    f"{caminho}"
                )
            )

        except Exception as erro:
            progresso.set(0)

            status.configure(
                text="Status: ocorreu um erro."
            )

            registrar_log(
                f"Erro: {erro}"
            )

            messagebox.showerror(
                "Erro",
                str(erro)
            )

        finally:
            botao_gerar.configure(
                state="normal",
                text="GERAR EXCEL"
            )

    # ==================================
    # BOTÃO GERAR
    # ==================================

    botao_gerar = ctk.CTkButton(
        pagina_relatorios,
        text="GERAR EXCEL",
        height=48,
        width=300,
        corner_radius=10,
        fg_color="#1D6B47",
        hover_color="#24875A",
        font=("Segoe UI", 14, "bold"),
        command=gerar_relatorio
    )

    botao_gerar.grid(
        row=6,
        column=0,
        pady=(8, 25)
    )

    # ==================================
    # CONECTAR O MENU
    # ==================================

    botao_relatorios.configure(
        command=mostrar_relatorios
    )

    botao_configuracoes.configure(
        command=mostrar_configuracoes
    )

    botao_sobre.configure(
        command=mostrar_sobre
    )

    # Abrir inicialmente em Relatórios
    mostrar_relatorios()

    janela.mainloop()