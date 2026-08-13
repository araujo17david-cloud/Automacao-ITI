import customtkinter as ctk

from PIL import Image

from src.version import (
    APP_NAME,
    COMPANY,
    COPYRIGHT,
    DESCRIPTION,
    VERSION
)


def criar_pagina_sobre(
    area_principal,
    caminho_logo
):
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

    # ============================
    # CABEÇALHO
    # ============================

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

    # ============================
    # CARTÃO SOBRE
    # ============================

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

    # ============================
    # LOGO
    # ============================

    if caminho_logo.exists():
        try:
            imagem_original = Image.open(
                caminho_logo
            )

            imagem_sobre = ctk.CTkImage(
                light_image=imagem_original,
                dark_image=imagem_original,
                size=(220, 85)
            )

            logo = ctk.CTkLabel(
                cartao_sobre,
                text="",
                image=imagem_sobre
            )

            logo.pack(
                pady=(30, 15)
            )

            # Mantém referência da imagem
            logo.imagem_sobre = imagem_sobre

        except Exception as erro:
            print(
                "Não foi possível carregar "
                f"a logo da tela Sobre: {erro}"
            )

    # ============================
    # NOME DA APLICAÇÃO
    # ============================

    ctk.CTkLabel(
        cartao_sobre,
        text=APP_NAME,
        font=("Segoe UI", 24, "bold"),
        text_color="#123B2A"
    ).pack(
        pady=(5, 4)
    )

    # ============================
    # VERSÃO
    # ============================

    ctk.CTkLabel(
        cartao_sobre,
        text=f"Versão {VERSION}",
        font=("Segoe UI", 13, "bold"),
        text_color="#1D6B47"
    ).pack(
        pady=4
    )

    # ============================
    # DESCRIÇÃO
    # ============================

    ctk.CTkLabel(
        cartao_sobre,
        text=DESCRIPTION,
        font=("Segoe UI", 13),
        text_color="#475467",
        justify="center",
        wraplength=580
    ).pack(
        padx=45,
        pady=(15, 10)
    )

    # ============================
    # EMPRESA E COPYRIGHT
    # ============================

    ctk.CTkLabel(
        cartao_sobre,
        text=(
            f"{COMPANY}\n"
            f"{COPYRIGHT}"
        ),
        font=("Segoe UI", 11),
        text_color="#98A2B3"
    ).pack(
        pady=(10, 30)
    )

    return pagina_sobre