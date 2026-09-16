# ============================================================
# D2 — DATA QUALITY ASSESSMENT TESTS
# ============================================================

import pytest

from src.data.validation import load_raw_dataset
from src.data.quality import (
    assess_accuracy,
    assess_completeness,
    assess_currency,
    assess_consistency,
    assess_representation,
    assess_bias,
)


@pytest.fixture(scope="module")
def raw_df():
    return load_raw_dataset()


# ============================================================
# 1. ACCURACY / CONFORMANCE
# ============================================================

def test_d2_accuracy_assessment_executes(raw_df):
    result = assess_accuracy(raw_df)

    assert isinstance(result, dict)
    assert "summary" in result


# ============================================================
# 2. COMPLETENESS
# ============================================================

def test_d2_completeness_assessment_executes(raw_df):
    result = assess_completeness(raw_df)

    assert isinstance(result, dict)

    assert result["total_rows"] == 101_766
    assert result["total_columns"] == 50

    assert (
        result["columns_with_missingness"]
        == 10
    )

    assert (
        result["columns_without_missingness"]
        == 40
    )


# ============================================================
# 3. CURRENCY
# ============================================================

def test_d2_currency_governance():
    result = assess_currency()

    assert result["source_start_year"] == 1999
    assert result["source_end_year"] == 2008
    assert result["encounter_level_dates_available"] is False
    assert result["temporal_recency_status"] == "HIGH RISK"
    assert result["status"] == "CONDITIONAL PASS"


# ============================================================
# 4. CONSISTENCY
# ============================================================

def test_d2_consistency_core_integrity(raw_df):
    result = assess_consistency(raw_df)

    assert (
        result["duplicate_checks"]["duplicate_encounter_ids"]
        == 0
    )

    assert (
        result["duplicate_checks"]["fully_duplicate_rows"]
        == 0
    )

    assert (
        result["medication_schema"][
            "missing_medication_columns"
        ]
        == []
    )

    assert result["medication_domain_issues"] == {}

    assert (
        result["readmission_consistency"][
            "missing_readmission_values"
        ]
        == 0
    )

    assert (
        result["readmission_consistency"][
            "unexpected_readmission_values"
        ]
        == 0
    )


# ============================================================
# 5. REPRESENTATION
# ============================================================

def test_d2_representation_population_contract(raw_df):
    result = assess_representation(raw_df)

    population = result["population_structure"]

    assert population["total_encounters"] == 101_766
    assert population["unique_patients"] == 71_518

    assert (
        population["patients_with_multiple_encounters"]
        > 0
    )

    assert (
        population["maximum_encounters_per_patient"]
        >= 1
    )


# ============================================================
# 6. BIAS ASSESSMENT
# ============================================================

def test_d2_bias_assessment_structure(raw_df):
    result = assess_bias(raw_df)

    assert "race_measurement_patterns" in result
    assert "gender_measurement_patterns" in result
    assert "age_measurement_patterns" in result

    assert "representation_risk_flags" in result
    assert "bias_risk_register" in result

    assert len(result["bias_risk_register"]) == 5


# ============================================================
# 7. PATIENT-LEVEL LEAKAGE RISK EVIDENCE
# ============================================================

def test_d2_repeated_patient_risk_detected(raw_df):
    result = assess_bias(raw_df)

    repeat_pct = result[
        "repeated_patient_structure"
    ][
        "repeat_patient_encounter_pct"
    ]

    assert repeat_pct > 0

    assert (
        result[
            "repeated_patient_structure"
        ][
            "maximum_encounters_per_patient"
        ]
        == 40
    )