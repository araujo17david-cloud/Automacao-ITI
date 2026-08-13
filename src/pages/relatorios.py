from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

import time

from src.api.download import baixar_dados
from src.components.dashboard import Dashboard
from src.components.historico import HistoricoRelatorios
from src.excel.excel import criar_excel
from src.services.config_service import (
    carregar_config
)
from src.services.dashboard_service import (
    carregar_dashboard,
    salvar_dashboard
)
from src.services.logger_service import logger
from src.services.tratamento import (
    filtrar_por_mes,
    filtrar_por_regiao,
    obter_certificados
)
from src.utils.meses import MESES


def criar_pagina_relatorios(
    area_principal,
    statusbar=None
):

    config = carregar_config()

    pasta_padrao = Path(
        config.get(
            "pasta_relatorios",
            "relatorios"
        )
    )

    pasta_padrao.mkdir(
        parents=True,
        exist_ok=True
    )
    
    pagina_relatorios = ctk.CTkFrame(
        area_principal,
        corner_radius=0,
        fg_color="#F4F6F8"
    )

    pagina_relatorios.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    pagina_relatorios.grid_columnconfigure(
        0,
        weight=1
    )

    pagina_relatorios.grid_rowconfigure(
        3,
        weight=1
    )

    # ============================
    # CABEÇALHO
    # ============================

    cabecalho = ctk.CTkFrame(
        pagina_relatorios,
        height=90,
        corner_radius=0,
        fg_color="white"
    )

    cabecalho.grid(
        row=0,
        column=0,
        sticky="ew"
    )

    cabecalho.grid_propagate(
        False
    )

    ctk.CTkLabel(
        cabecalho,
        text="Relatórios de Certificados",
        font=("Segoe UI", 28, "bold"),
        text_color="#1D2939"
    ).pack(
        anchor="w",
        padx=35,
        pady=(18, 2)
    )

    ctk.CTkLabel(
        cabecalho,
        text=(
            "Gere relatórios por mês e região "
            "com resumo e dashboard."
        ),
        font=("Segoe UI", 13),
        text_color="#5F6B7A"
    ).pack(
        anchor="w",
        padx=35
    )

        # ============================
    # DASHBOARD
    # ============================

    dashboard = Dashboard(
        pagina_relatorios
    )

    dashboard.frame.grid(
    row=1,
    column=0,
    sticky="ew",
    padx=30,
    pady=(20, 10)
)

    dados_dashboard = carregar_dashboard()

    dashboard.atualizar(
        certificados=dados_dashboard[
            "certificados"
        ],
        regioes=dados_dashboard[
            "regioes"
        ],
        ultima=dados_dashboard[
            "ultima"
        ],
        arquivos=dados_dashboard[
            "arquivos"
        ],
        tipo=dados_dashboard.get(
        "tipo",
        "--"
        )
    )

    # ============================
    # FORMULÁRIO
    # ============================

    painel_formulario = ctk.CTkFrame(
        pagina_relatorios,
        corner_radius=12,
        fg_color="white",
        border_width=1,
        border_color="#E4E7EC"
    )

    painel_formulario.grid(
    row=2,
    column=0,
    sticky="ew",
    padx=30,
    pady=(10, 15)
)

    painel_formulario.grid_columnconfigure(
        0,
        weight=1
    )

    painel_formulario.grid_columnconfigure(
        1,
        weight=1
    )

    ctk.CTkLabel(
        painel_formulario,
        text="Configuração do relatório",
        font=("Segoe UI", 17, "bold"),
        text_color="#1D2939"
    ).grid(
        row=0,
        column=0,
        columnspan=2,
        sticky="w",
        padx=25,
        pady=(20, 18)
    )

    ctk.CTkLabel(
        painel_formulario,
        text="Mês",
        font=("Segoe UI", 12, "bold")
    ).grid(
        row=1,
        column=0,
        sticky="w",
        padx=(25, 12)
    )

    ctk.CTkLabel(
        painel_formulario,
        text="Região",
        font=("Segoe UI", 12, "bold")
    ).grid(
        row=1,
        column=1,
        sticky="w",
        padx=(12, 25)
    )

    meses = [
        "Todos os meses",
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro"
    ]

    combo_mes = ctk.CTkComboBox(
        painel_formulario,
        values=meses,
        height=40
    )

    combo_mes.grid(
        row=2,
        column=0,
        sticky="ew",
        padx=(25, 12),
        pady=(7, 15)
    )

    combo_mes.set(
        "Todos os meses"
    )

    regioes = [
        "Todas",
        "Norte",
        "Nordeste",
        "Centro Oeste",
        "Centro-Oeste",
        "Sudeste",
        "Sul",
        "Exterior",
        "Exceções",
        "Outros"
    ]

    combo_regiao = ctk.CTkComboBox(
        painel_formulario,
        values=regioes,
        height=40
    )

    combo_regiao.grid(
        row=2,
        column=1,
        sticky="ew",
        padx=(12, 25),
        pady=(7, 15)
    )

    combo_regiao.set(
        "Todas"
    )

    # ============================
    # STATUS
    # ============================

        # ==================================
    # ÁREA INFERIOR
    # ==================================

    area_inferior = ctk.CTkFrame(
        pagina_relatorios,
        fg_color="transparent"
    )

    area_inferior.grid(
        row=3,
        column=0,
        sticky="nsew",
        padx=30,
        pady=(10, 25)
    )

    area_inferior.grid_columnconfigure(
        0,
        weight=1,
        uniform="colunas"
    )

    area_inferior.grid_columnconfigure(
        1,
        weight=1,
        uniform="colunas"
    )

    area_inferior.grid_rowconfigure(
        0,
        weight=1
    )

    coluna_esquerda = ctk.CTkFrame(
        area_inferior,
        corner_radius=12,
        fg_color="white",
        border_width=1,
        border_color="#E4E7EC"
    )

    coluna_esquerda.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=(0, 10)
    )

    coluna_esquerda.grid_columnconfigure(
        0,
        weight=1
    )

    coluna_esquerda.grid_rowconfigure(
        2,
        weight=1
    )

    status = ctk.CTkLabel(
        coluna_esquerda,
        text="Status: pronto",
        font=("Segoe UI", 12),
        text_color="#475467"
    )

    status.grid(
        row=0,
        column=0,
        pady=(25, 8)
    )

    progresso = ctk.CTkProgressBar(
        coluna_esquerda,
        height=12,
        progress_color="#1D6B47"
    )

    progresso.grid(
        row=1,
        column=0,
        sticky="ew",
        padx=30,
        pady=(5, 15)
    )

    progresso.set(0)

    coluna_direita = ctk.CTkFrame(
        area_inferior,
        fg_color="transparent"
    )

    coluna_direita.grid(
        row=0,
        column=1,
        sticky="nsew",
        padx=(10, 0)
    )

    coluna_direita.grid_columnconfigure(
        0,
        weight=1
    )

    coluna_direita.grid_rowconfigure(
        0,
        weight=1
    )

    # ============================
    # LOG
    # ============================

    caixa_log = ctk.CTkTextbox(
    coluna_esquerda,
        height=120,
        corner_radius=10,
        border_width=1,
        border_color="#E4E7EC",
        fg_color="white"
    )

    caixa_log.grid(
        row=2,
        column=0,
        sticky="nsew",
        padx=20,
        pady=(0, 12)
    )

    caixa_log.insert(
        "end",
        "Sistema pronto para gerar o relatório.\n"
    )

    caixa_log.configure(
        state="disabled"
    )

    def registrar_log(mensagem):
        caixa_log.configure(
            state="normal"
        )

        horario = datetime.now().strftime(
            "%H:%M:%S"
        )

        caixa_log.insert(
            "end",
            f"[{horario}] {mensagem}\n"
        )

        caixa_log.see(
            "end"
        )

        caixa_log.configure(
            state="disabled"
        )

    # ============================
    # HISTÓRICO DE RELATÓRIOS
    # ============================

    historico = HistoricoRelatorios(
        coluna_direita,
        limite=5
    )

    historico.frame.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    
    historico.atualizar(
        pasta_padrao
    )

    # ============================
    # GERAR RELATÓRIO
    # ============================

    def gerar_relatorio():
        inicio = time.perf_counter()

        logger.info(
            "Início da geração do relatório."
        )

        logger.info(
            f"Pasta padrão dos relatórios: "
            f"{pasta_padrao}"
        )

        botao_gerar.configure(
            state="disabled",
            text="GERANDO..."
        )

        progresso.set(0.05)

        status.configure(
            text=(
                "Status: aguardando local "
                "para salvar..."
            )
        )

        registrar_log(
            "Geração do relatório iniciada."
        )

        if statusbar:
            statusbar.atualizar(
                "Iniciando geração do relatório..."
            )

        pagina_relatorios.update_idletasks()

        try:
            data_atual = datetime.now().strftime(
                "%Y-%m-%d"
            )

            nome_sugerido = (
                f"Relatorio_ITI_{data_atual}.xlsx"
            )

            caminho_arquivo = (
                filedialog.asksaveasfilename(
                    title="Salvar relatório",
                    defaultextension=".xlsx",
                    initialdir=str(
                        pasta_padrao
                    ),
                    initialfile=nome_sugerido,
                    filetypes=[
                        (
                            "Arquivo Excel",
                            "*.xlsx"
                        )
                    ]
                )
            )

            if not caminho_arquivo:
                progresso.set(0)

                status.configure(
                    text="Status: operação cancelada."
                )

                registrar_log(
                    "Operação cancelada pelo usuário."
                )

                if statusbar:
                    statusbar.atualizar(
                        "Operação cancelada."
                    )

                return

            progresso.set(0.15)

            status.configure(
                text="Status: baixando dados..."
            )

            registrar_log(
                "Baixando os dados do Portal ITI."
            )

            if statusbar:
                statusbar.atualizar(
                    "Baixando dados do Portal ITI..."
                )

            pagina_relatorios.update_idletasks()

            logger.info(
                "Iniciando download dos dados do Portal ITI."
            )

            logger.info(
            "Download dos dados concluído."
            )

            
            dados = baixar_dados()

            progresso.set(0.40)

            registrar_log(
                "Dados baixados com sucesso."
            )

            status.configure(
                text="Status: tratando dados..."
            )

            if statusbar:
                statusbar.atualizar(
                    "Dados baixados. Tratando informações..."
                )

            pagina_relatorios.update_idletasks()

            certificados = obter_certificados(
                dados
            )

            logger.info(
                "Tratamento concluído. "
                f"{len(certificados)} registros processados."
            )

            if statusbar:
                statusbar.atualizar(
                    f"{len(certificados):,} registros processados"
                    .replace(",", ".")
                )

            progresso.set(0.60)

            mes_escolhido = combo_mes.get()

            if mes_escolhido != "Todos os meses":
                codigo_mes = MESES[
                    mes_escolhido
                ]

                certificados = filtrar_por_mes(
                    certificados,
                    codigo_mes
                )

            regiao_escolhida = (
                combo_regiao.get()
            )

            logger.info(
                "Filtros selecionados - "
                f"Mês: {mes_escolhido} | "
                f"Região: {regiao_escolhida}"
            )

            certificados = filtrar_por_regiao(
                certificados,
                regiao_escolhida
            )

            progresso.set(0.80)

            registrar_log(
                "Filtros aplicados aos dados."
            )

            if not certificados:
                progresso.set(0)

                status.configure(
                    text=(
                        "Status: nenhum registro "
                        "encontrado."
                    )
                )

                registrar_log(
                    "Nenhum registro encontrado."
                )

                if statusbar:
                    statusbar.atualizar(
                        "Nenhum registro encontrado."
                    )

                messagebox.showwarning(
                    "Aviso",
                    (
                        "Nenhum registro encontrado "
                        "para os filtros selecionados."
                    )
                )

                return

            status.configure(
                text="Status: criando Excel..."
            )

            progresso.set(0.90)

            registrar_log(
                "Criando o arquivo Excel."
            )

            if statusbar:
                statusbar.atualizar(
                    "Criando arquivo Excel..."
                )

            pagina_relatorios.update_idletasks()

            logger.info(
                "Iniciando criação do arquivo Excel."
            )

            caminho = criar_excel(
                certificados,
                caminho_arquivo
            )

            logger.info(
                f"Excel criado com sucesso: {caminho}"
            )   

            if statusbar:
                statusbar.atualizar(
                    "Excel criado com sucesso."
            )

            total_certificados = sum(
                int(registro["count"])
                for registro in certificados
            )

            regioes_encontradas = {
                registro["reg"]
                for registro in certificados
            }

            quantidade_regioes = len(
                regioes_encontradas
            )

            ultima_geracao = (
                datetime.now().strftime(
                    "%d/%m/%Y %H:%M"
                )
            )

            pasta_relatorios = (
                Path(caminho).parent
            )

            arquivos_gerados = len(
                list(
                    pasta_relatorios.glob(
                        "*.xlsx"
                    )
                )
            )

            dashboard.atualizar(
                certificados=total_certificados,
                regioes=quantidade_regioes,
                ultima=ultima_geracao,
                arquivos=arquivos_gerados,
                tipo="Manual"
            )

            salvar_dashboard(
                certificados=total_certificados,
                regioes=quantidade_regioes,
                ultima=ultima_geracao,
                arquivos=arquivos_gerados,
                tipo="Manual"
            )

            historico.atualizar(
                Path(caminho).parent
            )

            tempo_total = (
                time.perf_counter()
                - inicio
            )

            logger.info(
                f"Relatório concluído em "
                f"{tempo_total:.2f} segundos."
            )

            progresso.set(1)

            status.configure(
                text="Status: relatório concluído."
            )

            registrar_log(
                f"Relatório salvo em: {caminho}"
            )

            if statusbar:
                statusbar.atualizar(
                    f"Concluído em {tempo_total:.2f} segundos."
                    .replace(".", ",")
                )

            pagina_relatorios.update_idletasks()

            messagebox.showinfo(
                "Sucesso",
                (
                    "Relatório gerado com sucesso!\n\n"
                    f"{caminho}"
                )
            )

        except Exception as erro:
            logger.exception(
                "Erro durante a geração do relatório."
            )
            progresso.set(0)

            status.configure(
                text="Status: ocorreu um erro."
            )

            registrar_log(
                f"Erro: {erro}"
            )

            if statusbar:
                statusbar.atualizar(
                    "Erro ao gerar relatório."
                )

            messagebox.showerror(
                "Erro",
                str(erro)
            )

        finally:
            botao_gerar.configure(
                state="normal",
                text="📊  GERAR EXCEL"
            )

    # ============================
    # BOTÃO GERAR
    # ============================

    botao_gerar = ctk.CTkButton(
    coluna_esquerda,
    text="📊  GERAR EXCEL",
    height=52,
    corner_radius=9,
    fg_color="#1D7A4D",
    hover_color="#17633F",
    font=("Segoe UI", 15, "bold"),
    command=gerar_relatorio
)

    botao_gerar.grid(
        row=3,
        column=0,
        sticky="ew",
        padx=20,
        pady=(8, 20)
    )

    return pagina_relatorios