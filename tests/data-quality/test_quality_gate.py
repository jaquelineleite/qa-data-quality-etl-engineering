import json

from scripts.quality_gate import (
    QUARANTINE_OUTPUT,
    VALID_OUTPUT,
    executar_quality_gate,
)


def executar_gate():
    return executar_quality_gate()


def carregar_json(arquivo):
    with open(arquivo, encoding="utf-8") as f:
        return json.load(f)


def test_quality_gate_deve_processar_cinco_transacoes():
    resultado = executar_gate()

    assert resultado["total"] == 5


def test_quality_gate_deve_aprovar_tres_transacoes():
    resultado = executar_gate()

    assert resultado["validas"] == 3


def test_quality_gate_deve_rejeitar_duas_transacoes():
    resultado = executar_gate()

    assert resultado["rejeitadas"] == 2


def test_transacoes_validas_nao_devem_conter_1004_e_1005():
    executar_gate()

    validas = carregar_json(VALID_OUTPUT)

    ids = {
        item["transacao_id"]
        for item in validas
    }

    assert 1004 not in ids
    assert 1005 not in ids


def test_transacoes_rejeitadas_devem_ir_para_quarentena():
    executar_gate()

    rejeitadas = carregar_json(
        QUARANTINE_OUTPUT
    )

    ids = {
        item["transacao_id"]
        for item in rejeitadas
    }

    assert ids == {1004, 1005}


def test_registro_1004_deve_indicar_valor_bruto_invalido():
    executar_gate()

    rejeitadas = carregar_json(
        QUARANTINE_OUTPUT
    )

    registro = next(
        item
        for item in rejeitadas
        if item["transacao_id"] == 1004
    )

    assert (
        "INVALID_GROSS_AMOUNT"
        in registro["rejection_reasons"]
    )


def test_registro_1005_deve_indicar_status_invalido():
    executar_gate()

    rejeitadas = carregar_json(
        QUARANTINE_OUTPUT
    )

    registro = next(
        item
        for item in rejeitadas
        if item["transacao_id"] == 1005
    )

    assert (
        "INVALID_STATUS"
        in registro["rejection_reasons"]
    )
