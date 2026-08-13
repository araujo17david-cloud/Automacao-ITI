import json


from src.utils.caminhos import (
    ARQUIVO_CONFIG,
    PASTA_CONFIG,
    PASTA_RELATORIOS
)


CONFIG_PADRAO = {
    "tema": "Light",
    "pasta_relatorios": str(
        PASTA_RELATORIOS
    ),
    "agendamento_ativo": False,
    "dia_agendamento": 1,
    "horario_agendamento": "08:00",
    "ultima_execucao_automatica": "--"
}


def carregar_config():

    PASTA_CONFIG.mkdir(
        exist_ok=True
    )

    if not ARQUIVO_CONFIG.exists():

        salvar_config(
            CONFIG_PADRAO
        )

        return CONFIG_PADRAO.copy()

    with open(
        ARQUIVO_CONFIG,
        "r",
        encoding="utf-8"
    ) as arquivo:

        return json.load(
            arquivo
        )


def salvar_config(config):

    PASTA_CONFIG.mkdir(
        exist_ok=True
    )

    with open(
        ARQUIVO_CONFIG,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            config,
            arquivo,
            indent=4,
            ensure_ascii=False
        )