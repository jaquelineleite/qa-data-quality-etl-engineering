import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "json"
    / "transacoes.json"
)

VALID_OUTPUT = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "transacoes_validas.json"
)

QUARANTINE_OUTPUT = (
    PROJECT_ROOT
    / "data"
    / "quarantine"
    / "transacoes_rejeitadas.json"
)


STATUS_PERMITIDOS = {
    "APROVADA",
    "NEGADA",
    "CANCELADA",
}


def validar_transacao(transacao):
    erros = []

    campos_obrigatorios = [
        "transacao_id",
        "cliente_id",
        "estabelecimento_id",
        "data_transacao",
        "valor_bruto",
        "taxa",
        "status",
    ]

    for campo in campos_obrigatorios:
        if transacao.get(campo) in (None, ""):
            erros.append(f"MISSING_{campo.upper()}")

    valor_bruto = transacao.get("valor_bruto")
    taxa = transacao.get("taxa")
    status = transacao.get("status")

    if valor_bruto is not None and valor_bruto <= 0:
        erros.append("INVALID_GROSS_AMOUNT")

    if taxa is not None and taxa < 0:
        erros.append("NEGATIVE_FEE")

    if (
        valor_bruto is not None
        and taxa is not None
        and taxa > valor_bruto
    ):
        erros.append("FEE_EXCEEDS_GROSS_AMOUNT")

    if status not in STATUS_PERMITIDOS:
        erros.append("INVALID_STATUS")

    return erros


def executar_quality_gate():
    with open(INPUT_FILE, encoding="utf-8") as arquivo:
        transacoes = json.load(arquivo)

    validas = []
    rejeitadas = []

    for transacao in transacoes:
        erros = validar_transacao(transacao)

        if erros:
            rejeitada = transacao.copy()
            rejeitada["quality_status"] = "REJECTED"
            rejeitada["rejection_reasons"] = erros

            rejeitadas.append(rejeitada)

        else:
            aprovada = transacao.copy()
            aprovada["quality_status"] = "APPROVED"

            validas.append(aprovada)

    VALID_OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    QUARANTINE_OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        VALID_OUTPUT,
        "w",
        encoding="utf-8",
    ) as arquivo:
        json.dump(
            validas,
            arquivo,
            indent=2,
            ensure_ascii=False,
        )

    with open(
        QUARANTINE_OUTPUT,
        "w",
        encoding="utf-8",
    ) as arquivo:
        json.dump(
            rejeitadas,
            arquivo,
            indent=2,
            ensure_ascii=False,
        )

    return {
        "total": len(transacoes),
        "validas": len(validas),
        "rejeitadas": len(rejeitadas),
    }


if __name__ == "__main__":
    resultado = executar_quality_gate()

    print("=== DATA QUALITY GATE ===")
    print(f"Total analisado: {resultado['total']}")
    print(f"Aprovadas:       {resultado['validas']}")
    print(f"Rejeitadas:      {resultado['rejeitadas']}")
