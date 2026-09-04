import time
from pathlib import Path

from scripts.data_quality_metrics import calcular_metricas


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "generated"


DATASETS = {
    "100K": DATA_DIR / "transacoes_100k.csv",
    "1M": DATA_DIR / "transacoes_1m.csv",
}


def executar_benchmark():
    print("=== LARGE DATASET BENCHMARK ===")

    resultados = {}

    for nome, arquivo in DATASETS.items():
        if not arquivo.exists():
            raise FileNotFoundError(
                f"Dataset não encontrado: {arquivo}"
            )

        inicio = time.perf_counter()

        metricas = calcular_metricas(arquivo)

        tempo = round(
            time.perf_counter() - inicio,
            4,
        )

        resultados[nome] = {
            **metricas,
            "processing_time_seconds": tempo,
        }

        print()
        print(f"Dataset: {nome}")
        print(f"Registros: {metricas['total_records']:,}")
        print(f"Válidos: {metricas['valid_records']:,}")
        print(f"Inválidos: {metricas['invalid_records']:,}")
        print(
            f"Data Quality Score: "
            f"{metricas['data_quality_score']}%"
        )
        print(f"Tempo: {tempo}s")

    return resultados


if __name__ == "__main__":
    executar_benchmark()
