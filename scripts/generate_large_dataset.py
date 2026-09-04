import argparse
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "data" / "generated"


STATUS_VALIDOS = [
    "APROVADA",
    "NEGADA",
    "CANCELADA",
]


def gerar_dataset(quantidade: int, arquivo_saida: Path):
    random.seed(42)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    data_base = datetime(2026, 1, 1)

    with open(
        arquivo_saida,
        "w",
        newline="",
        encoding="utf-8",
    ) as arquivo:
        writer = csv.writer(arquivo)

        writer.writerow([
            "transacao_id",
            "cliente_id",
            "estabelecimento_id",
            "data_transacao",
            "valor_bruto",
            "taxa",
            "status",
        ])

        for i in range(1, quantidade + 1):
            transacao_id = 1_000_000 + i
            cliente_id = random.randint(1, 10_000)
            estabelecimento_id = random.randint(1, 500)

            data_transacao = (
                data_base
                + timedelta(
                    seconds=random.randint(
                        0,
                        31_536_000,
                    )
                )
            )

            valor_bruto = round(
                random.uniform(10, 5000),
                2,
            )

            taxa = round(
                valor_bruto
                * random.uniform(0.005, 0.05),
                2,
            )

            status = random.choice(
                STATUS_VALIDOS
            )

            # 1% dos registros contém defeito controlado
            if i % 100 == 0:
                if i % 200 == 0:
                    valor_bruto = -valor_bruto
                else:
                    status = "STATUS_INVALIDO"

            writer.writerow([
                transacao_id,
                cliente_id,
                estabelecimento_id,
                data_transacao.isoformat(),
                valor_bruto,
                taxa,
                status,
            ])

    print(
        f"Dataset gerado: {arquivo_saida}"
    )

    print(
        f"Registros: {quantidade:,}"
    )


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--records",
        type=int,
        default=100_000,
    )

    parser.add_argument(
        "--output",
        default="transacoes_100k.csv",
    )

    args = parser.parse_args()

    arquivo_saida = (
        OUTPUT_DIR
        / args.output
    )

    gerar_dataset(
        args.records,
        arquivo_saida,
    )


if __name__ == "__main__":
    main()
