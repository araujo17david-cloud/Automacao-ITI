import getpass

import customtkinter as ctk

from src.version import (
    APP_NAME,
    VERSION
)


class StatusBar:

    def __init__(
        self,
        master
    ):
        self.frame = ctk.CTkFrame(
            master,
            height=32,
            corner_radius=0,
            fg_color="#E9EEF2"
        )

        self.frame.grid_propagate(
            False
        )

        self.frame.grid_columnconfigure(
            0,
            weight=1
        )

        usuario = getpass.getuser()

        self.texto_status = ctk.CTkLabel(
            self.frame,
            text=(
                f"Pronto | Usuário: {usuario}"
            ),
            font=("Segoe UI", 10),
            text_color="#475467"
        )

        self.texto_status.grid(
            row=0,
            column=0,
            sticky="w",
            padx=15
        )

        self.texto_versao = ctk.CTkLabel(
            self.frame,
            text=f"{APP_NAME} • v{VERSION}",
            font=("Segoe UI", 10),
            text_color="#667085"
        )

        self.texto_versao.grid(
            row=0,
            column=1,
            sticky="e",
            padx=15
        )

    def atualizar(
        self,
        texto
    ):
        self.texto_status.configure(
            text=texto
        )