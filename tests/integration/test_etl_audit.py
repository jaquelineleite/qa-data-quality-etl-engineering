from etl.audit import (
    gerar_auditoria,
)


def test_reconciliacao_deve_passar():
    auditoria = gerar_auditoria()

    assert (
        auditoria[
            "reconciliation_status"
        ]
        == "PASSED"
    )


def test_nao_deve_existir_registro_ausente_no_warehouse():
    auditoria = gerar_auditoria()

    assert (
        auditoria[
            "missing_in_warehouse"
        ]
        == []
    )


def test_nao_deve_existir_registro_extra_no_warehouse():
    auditoria = gerar_auditoria()

    assert (
        auditoria[
            "extra_in_warehouse"
        ]
        == []
    )


def test_quantidade_staging_e_warehouse_deve_ser_igual():
    auditoria = gerar_auditoria()

    assert (
        auditoria[
            "staging_records"
        ]
        ==
        auditoria[
            "warehouse_records"
        ]
    )
