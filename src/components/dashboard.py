import customtkinter as ctk


class Dashboard:

    def __init__(self, master):

        self.frame = ctk.CTkFrame(
            master,
            fg_color="transparent"
        )

        self.icones = {
            "Certificados": "🛡",
            "Regiões": "📍",
            "Última geração": "📅",
            "Arquivos": "📄"
        }

        self.frame.grid_columnconfigure(
            (0, 1, 2, 3),
            weight=1
        )

        self.cartoes = {}

        self.tipo_geracao = None

        self._criar_cartao(
            0,
            "Certificados",
            "0"
        )

        self._criar_cartao(
            1,
            "Regiões",
            "0"
        )

        self._criar_cartao(
            2,
            "Última geração",
            "--"
        )

        self._criar_cartao(
            3,
            "Arquivos",
            "0"
        )

    def _criar_cartao(
        self,
        coluna,
        titulo,
        valor
    ):

        cartao = ctk.CTkFrame(
            self.frame,
            height=105,
            corner_radius=12,
            fg_color="white",
            border_width=1,
            border_color="#E4E7EC"
        )

        cartao.grid(
            row=0,
            column=coluna,
            padx=8,
            sticky="nsew"
        )

        cartao.grid_propagate(
            False
        )

        titulo_label = ctk.CTkLabel(
            cartao,
            text=(
                f"{self.icones.get(titulo, '')}  "
                f"{titulo}"
            ),
            font=("Segoe UI", 12),
            text_color="#667085"
        )

        titulo_label.pack(
            anchor="w",
            padx=18,
            pady=(15, 2)
        )

        valor_label = ctk.CTkLabel(
            cartao,
            text=valor,
            font=("Segoe UI", 23, "bold"),
            text_color="#0F5C3C"
        )

        valor_label.pack(
            anchor="w",
            padx=18
        )

        self.cartoes[
            titulo
        ] = valor_label

        # ============================
        # TIPO DA ÚLTIMA GERAÇÃO
        # ============================

        if titulo == "Última geração":

            self.tipo_geracao = ctk.CTkLabel(
                cartao,
                text="Tipo: --",
                font=("Segoe UI", 10, "bold"),
                text_color="#667085"
            )

            self.tipo_geracao.pack(
                anchor="w",
                padx=18,
                pady=(2, 0)
            )

    def atualizar(
        self,
        certificados,
        regioes,
        ultima,
        arquivos,
        tipo="--"
    ):

        self.cartoes[
            "Certificados"
        ].configure(
            text=(
                f"{certificados:,}"
                .replace(",", ".")
            )
        )

        self.cartoes[
            "Regiões"
        ].configure(
            text=str(
                regioes
            )
        )

        self.cartoes[
            "Última geração"
        ].configure(
            text=ultima
        )

        self.cartoes[
            "Arquivos"
        ].configure(
            text=str(
                arquivos
            )
        )

        if self.tipo_geracao:

            self.tipo_geracao.configure(
                text=f"Tipo: {tipo}"
            )