import customtkinter as ctk

from src.gui.tema import (
    FONTE_NORMAL,
    FONTE_TITULO
)


def criar_titulo(janela):
    return ctk.CTkLabel(
        janela,
        text="AUTOMAÇÃO ITI",
        font=FONTE_TITULO
    )


def criar_descricao(janela):
    return ctk.CTkLabel(
        janela,
        text="Gere o relatório de certificados mensais por região.",
        font=FONTE_NORMAL
    )