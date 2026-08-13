import customtkinter as ctk

from PIL import Image

from src.version import (
    VERSION
)


def criar_menu(
    janela,
    caminho_logo
):
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

    menu_lateral.grid_propagate(False)

    # ----------------------------
    # Logo
    # ----------------------------

    if caminho_logo.exists():

        try:

            imagem = Image.open(
                caminho_logo
            )

            logo_ctk = ctk.CTkImage(
                light_image=imagem,
                dark_image=imagem,
                size=(180, 70)
            )

            logo = ctk.CTkLabel(
                menu_lateral,
                text="",
                image=logo_ctk
            )

            logo.pack(
                pady=(30, 20)
            )

            logo.logo_ctk = logo_ctk

        except Exception as erro:

            print(
                "Erro ao carregar logo:",
                erro
            )

    titulo = ctk.CTkLabel(
        menu_lateral,
        text="AUTOMAÇÃO ITI",
        font=(
            "Segoe UI",
            20,
            "bold"
        ),
        text_color="white"
    )

    titulo.pack(
        pady=(5, 30)
    )

    # ----------------------------
    # Botões
    # ----------------------------

    botao_relatorios = ctk.CTkButton(
        menu_lateral,
        text="📊  Relatórios",
        height=46,
        corner_radius=8,
        fg_color="#1D6B47",
        hover_color="#24875A",
        anchor="w",
        font=("Segoe UI", 14, "bold")
    )

    botao_relatorios.pack(
        fill="x",
        padx=14,
        pady=6
    )

    botao_configuracoes = ctk.CTkButton(
        menu_lateral,
        text="⚙  Configurações",
        height=46,
        corner_radius=8,
        fg_color="transparent",
        hover_color="#1D6B47",
        anchor="w",
        font=("Segoe UI", 14)
    )

    botao_configuracoes.pack(
        fill="x",
        padx=14,
        pady=6
    )

    botao_sobre = ctk.CTkButton(
        menu_lateral,
        text="ⓘ  Sobre",
        height=46,
        corner_radius=8,
        fg_color="transparent",
        hover_color="#1D6B47",
        anchor="w",
        font=("Segoe UI", 14)
    )

    botao_sobre.pack(
        fill="x",
        padx=14,
        pady=6
    )

    versao = ctk.CTkLabel(
        menu_lateral,
        text=(
    "INCD\n"
    f"Versão {VERSION}"
),
        font=("Segoe UI", 11),
        text_color="#D2E8DC"
    )

    versao.pack(
        side="bottom",
        pady=24
    )

    return {
        "frame": menu_lateral,
        "relatorios": botao_relatorios,
        "configuracoes": botao_configuracoes,
        "sobre": botao_sobre
    }