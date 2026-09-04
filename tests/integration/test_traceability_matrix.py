import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MATRIX_FILE = (
    PROJECT_ROOT
    / "docs"
    / "traceability-matrix.json"
)


def load_matrix():
    with open(
        MATRIX_FILE,
        encoding="utf-8",
    ) as file:
        return json.load(file)


def test_traceability_matrix_exists():
    assert MATRIX_FILE.exists()


def test_requirement_ids_are_unique():
    matrix = load_matrix()

    ids = [
        item["requirement_id"]
        for item in matrix
    ]

    assert len(ids) == len(set(ids))


def test_required_traceability_fields_exist():
    matrix = load_matrix()

    required_fields = {
        "requirement_id",
        "requirement",
        "source_document",
        "automated_test",
        "evidence",
        "defects",
    }

    for item in matrix:
        assert required_fields.issubset(
            item.keys()
        )


def test_referenced_artifacts_exist():
    matrix = load_matrix()

    for item in matrix:
        paths = [
            item["source_document"],
            item["automated_test"],
            item["evidence"],
        ]

        for relative_path in paths:
            path = (
                PROJECT_ROOT
                / relative_path
            )

            assert path.exists(), (
                f"Artefato inexistente: "
                f"{relative_path}"
            )


def test_referenced_defects_exist():
    matrix = load_matrix()

    for item in matrix:
        for defect in item["defects"]:
            path = PROJECT_ROOT / defect

            assert path.exists(), (
                f"Defeito inexistente: "
                f"{defect}"
            )
