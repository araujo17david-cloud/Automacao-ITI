import logging
from pathlib import Path


PASTA_LOGS = Path("logs")
PASTA_LOGS.mkdir(
    parents=True,
    exist_ok=True
)


logging.basicConfig(
    filename=PASTA_LOGS / "automacao_iti.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


def registrar_info(mensagem):
    logging.info(mensagem)


def registrar_erro(mensagem):
    logging.exception(mensagem)