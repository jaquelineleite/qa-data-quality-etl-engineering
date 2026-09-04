from pathlib import Path

from openpyxl import Workbook


PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "excel"
    / "estabelecimentos.xlsx"
)


def gerar_excel():
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "estabelecimentos"

    sheet.append([
        "estabelecimento_id",
        "nome",
        "categoria",
        "cidade",
        "estado",
    ])

    dados = [
        [
            101,
            "Tech Store",
            "ELETRONICOS",
            "Sao Paulo",
            "SP",
        ],
        [
            102,
            "Market Center",
            "SUPERMERCADO",
            "Campinas",
            "SP",
        ],
        [
            103,
            "Fashion Shop",
            "VESTUARIO",
            "Osasco",
            "SP",
        ],
        [
            104,
            "Pharma Plus",
            "FARMACIA",
            "Sao Paulo",
            "SP",
        ],
        [
            105,
            "Invalid Store",
            "",
            "Sorocaba",
            "SP",
        ],
    ]

    for linha in dados:
        sheet.append(linha)

    workbook.save(OUTPUT_FILE)

    print(
        f"Excel gerado: {OUTPUT_FILE}"
    )
    print(
        f"Registros: {len(dados)}"
    )


if __name__ == "__main__":
    gerar_excel()
