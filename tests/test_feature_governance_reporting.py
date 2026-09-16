# ============================================================
# D4 — FEATURE GOVERNANCE EVIDENCE PACKAGE TESTS
# ============================================================

from pathlib import Path

import pandas as pd
import pytest
import yaml

from src.data.feature_governance import (
    APPROVED,
    CONDITIONAL,
    BLOCKED,
    IDENTIFIER_ONLY,
    TARGET_ONLY,
)
from src.data.feature_governance_reporting import (
    FEATURE_REGISTER_PATH,
    LEAKAGE_REGISTER_PATH,
    DISPOSITION_SUMMARY_PATH,
    PREDICTION_TIME_CONTRACT_PATH,
    GOVERNANCE_REPORT_PATH,
    GATE_DECISION_PATH,
    MANIFEST_PATH,
    generate_d4_evidence_package,
)


# ============================================================
# D4.RT1 — SHARED EVIDENCE PACKAGE
# ============================================================

@pytest.fixture(scope="module")
def d4_evidence():
    return generate_d4_evidence_package()


# ============================================================
# D4.RT2 — GENERATOR STATUS
# ============================================================

def test_d4_evidence_generation_succeeds(d4_evidence):
    assert d4_evidence["status"] == "SUCCESS"


def test_d4_gate_is_pass(d4_evidence):
    assert d4_evidence["gate_decision"] == "PASS"


def test_d4_evidence_counts_reconcile(d4_evidence):
    assert d4_evidence["total_fields"] == 51
    assert d4_evidence["approved"] == 8
    assert d4_evidence["conditional"] == 33
    assert d4_evidence["blocked"] == 6
    assert d4_evidence["identifier_only"] == 2
    assert d4_evidence["target_only"] == 2
    assert d4_evidence["unassessed"] == 0


# ============================================================
# D4.RT3 — REQUIRED ARTIFACT EXISTENCE
# ============================================================

@pytest.mark.parametrize(
    "path",
    [
        FEATURE_REGISTER_PATH,
        LEAKAGE_REGISTER_PATH,
        DISPOSITION_SUMMARY_PATH,
        PREDICTION_TIME_CONTRACT_PATH,
        GOVERNANCE_REPORT_PATH,
        GATE_DECISION_PATH,
        MANIFEST_PATH,
    ],
)
def test_required_d4_artifact_exists(
    d4_evidence,
    path,
):
    assert Path(path).exists()
    assert Path(path).is_file()
    assert Path(path).stat().st_size > 0


# ============================================================
# D4.RT4 — FEATURE GOVERNANCE REGISTER
# ============================================================

def test_feature_register_contains_51_fields(d4_evidence):
    register = pd.read_csv(
        FEATURE_REGISTER_PATH
    )

    assert len(register) == 51


def test_feature_register_has_no_unassessed_fields(
    d4_evidence,
):
    register = pd.read_csv(
        FEATURE_REGISTER_PATH
    )

    assert not (
        register[
            "governance_disposition"
        ]
        == "UNASSESSED"
    ).any()


def test_feature_register_dispositions_are_valid(
    d4_evidence,
):
    register = pd.read_csv(
        FEATURE_REGISTER_PATH
    )

    valid = {
        APPROVED,
        CONDITIONAL,
        BLOCKED,
        IDENTIFIER_ONLY,
        TARGET_ONLY,
    }

    assert set(
        register[
            "governance_disposition"
        ].unique()
    ) == valid


def test_feature_register_has_unique_features(
    d4_evidence,
):
    register = pd.read_csv(
        FEATURE_REGISTER_PATH
    )

    assert (
        register["feature"]
        .duplicated()
        .sum()
        == 0
    )


# ============================================================
# D4.RT5 — IDENTIFIER AND TARGET SAFETY
# ============================================================

def test_identifier_fields_are_not_predictors(
    d4_evidence,
):
    register = pd.read_csv(
        FEATURE_REGISTER_PATH
    )

    identifiers = register[
        register["feature"].isin(
            {
                "encounter_id",
                "patient_nbr",
            }
        )
    ]

    assert (
        identifiers[
            "governance_disposition"
        ]
        == IDENTIFIER_ONLY
    ).all()


def test_target_fields_are_not_predictors(
    d4_evidence,
):
    register = pd.read_csv(
        FEATURE_REGISTER_PATH
    )

    targets = register[
        register["feature"].isin(
            {
                "readmitted",
                "readmitted_30d",
            }
        )
    ]

    assert (
        targets[
            "governance_disposition"
        ]
        == TARGET_ONLY
    ).all()


# ============================================================
# D4.RT6 — BLOCKED FEATURE SAFETY
# ============================================================

def test_expected_retrospective_fields_are_blocked(
    d4_evidence,
):
    register = pd.read_csv(
        FEATURE_REGISTER_PATH
    )

    expected_blocked = {
        "discharge_disposition_id",
        "time_in_hospital",
        "num_lab_procedures",
        "num_procedures",
        "num_medications",
        "number_diagnoses",
    }

    actual_blocked = set(
        register.loc[
            register[
                "governance_disposition"
            ] == BLOCKED,
            "feature",
        ]
    )

    assert actual_blocked == expected_blocked


# ============================================================
# D4.RT7 — LEAKAGE DECISION REGISTER
# ============================================================

def test_leakage_register_excludes_directly_approved_fields(
    d4_evidence,
):
    leakage = pd.read_csv(
        LEAKAGE_REGISTER_PATH
    )

    assert not (
        leakage[
            "governance_disposition"
        ]
        == APPROVED
    ).any()


def test_leakage_register_contains_43_fields(
    d4_evidence,
):
    leakage = pd.read_csv(
        LEAKAGE_REGISTER_PATH
    )

    # 33 conditional
    # + 6 blocked
    # + 2 identifiers
    # + 2 targets
    assert len(leakage) == 43


def test_leakage_register_contains_no_missing_decisions(
    d4_evidence,
):
    leakage = pd.read_csv(
        LEAKAGE_REGISTER_PATH
    )

    required_columns = [
        "governance_disposition",
        "prediction_time_status",
        "leakage_risk",
        "rationale",
        "permitted_use",
    ]

    assert not leakage[
        required_columns
    ].isna().any().any()


# ============================================================
# D4.RT8 — DISPOSITION SUMMARY
# ============================================================

def test_disposition_summary_reconciles_to_51(
    d4_evidence,
):
    summary = pd.read_csv(
        DISPOSITION_SUMMARY_PATH
    )

    assert int(
        summary[
            "feature_count"
        ].sum()
    ) == 51


def test_disposition_summary_counts_are_correct(
    d4_evidence,
):
    summary = pd.read_csv(
        DISPOSITION_SUMMARY_PATH
    )

    counts = dict(
        zip(
            summary[
                "governance_disposition"
            ],
            summary[
                "feature_count"
            ],
        )
    )

    assert counts[APPROVED] == 8
    assert counts[CONDITIONAL] == 33
    assert counts[BLOCKED] == 6
    assert counts[IDENTIFIER_ONLY] == 2
    assert counts[TARGET_ONLY] == 2


# ============================================================
# D4.RT9 — PREDICTION-TIME CONTRACT DOCUMENT
# ============================================================

def test_prediction_time_contract_contains_core_controls(
    d4_evidence,
):
    text = (
        PREDICTION_TIME_CONTRACT_PATH
        .read_text(
            encoding="utf-8"
        )
    )

    assert "Prediction-Time Governance Contract" in text
    assert "before discharge" in text.lower()
    assert "locked test" in text.lower()
    assert "30 days" in text.lower()


# ============================================================
# D4.RT10 — GOVERNANCE REPORT
# ============================================================

def test_governance_report_contains_key_controls(
    d4_evidence,
):
    text = (
        GOVERNANCE_REPORT_PATH
        .read_text(
            encoding="utf-8"
        )
    )

    normalized_text = " ".join(
        text.split()
    )

    assert "Total governed fields: 51" in normalized_text
    assert "APPROVED: 8" in normalized_text
    assert "CONDITIONAL: 33" in normalized_text
    assert "BLOCKED: 6" in normalized_text
    assert "No unassessed fields remain" in normalized_text
    assert "locked-test" in normalized_text.lower()


def test_governance_report_blocks_direct_conditional_use(
    d4_evidence,
):
    text = (
        GOVERNANCE_REPORT_PATH
        .read_text(
            encoding="utf-8"
        )
    )

    normalized_text = " ".join(
        text.split()
    )

    assert (
        "No CONDITIONAL or BLOCKED field "
        "is authorized for direct primary "
        "model entry"
    ) in normalized_text

# ============================================================
# D4.RT11 — GATE DECISION
# ============================================================

def test_gate_decision_is_pass(
    d4_evidence,
):
    text = (
        GATE_DECISION_PATH
        .read_text(
            encoding="utf-8"
        )
    )

    assert "**PASS**" in text


def test_gate_does_not_approve_clinical_deployment(
    d4_evidence,
):
    text = (
        GATE_DECISION_PATH
        .read_text(
            encoding="utf-8"
        )
    )

    assert "**NOT APPROVED**" in text


def test_gate_requires_patient_level_splitting(
    d4_evidence,
):
    text = (
        GATE_DECISION_PATH
        .read_text(
            encoding="utf-8"
        )
    )

    assert (
        "Patient-level disjoint splitting"
        in text
    )


def test_gate_protects_locked_test(
    d4_evidence,
):
    text = (
        GATE_DECISION_PATH
        .read_text(
            encoding="utf-8"
        )
    )

    assert "Locked-test data" in text


# ============================================================
# D4.RT12 — MACHINE-READABLE MANIFEST
# ============================================================

def test_d4_manifest_is_valid_yaml(
    d4_evidence,
):
    manifest = yaml.safe_load(
        MANIFEST_PATH.read_text(
            encoding="utf-8"
        )
    )

    assert isinstance(
        manifest,
        dict,
    )


def test_d4_manifest_gate_is_pass(
    d4_evidence,
):
    manifest = yaml.safe_load(
        MANIFEST_PATH.read_text(
            encoding="utf-8"
        )
    )

    assert (
        manifest[
            "gate_decision"
        ]
        == "PASS"
    )


def test_d4_manifest_field_counts_reconcile(
    d4_evidence,
):
    manifest = yaml.safe_load(
        MANIFEST_PATH.read_text(
            encoding="utf-8"
        )
    )

    counts = manifest[
        "field_counts"
    ]

    assert counts["total"] == 51
    assert counts["approved"] == 8
    assert counts["conditional"] == 33
    assert counts["blocked"] == 6
    assert (
        counts[
            "identifier_governance_only"
        ]
        == 2
    )
    assert counts["target_outcome"] == 2
    assert counts["unassessed"] == 0


def test_d4_manifest_requires_locked_test_protection(
    d4_evidence,
):
    manifest = yaml.safe_load(
        MANIFEST_PATH.read_text(
            encoding="utf-8"
        )
    )

    assert (
        manifest[
            "mandatory_controls"
        ][
            "locked_test_protection_required"
        ]
        is True
    )


def test_d4_manifest_prohibits_blocked_features(
    d4_evidence,
):
    manifest = yaml.safe_load(
        MANIFEST_PATH.read_text(
            encoding="utf-8"
        )
    )

    assert (
        manifest[
            "mandatory_controls"
        ][
            "blocked_features_prohibited"
        ]
        is True
    )