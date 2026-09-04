from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

EXCEL_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "excel"
    / "estabelecimentos.xlsx"
)

COLUNAS_ESPERADAS = [
    "estabelecimento_id",
    "nome",
    "categoria",
    "cidade",
    "estado",
]


def carregar_excel():
    return pd.read_excel(
        EXCEL_FILE,
        engine="openpyxl",
    )


def calcular_metricas_excel():
    df = carregar_excel()

    schema_valido = (
        list(df.columns)
        == COLUNAS_ESPERADAS
    )

    ids_duplicados = int(
        df["estabelecimento_id"]
        .duplicated()
        .sum()
    )

    categoria_nula = int(
        df["categoria"]
        .isna()
        .sum()
    )

    nome_nulo = int(
        df["nome"]
        .isna()
        .sum()
    )

    estados_invalidos = int(
        (
            df["estado"]
            .fillna("")
            .astype(str)
            .str.strip()
            .str.len()
            != 2
        ).sum()
    )

    invalid_mask = (
        df["categoria"].isna()
        | df["nome"].isna()
        | df["estabelecimento_id"]
            .duplicated(keep=False)
        | (
            df["estado"]
            .fillna("")
            .astype(str)
            .str.strip()
            .str.len()
            != 2
        )
    )

    total = len(df)
    invalidos = int(
        invalid_mask.sum()
    )
    validos = total - invalidos

    return {
        "total_records": total,
        "valid_records": validos,
        "invalid_records": invalidos,
        "schema_valid": schema_valido,
        "duplicate_ids": ids_duplicados,
        "missing_category": categoria_nula,
        "missing_name": nome_nulo,
        "invalid_state": estados_invalidos,
    }


if __name__ == "__main__":
    metricas = calcular_metricas_excel()

    print("=== EXCEL DATA QUALITY ===")

    for chave, valor in metricas.items():
        print(f"{chave}: {valor}")
