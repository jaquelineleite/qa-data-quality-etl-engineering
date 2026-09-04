import json
import sys
import time
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from scripts.data_quality_metrics import (
    DATASET,
    calcular_metricas,
)


OUTPUT_FILE = (
    PROJECT_ROOT
    / "reports"
    / "data-quality-metrics.json"
)


def gerar_relatorio():
    inicio = time.perf_counter()

    metricas = calcular_metricas(DATASET)

    fim = time.perf_counter()

    tempo_processamento = round(
        fim - inicio,
        4,
    )

    relatorio = {
        **metricas,
        "processing_time_seconds": tempo_processamento,
        "dataset": DATASET.name,
    }

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
    ) as arquivo:
        json.dump(
            relatorio,
            arquivo,
            indent=2,
            ensure_ascii=False,
        )

    print("=== DATA QUALITY REPORT ===")
    print(f"Dataset: {relatorio['dataset']}")
    print(f"Total: {relatorio['total_records']:,}")
    print(f"Validos: {relatorio['valid_records']:,}")
    print(f"Invalidos: {relatorio['invalid_records']:,}")
    print(
        f"Quality Score: "
        f"{relatorio['data_quality_score']}%"
    )
    print(
        f"Tempo: "
        f"{relatorio['processing_time_seconds']}s"
    )


if __name__ == "__main__":
    gerar_relatorio()
