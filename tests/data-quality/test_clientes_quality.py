from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CLIENTES_FILE = PROJECT_ROOT / "data" / "raw" / "csv" / "clientes.csv"


def carregar_clientes():
    return pd.read_csv(
        CLIENTES_FILE,
        dtype={
            "cliente_id": "Int64",
            "cpf": "string",
        },
    )


def test_arquivo_clientes_existe():
    assert CLIENTES_FILE.exists(), (
        f"Arquivo não encontrado: {CLIENTES_FILE}"
    )


def test_cliente_id_nao_deve_ser_nulo():
    clientes = carregar_clientes()

    quantidade_nulos = clientes["cliente_id"].isna().sum()

    assert quantidade_nulos == 0, (
        f"Foram encontrados {quantidade_nulos} cliente_id nulos."
    )


def test_cliente_id_deve_ser_unico():
    clientes = carregar_clientes()

    duplicados = clientes[
        clientes["cliente_id"].duplicated(keep=False)
    ]

    assert duplicados.empty, (
        "Foram encontrados cliente_id duplicados:\n"
        f"{duplicados.to_string(index=False)}"
    )


def test_nome_deve_ser_preenchido():
    clientes = carregar_clientes()

    invalidos = clientes[
        clientes["nome"].isna()
        | clientes["nome"].astype(str).str.strip().eq("")
    ]

    assert invalidos.empty, (
        "Clientes encontrados sem nome:\n"
        f"{invalidos.to_string(index=False)}"
    )


def test_cpf_deve_possuir_11_digitos():
    clientes = carregar_clientes()

    cpf = clientes["cpf"].fillna("").str.replace(
        r"\D",
        "",
        regex=True,
    )

    invalidos = clientes[cpf.str.len() != 11]

    assert invalidos.empty, (
        "CPFs com tamanho inválido encontrados:\n"
        f"{invalidos.to_string(index=False)}"
    )


def test_estado_deve_possuir_duas_posicoes():
    clientes = carregar_clientes()

    estado = clientes["estado"].fillna("").astype(str).str.strip()

    invalidos = clientes[estado.str.len() != 2]

    assert invalidos.empty, (
        "Estados inválidos encontrados:\n"
        f"{invalidos.to_string(index=False)}"
    )
