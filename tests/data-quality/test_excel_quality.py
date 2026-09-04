from scripts.excel_quality import (
    EXCEL_FILE,
    calcular_metricas_excel,
)


def test_arquivo_excel_deve_existir():
    assert EXCEL_FILE.exists()


def test_excel_deve_conter_cinco_registros():
    metricas = calcular_metricas_excel()

    assert (
        metricas["total_records"]
        == 5
    )


def test_schema_excel_deve_ser_valido():
    metricas = calcular_metricas_excel()

    assert (
        metricas["schema_valid"]
        is True
    )


def test_excel_nao_deve_conter_ids_duplicados():
    metricas = calcular_metricas_excel()

    assert (
        metricas["duplicate_ids"]
        == 0
    )


def test_excel_deve_identificar_um_registro_invalido():
    metricas = calcular_metricas_excel()

    assert (
        metricas["invalid_records"]
        == 1
    )


def test_excel_deve_identificar_categoria_ausente():
    metricas = calcular_metricas_excel()

    assert (
        metricas["missing_category"]
        == 1
    )


def test_excel_deve_conter_quatro_registros_validos():
    metricas = calcular_metricas_excel()

    assert (
        metricas["valid_records"]
        == 4
    )


def test_estados_devem_ser_validos():
    metricas = calcular_metricas_excel()

    assert (
        metricas["invalid_state"]
        == 0
    )
