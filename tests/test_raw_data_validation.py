# ============================================================
# D1 — AUTOMATED RAW DATA CONTRACT TESTS
# ============================================================

from src.data.validation import (
    EXPECTED_COLUMNS,
    EXPECTED_ROWS,
    EXPECTED_SHA256,
    calculate_sha256,
    load_raw_dataset,
    validate_raw_dataset,
)
from src.data.config import get_primary_dataset_path


# ============================================================
# TEST 1 — RAW DATASET EXISTS
# ============================================================

def test_raw_dataset_exists():
    path = get_primary_dataset_path()

    assert path.exists()
    assert path.is_file()


# ============================================================
# TEST 2 — RAW DATASET CRYPTOGRAPHIC INTEGRITY
# ============================================================

def test_raw_dataset_sha256():
    path = get_primary_dataset_path()

    assert calculate_sha256(path) == EXPECTED_SHA256


# ============================================================
# TEST 3 — RAW DATASET DIMENSIONS
# ============================================================

def test_raw_dataset_dimensions():
    df = load_raw_dataset()

    assert df.shape == (EXPECTED_ROWS, EXPECTED_COLUMNS)


# ============================================================
# TEST 4 — ENCOUNTER IDENTIFIER INTEGRITY
# ============================================================

def test_encounter_identifier_integrity():
    results = validate_raw_dataset()

    assert results["encounter_id_missing"] == 0
    assert results["encounter_id_duplicates"] == 0
    assert results["encounter_id_integrity"] is True


# ============================================================
# TEST 5 — PATIENT IDENTIFIER PRESENCE
# ============================================================

def test_patient_identifier_presence():
    results = validate_raw_dataset()

    assert results["patient_nbr_missing"] == 0
    assert results["patient_identifier_present"] is True


# ============================================================
# TEST 6 — SOURCE TARGET CONTRACT
# ============================================================

def test_source_target_contract():
    results = validate_raw_dataset()

    assert results["observed_target_values"] == ["<30", ">30", "NO"]
    assert results["target_values_match"] is True
    assert results["source_target_missing"] == 0


# ============================================================
# TEST 7 — REQUIRED SCHEMA
# ============================================================

def test_required_schema():
    results = validate_raw_dataset()

    assert results["missing_required_columns"] == []
    assert results["required_columns_present"] is True


# ============================================================
# TEST 8 — D1 STRUCTURAL GATE
# ============================================================

def test_d1_structural_gate():
    results = validate_raw_dataset()

    assert results["d1_structural_gate"] == "PASS"