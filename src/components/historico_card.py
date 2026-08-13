import os

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

        # -----------------------------
        # Nome do arquivo
        # -----------------------------

        ctk.CTkLabel(
            self,
            text=f"📄 {arquivo.name}",
            font=("Segoe UI", 14, "bold"),
            anchor="w"
        ).pack(
            fill="x",
            padx=18,
            pady=(15, 5)
        )

        # -----------------------------
        # Data
        # -----------------------------

        from datetime import datetime

        data = datetime.fromtimestamp(
            arquivo.stat().st_mtime
        )

        ctk.CTkLabel(
            self,
            text=data.strftime(
                "%d/%m/%Y %H:%M"
            ),
            font=("Segoe UI", 11),
            text_color="#667085"
        ).pack(
            anchor="w",
            padx=18
        )

        # -----------------------------
        # Botões
        # -----------------------------

        area = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        area.pack(
            fill="x",
            padx=18,
            pady=(12, 15)
        )

        ctk.CTkButton(
            area,
            text="Abrir",
            width=100,
            fg_color="#1D6B47",
            hover_color="#24875A",
            command=self.abrir
        ).pack(
            side="left"
        )

        ctk.CTkButton(
            area,
            text="Pasta",
            width=100,
            fg_color="#475467",
            hover_color="#344054",
            command=self.abrir_pasta
        ).pack(
            side="left",
            padx=8
        )

    def abrir(self):

        os.startfile(
            self.arquivo
        )

    def abrir_pasta(self):

        os.startfile(
            self.arquivo.parent
        )