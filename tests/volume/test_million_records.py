from pathlib import Path

import pytest

from scripts.data_quality_metrics import calcular_metricas


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_1M = (
    PROJECT_ROOT
    / "data"
    / "generated"
    / "transacoes_1m.csv"
)


@pytest.mark.skipif(
    not DATASET_1M.exists(),
    reason="Dataset local de 1M não foi gerado.",
)
def test_dataset_de_um_milhao():
    metricas = calcular_metricas(
        DATASET_1M
    )

    assert metricas["total_records"] == 1_000_000
    assert metricas["valid_records"] == 990_000
    assert metricas["invalid_records"] == 10_000
    assert metricas["data_quality_score"] == 99.0
    assert metricas["duplicate_records"] == 0
    assert metricas["null_records"] == 0
