import subprocess
import sys

from pathlib import Path

from src.services.logger_service import logger


NOME_TAREFA = "Automacao_ITI_Relatorio_Mensal"


def obter_comando_aplicacao():
    """
    Retorna o programa e os argumentos que
    o Agendador do Windows deverá executar.
    """

    if getattr(
        sys,
        "frozen",
        False
    ):
        programa = Path(
            sys.executable
        ).resolve()

        return (
            f'"{programa}" '
            f'--automatico'
        )

    python_exe = Path(
        sys.executable
    ).resolve()

    main_py = (
        Path(__file__)
        .resolve()
        .parents[2]
        / "main.py"
    )

    return (
        f'"{python_exe}" '
        f'"{main_py}" '
        f'--automatico'
    )


def remover_agendamento():
    resultado = subprocess.run(
        [
            "schtasks",
            "/Delete",
            "/TN",
            NOME_TAREFA,
            "/F"
        ],
        capture_output=True,
        text=True,
        creationflags=subprocess.CREATE_NO_WINDOW
    )

    if resultado.returncode == 0:
        logger.info(
            "Agendamento automático removido."
        )

        return True

    logger.info(
        "Nenhum agendamento anterior "
        "precisou ser removido."
    )

    return False


def criar_agendamento(
    dia,
    horario
):
    comando_aplicacao = (
        obter_comando_aplicacao()
    )

    logger.info(
        "Configurando geração automática: "
        f"dia {dia}, às {horario}."
    )

    # Remove a tarefa antiga antes
    # de criar a nova.
    remover_agendamento()

    comando = [
        "schtasks",
        "/Create",
        "/TN",
        NOME_TAREFA,
        "/TR",
        comando_aplicacao,
        "/SC",
        "MONTHLY",
        "/D",
        str(dia),
        "/ST",
        horario,
        "/F"
    ]

    resultado = subprocess.run(
        comando,
        capture_output=True,
        text=True,
        creationflags=subprocess.CREATE_NO_WINDOW
    )

    if resultado.returncode != 0:
        logger.error(
            "Erro ao criar agendamento: "
            f"{resultado.stderr}"
        )

        raise RuntimeError(
            "Não foi possível criar o "
            "agendamento automático no Windows."
        )

    logger.info(
        "Agendamento mensal criado "
        "com sucesso."
    )

    return True