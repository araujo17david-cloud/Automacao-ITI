import os

from datetime import datetime

import customtkinter as ctk


class HistoricoCard(ctk.CTkFrame):

    def __init__(
        self,
        master,
        arquivo
    ):
        super().__init__(
            master,
            corner_radius=10,
            fg_color="white",
            border_width=1,
            border_color="#E4E7EC"
        )

        self.arquivo = arquivo

        # ==================================
        # NOME DO ARQUIVO
        # ==================================

        ctk.CTkLabel(
            self,
            text=f"📄  {arquivo.name}",
            font=("Segoe UI", 14, "bold"),
            text_color="#1D2939",
            anchor="w"
        ).pack(
            fill="x",
            padx=18,
            pady=(15, 5)
        )

        # ==================================
        # DATA DE MODIFICAÇÃO
        # ==================================

        data = datetime.fromtimestamp(
            arquivo.stat().st_mtime
        )

        texto_data = data.strftime(
            "%d/%m/%Y às %H:%M"
        )

        ctk.CTkLabel(
            self,
            text=f"Gerado em: {texto_data}",
            font=("Segoe UI", 11),
            text_color="#667085"
        ).pack(
            anchor="w",
            padx=18
        )

        # ==================================
        # TAMANHO
        # ==================================

        tamanho_mb = (
            arquivo.stat().st_size
            / 1024
            / 1024
        )

        tamanho_formatado = (
            f"{tamanho_mb:.2f}"
            .replace(".", ",")
        )

        ctk.CTkLabel(
            self,
            text=f"Tamanho: {tamanho_formatado} MB",
            font=("Segoe UI", 11),
            text_color="#667085"
        ).pack(
            anchor="w",
            padx=18,
            pady=(3, 0)
        )

        # ==================================
        # BOTÕES
        # ==================================

        area_botoes = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        area_botoes.pack(
            fill="x",
            padx=18,
            pady=(12, 15)
        )

        botao_abrir = ctk.CTkButton(
            area_botoes,
            text="Abrir",
            width=110,
            height=34,
            fg_color="#1D6B47",
            hover_color="#24875A",
            command=self.abrir
        )

        botao_abrir.pack(
            side="left"
        )

        botao_pasta = ctk.CTkButton(
            area_botoes,
            text="Abrir pasta",
            width=110,
            height=34,
            fg_color="#475467",
            hover_color="#344054",
            command=self.abrir_pasta
        )

        botao_pasta.pack(
            side="left",
            padx=(8, 0)
        )

    def abrir(self):
        try:
            os.startfile(
                str(self.arquivo)
            )

        except OSError as erro:
            print(
                "Não foi possível abrir "
                f"o arquivo: {erro}"
            )

    def abrir_pasta(self):
        try:
            os.startfile(
                str(self.arquivo.parent)
            )

        except OSError as erro:
            print(
                "Não foi possível abrir "
                f"a pasta: {erro}"
            )