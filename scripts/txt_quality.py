import csv
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

TXT_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "txt"
    / "cancelamentos.txt"
)

REQUIRED_COLUMNS = {
    "transacao_id",
    "motivo",
    "data_cancelamento",
}

VALID_MOTIVOS = {
    "FRAUDE_SUSPEITA",
    "SOLICITACAO_CLIENTE",
}


def load_cancelamentos(path=TXT_FILE):
    with open(path, encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file, delimiter="|")

        return {
            "headers": reader.fieldnames,
            "records": list(reader),
        }


def validar_data(value):
    try:
        datetime.strptime(
            value,
            "%Y-%m-%d %H:%M:%S",
        )
        return True
    except (ValueError, TypeError):
        return False


def calcular_metricas_txt(path=TXT_FILE):
    data = load_cancelamentos(path)

    headers = data["headers"] or []
    records = data["records"]

    schema_valid = set(headers) == REQUIRED_COLUMNS

    duplicate_ids = (
        len(records)
        - len(
            {
                row["transacao_id"]
                for row in records
            }
        )
    )

    missing_required = 0
    invalid_motives = 0
    invalid_dates = 0
    invalid_ids = 0
    invalid_records = 0

    for row in records:
        errors = []

        if any(
            not row.get(column)
            for column in REQUIRED_COLUMNS
        ):
            missing_required += 1
            errors.append("MISSING_REQUIRED_FIELD")

        try:
            transaction_id = int(
                row.get("transacao_id", "")
            )

            if transaction_id <= 0:
                raise ValueError

        except ValueError:
            invalid_ids += 1
            errors.append("INVALID_TRANSACTION_ID")

        if (
            row.get("motivo")
            not in VALID_MOTIVOS
        ):
            invalid_motives += 1
            errors.append("INVALID_REASON")

        if not validar_data(
            row.get("data_cancelamento")
        ):
            invalid_dates += 1
            errors.append("INVALID_DATE")

        if errors:
            invalid_records += 1

    return {
        "total_records": len(records),
        "valid_records": (
            len(records) - invalid_records
        ),
        "invalid_records": invalid_records,
        "schema_valid": schema_valid,
        "duplicate_ids": duplicate_ids,
        "missing_required": missing_required,
        "invalid_ids": invalid_ids,
        "invalid_motives": invalid_motives,
        "invalid_dates": invalid_dates,
    }


if __name__ == "__main__":
    metrics = calcular_metricas_txt()

    print("=== TXT DATA QUALITY ===")

    for key, value in metrics.items():
        print(f"{key}: {value}")
