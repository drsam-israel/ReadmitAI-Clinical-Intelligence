# ============================================================
# D12 — EXPLAINABILITY REPORTING & EVIDENCE PACKAGE TESTS
# ============================================================

from __future__ import annotations

import csv
from pathlib import Path

import pytest

from src.models import explainability as d12
from src.models import explainability_reporting as report


# ============================================================
# D12-RT.01 — PACKAGE GENERATION
# ============================================================

@pytest.fixture(scope="module")
def package_result():
    return report.validate_d12_explainability_reporting_package()


def test_d12_reporting_package_passes(package_result):
    assert package_result["validation_status"] == "PASS"
    assert package_result["failed_checks"] == []


def test_d12_reporting_package_artifact_count(package_result):
    assert package_result["artifact_count"] == 13


def test_d12_reporting_package_disposition(package_result):
    assert package_result["disposition"] == (
        "CONDITIONAL_PASS_PROGRESS_TO_D13_WITH_EXPLAINABILITY_LIMITATIONS"
    )
    assert package_result["progression_authorized"] is True
    assert package_result["next_lifecycle_stage"] == (
        "D13_MODEL_REGISTRY_AND_ARTIFACT_FREEZE"
    )


def test_d12_reporting_package_expected_counts(package_result):
    assert package_result["source_feature_family_count"] == 10
    assert package_result["local_explanation_case_count"] == 5
    assert package_result["attribution_stability_slice_count"] == 42
    assert package_result["adequate_support_slice_count"] == 34
    assert package_result["low_support_slice_count"] == 8
    assert package_result["clinical_plausibility_review_item_count"] == 6
    assert package_result["d11_carry_forward_resolution_count"] == 6
    assert package_result["explainability_limitation_count"] == 8


def test_d12_reporting_package_preserves_lifecycle_boundary(package_result):
    assert package_result["locked_test_accessed"] is False
    assert package_result["deployment_authorized"] is False


# ============================================================
# D12-RT.02 — ARTIFACT EXISTENCE
# ============================================================

def test_d12_all_expected_artifacts_exist():
    paths = [
        report.D12_MANIFEST_PATH,
        report.D12_CONTRACT_PATH,
        report.D12_GATE_PATH,
        report.D12_GLOBAL_TRANSFORMED_PATH,
        report.D12_GLOBAL_SOURCE_FAMILY_PATH,
        report.D12_DIRECTIONALITY_PATH,
        report.D12_LOCAL_CASES_PATH,
        report.D12_LOCAL_CONTRIBUTORS_PATH,
        report.D12_STABILITY_PATH,
        report.D12_CLINICAL_PLAUSIBILITY_PATH,
        report.D12_D11_CARRY_FORWARD_PATH,
        report.D12_LIMITATIONS_PATH,
        report.D12_INTEGRITY_PATH,
    ]
    assert len(paths) == 13
    assert all(path.exists() for path in paths)
    assert all(path.stat().st_size > 0 for path in paths)


# ============================================================
# D12-RT.03 — MANIFEST & GOVERNANCE DOCUMENTS
# ============================================================

def test_d12_manifest_contains_frozen_identity():
    text = report.D12_MANIFEST_PATH.read_text(encoding="utf-8")
    assert 'stage: "D12"' in text
    assert d12.D12_EXPECTED_MODEL_SHA256 in text
    assert d12.D12_EXPECTED_D7_PREPROCESSOR_SHA256 in text
    assert d12.D12_EXPECTED_D7_SCHEMA_SHA256 in text
    assert "development_threshold: 0.12" in text
    assert "validation_encounters: 15052" in text
    assert "locked_test_accessed: false" in text
    assert "deployment_authorized: false" in text


def test_d12_contract_contains_governance_boundary():
    text = report.D12_CONTRACT_PATH.read_text(encoding="utf-8")
    assert "Explainability & Model Interpretation Governance Contract" in text
    assert "Locked TEST evaluation stage: D14" in text
    assert "SHAP values are not interpreted as direct probability-point changes" in text
    assert "D12 progression is not deployment authorization" in text


def test_d12_gate_decision_contains_final_disposition():
    text = report.D12_GATE_PATH.read_text(encoding="utf-8")
    assert d12.D12_GOVERNANCE_DISPOSITION in text
    assert "Progression authorized: **True**" in text
    assert "Deployment authorized: **False**" in text
    assert "The locked TEST set remains reserved for D14" in text


# ============================================================
# D12-RT.04 — CSV EVIDENCE COUNTS
# ============================================================

def _read_csv(path: Path):
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_d12_global_transformed_attribution_has_49_rows():
    rows = _read_csv(report.D12_GLOBAL_TRANSFORMED_PATH)
    assert len(rows) == 49


def test_d12_global_source_family_attribution_has_10_rows():
    rows = _read_csv(report.D12_GLOBAL_SOURCE_FAMILY_PATH)
    assert len(rows) == 10
    assert {row["source_feature_family"] for row in rows} == set(
        d12.D12_SOURCE_FEATURE_FAMILIES
    )


def test_d12_local_case_table_has_5_rows():
    rows = _read_csv(report.D12_LOCAL_CASES_PATH)
    assert len(rows) == 5


def test_d12_local_contributor_table_has_50_rows():
    rows = _read_csv(report.D12_LOCAL_CONTRIBUTORS_PATH)
    # 5 cases × (5 upward + 5 downward contributors)
    assert len(rows) == 50


def test_d12_stability_table_has_42_rows():
    rows = _read_csv(report.D12_STABILITY_PATH)
    assert len(rows) == 42
    adequate = [row for row in rows if row["support_adequate"] == "True"]
    low_support = [row for row in rows if row["support_adequate"] == "False"]
    assert len(adequate) == 34
    assert len(low_support) == 8


def test_d12_clinical_plausibility_table_has_6_rows():
    rows = _read_csv(report.D12_CLINICAL_PLAUSIBILITY_PATH)
    assert len(rows) == 6


def test_d12_d11_carry_forward_table_has_6_rows():
    rows = _read_csv(report.D12_D11_CARRY_FORWARD_PATH)
    assert len(rows) == 6
    assert [row["carry_forward_id"] for row in rows] == [
        "D11-CF-01",
        "D11-CF-02",
        "D11-CF-03",
        "D11-CF-04",
        "D11-CF-05",
        "D11-CF-06",
    ]


def test_d12_limitations_table_has_8_rows():
    rows = _read_csv(report.D12_LIMITATIONS_PATH)
    assert len(rows) == 8
    assert [row["limitation_id"] for row in rows] == [
        "D12-LIM-01",
        "D12-LIM-02",
        "D12-LIM-03",
        "D12-LIM-04",
        "D12-LIM-05",
        "D12-LIM-06",
        "D12-LIM-07",
        "D12-LIM-08",
    ]


# ============================================================
# D12-RT.05 — ARTIFACT INTEGRITY
# ============================================================

def test_d12_integrity_table_has_12_governed_artifacts():
    rows = _read_csv(report.D12_INTEGRITY_PATH)
    assert len(rows) == 12
    assert all(row["exists"] == "True" for row in rows)
    assert all(int(row["size_bytes"]) > 0 for row in rows)
    assert all(len(row["sha256"]) == 64 for row in rows)


def test_d12_integrity_hashes_match_current_artifacts():
    rows = _read_csv(report.D12_INTEGRITY_PATH)
    for row in rows:
        path = Path(row["artifact"])
        assert path.exists()
        assert report._sha256(path) == row["sha256"]


# ============================================================
# D12-RT.06 — DETERMINISTIC REPORTING CONTROL
# ============================================================

def test_d12_reporting_manifest_has_no_generated_timestamp():
    text = report.D12_MANIFEST_PATH.read_text(encoding="utf-8").lower()
    assert "generated_at" not in text
    assert "timestamp" not in text


def test_d12_reporting_does_not_authorize_deployment():
    manifest = report.D12_MANIFEST_PATH.read_text(encoding="utf-8")
    gate = report.D12_GATE_PATH.read_text(encoding="utf-8")
    assert "deployment_authorized: false" in manifest
    assert "Deployment authorized: **False**" in gate