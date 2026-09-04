import csv
import json
from pathlib import Path

import pandas as pd

from scripts.database_connection import get_connection
from scripts.quality_gate import validar_transacao


PROJECT_ROOT = Path(__file__).resolve().parents[1]

CLIENTES_FILE = (
    PROJECT_ROOT / "data" / "raw" / "csv" / "clientes.csv"
)

ESTABELECIMENTOS_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "excel"
    / "estabelecimentos.xlsx"
)

TRANSACOES_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "json"
    / "transacoes.json"
)


def carregar_clientes():
    with open(
        CLIENTES_FILE,
        encoding="utf-8",
    ) as arquivo:
        return list(csv.DictReader(arquivo))


def carregar_estabelecimentos():
    df = pd.read_excel(
        ESTABELECIMENTOS_FILE,
        engine="openpyxl",
    )

    df = df.where(
        pd.notna(df),
        None,
    )

    return df.to_dict(
        orient="records"
    )


def carregar_transacoes():
    with open(
        TRANSACOES_FILE,
        encoding="utf-8",
    ) as arquivo:
        return json.load(arquivo)


def executar_carga():
    clientes = carregar_clientes()
    estabelecimentos = carregar_estabelecimentos()
    transacoes = carregar_transacoes()

    transacoes_validas = [
        item
        for item in transacoes
        if not validar_transacao(item)
    ]

    with get_connection() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                TRUNCATE TABLE
                    warehouse.fact_transacao,
                    warehouse.dim_cliente,
                    warehouse.dim_estabelecimento,
                    staging.transacoes,
                    staging.clientes,
                    staging.estabelecimentos,
                    source.transacoes,
                    source.clientes,
                    source.estabelecimentos
                RESTART IDENTITY CASCADE;
                """
            )

            for cliente in clientes:
                cursor.execute(
                    """
                    INSERT INTO source.clientes (
                        cliente_id,
                        nome,
                        cpf,
                        email,
                        cidade,
                        estado,
                        data_cadastro
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """,
                    (
                        int(cliente["cliente_id"]),
                        cliente["nome"],
                        cliente["cpf"],
                        cliente["email"] or None,
                        cliente["cidade"],
                        cliente["estado"],
                        cliente["data_cadastro"],
                    ),
                )

                cursor.execute(
                    """
                    INSERT INTO staging.clientes (
                        cliente_id,
                        nome,
                        cpf,
                        email,
                        cidade,
                        estado,
                        data_cadastro
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """,
                    (
                        int(cliente["cliente_id"]),
                        cliente["nome"],
                        cliente["cpf"],
                        cliente["email"] or None,
                        cliente["cidade"],
                        cliente["estado"],
                        cliente["data_cadastro"],
                    ),
                )

                cursor.execute(
                    """
                    INSERT INTO warehouse.dim_cliente (
                        cliente_id,
                        nome,
                        cpf,
                        email,
                        cidade,
                        estado,
                        data_cadastro
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """,
                    (
                        int(cliente["cliente_id"]),
                        cliente["nome"],
                        cliente["cpf"],
                        cliente["email"] or None,
                        cliente["cidade"],
                        cliente["estado"],
                        cliente["data_cadastro"],
                    ),
                )

            for estabelecimento in estabelecimentos:
                dados = (
                    int(estabelecimento["estabelecimento_id"]),
                    estabelecimento["nome"],
                    estabelecimento["categoria"],
                    estabelecimento["cidade"],
                    estabelecimento["estado"],
                )

                cursor.execute(
                    """
                    INSERT INTO source.estabelecimentos (
                        estabelecimento_id,
                        nome,
                        categoria,
                        cidade,
                        estado
                    )
                    VALUES (%s, %s, %s, %s, %s);
                    """,
                    dados,
                )

                cursor.execute(
                    """
                    INSERT INTO staging.estabelecimentos (
                        estabelecimento_id,
                        nome,
                        categoria,
                        cidade,
                        estado
                    )
                    VALUES (%s, %s, %s, %s, %s);
                    """,
                    dados,
                )

                cursor.execute(
                    """
                    INSERT INTO warehouse.dim_estabelecimento (
                        estabelecimento_id,
                        nome,
                        categoria,
                        cidade,
                        estado
                    )
                    VALUES (%s, %s, %s, %s, %s);
                    """,
                    dados,
                )

            for transacao in transacoes:
                cursor.execute(
                    """
                    INSERT INTO source.transacoes (
                        transacao_id,
                        cliente_id,
                        estabelecimento_id,
                        data_transacao,
                        valor_bruto,
                        taxa,
                        status
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """,
                    (
                        transacao["transacao_id"],
                        transacao["cliente_id"],
                        transacao["estabelecimento_id"],
                        transacao["data_transacao"],
                        transacao["valor_bruto"],
                        transacao["taxa"],
                        transacao["status"],
                    ),
                )

            for transacao in transacoes_validas:
                cursor.execute(
                    """
                    INSERT INTO staging.transacoes (
                        transacao_id,
                        cliente_id,
                        estabelecimento_id,
                        data_transacao,
                        valor_bruto,
                        taxa,
                        status
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """,
                    (
                        transacao["transacao_id"],
                        transacao["cliente_id"],
                        transacao["estabelecimento_id"],
                        transacao["data_transacao"],
                        transacao["valor_bruto"],
                        transacao["taxa"],
                        transacao["status"].upper(),
                    ),
                )

                cursor.execute(
                    """
                    INSERT INTO warehouse.fact_transacao (
                        transacao_id,
                        cliente_sk,
                        estabelecimento_sk,
                        data_transacao,
                        valor_bruto,
                        taxa,
                        valor_liquido,
                        status
                    )
                    SELECT
                        %s,
                        c.cliente_sk,
                        e.estabelecimento_sk,
                        %s,
                        %s,
                        %s,
                        %s - %s,
                        %s
                    FROM warehouse.dim_cliente c
                    CROSS JOIN warehouse.dim_estabelecimento e
                    WHERE c.cliente_id = %s
                      AND e.estabelecimento_id = %s;
                    """,
                    (
                        transacao["transacao_id"],
                        transacao["data_transacao"],
                        transacao["valor_bruto"],
                        transacao["taxa"],
                        transacao["valor_bruto"],
                        transacao["taxa"],
                        transacao["status"].upper(),
                        transacao["cliente_id"],
                        transacao["estabelecimento_id"],
                    ),
                )

        conn.commit()

    resultado = {
        "source_records": len(transacoes),
        "staging_records": len(transacoes_validas),
        "warehouse_records": len(transacoes_validas),
        "rejected_records": (
            len(transacoes)
            - len(transacoes_validas)
        ),
    }

    print("=== POSTGRESQL DATA LOAD ===")

    for chave, valor in resultado.items():
        print(f"{chave}: {valor}")

    return resultado


if __name__ == "__main__":
    executar_carga()
