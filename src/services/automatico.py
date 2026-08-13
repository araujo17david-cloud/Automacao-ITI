from datetime import datetime
from pathlib import Path

from src.api.download import baixar_dados
from src.excel.excel import criar_excel
from src.services.config_service import (
    carregar_config,
    salvar_config
)
from src.services.dashboard_service import salvar_dashboard
from src.services.logger_service import logger
from src.services.tratamento import obter_certificados


def gerar_relatorio_automatico():
    logger.info(
        "=" * 60
    )

    logger.info(
        "Iniciando geração AUTOMÁTICA mensal."
    )

    try:
        config = carregar_config()

        pasta_relatorios = Path(
            config.get(
                "pasta_relatorios",
                "relatorios"
            )
        )

        pasta_relatorios.mkdir(
            parents=True,
            exist_ok=True
        )

        agora = datetime.now()

        nome_arquivo = (
            f"Relatorio_ITI_"
            f"{agora.strftime('%Y-%m')}.xlsx"
        )

        caminho_arquivo = (
            pasta_relatorios
            / nome_arquivo
        )

        # ==================================
        # EVITAR DUPLICIDADE
        # ==================================

        if caminho_arquivo.exists():
            logger.warning(
                "Relatório automático não gerado. "
                "Já existe um relatório para este mês: "
                f"{caminho_arquivo}"
            )

            return caminho_arquivo

        # ==================================
        # DOWNLOAD
        # ==================================

        logger.info(
            "Baixando dados do Portal ITI."
        )

        dados = baixar_dados()

        logger.info(
            "Download concluído."
        )

        # ==================================
        # TRATAMENTO
        # ==================================

        certificados = obter_certificados(
            dados
        )

        logger.info(
            f"{len(certificados)} registros processados."
        )

        if not certificados:
            raise ValueError(
                "Nenhum certificado encontrado "
                "para gerar o relatório automático."
            )

        # ==================================
        # CRIAR EXCEL
        # ==================================

        logger.info(
            "Criando relatório automático."
        )

        caminho = criar_excel(
            certificados,
            caminho_arquivo
        )

        # ==================================
        # DASHBOARD
        # ==================================

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

        arquivos_gerados = len(
            list(
                pasta_relatorios.glob(
                    "*.xlsx"
                )
            )
        )

        salvar_dashboard(
            certificados=total_certificados,
            regioes=quantidade_regioes,
            ultima=ultima_geracao,
            arquivos=arquivos_gerados,
            tipo="Automática"
        )

        config[
            "ultima_execucao_automatica"
        ] = datetime.now().strftime(
            "%d/%m/%Y %H:%M"
        )

        salvar_config(
            config
        )

        logger.info(
            "Dashboard atualizado pela "
            "geração automática."
        )

        logger.info(
            f"Relatório automático criado: {caminho}"
        )

        return caminho

    except Exception:
        logger.exception(
            "Erro durante a geração automática mensal."
        )

        raise