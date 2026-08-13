def obter_certificados(dados):
    for item in dados:
        if "certDistCerMen" in item:
            return item["certDistCerMen"]

    raise ValueError(
        "Os dados de certificados mensais por região não foram encontrados."
    )


def filtrar_por_mes(certificados, mes):
    resultado = []

    for registro in certificados:
        anomes = str(registro["anomes"])

        # Aceita formatos como 202607 e 2026-07
        mes_registro = anomes.replace("-", "")[4:6]

        if mes_registro == mes:
            resultado.append(registro)

    return resultado


def filtrar_por_regiao(certificados, regiao):
    if regiao == "Todas":
        return certificados

    resultado = []

    for registro in certificados:
        if registro["reg"] == regiao:
            resultado.append(registro)

    return resultado