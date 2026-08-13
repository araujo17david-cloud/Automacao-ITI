from datetime import datetime
from tkinter import (
    filedialog,
    messagebox
)

import customtkinter as ctk

from src.services.automatico import (
    gerar_relatorio_automatico
)

from src.services.agendamento_service import (
    criar_agendamento,
    remover_agendamento
)

from src.services.config_service import (
    carregar_config,
    salvar_config
)


def criar_pagina_configuracoes(
    area_principal
):

    config = carregar_config()
    
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

    # ============================
    # CABEÇALHO
    # ============================

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
        text=(
            "Preferências visuais "
            "e opções da aplicação."
        ),
        font=("Segoe UI", 13),
        text_color="#667085"
    ).pack(
        anchor="w",
        padx=35
    )

    # ============================
    # ÁREA COM ROLAGEM
    # ============================

    area_scroll = ctk.CTkScrollableFrame(
        pagina_configuracoes,
        corner_radius=0,
        fg_color="#F4F6F8"
    )

    area_scroll.grid(
        row=1,
        column=0,
        sticky="nsew"
    )

    area_scroll.grid_columnconfigure(
        0,
        weight=1
    )

    pagina_configuracoes.grid_rowconfigure(
        1,
        weight=1
    )

    # ============================
    # PAINEL
    # ============================

    painel_configuracoes = ctk.CTkFrame(
        area_scroll,
        corner_radius=14,
        fg_color="white",
        border_width=1,
        border_color="#E4E7EC"
    )

    painel_configuracoes.grid(
        row=0,
        column=0,
        sticky="ew",
        padx=80,
        pady=(40, 40)
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

    temas_interface = {
        "Light": "Claro",
        "Dark": "Escuro",
        "System": "Sistema"
    }

    tema_atual = config.get(
        "tema",
        "Light"
    )

    combo_tema.set(
        temas_interface.get(
            tema_atual,
            "Claro"
        )
    )

    def alterar_tema(tema):
        temas = {
            "Claro": "Light",
            "Escuro": "Dark",
            "Sistema": "System"
        }

        tema_sistema = temas.get(
            tema,
            "Light"
        )

        ctk.set_appearance_mode(
            tema_sistema
        )

        config["tema"] = tema_sistema

        salvar_config(
            config
        )

        ctk.set_appearance_mode(
            temas.get(
                tema,
                "Light"
            )
        )

    combo_tema.configure(
        command=alterar_tema
    )

    ctk.CTkLabel(
        painel_configuracoes,
        text="Pasta padrão dos relatórios",
        font=("Segoe UI", 15, "bold"),
        text_color="#1D2939"
    ).grid(
        row=2,
        column=0,
        sticky="w",
        padx=30,
        pady=(10, 8)
    )

    entrada_pasta = ctk.CTkEntry(
        painel_configuracoes,
        height=40
    )

    entrada_pasta.grid(
        row=3,
        column=0,
        sticky="ew",
        padx=30,
        pady=(0, 10)
    )

    entrada_pasta.insert(
        0,
        config.get(
            "pasta_relatorios",
            "relatorios"
        )
    )

    def escolher_pasta():
        pasta = filedialog.askdirectory(
            title="Escolha a pasta padrão dos relatórios"
        )

        if not pasta:
            return

        entrada_pasta.delete(
            0,
            "end"
        )

        entrada_pasta.insert(
            0,
            pasta
        )

        config["pasta_relatorios"] = pasta

        salvar_config(
            config
        )

    botao_pasta = ctk.CTkButton(
        painel_configuracoes,
        text="Escolher pasta",
        height=40,
        fg_color="#1D6B47",
        hover_color="#24875A",
        command=escolher_pasta
    )

    botao_pasta.grid(
        row=4,
        column=0,
        sticky="w",
        padx=30,
        pady=(0, 30)
    )

        # ============================
    # AGENDAMENTO MENSAL
    # ============================

    ctk.CTkLabel(
        painel_configuracoes,
        text="Geração automática mensal",
        font=("Segoe UI", 15, "bold"),
        text_color="#1D2939"
    ).grid(
        row=5,
        column=0,
        sticky="w",
        padx=30,
        pady=(15, 8)
    )

    switch_agendamento = ctk.CTkSwitch(
        painel_configuracoes,
        text="Ativar geração automática mensal",
        onvalue=True,
        offvalue=False
    )

    switch_agendamento.grid(
        row=6,
        column=0,
        sticky="w",
        padx=30,
        pady=(0, 15)
    )

    if config.get(
        "agendamento_ativo",
        False
    ):
        switch_agendamento.select()

    else:
        switch_agendamento.deselect()

    ctk.CTkLabel(
        painel_configuracoes,
        text="Dia do mês",
        font=("Segoe UI", 12, "bold"),
        text_color="#475467"
    ).grid(
        row=7,
        column=0,
        sticky="w",
        padx=30,
        pady=(5, 5)
    )

    dias = [
        str(numero)
        for numero in range(
            1,
            29
        )
    ]

    combo_dia = ctk.CTkComboBox(
        painel_configuracoes,
        values=dias,
        height=40
    )

    combo_dia.grid(
        row=8,
        column=0,
        sticky="ew",
        padx=30,
        pady=(0, 15)
    )

    combo_dia.set(
        str(
            config.get(
                "dia_agendamento",
                1
            )
        )
    )

    ctk.CTkLabel(
        painel_configuracoes,
        text="Horário",
        font=("Segoe UI", 12, "bold"),
        text_color="#475467"
    ).grid(
        row=9,
        column=0,
        sticky="w",
        padx=30,
        pady=(5, 5)
    )

    entrada_horario = ctk.CTkEntry(
        painel_configuracoes,
        height=40,
        placeholder_text="08:00"
    )

    entrada_horario.grid(
        row=10,
        column=0,
        sticky="ew",
        padx=30,
        pady=(0, 15)
    )

    entrada_horario.insert(
        0,
        config.get(
            "horario_agendamento",
            "08:00"
        )
    )

    def calcular_proxima_execucao(
        dia,
        horario
    ):
        agora = datetime.now()

        hora, minuto = map(
            int,
            horario.split(":")
        )

        ano = agora.year
        mes = agora.month

        proxima = datetime(
            ano,
            mes,
            dia,
            hora,
            minuto
        )

        if proxima <= agora:
            if mes == 12:
                ano += 1
                mes = 1

            else:
                mes += 1

            proxima = datetime(
                ano,
                mes,
                dia,
                hora,
                minuto
            )

        return proxima.strftime(
            "%d/%m/%Y às %H:%M"
        )

    def salvar_agendamento():
        try:
            dia = int(
                combo_dia.get()
            )

            horario = (
                entrada_horario
                .get()
                .strip()
            )

            partes = horario.split(":")

            if len(partes) != 2:
                raise ValueError(
                    "Horário inválido."
                )

            hora = int(
                partes[0]
            )

            minuto = int(
                partes[1]
            )

            if not (
                0 <= hora <= 23
                and
                0 <= minuto <= 59
            ):
                raise ValueError(
                    "Horário inválido."
                )

            horario = (
                f"{hora:02d}:"
                f"{minuto:02d}"
            )

            ativo = (
                switch_agendamento.get()
            )

            if ativo:
                criar_agendamento(
                    dia,
                    horario
                )

            else:
                remover_agendamento()

            config[
                "agendamento_ativo"
            ] = bool(
                ativo
            )

            config[
                "dia_agendamento"
            ] = dia

            config[
                "horario_agendamento"
            ] = horario

            salvar_config(
                config
            )

            if ativo:
                proxima = calcular_proxima_execucao(
                    dia,
                    horario
                )

                label_proxima_execucao.configure(
                    text=(
                        "Próxima execução prevista: "
                        f"{proxima}"
                    )
                )

            else:
                label_proxima_execucao.configure(
                    text=(
                        "Próxima execução prevista: "
                        "agendamento desativado"
                    )
                )

            entrada_horario.delete(
                0,
                "end"
            )

            entrada_horario.insert(
                0,
                horario
            )

            messagebox.showinfo(
                "Agendamento",
                (
                    "Configuração do agendamento "
                    "salva com sucesso."
                )
            )

        except ValueError:
            messagebox.showwarning(
                "Horário inválido",
                (
                    "Informe um horário válido "
                    "no formato HH:MM.\n\n"
                    "Exemplo: 08:00"
                )
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                (
                    "Não foi possível configurar "
                    "a geração automática.\n\n"
                    f"{erro}"
                )
            )

    def executar_agora():
        try:
            resposta = messagebox.askyesno(
                "Executar agora",
                (
                    "Deseja executar agora a "
                    "geração automática do relatório?"
                )
            )

            if not resposta:
                return

            caminho = (
                gerar_relatorio_automatico()
            )

            if caminho:
                messagebox.showinfo(
                    "Concluído",
                    (
                        "Geração automática concluída.\n\n"
                        f"{caminho}"
                    )
                )

            else:
                messagebox.showinfo(
                    "Informação",
                    (
                        "Nenhum novo relatório "
                        "precisou ser gerado."
                    )
                )

            config_atualizada = (
                carregar_config()
            )

            ultima_execucao = (
                config_atualizada.get(
                    "ultima_execucao_automatica",
                    "--"
                )
            )

            label_ultima_execucao.configure(
                text=(
                    "Última execução automática: "
                    f"{ultima_execucao}"
                )
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                (
                    "Não foi possível executar "
                    "a geração automática.\n\n"
                    f"{erro}"
                )
            )

    # ============================
    # INFORMAÇÕES DO AGENDAMENTO
    # ============================

    quadro_agendamento = ctk.CTkFrame(
        painel_configuracoes,
        corner_radius=10,
        fg_color="#F8FAFC",
        border_width=1,
        border_color="#E4E7EC"
    )

    quadro_agendamento.grid(
        row=11,
        column=0,
        sticky="ew",
        padx=30,
        pady=(5, 15)
    )

    quadro_agendamento.grid_columnconfigure(
        0,
        weight=1
    )

    
    label_proxima_execucao = ctk.CTkLabel(
        quadro_agendamento,
        text="Próxima execução prevista: --",
        font=("Segoe UI", 12, "bold"),
        text_color="#1D2939"
    )

    label_proxima_execucao.pack(
        anchor="w",
        padx=18,
        pady=(15, 5)
    )

    label_ultima_execucao = ctk.CTkLabel(
        quadro_agendamento,
        text=(
            "Última execução automática: "
            f"{config.get(
                'ultima_execucao_automatica',
                '--'
            )}"
        ),
        font=("Segoe UI", 11),
        text_color="#667085"
    )

    label_ultima_execucao.pack(
        anchor="w",
        padx=18,
        pady=(0, 15)
    )

    if config.get(
        "agendamento_ativo",
        False
    ):
        try:
            proxima = calcular_proxima_execucao(
                int(
                    config.get(
                        "dia_agendamento",
                        1
                    )
                ),
                config.get(
                    "horario_agendamento",
                    "08:00"
                )
            )

            label_proxima_execucao.configure(
                text=(
                    "Próxima execução prevista: "
                    f"{proxima}"
                )
            )

        except Exception:
            label_proxima_execucao.configure(
                text=(
                    "Próxima execução prevista: "
                    "não disponível"
                )
            )

    else:
        label_proxima_execucao.configure(
            text=(
                "Próxima execução prevista: "
                "agendamento desativado"
            )
        )

    # ============================
    # BOTÕES DO AGENDAMENTO
    # ============================

    area_botoes_agendamento = ctk.CTkFrame(
        painel_configuracoes,
        fg_color="transparent"
    )

    area_botoes_agendamento.grid(
        row=12,
        column=0,
        sticky="w",
        padx=30,
        pady=(0, 30)
    )    

    botao_salvar_agendamento = ctk.CTkButton(
        area_botoes_agendamento,
        text="Salvar agendamento",
        height=40,
        fg_color="#1D6B47",
        hover_color="#24875A",
        command=salvar_agendamento
    )

    botao_salvar_agendamento.pack(
        side="left"
    )

    botao_executar_agora = ctk.CTkButton(
        area_botoes_agendamento,
        text="Executar agora",
        height=40,
        fg_color="#475467",
        hover_color="#344054",
        command=executar_agora
    )

    botao_executar_agora.pack(
        side="left",
        padx=(10, 0)
    )

    return pagina_configuracoes