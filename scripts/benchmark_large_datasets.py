import json
import time
from pathlib import Path

from scripts.data_quality_metrics import calcular_metricas


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "generated"
REPORTS_DIR = PROJECT_ROOT / "reports"

REPORT_FILE = REPORTS_DIR / "benchmark-metrics.json"

DATASETS = {
    "100K": DATA_DIR / "transacoes_100k.csv",
    "1M": DATA_DIR / "transacoes_1m.csv",
}


def executar_benchmark():
    print("=== LARGE DATASET BENCHMARK ===")

    REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    resultados = {}

    for nome, arquivo in DATASETS.items():
        if not arquivo.exists():
            print()
            print(
                f"Dataset {nome} não encontrado. "
                "Benchmark ignorado."
            )
            continue

        inicio = time.perf_counter()

        metricas = calcular_metricas(
            arquivo
        )

        tempo = (
            time.perf_counter()
            - inicio
        )

        total = metricas["total_records"]

        throughput = (
            total / tempo
            if tempo > 0
            else 0
        )

        resultado = {
            **metricas,
            "processing_time_seconds": round(
                tempo,
                4,
            ),
            "records_per_second": round(
                throughput,
                2,
            ),
        }

        resultados[nome] = resultado

        print()
        print(f"Dataset: {nome}")
        print(
            f"Registros: "
            f"{total:,}"
        )
        print(
            f"Válidos: "
            f"{metricas['valid_records']:,}"
        )
        print(
            f"Inválidos: "
            f"{metricas['invalid_records']:,}"
        )
        print(
            f"Data Quality Score: "
            f"{metricas['data_quality_score']}%"
        )
        print(
            f"Tempo: "
            f"{resultado['processing_time_seconds']}s"
        )
        print(
            f"Throughput: "
            f"{resultado['records_per_second']:,.2f} "
            "registros/s"
        )

    with open(
        REPORT_FILE,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            resultados,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print()
    print(
        f"Relatório gerado: "
        f"{REPORT_FILE}"
    )

    return resultados


if __name__ == "__main__":
    executar_benchmark()
