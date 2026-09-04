from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATASET = (
    PROJECT_ROOT
    / "data"
    / "generated"
    / "transacoes_100k.csv"
)


STATUS_VALIDOS = {
    "APROVADA",
    "NEGADA",
    "CANCELADA",
}


def calcular_metricas(
    arquivo: Path = DATASET,
):
    df = pd.read_csv(arquivo)

    invalid_amount = (
        df["valor_bruto"] <= 0
    )

    invalid_fee = (
        (df["taxa"] < 0)
        | (
            df["taxa"]
            > df["valor_bruto"]
        )
    )

    invalid_status = (
        ~df["status"].isin(
            STATUS_VALIDOS
        )
    )

    nulls = df[
        [
            "transacao_id",
            "cliente_id",
            "estabelecimento_id",
            "data_transacao",
            "valor_bruto",
            "taxa",
            "status",
        ]
    ].isna().any(axis=1)

    duplicates = (
        df["transacao_id"]
        .duplicated(
            keep=False
        )
    )

    invalid_mask = (
        invalid_amount
        | invalid_fee
        | invalid_status
        | nulls
        | duplicates
    )

    total = len(df)

    invalidos = int(
        invalid_mask.sum()
    )

    validos = total - invalidos

    score = round(
        (
            validos
            / total
        )
        * 100,
        2,
    )

    return {
        "total_records": total,
        "valid_records": validos,
        "invalid_records": invalidos,
        "invalid_amount": int(
            invalid_amount.sum()
        ),
        "invalid_fee": int(
            invalid_fee.sum()
        ),
        "invalid_status": int(
            invalid_status.sum()
        ),
        "null_records": int(
            nulls.sum()
        ),
        "duplicate_records": int(
            duplicates.sum()
        ),
        "data_quality_score": score,
    }


if __name__ == "__main__":
    metrics = calcular_metricas()

    print(
        "=== DATA QUALITY METRICS ==="
    )

    for chave, valor in metrics.items():
        print(
            f"{chave}: {valor}"
        )
