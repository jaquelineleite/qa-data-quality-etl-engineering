import json
from pathlib import Path

from scripts.txt_quality import (
    REQUIRED_COLUMNS,
    TXT_FILE,
    calcular_metricas_txt,
    load_cancelamentos,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

TRANSACTIONS_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "json"
    / "transacoes.json"
)


def test_txt_file_exists():
    assert TXT_FILE.exists()


def test_txt_has_expected_schema():
    data = load_cancelamentos()

    assert set(data["headers"]) == REQUIRED_COLUMNS


def test_txt_has_expected_record_count():
    metrics = calcular_metricas_txt()

    assert metrics["total_records"] == 2


def test_txt_has_no_invalid_records():
    metrics = calcular_metricas_txt()

    assert metrics["invalid_records"] == 0
    assert metrics["valid_records"] == 2


def test_txt_has_no_duplicate_transaction_ids():
    metrics = calcular_metricas_txt()

    assert metrics["duplicate_ids"] == 0


def test_txt_has_no_missing_required_fields():
    metrics = calcular_metricas_txt()

    assert metrics["missing_required"] == 0


def test_txt_has_valid_reason_and_date():
    metrics = calcular_metricas_txt()

    assert metrics["invalid_motives"] == 0
    assert metrics["invalid_dates"] == 0


def test_cancellation_transactions_exist_in_json():
    txt_data = load_cancelamentos()

    with open(
        TRANSACTIONS_FILE,
        encoding="utf-8",
    ) as file:
        transactions = json.load(file)

    transaction_ids = {
        str(transaction["transacao_id"])
        for transaction in transactions
    }

    cancellation_ids = {
        row["transacao_id"]
        for row in txt_data["records"]
    }

    assert cancellation_ids.issubset(
        transaction_ids
    )
