import json
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TRANSACOES_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "json"
    / "transacoes.json"
)

STATUS_PERMITIDOS = {
    "APROVADA",
    "NEGADA",
    "CANCELADA",
}


def carregar_transacoes():
    with open(TRANSACOES_FILE, encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    return pd.DataFrame(dados)


def test_arquivo_transacoes_existe():
    assert TRANSACOES_FILE.exists(), (
        f"Arquivo não encontrado: {TRANSACOES_FILE}"
    )


def test_transacao_id_deve_ser_unico():
    transacoes = carregar_transacoes()

    duplicados = transacoes[
        transacoes["transacao_id"].duplicated(keep=False)
    ]

    assert duplicados.empty, (
        "Transações duplicadas encontradas:\n"
        f"{duplicados.to_string(index=False)}"
    )


def test_valor_bruto_deve_ser_maior_que_zero():
    transacoes = carregar_transacoes()

    invalidos = transacoes[
        transacoes["valor_bruto"] <= 0
    ]

    assert invalidos.empty, (
        "Transações com valor bruto inválido:\n"
        f"{invalidos.to_string(index=False)}"
    )


def test_taxa_nao_deve_ser_negativa():
    transacoes = carregar_transacoes()

    invalidos = transacoes[
        transacoes["taxa"] < 0
    ]

    assert invalidos.empty, (
        "Transações com taxa negativa:\n"
        f"{invalidos.to_string(index=False)}"
    )


def test_taxa_nao_deve_superar_valor_bruto():
    transacoes = carregar_transacoes()

    invalidos = transacoes[
        transacoes["taxa"] > transacoes["valor_bruto"]
    ]

    assert invalidos.empty, (
        "Taxa superior ao valor bruto:\n"
        f"{invalidos.to_string(index=False)}"
    )


def test_status_deve_pertencer_ao_dominio():
    transacoes = carregar_transacoes()

    invalidos = transacoes[
        ~transacoes["status"].isin(STATUS_PERMITIDOS)
    ]

    assert invalidos.empty, (
        "Status inválidos encontrados:\n"
        f"{invalidos.to_string(index=False)}"
    )
