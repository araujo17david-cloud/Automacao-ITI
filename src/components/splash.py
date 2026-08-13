import customtkinter as ctk

from PIL import Image

from src.version import APP_NAME, VERSION


class SplashScreen:

    def __init__(
        self,
        master,
        caminho_logo=None
    ):
        self.janela = ctk.CTkToplevel(master)

        self.janela.overrideredirect(True)
        self.janela.attributes("-topmost", True)

        largura = 420
        altura = 300

        largura_tela = self.janela.winfo_screenwidth()
        altura_tela = self.janela.winfo_screenheight()

        pos_x = (largura_tela - largura) // 2
        pos_y = (altura_tela - altura) // 2

        self.janela.geometry(
            f"{largura}x{altura}+{pos_x}+{pos_y}"
        )

        self.janela.configure(
            fg_color="#123B2A"
        )

        if caminho_logo and caminho_logo.exists():
            try:
                imagem = Image.open(caminho_logo)

                imagem_logo = ctk.CTkImage(
                    light_image=imagem,
                    dark_image=imagem,
                    size=(180, 70)
                )

                logo = ctk.CTkLabel(
                    self.janela,
                    text="",
                    image=imagem_logo
                )

                logo.pack(
                    pady=(35, 15)
                )

                logo.imagem_logo = imagem_logo

            except Exception as erro:
                print(
                    "Erro ao carregar logo da Splash:",
                    erro
                )

        ctk.CTkLabel(
            self.janela,
            text=APP_NAME,
            font=("Segoe UI", 24, "bold"),
            text_color="white"
        ).pack(
            pady=(5, 3)
        )

        ctk.CTkLabel(
            self.janela,
            text=f"Versão {VERSION}",
            font=("Segoe UI", 12),
            text_color="#D2E8DC"
        ).pack()

        self.status = ctk.CTkLabel(
            self.janela,
            text="Carregando...",
            font=("Segoe UI", 11),
            text_color="#D2E8DC"
        )

        self.status.pack(
            pady=(25, 8)
        )

        self.progresso = ctk.CTkProgressBar(
            self.janela,
            width=280,
            height=8,
            progress_color="#55B685"
        )

        self.progresso.pack()

        self.progresso.set(0)

        self.janela.update_idletasks()
        self.janela.update()

    def atualizar(
        self,
        texto,
        progresso
    ):
        if not self.janela.winfo_exists():
            return

        self.status.configure(
            text=texto
        )

        self.progresso.set(
            progresso
        )

        self.janela.update_idletasks()
        self.janela.update()

    def fechar(self):
        if self.janela.winfo_exists():
            self.janela.destroy()