from scripts.data_quality_metrics import (
    DATASET,
    calcular_metricas,
)
from scripts.generate_large_dataset import (
    gerar_dataset,
)


def preparar_dataset():
    if not DATASET.exists():
        gerar_dataset(
            100_000,
            DATASET,
        )


def test_dataset_deve_conter_100_mil_registros():
    preparar_dataset()

    metricas = calcular_metricas()

    assert (
        metricas["total_records"]
        == 100_000
    )


def test_dataset_deve_conter_1000_registros_invalidos():
    preparar_dataset()

    metricas = calcular_metricas()

    assert (
        metricas["invalid_records"]
        == 1_000
    )


def test_dataset_deve_conter_99000_registros_validos():
    preparar_dataset()

    metricas = calcular_metricas()

    assert (
        metricas["valid_records"]
        == 99_000
    )


def test_data_quality_score_deve_ser_99_porcento():
    preparar_dataset()

    metricas = calcular_metricas()

    assert (
        metricas["data_quality_score"]
        == 99.0
    )


def test_nao_deve_existir_transacao_id_duplicado():
    preparar_dataset()

    metricas = calcular_metricas()

    assert (
        metricas["duplicate_records"]
        == 0
    )


def test_nao_deve_existir_campo_obrigatorio_nulo():
    preparar_dataset()

    metricas = calcular_metricas()

    assert (
        metricas["null_records"]
        == 0
    )
