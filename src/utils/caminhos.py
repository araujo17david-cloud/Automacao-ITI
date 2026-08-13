import os
import sys

from pathlib import Path


def obter_pasta_executavel():
    if getattr(
        sys,
        "frozen",
        False
    ):
        return Path(
            sys.executable
        ).resolve().parent

    return Path(
        __file__
    ).resolve().parents[2]


def obter_pasta_recursos():
    if getattr(
        sys,
        "frozen",
        False
    ):
        return Path(
            sys._MEIPASS
        )

    return Path(
        __file__
    ).resolve().parents[2]


def obter_pasta_dados_usuario():
    local_appdata = os.getenv(
        "LOCALAPPDATA"
    )

    if local_appdata:
        return (
            Path(local_appdata)
            / "Automacao_ITI"
        )

    return (
        Path.home()
        / "Automacao_ITI"
    )


# ==================================
# PASTAS PRINCIPAIS
# ==================================

PASTA_BASE = obter_pasta_executavel()

PASTA_RECURSOS = obter_pasta_recursos()

PASTA_DADOS = obter_pasta_dados_usuario()


# ==================================
# ASSETS
# ==================================

PASTA_ASSETS = (
    PASTA_RECURSOS
    / "assets"
)

CAMINHO_LOGO = (
    PASTA_ASSETS
    / "logo.png"
)

CAMINHO_ICONE = (
    PASTA_ASSETS
    / "logo.ico"
)


# ==================================
# DADOS DO USUÁRIO
# ==================================

PASTA_CONFIG = (
    PASTA_DADOS
    / "config"
)

PASTA_LOGS = (
    PASTA_DADOS
    / "logs"
)

PASTA_RELATORIOS = (
    Path.home()
    / "Documents"
    / "Automacao_ITI"
    / "Relatorios"
)


# ==================================
# ARQUIVOS DE CONFIGURAÇÃO
# ==================================

ARQUIVO_CONFIG = (
    PASTA_CONFIG
    / "config.json"
)

ARQUIVO_DASHBOARD = (
    PASTA_CONFIG
    / "dashboard.json"
)