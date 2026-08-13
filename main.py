import sys

from src.gui.janela import iniciar
from src.services.automatico import (
    gerar_relatorio_automatico
)


def main():
    if "--automatico" in sys.argv:
        gerar_relatorio_automatico()
        return

    iniciar()


if __name__ == "__main__":
    main()