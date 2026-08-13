from datetime import datetime
from pathlib import Path

import pandas as pd

from openpyxl import load_workbook
from openpyxl.chart import (
    BarChart,
    LineChart,
    Reference
)

from openpyxl.chart.label import DataLabelList

from openpyxl.styles import (
    Alignment,
    Border,
    Font,
    PatternFill,
    Side
)
from openpyxl.utils import get_column_letter


def ajustar_largura_colunas(planilha):
    """
    Ajusta automaticamente a largura das colunas
    com base no maior conteúdo encontrado.
    """

    for coluna in planilha.columns:
        maior = 0
        letra = get_column_letter(
            coluna[0].column
        )

        for celula in coluna:
            if celula.value is not None:
                tamanho = len(
                    str(celula.value)
                )

                maior = max(
                    maior,
                    tamanho
                )

        planilha.column_dimensions[
            letra
        ].width = maior + 3


def criar_excel(
    certificados,
    caminho_arquivo
):
    """
    Cria um arquivo Excel com três abas:

    1. Dashboard
    2. Resumo
    3. Certificados
    """

    caminho = Path(caminho_arquivo)

    caminho.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df = pd.DataFrame(
        certificados
    )

    if df.empty:
        raise ValueError(
            "Não existem dados para gerar o relatório."
        )

    # Validar as colunas necessárias
    colunas_obrigatorias = {
        "anomes",
        "reg",
        "count"
    }

    colunas_ausentes = (
        colunas_obrigatorias
        - set(df.columns)
    )

    if colunas_ausentes:
        raise ValueError(
            "Colunas obrigatórias não encontradas: "
            + ", ".join(
                sorted(colunas_ausentes)
            )
        )

    # Garantir que count seja numérico
    df["count"] = pd.to_numeric(
        df["count"],
        errors="coerce"
    )

    if df["count"].isna().any():
        raise ValueError(
            "Foram encontrados valores inválidos "
            "na coluna count."
        )

    # Aceitar formatos como:
    # 202601
    # 2026-01
    df["anomes_limpo"] = (
        df["anomes"]
        .astype(str)
        .str.replace(
            "-",
            "",
            regex=False
        )
        .str.strip()
    )

    # Converter ano e mês para uma data real
    df["data_mes"] = pd.to_datetime(
        df["anomes_limpo"],
        format="%Y%m",
        errors="coerce"
    )

    if df["data_mes"].isna().any():
        valores_invalidos = (
            df.loc[
                df["data_mes"].isna(),
                "anomes"
            ]
            .astype(str)
            .unique()
            .tolist()
        )

        raise ValueError(
            "Foram encontrados valores inválidos "
            "na coluna anomes: "
            + ", ".join(valores_invalidos)
        )

    meses_pt = {
        1: "Janeiro",
        2: "Fevereiro",
        3: "Março",
        4: "Abril",
        5: "Maio",
        6: "Junho",
        7: "Julho",
        8: "Agosto",
        9: "Setembro",
        10: "Outubro",
        11: "Novembro",
        12: "Dezembro"
    }

    # Criar textos como Janeiro/2025
    df["mes_ano"] = df[
        "data_mes"
    ].apply(
        lambda data: (
            f"{meses_pt[data.month]}"
            f"/{data.year}"
        )
    )

    # Descobrir a ordem cronológica
    ordem_cronologica = (
        df[
            [
                "data_mes",
                "mes_ano"
            ]
        ]
        .drop_duplicates()
        .sort_values("data_mes")
        ["mes_ano"]
        .tolist()
    )

    # Criar a tabela dinâmica
    resumo = pd.pivot_table(
        df,
        values="count",
        index="reg",
        columns="mes_ano",
        aggfunc="sum",
        fill_value=0
    )

    resumo = resumo.reindex(
        columns=ordem_cronologica,
        fill_value=0
    )

    # Total por região
    resumo["Total"] = resumo.sum(
        axis=1
    )

    # Ordem das regiões
    ordem_regioes = [
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

    regioes_existentes = [
        regiao
        for regiao in ordem_regioes
        if regiao in resumo.index
    ]

    outras_regioes = sorted(
        [
            regiao
            for regiao in resumo.index
            if regiao not in ordem_regioes
        ]
    )

    resumo = resumo.reindex(
        regioes_existentes
        + outras_regioes
    )

    # Total geral
    resumo.loc["TOTAL"] = resumo.sum(
        axis=0
    )

    resumo.index.name = "Região"

    # Remover colunas auxiliares
    # da aba detalhada
    df_detalhado = df.drop(
        columns=[
            "anomes_limpo",
            "data_mes",
            "mes_ano"
        ]
    )

    # Criar inicialmente as duas abas
    with pd.ExcelWriter(
        caminho,
        engine="openpyxl"
    ) as writer:
        resumo.to_excel(
            writer,
            sheet_name="Resumo",
            index=True
        )

        df_detalhado.to_excel(
            writer,
            sheet_name="Certificados",
            index=False
        )

    # Abrir o arquivo para formatação
    wb = load_workbook(caminho)

    # ==================================
    # ESTILOS
    # ==================================

    preenchimento_cabecalho = PatternFill(
        fill_type="solid",
        start_color="1F4E78",
        end_color="1F4E78"
    )

    fonte_cabecalho = Font(
        bold=True,
        color="FFFFFF"
    )

    preenchimento_total = PatternFill(
        fill_type="solid",
        start_color="1F4E78",
        end_color="1F4E78"
    )

    fonte_total = Font(
        bold=True,
        color="FFFFFF"
    )

    preenchimento_indicador = PatternFill(
        fill_type="solid",
        start_color="D9EAF7",
        end_color="D9EAF7"
    )

    borda = Border(
        left=Side(
            style="thin",
            color="B7B7B7"
        ),
        right=Side(
            style="thin",
            color="B7B7B7"
        ),
        top=Side(
            style="thin",
            color="B7B7B7"
        ),
        bottom=Side(
            style="thin",
            color="B7B7B7"
        )
    )

    centralizar = Alignment(
        horizontal="center",
        vertical="center"
    )

    alinhar_esquerda = Alignment(
        horizontal="left",
        vertical="center"
    )

    # ==================================
    # ABA DASHBOARD
    # ==================================

    ws_dashboard = wb.create_sheet(
        title="Dashboard",
        index=0
    )

    ws_dashboard.sheet_view.showGridLines = False

    ws_dashboard.sheet_view.zoomScale = 85

    ws_dashboard.sheet_view.showRowColHeaders = False

    # Título
    ws_dashboard["A1"] = (
        "DASHBOARD - CERTIFICADOS DIGITAIS"
    )

    ws_dashboard.merge_cells(
        "A1:H1"
    )

    ws_dashboard["A1"].fill = (
        preenchimento_cabecalho
    )

    ws_dashboard["A1"].font = Font(
        size=20,
        bold=True,
        color="FFFFFF"
    )

    ws_dashboard["A1"].alignment = (
        centralizar
    )

    ws_dashboard.row_dimensions[
        1
    ].height = 32

    ws_dashboard["A2"] = (
    "Visão geral da emissão de certificados "
    "por período e região"
)

    ws_dashboard.merge_cells("A2:H2")

    ws_dashboard["A2"].font = Font(
        size=11,
        italic=True,
        color="666666"
)

    ws_dashboard["A2"].alignment = centralizar

    ws_dashboard.row_dimensions[2].height = 22

    # Indicadores
    total_certificados = int(
        resumo.loc[
            "TOTAL",
            "Total"
        ]
    )

    quantidade_regioes = (
        len(resumo.index) - 1
    )

    ws_dashboard["A3"] = (
        "Total de Certificados"
    )

    ws_dashboard["B3"] = (
        total_certificados
    )

    ws_dashboard["A4"] = (
        "Quantidade de Regiões"
    )

    ws_dashboard["B4"] = (
        quantidade_regioes
    )

    ws_dashboard["A5"] = "Período"

    ws_dashboard["B5"] = (
        ordem_cronologica[0]
        + " até "
        + ordem_cronologica[-1]
    )

    ws_dashboard["A6"] = "Gerado em"

    ws_dashboard["B6"] = (
        datetime.now().strftime(
            "%d/%m/%Y %H:%M"
        )
    )

    for numero_linha in range(3, 7):
        celula_titulo = ws_dashboard.cell(
            row=numero_linha,
            column=1
        )

        celula_valor = ws_dashboard.cell(
            row=numero_linha,
            column=2
        )

        celula_titulo.font = Font(
            bold=True,
            color="1F1F1F"
        )

        celula_titulo.fill = (
            preenchimento_indicador
        )

        celula_valor.fill = PatternFill(
            fill_type="solid",
            start_color="F4F8FB",
            end_color="F4F8FB"
        )

        celula_titulo.border = borda
        celula_valor.border = borda

        celula_titulo.alignment = (
            alinhar_esquerda
        )

        celula_valor.alignment = (
            centralizar
        )

        ws_dashboard.row_dimensions[
            numero_linha
        ].height = 26
    
        celula_titulo = (
            ws_dashboard.cell(
                row=numero_linha,
                column=1
            )
        )

        celula_valor = (
            ws_dashboard.cell(
                row=numero_linha,
                column=2
            )
        )

        celula_titulo.font = Font(
            bold=True
        )

        celula_titulo.fill = (
            preenchimento_indicador
        )

        celula_titulo.border = borda
        celula_valor.border = borda

        celula_titulo.alignment = (
            alinhar_esquerda
        )

        celula_valor.alignment = (
            centralizar
        )

    ws_dashboard["B3"].number_format = (
        "#,##0"
    )

    ws_dashboard["B4"].number_format = "0"

    ws_dashboard["B3"].font = Font(
        size=13,
        bold=True,
        color="1F4E78"
)

    ws_dashboard["B4"].font = Font(
    size=13,
    bold=True,
    color="1F4E78"
)

    ws_dashboard["B5"].font = Font(
        bold=True
)

    ws_dashboard["B6"].font = Font(
        bold=True
)

    ws_dashboard.column_dimensions[
        "A"
    ].width = 25

    ws_dashboard.column_dimensions[
        "B"
    ].width = 28

    # ----------------------------------
    # Dados auxiliares por região
    # ----------------------------------

    ws_dashboard["A9"] = "Região"
    ws_dashboard["B9"] = "Total"

    linha_dashboard = 10

    for regiao in resumo.index:
        if regiao == "TOTAL":
            continue

        ws_dashboard.cell(
            row=linha_dashboard,
            column=1,
            value=regiao
        )

        ws_dashboard.cell(
            row=linha_dashboard,
            column=2,
            value=int(
                resumo.loc[
                    regiao,
                    "Total"
                ]
            )
        )

        linha_dashboard += 1

    # ----------------------------------
    # Gráfico por região
    # ----------------------------------

        # ----------------------------------
    # Gráfico horizontal por região
    # ----------------------------------

    grafico_regiao = BarChart()

    # "bar" cria barras horizontais
    grafico_regiao.type = "bar"
    grafico_regiao.style = 10

    grafico_regiao.title = (
        "Certificados por Região"
    )

    # No gráfico horizontal, o eixo X representa os valores
    grafico_regiao.x_axis.title = (
        "Quantidade de Certificados"
    )

    # O eixo Y representa as regiões
    grafico_regiao.y_axis.title = (
        "Região"
    )

    dados_regiao = Reference(
        ws_dashboard,
        min_col=2,
        min_row=9,
        max_row=linha_dashboard - 1
    )

    categorias_regiao = Reference(
        ws_dashboard,
        min_col=1,
        min_row=10,
        max_row=linha_dashboard - 1
    )

    grafico_regiao.add_data(
        dados_regiao,
        titles_from_data=True
    )

    grafico_regiao.set_categories(
        categorias_regiao
    )

    grafico_regiao.dataLabels = (
        DataLabelList()
    )

    # Exibir somente os valores
    grafico_regiao.dataLabels.showVal = True
    grafico_regiao.dataLabels.showSerName = False
    grafico_regiao.dataLabels.showCatName = False

    # Remover a legenda "Total"
    grafico_regiao.legend = None

    # Mostrar a primeira região no topo
    grafico_regiao.y_axis.reverseOrder = True

    grafico_regiao.height = 10
    grafico_regiao.width = 19

    ws_dashboard.add_chart(
        grafico_regiao,
        "D3"
    )

    # ----------------------------------
    # Dados auxiliares mensais
    # ----------------------------------

    linha_inicio_meses = max(
        linha_dashboard + 3,
        22
    )

    ws_dashboard.cell(
        row=linha_inicio_meses,
        column=1,
        value="Período"
    )

    ws_dashboard.cell(
        row=linha_inicio_meses,
        column=2,
        value="Total"
    )

    linha_mes = linha_inicio_meses + 1

    for periodo in ordem_cronologica:
        ws_dashboard.cell(
            row=linha_mes,
            column=1,
            value=periodo
        )

        ws_dashboard.cell(
            row=linha_mes,
            column=2,
            value=int(
                resumo.loc[
                    "TOTAL",
                    periodo
                ]
            )
        )

        linha_mes += 1

    # ----------------------------------
    # Gráfico de evolução mensal
    # ----------------------------------

    grafico_mensal = LineChart()

    grafico_mensal.style = 13

    grafico_mensal.title = (
        "Evolução Mensal dos Certificados"
    )

    grafico_mensal.y_axis.title = (
        "Quantidade de Certificados"
    )

    grafico_mensal.x_axis.title = (
        "Período"
    )

    dados_mensais = Reference(
        ws_dashboard,
        min_col=2,
        min_row=linha_inicio_meses,
        max_row=linha_mes - 1
    )

    categorias_mensais = Reference(
        ws_dashboard,
        min_col=1,
        min_row=linha_inicio_meses + 1,
        max_row=linha_mes - 1
    )

    grafico_mensal.add_data(
        dados_mensais,
        titles_from_data=True
    )

    for serie in grafico_mensal.series:
        serie.marker.symbol = "circle"
        serie.marker.size = 7
        serie.graphicalProperties.line.width = 25000

    grafico_mensal.set_categories(
        categorias_mensais
    )

    grafico_mensal.legend = None
    grafico_mensal.height = 10
    grafico_mensal.width = 22

    ws_dashboard.add_chart(
        grafico_mensal,
        "D22"
    )

    # for numero_linha in range(
#     9,
#     linha_dashboard
# ):
#     ws_dashboard.row_dimensions[
#         numero_linha
#     ].hidden = True

    # Ocultar dados auxiliares mensais
    # for numero_linha in range(
#     linha_inicio_meses,
#     linha_mes
# ):
#     ws_dashboard.row_dimensions[
#         numero_linha
#     ].hidden = True

    # ==================================
    # ABA RESUMO
    # ==================================

    ws_resumo = wb["Resumo"]

    # Inserir linhas para título e data
    ws_resumo.insert_rows(
        1,
        amount=3
    )

    ws_resumo["A1"] = (
        "RELATÓRIO DE CERTIFICADOS "
        "DIGITAIS DO ITI"
    )

    ws_resumo["A2"] = (
        "Gerado em: "
        + datetime.now().strftime(
            "%d/%m/%Y às %H:%M"
        )
    )

    ultima_coluna = get_column_letter(
        ws_resumo.max_column
    )

    ws_resumo.merge_cells(
        f"A1:{ultima_coluna}1"
    )

    ws_resumo.merge_cells(
        f"A2:{ultima_coluna}2"
    )

    ws_resumo["A1"].font = Font(
        size=18,
        bold=True,
        color="1F1F1F"
    )

    ws_resumo["A2"].font = Font(
        italic=True,
        color="666666"
    )

    ws_resumo["A1"].alignment = (
        centralizar
    )

    ws_resumo["A2"].alignment = (
        centralizar
    )

    # Cabeçalho da tabela
    for celula in ws_resumo[4]:
        celula.fill = (
            preenchimento_cabecalho
        )

        celula.font = fonte_cabecalho
        celula.alignment = centralizar
        celula.border = borda

    ultima_linha_resumo = (
        ws_resumo.max_row
    )

    # Corpo da tabela
    for linha in ws_resumo.iter_rows(
        min_row=5,
        max_row=ultima_linha_resumo
    ):
        for celula in linha:
            celula.border = borda

            if celula.column == 1:
                celula.alignment = (
                    alinhar_esquerda
                )

            else:
                celula.alignment = (
                    centralizar
                )

                celula.number_format = (
                    "#,##0"
                )

    # Linha TOTAL
    for celula in ws_resumo[
        ultima_linha_resumo
    ]:
        celula.fill = (
            preenchimento_total
        )

        celula.font = fonte_total
        celula.border = borda

    ajustar_largura_colunas(
        ws_resumo
    )

    ws_resumo.column_dimensions[
        "A"
    ].width = 22

    # Largura mínima das colunas
    # de mês/ano
    for coluna_numero in range(
        2,
        ws_resumo.max_column + 1
    ):
        letra = get_column_letter(
            coluna_numero
        )

        largura_atual = (
            ws_resumo
            .column_dimensions[letra]
            .width
        )

        if largura_atual < 17:
            ws_resumo.column_dimensions[
                letra
            ].width = 17

    ws_resumo.row_dimensions[
        1
    ].height = 28

    ws_resumo.row_dimensions[
        2
    ].height = 22

    ws_resumo.row_dimensions[
        4
    ].height = 24

    ws_resumo.freeze_panes = "B5"

    ws_resumo.auto_filter.ref = (
        f"A4:{ultima_coluna}"
        f"{ultima_linha_resumo}"
    )

    # ==================================
    # ABA CERTIFICADOS
    # ==================================

    ws_dados = wb["Certificados"]

    for celula in ws_dados[1]:
        celula.fill = (
            preenchimento_cabecalho
        )

        celula.font = fonte_cabecalho
        celula.alignment = centralizar
        celula.border = borda

    for linha in ws_dados.iter_rows(
        min_row=2
    ):
        for celula in linha:
            celula.border = borda

            titulo_coluna = (
                ws_dados.cell(
                    row=1,
                    column=celula.column
                ).value
            )

            if titulo_coluna == "count":
                celula.number_format = (
                    "#,##0"
                )

    ajustar_largura_colunas(
        ws_dados
    )

    ws_dados.freeze_panes = "A2"

    ws_dados.auto_filter.ref = (
        ws_dados.dimensions
    )

    # ==================================
    # ORDEM DAS ABAS E SALVAMENTO
    # ==================================

    wb._sheets = [
        ws_dashboard,
        ws_resumo,
        ws_dados
    ]

    wb.active = 0

    wb.save(caminho)

    return caminho.resolve()