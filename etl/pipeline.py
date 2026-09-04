import json
from pathlib import Path

from scripts.quality_gate import (
    INPUT_FILE,
    validar_transacao,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]

STAGING_OUTPUT = (
    PROJECT_ROOT
    / "data"
    / "etl-output"
    / "staging"
    / "transacoes_staging.json"
)

WAREHOUSE_OUTPUT = (
    PROJECT_ROOT
    / "data"
    / "etl-output"
    / "warehouse"
    / "fact_transacao.json"
)

QUARANTINE_OUTPUT = (
    PROJECT_ROOT
    / "data"
    / "quarantine"
    / "transacoes_rejeitadas.json"
)


def carregar_origem():
    with open(
        INPUT_FILE,
        encoding="utf-8",
    ) as arquivo:
        return json.load(arquivo)


def transformar_para_staging(transacao):
    return {
        "transacao_id": int(
            transacao["transacao_id"]
        ),
        "cliente_id": int(
            transacao["cliente_id"]
        ),
        "estabelecimento_id": int(
            transacao["estabelecimento_id"]
        ),
        "data_transacao": (
            transacao["data_transacao"]
        ),
        "valor_bruto": round(
            float(transacao["valor_bruto"]),
            2,
        ),
        "taxa": round(
            float(transacao["taxa"]),
            2,
        ),
        "status": (
            transacao["status"]
            .strip()
            .upper()
        ),
    }


def transformar_para_warehouse(transacao):
    valor_liquido = round(
        transacao["valor_bruto"]
        - transacao["taxa"],
        2,
    )

    return {
        "transacao_id": (
            transacao["transacao_id"]
        ),
        "cliente_id": (
            transacao["cliente_id"]
        ),
        "estabelecimento_id": (
            transacao["estabelecimento_id"]
        ),
        "data_transacao": (
            transacao["data_transacao"]
        ),
        "valor_bruto": (
            transacao["valor_bruto"]
        ),
        "taxa": (
            transacao["taxa"]
        ),
        "valor_liquido": valor_liquido,
        "status": transacao["status"],
        "source_system": (
            "TRANSACTIONS_JSON"
        ),
        "etl_status": "LOADED",
    }


def salvar_json(caminho, dados):
    caminho.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        caminho,
        "w",
        encoding="utf-8",
    ) as arquivo:
        json.dump(
            dados,
            arquivo,
            indent=2,
            ensure_ascii=False,
        )


def executar_etl():
    origem = carregar_origem()

    staging = []
    warehouse = []
    rejeitadas = []

    for transacao in origem:
        erros = validar_transacao(
            transacao
        )

        if erros:
            rejeitada = transacao.copy()

            rejeitada[
                "quality_status"
            ] = "REJECTED"

            rejeitada[
                "rejection_reasons"
            ] = erros

            rejeitadas.append(
                rejeitada
            )

            continue

        registro_staging = (
            transformar_para_staging(
                transacao
            )
        )

        staging.append(
            registro_staging
        )

        warehouse.append(
            transformar_para_warehouse(
                registro_staging
            )
        )

    salvar_json(
        STAGING_OUTPUT,
        staging,
    )

    salvar_json(
        WAREHOUSE_OUTPUT,
        warehouse,
    )

    salvar_json(
        QUARANTINE_OUTPUT,
        rejeitadas,
    )

    return {
        "source_records": len(origem),
        "staging_records": len(staging),
        "warehouse_records": (
            len(warehouse)
        ),
        "rejected_records": (
            len(rejeitadas)
        ),
    }


if __name__ == "__main__":
    resultado = executar_etl()

    print("=== ETL EXECUTION ===")

    print(
        f"Source:     "
        f"{resultado['source_records']}"
    )

    print(
        f"Staging:    "
        f"{resultado['staging_records']}"
    )

    print(
        f"Warehouse:  "
        f"{resultado['warehouse_records']}"
    )

    print(
        f"Rejected:   "
        f"{resultado['rejected_records']}"
    )
