import json
from datetime import datetime, timezone
from pathlib import Path

from etl.pipeline import (
    STAGING_OUTPUT,
    WAREHOUSE_OUTPUT,
    executar_etl,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]

AUDIT_OUTPUT = (
    PROJECT_ROOT
    / "reports"
    / "etl-audit.json"
)


def carregar_json(caminho):
    with open(
        caminho,
        encoding="utf-8",
    ) as arquivo:
        return json.load(arquivo)


def gerar_auditoria():
    resultado = executar_etl()

    staging = carregar_json(
        STAGING_OUTPUT
    )

    warehouse = carregar_json(
        WAREHOUSE_OUTPUT
    )

    staging_ids = {
        item["transacao_id"]
        for item in staging
    }

    warehouse_ids = {
        item["transacao_id"]
        for item in warehouse
    }

    missing_in_warehouse = sorted(
        staging_ids - warehouse_ids
    )

    extra_in_warehouse = sorted(
        warehouse_ids - staging_ids
    )

    reconciled = (
        len(missing_in_warehouse) == 0
        and len(extra_in_warehouse) == 0
        and len(staging) == len(warehouse)
    )

    audit = {
        "execution_timestamp_utc": (
            datetime.now(timezone.utc)
            .isoformat()
        ),
        "source_records": (
            resultado["source_records"]
        ),
        "staging_records": (
            resultado["staging_records"]
        ),
        "warehouse_records": (
            resultado["warehouse_records"]
        ),
        "rejected_records": (
            resultado["rejected_records"]
        ),
        "missing_in_warehouse": (
            missing_in_warehouse
        ),
        "extra_in_warehouse": (
            extra_in_warehouse
        ),
        "reconciliation_status": (
            "PASSED"
            if reconciled
            else "FAILED"
        ),
    }

    AUDIT_OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        AUDIT_OUTPUT,
        "w",
        encoding="utf-8",
    ) as arquivo:
        json.dump(
            audit,
            arquivo,
            indent=2,
            ensure_ascii=False,
        )

    print("=== ETL AUDIT ===")
    print(
        f"Source: {audit['source_records']}"
    )
    print(
        f"Staging: {audit['staging_records']}"
    )
    print(
        f"Warehouse: {audit['warehouse_records']}"
    )
    print(
        f"Rejected: {audit['rejected_records']}"
    )
    print(
        "Reconciliation: "
        f"{audit['reconciliation_status']}"
    )

    return audit


if __name__ == "__main__":
    gerar_auditoria()
