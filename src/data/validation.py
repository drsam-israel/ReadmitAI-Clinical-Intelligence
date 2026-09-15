# ============================================================
# D1 — RAW DATA INGESTION & VALIDATION
# PROGRAMMATIC DATA CONTRACT VALIDATOR
# ============================================================

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import pandas as pd

from src.data.config import get_primary_dataset_path


# ============================================================
# 1. GOVERNED RAW DATA EXPECTATIONS
# ============================================================

EXPECTED_ROWS = 101_766
EXPECTED_COLUMNS = 50

EXPECTED_REQUIRED_COLUMNS = {
    "encounter_id",
    "patient_nbr",
    "race",
    "gender",
    "age",
    "admission_type_id",
    "discharge_disposition_id",
    "admission_source_id",
    "time_in_hospital",
    "number_outpatient",
    "number_emergency",
    "number_inpatient",
    "diag_1",
    "diag_2",
    "diag_3",
    "max_glu_serum",
    "A1Cresult",
    "change",
    "diabetesMed",
    "readmitted",
}

EXPECTED_TARGET_VALUES = {"NO", ">30", "<30"}

EXPECTED_SHA256 = (
    "0689e7ec031237dc63031b938805c483"
    "77748761a3b26acab621567afa24df97"
)


# ============================================================
# 2. SHA-256 FILE INTEGRITY
# ============================================================

def calculate_sha256(file_path: Path) -> str:
    """Calculate SHA-256 without modifying the source file."""

    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


# ============================================================
# 3. CONTROLLED RAW DATA LOADER
# ============================================================

def load_raw_dataset(file_path: Path | None = None) -> pd.DataFrame:
    """
    Load the immutable raw dataset.

    No cleaning, imputation, target engineering, cohort filtering,
    or feature engineering is performed here.
    """

    if file_path is None:
        file_path = get_primary_dataset_path()

    if not file_path.exists():
        raise FileNotFoundError(f"Raw dataset not found: {file_path}")

    return pd.read_csv(
        file_path,
        low_memory=False,
    )


# ============================================================
# 4. RAW DATA CONTRACT VALIDATION
# ============================================================

def validate_raw_dataset(
    file_path: Path | None = None,
) -> dict[str, Any]:
    """Validate raw-data integrity and structural contract."""

    if file_path is None:
        file_path = get_primary_dataset_path()

    results: dict[str, Any] = {}

    # --------------------------------------------------------
    # File existence
    # --------------------------------------------------------

    results["file_exists"] = file_path.exists()

    if not results["file_exists"]:
        raise FileNotFoundError(f"Raw dataset not found: {file_path}")

    # --------------------------------------------------------
    # Cryptographic integrity
    # --------------------------------------------------------

    actual_sha256 = calculate_sha256(file_path)

    results["sha256"] = actual_sha256
    results["sha256_match"] = actual_sha256 == EXPECTED_SHA256

    # --------------------------------------------------------
    # Controlled ingestion
    # --------------------------------------------------------

    df = load_raw_dataset(file_path)

    results["rows"] = int(df.shape[0])
    results["columns"] = int(df.shape[1])

    results["row_count_match"] = results["rows"] == EXPECTED_ROWS
    results["column_count_match"] = results["columns"] == EXPECTED_COLUMNS

    # --------------------------------------------------------
    # Required schema
    # --------------------------------------------------------

    actual_columns = set(df.columns)

    missing_required = sorted(
        EXPECTED_REQUIRED_COLUMNS - actual_columns
    )

    results["missing_required_columns"] = missing_required
    results["required_columns_present"] = len(missing_required) == 0

    # --------------------------------------------------------
    # Encounter identifier integrity
    # --------------------------------------------------------

    results["encounter_id_missing"] = int(
        df["encounter_id"].isna().sum()
    )

    results["encounter_id_duplicates"] = int(
        df["encounter_id"].duplicated().sum()
    )

    results["encounter_id_integrity"] = (
        results["encounter_id_missing"] == 0
        and results["encounter_id_duplicates"] == 0
    )

    # --------------------------------------------------------
    # Patient identifier presence
    # --------------------------------------------------------

    results["patient_nbr_missing"] = int(
        df["patient_nbr"].isna().sum()
    )

    results["patient_identifier_present"] = (
        results["patient_nbr_missing"] == 0
    )

    # --------------------------------------------------------
    # Source target integrity
    # --------------------------------------------------------

    observed_target_values = set(
        df["readmitted"].dropna().astype(str).unique()
    )

    results["observed_target_values"] = sorted(
        observed_target_values
    )

    results["target_values_match"] = (
        observed_target_values == EXPECTED_TARGET_VALUES
    )

    results["source_target_missing"] = int(
        df["readmitted"].isna().sum()
    )

    # --------------------------------------------------------
    # Overall D1 structural gate
    # --------------------------------------------------------

    gate_checks = [
        results["sha256_match"],
        results["row_count_match"],
        results["column_count_match"],
        results["required_columns_present"],
        results["encounter_id_integrity"],
        results["patient_identifier_present"],
        results["target_values_match"],
        results["source_target_missing"] == 0,
    ]

    results["d1_structural_gate"] = (
        "PASS" if all(gate_checks) else "FAIL"
    )

    return results