from pathlib import Path

import customtkinter as ctk

from src.components.historico_card import HistoricoCard


class HistoricoRelatorios:

    def __init__(
        self,
        master,
        limite=5
    ):
        self.limite = limite
        self.arquivos = []

        self.frame = ctk.CTkFrame(
            master,
            corner_radius=12,
            fg_color="white",
            border_width=1,
            border_color="#E4E7EC"
        )

        # ============================
        # TÍTULO
        # ============================

        titulo = ctk.CTkLabel(
            self.frame,
            text="Relatórios recentes",
            font=("Segoe UI", 16, "bold"),
            text_color="#1D2939"
        )

        titulo.pack(
            anchor="w",
            padx=20,
            pady=(15, 10)
        )

        # ============================
        # ÁREA DOS CARTÕES
        # ============================

        self.area_cartoes = (
            ctk.CTkScrollableFrame(
                self.frame,
                height=220,
                fg_color="transparent"
            )
        )

        self.area_cartoes.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=(0, 15)
)

    def atualizar(
        self,
        pasta
    ):
        pasta = Path(pasta)

        # Limpar cartões antigos
        for widget in (
            self.area_cartoes.winfo_children()
        ):
            widget.destroy()

        if not pasta.exists():
            self.arquivos = []

            self._mostrar_vazio()

            return

        arquivos = list(
            pasta.glob("*.xlsx")
        )

        arquivos.sort(
            key=lambda arquivo: (
                arquivo.stat().st_mtime
            ),
            reverse=True
        )

        self.arquivos = arquivos[
            :self.limite
        ]

        if not self.arquivos:
            self._mostrar_vazio()

            return

        # Criar um cartão por arquivo
        for arquivo in self.arquivos:
            cartao = HistoricoCard(
                self.area_cartoes,
                arquivo
            )

            cartao.pack(
                fill="x",
                padx=5,
                pady=6
            )

    def _mostrar_vazio(self):
        mensagem = ctk.CTkLabel(
            self.area_cartoes,
            text=(
                "Nenhum relatório "
                "encontrado."
            ),
            font=("Segoe UI", 12),
            text_color="#667085"
        )

        mensagem.pack(
            pady=30
        )