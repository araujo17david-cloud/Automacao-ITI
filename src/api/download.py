import requests


URL_ITI = "https://numeros.iti.gov.br/assets/paneljson/panels.json"


def baixar_dados():
    resposta = requests.get(
        URL_ITI,
        timeout=30
    )

    resposta.raise_for_status()

    return resposta.json()