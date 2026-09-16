# ============================================================
# D3 — COHORT EVIDENCE PACKAGE TESTS
# ============================================================

import pandas as pd
import yaml

from src.data.cohort import (
    DERIVED_TARGET_COLUMN,
    ENCOUNTER_ID_COLUMN,
    EXPIRED_DISPOSITION_IDS,
    HOSPICE_DISPOSITION_IDS,
)
from src.data.cohort_reporting import (
    COHORT_ARTIFACT_PATH,
    COHORT_FLOW_PATH,
    DISPOSITION_ASSESSMENT_PATH,
    OUTCOME_DISTRIBUTION_PATH,
    EXCLUSION_LOG_PATH,
    COHORT_DEFINITION_REPORT_PATH,
    GATE_DECISION_PATH,
    MANIFEST_PATH,
    calculate_sha256,
    generate_d3_evidence_package,
)


# ============================================================
# D3.RT1 — GENERATOR EXECUTION
# ============================================================

def test_d3_evidence_generator_succeeds():
    result = generate_d3_evidence_package()

    assert result["status"] == "SUCCESS"
    assert result["gate_decision"] == "PASS"
    assert result["governed_encounters"] == 100_114
    assert result["governed_patients"] == 70_439
    assert result["positive_30d"] == 11_357


# ============================================================
# D3.RT2 — REQUIRED ARTIFACT EXISTENCE
# ============================================================

def test_all_d3_artifacts_exist():
    required_paths = [
        COHORT_ARTIFACT_PATH,
        COHORT_FLOW_PATH,
        DISPOSITION_ASSESSMENT_PATH,
        OUTCOME_DISTRIBUTION_PATH,
        EXCLUSION_LOG_PATH,
        COHORT_DEFINITION_REPORT_PATH,
        GATE_DECISION_PATH,
        MANIFEST_PATH,
    ]

    for path in required_paths:
        assert path.exists(), f"Missing D3 artifact: {path}"


# ============================================================
# D3.RT3 — PERSISTED COHORT INTEGRITY
# ============================================================

def test_persisted_cohort_integrity():
    cohort = pd.read_parquet(COHORT_ARTIFACT_PATH)

    assert len(cohort) == 100_114
    assert cohort[ENCOUNTER_ID_COLUMN].duplicated().sum() == 0

    assert int(
        cohort[DERIVED_TARGET_COLUMN].sum()
    ) == 11_357

    assert set(
        cohort[DERIVED_TARGET_COLUMN].unique()
    ) == {0, 1}


def test_persisted_cohort_excludes_expired_dispositions():
    cohort = pd.read_parquet(COHORT_ARTIFACT_PATH)

    assert not cohort[
        "discharge_disposition_id"
    ].isin(EXPIRED_DISPOSITION_IDS).any()


def test_persisted_cohort_retains_hospice():
    cohort = pd.read_parquet(COHORT_ARTIFACT_PATH)

    hospice_count = int(
        cohort[
            "discharge_disposition_id"
        ].isin(HOSPICE_DISPOSITION_IDS).sum()
    )

    assert hospice_count == 771


# ============================================================
# D3.RT4 — COHORT FLOW EVIDENCE
# ============================================================

def test_cohort_flow_table():
    flow = pd.read_csv(COHORT_FLOW_PATH)

    assert len(flow) == 3

    assert int(
        flow.iloc[0]["encounters"]
    ) == 101_766

    assert int(
        flow.iloc[-1]["encounters"]
    ) == 100_114

    assert int(
        flow["excluded_at_stage"].sum()
    ) == 1_652


# ============================================================
# D3.RT5 — OUTCOME DISTRIBUTION EVIDENCE
# ============================================================

def test_outcome_distribution_table():
    outcome = pd.read_csv(
        OUTCOME_DISTRIBUTION_PATH
    )

    distribution = dict(
        zip(
            outcome[DERIVED_TARGET_COLUMN],
            outcome["encounters"],
        )
    )

    assert distribution == {
        0: 88_757,
        1: 11_357,
    }


# ============================================================
# D3.RT6 — EXCLUSION LOG EVIDENCE
# ============================================================

def test_exclusion_log():
    exclusion_log = pd.read_csv(
        EXCLUSION_LOG_PATH
    )

    observed_ids = set(
        exclusion_log[
            "discharge_disposition_id"
        ].astype(int)
    )

    # ID 21 is part of the governed rule but has no
    # observed encounters in this source dataset.
    assert observed_ids == {11, 19, 20}

    assert int(
        exclusion_log["encounters"].sum()
    ) == 1_652

    assert (
        exclusion_log["cohort_action"]
        == "EXCLUDE"
    ).all()


# ============================================================
# D3.RT7 — MANIFEST VALIDATION
# ============================================================

def test_d3_manifest():
    with MANIFEST_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        manifest = yaml.safe_load(file)

    assert manifest["gate"]["decision"] == "PASS"

    assert (
        manifest["cohort"]["governed_encounters"]
        == 100_114
    )

    assert (
        manifest["cohort"]["governed_unique_patients"]
        == 70_439
    )

    assert (
        manifest["outcome"]["positive_count"]
        == 11_357
    )

    assert (
        manifest["governance"][
            "clinical_deployment_approved"
        ]
        is False
    )


# ============================================================
# D3.RT8 — MANIFEST CHECKSUM VALIDATION
# ============================================================

def test_manifest_checksum_matches_persisted_cohort():
    with MANIFEST_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        manifest = yaml.safe_load(file)

    manifest_hash = (
        manifest[
            "persisted_cohort"
        ]["sha256"]
    )

    actual_hash = calculate_sha256(
        COHORT_ARTIFACT_PATH
    )

    assert manifest_hash == actual_hash


# ============================================================
# D3.RT9 — GOVERNANCE DOCUMENTATION
# ============================================================

def test_governance_report_contains_core_controls():
    report = (
        COHORT_DEFINITION_REPORT_PATH
        .read_text(encoding="utf-8")
    )

    assert "100,114" in report
    assert "11,357" in report
    assert "70,439" in report
    assert "Hospice is not treated as equivalent to death" in report
    assert "Raw source dataset remains immutable" in report


def test_gate_decision_document():
    gate = GATE_DECISION_PATH.read_text(
        encoding="utf-8"
    )

    assert "**PASS**" in gate
    assert "D4" in gate
    assert "does not authorize" in gate