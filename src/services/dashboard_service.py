import json


from src.utils.caminhos import (
    ARQUIVO_DASHBOARD,
    PASTA_CONFIG
)


def salvar_dashboard(
    certificados,
    regioes,
    ultima,
    arquivos,
    tipo="Manual"
):
    PASTA_CONFIG.mkdir(
        exist_ok=True
    )

    dados = {
        "certificados": certificados,
        "regioes": regioes,
        "ultima": ultima,
        "arquivos": arquivos,
        "tipo": tipo
    }

    with open(
        ARQUIVO_DASHBOARD,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            dados,
            arquivo,
            indent=4,
            ensure_ascii=False
        )


def carregar_dashboard():

    if not ARQUIVO_DASHBOARD.exists():

        return {
            "certificados": 0,
            "regioes": 0,
            "ultima": "--",
            "arquivos": 0,
            "tipo": "--"
        }

    with open(
        ARQUIVO_DASHBOARD,
        "r",
        encoding="utf-8"
    ) as arquivo:

        return json.load(
            arquivo
        )