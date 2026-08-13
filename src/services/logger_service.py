import logging

from datetime import datetime
from src.utils.caminhos import (
    PASTA_LOGS
)


def configurar_logger():
    PASTA_LOGS.mkdir(
        parents=True,
        exist_ok=True
    )

    data_atual = datetime.now().strftime(
        "%Y-%m-%d"
    )

    caminho_log = (
        PASTA_LOGS
        / f"{data_atual}.log"
    )

    logger = logging.getLogger(
        "automacao_iti"
    )

    logger.setLevel(
        logging.INFO
    )

    # Evitar criar handlers duplicados
    if logger.handlers:
        return logger

    formatador = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S"
    )

    arquivo_handler = logging.FileHandler(
        caminho_log,
        encoding="utf-8"
    )

    arquivo_handler.setFormatter(
        formatador
    )

    logger.addHandler(
        arquivo_handler
    )

    return logger


logger = configurar_logger()