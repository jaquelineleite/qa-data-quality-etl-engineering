import json

from etl.pipeline import (
    STAGING_OUTPUT,
    WAREHOUSE_OUTPUT,
    executar_etl,
)


def carregar_json(caminho):
    with open(
        caminho,
        encoding="utf-8",
    ) as arquivo:
        return json.load(arquivo)


def test_etl_deve_ler_cinco_registros():
    resultado = executar_etl()

    assert (
        resultado["source_records"]
        == 5
    )


def test_etl_deve_carregar_tres_registros_no_staging():
    resultado = executar_etl()

    assert (
        resultado["staging_records"]
        == 3
    )


def test_etl_deve_carregar_tres_registros_no_warehouse():
    resultado = executar_etl()

    assert (
        resultado[
            "warehouse_records"
        ]
        == 3
    )


def test_etl_deve_rejeitar_dois_registros():
    resultado = executar_etl()

    assert (
        resultado[
            "rejected_records"
        ]
        == 2
    )


def test_warehouse_nao_deve_conter_registros_invalidos():
    executar_etl()

    warehouse = carregar_json(
        WAREHOUSE_OUTPUT
    )

    ids = {
        registro["transacao_id"]
        for registro in warehouse
    }

    assert 1004 not in ids
    assert 1005 not in ids


def test_valor_liquido_deve_ser_calculado_corretamente():
    executar_etl()

    warehouse = carregar_json(
        WAREHOUSE_OUTPUT
    )

    for registro in warehouse:
        esperado = round(
            registro["valor_bruto"]
            - registro["taxa"],
            2,
        )

        assert (
            registro["valor_liquido"]
            == esperado
        )


def test_source_to_target_ids_devem_ser_consistentes():
    executar_etl()

    staging = carregar_json(
        STAGING_OUTPUT
    )

    warehouse = carregar_json(
        WAREHOUSE_OUTPUT
    )

    staging_ids = {
        registro["transacao_id"]
        for registro in staging
    }

    warehouse_ids = {
        registro["transacao_id"]
        for registro in warehouse
    }

    assert (
        staging_ids
        == warehouse_ids
    )


def test_status_no_warehouse_deve_estar_normalizado():
    executar_etl()

    warehouse = carregar_json(
        WAREHOUSE_OUTPUT
    )

    status_validos = {
        "APROVADA",
        "NEGADA",
        "CANCELADA",
    }

    for registro in warehouse:
        assert (
            registro["status"]
            in status_validos
        )
