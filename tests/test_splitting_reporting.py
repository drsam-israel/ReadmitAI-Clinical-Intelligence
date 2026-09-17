# ============================================================
# D5 — SPLIT PERSISTENCE & EVIDENCE PACKAGE TESTS
# ============================================================

from pathlib import Path

import pandas as pd
import yaml

from src.data.splitting import (
    GROUP_COLUMN,
    TRAIN_LABEL,
    VALIDATION_LABEL,
    TEST_LABEL,
)

from src.data.splitting_reporting import (
    PATIENT_ASSIGNMENT_PATH,
    SPLIT_SUMMARY_PATH,
    OVERLAP_AUDIT_PATH,
    SPLIT_CONTRACT_PATH,
    GATE_DECISION_PATH,
    MANIFEST_PATH,
    calculate_sha256,
    generate_d5_evidence_package,
)


# ============================================================
# D5.RT1 — EXPECTED FROZEN CHECKSUM
# ============================================================

EXPECTED_ASSIGNMENT_SHA256 = (
    "D575A296909467EB4CDE7529978D5306C38BFE26959A4EBEA907CE209472977E"
)


# ============================================================
# D5.RT2 — REQUIRED ARTIFACT EXISTENCE
# ============================================================

def test_patient_assignment_exists():
    assert PATIENT_ASSIGNMENT_PATH.exists()


def test_split_summary_exists():
    assert SPLIT_SUMMARY_PATH.exists()


def test_overlap_audit_exists():
    assert OVERLAP_AUDIT_PATH.exists()


def test_split_contract_exists():
    assert SPLIT_CONTRACT_PATH.exists()


def test_gate_decision_exists():
    assert GATE_DECISION_PATH.exists()


def test_manifest_exists():
    assert MANIFEST_PATH.exists()


# ============================================================
# D5.RT3 — AUTHORITATIVE ASSIGNMENT INTEGRITY
# ============================================================

def test_assignment_checksum_matches_frozen_value():
    observed = calculate_sha256(
        PATIENT_ASSIGNMENT_PATH
    )

    assert observed == EXPECTED_ASSIGNMENT_SHA256


def test_assignment_has_expected_patient_count():
    assignment = pd.read_csv(
        PATIENT_ASSIGNMENT_PATH
    )

    assert len(assignment) == 70_439


def test_assignment_has_unique_patients():
    assignment = pd.read_csv(
        PATIENT_ASSIGNMENT_PATH
    )

    assert not assignment[
        GROUP_COLUMN
    ].duplicated().any()


def test_assignment_has_no_missing_split_labels():
    assignment = pd.read_csv(
        PATIENT_ASSIGNMENT_PATH
    )

    assert assignment[
        "split"
    ].notna().all()


def test_assignment_contains_exactly_three_splits():
    assignment = pd.read_csv(
        PATIENT_ASSIGNMENT_PATH
    )

    assert set(
        assignment["split"].unique()
    ) == {
        TRAIN_LABEL,
        VALIDATION_LABEL,
        TEST_LABEL,
    }


# ============================================================
# D5.RT4 — FROZEN PATIENT COUNTS
# ============================================================

def test_frozen_train_patient_count():
    assignment = pd.read_csv(
        PATIENT_ASSIGNMENT_PATH
    )

    assert int(
        (
            assignment["split"]
            == TRAIN_LABEL
        ).sum()
    ) == 49_306


def test_frozen_validation_patient_count():
    assignment = pd.read_csv(
        PATIENT_ASSIGNMENT_PATH
    )

    assert int(
        (
            assignment["split"]
            == VALIDATION_LABEL
        ).sum()
    ) == 10_565


def test_frozen_test_patient_count():
    assignment = pd.read_csv(
        PATIENT_ASSIGNMENT_PATH
    )

    assert int(
        (
            assignment["split"]
            == TEST_LABEL
        ).sum()
    ) == 10_568


# ============================================================
# D5.RT5 — SPLIT SUMMARY INTEGRITY
# ============================================================

def test_split_summary_has_three_rows():
    summary = pd.read_csv(
        SPLIT_SUMMARY_PATH
    )

    assert len(summary) == 3


def test_split_summary_encounters_reconcile():
    summary = pd.read_csv(
        SPLIT_SUMMARY_PATH
    )

    assert int(
        summary["encounters"].sum()
    ) == 100_114


def test_split_summary_patients_reconcile():
    summary = pd.read_csv(
        SPLIT_SUMMARY_PATH
    )

    assert int(
        summary["patients"].sum()
    ) == 70_439


def test_split_summary_positive_outcomes_reconcile():
    summary = pd.read_csv(
        SPLIT_SUMMARY_PATH
    )

    assert int(
        summary[
            "positive_encounters"
        ].sum()
    ) == 11_357


# ============================================================
# D5.RT6 — PATIENT OVERLAP EVIDENCE
# ============================================================

def test_overlap_audit_has_four_controls():
    audit = pd.read_csv(
        OVERLAP_AUDIT_PATH
    )

    assert len(audit) == 4


def test_all_overlap_controls_pass():
    audit = pd.read_csv(
        OVERLAP_AUDIT_PATH
    )

    assert (
        audit["status"]
        == "PASS"
    ).all()


def test_all_observed_overlap_values_are_zero():
    audit = pd.read_csv(
        OVERLAP_AUDIT_PATH
    )

    assert (
        audit[
            "observed_value"
        ] == 0
    ).all()


# ============================================================
# D5.RT7 — MANIFEST GOVERNANCE
# ============================================================

def test_manifest_declares_d5():
    manifest = yaml.safe_load(
        MANIFEST_PATH.read_text(
            encoding="utf-8"
        )
    )

    assert manifest["stage"] == "D5"


def test_manifest_gate_is_pass():
    manifest = yaml.safe_load(
        MANIFEST_PATH.read_text(
            encoding="utf-8"
        )
    )

    assert (
        manifest["gate_decision"]
        == "PASS"
    )


def test_manifest_declares_locked_test():
    manifest = yaml.safe_load(
        MANIFEST_PATH.read_text(
            encoding="utf-8"
        )
    )

    assert (
        manifest[
            "locked_test"
        ]["status"]
        == "LOCKED"
    )

    assert (
        manifest[
            "locked_test"
        ][
            "development_use_permitted"
        ]
        is False
    )


def test_manifest_checksum_matches_artifact():
    manifest = yaml.safe_load(
        MANIFEST_PATH.read_text(
            encoding="utf-8"
        )
    )

    manifest_checksum = (
        manifest[
            "authoritative_assignment"
        ]["sha256"]
    )

    observed_checksum = (
        calculate_sha256(
            PATIENT_ASSIGNMENT_PATH
        )
    )

    assert (
        manifest_checksum
        == observed_checksum
        == EXPECTED_ASSIGNMENT_SHA256
    )


def test_manifest_source_counts_are_correct():
    manifest = yaml.safe_load(
        MANIFEST_PATH.read_text(
            encoding="utf-8"
        )
    )

    assert (
        manifest[
            "source_counts"
        ]["encounters"]
        == 100_114
    )

    assert (
        manifest[
            "source_counts"
        ]["patients"]
        == 70_439
    )


def test_manifest_declares_zero_patient_overlap():
    manifest = yaml.safe_load(
        MANIFEST_PATH.read_text(
            encoding="utf-8"
        )
    )

    overlap = manifest[
        "patient_overlap"
    ]

    assert (
        overlap[
            "multi_split_patients"
        ]
        == 0
    )

    assert (
        overlap[
            "train_validation"
        ]
        == 0
    )

    assert (
        overlap[
            "train_test"
        ]
        == 0
    )

    assert (
        overlap[
            "validation_test"
        ]
        == 0
    )


# ============================================================
# D5.RT8 — HUMAN-READABLE GOVERNANCE DOCUMENTS
# ============================================================

def test_split_contract_prohibits_patient_overlap():
    text = SPLIT_CONTRACT_PATH.read_text(
        encoding="utf-8"
    )

    normalized = " ".join(
        text.split()
    ).lower()

    assert (
        "patient overlap across train, validation, "
        "and locked test is prohibited"
        in normalized
    )


def test_split_contract_protects_locked_test():
    text = SPLIT_CONTRACT_PATH.read_text(
        encoding="utf-8"
    )

    normalized = " ".join(
        text.split()
    ).lower()

    assert (
        "locked test partition must not influence"
        in normalized
    )


def test_gate_document_declares_pass():
    text = GATE_DECISION_PATH.read_text(
        encoding="utf-8"
    )

    normalized = " ".join(
        text.split()
    )

    assert (
        "D5 lifecycle gate: **PASS**"
        in normalized
    )


def test_gate_document_keeps_test_locked():
    text = GATE_DECISION_PATH.read_text(
        encoding="utf-8"
    )

    normalized = " ".join(
        text.split()
    )

    assert (
        "test partition remains **LOCKED**"
        in normalized
    )


def test_gate_document_does_not_approve_deployment():
    text = GATE_DECISION_PATH.read_text(
        encoding="utf-8"
    )

    normalized = " ".join(
        text.split()
    )

    assert (
        "**NOT APPROVED**"
        in normalized
    )


# ============================================================
# D5.RT9 — REGENERATION STABILITY
# ============================================================

def test_regenerated_evidence_preserves_assignment_checksum():
    result = generate_d5_evidence_package()

    assert (
        result[
            "assignment_checksum"
        ]
        == EXPECTED_ASSIGNMENT_SHA256
    )


def test_regenerated_evidence_gate_remains_pass():
    result = generate_d5_evidence_package()

    assert (
        result[
            "gate_decision"
        ]
        == "PASS"
    )


# ============================================================
# D5.RT10 — AUTHORITATIVE ARTIFACT PATH
# ============================================================

def test_manifest_points_to_authoritative_assignment():
    manifest = yaml.safe_load(
        MANIFEST_PATH.read_text(
            encoding="utf-8"
        )
    )

    assert (
        manifest[
            "authoritative_assignment"
        ]["path"]
        ==
        "artifacts/splits/"
        "D5_patient_split_assignment.csv"
    )