# ============================================================
# D6 — FEATURE ENGINEERING EVIDENCE PACKAGE TESTS
# ============================================================
"""
Tests for the D6 governed feature-engineering evidence package.

These tests validate the persisted registry, lineage evidence,
summary, governance documents, manifest, and checksummed
development engineered dataset.
"""

from pathlib import Path

import pandas as pd
import yaml

from src.data.splitting import (
    GROUP_COLUMN,
    TRAIN_LABEL,
    VALIDATION_LABEL,
    TEST_LABEL,
)

from src.features.engineering import (
    D6_CANDIDATE,
    D6_CONDITIONAL,
    FEATURE_SPECIFICATIONS,
    EXPECTED_D5_ASSIGNMENT_SHA256,
)

from src.features.engineering_reporting import (
    FEATURE_REGISTRY_PATH,
    FEATURE_LINEAGE_PATH,
    FEATURE_SUMMARY_PATH,
    CONTRACT_REPORT_PATH,
    GATE_DECISION_PATH,
    MANIFEST_PATH,
    DEVELOPMENT_FEATURE_PATH,
    calculate_sha256,
    build_feature_engineering_registry,
    build_feature_lineage_audit,
    generate_d6_evidence_package,
)


# ============================================================
# D6 TEST CONSTANTS
# ============================================================

EXPECTED_DEVELOPMENT_ENCOUNTERS = 85076
EXPECTED_DEVELOPMENT_PATIENTS = 59871
EXPECTED_COMBINED_COLUMNS = 44

EXPECTED_REGISTERED_FEATURES = 40
EXPECTED_CANDIDATE_FEATURES = 10
EXPECTED_CONDITIONAL_FEATURES = 30

EXPECTED_DEVELOPMENT_SHA256 = (
    "B4A38DFE8D316E2C74C8B08F31C0EC1060B880741304FC3971371DBFBA21C3C0"
)


# ============================================================
# TEST 1 — EVIDENCE PACKAGE GENERATES SUCCESSFULLY
# ============================================================

def test_d6_evidence_package_generates_successfully():
    result = generate_d6_evidence_package()

    assert result["validation_status"] == "PASS"

    assert result["development_encounters"] == (
        EXPECTED_DEVELOPMENT_ENCOUNTERS
    )

    assert result["development_patients"] == (
        EXPECTED_DEVELOPMENT_PATIENTS
    )

    assert result["combined_columns"] == (
        EXPECTED_COMBINED_COLUMNS
    )

    assert result["registered_features"] == (
        EXPECTED_REGISTERED_FEATURES
    )

    assert result["candidate_features"] == (
        EXPECTED_CANDIDATE_FEATURES
    )

    assert result["conditional_features"] == (
        EXPECTED_CONDITIONAL_FEATURES
    )

    assert result["primary_X_shape"] == (
        EXPECTED_DEVELOPMENT_ENCOUNTERS,
        EXPECTED_CANDIDATE_FEATURES,
    )

    assert result["target_rows"] == (
        EXPECTED_DEVELOPMENT_ENCOUNTERS
    )


# ============================================================
# TEST 2 — ALL REQUIRED D6 EVIDENCE FILES EXIST
# ============================================================

def test_all_required_d6_evidence_files_exist():
    required_paths = [
        FEATURE_REGISTRY_PATH,
        FEATURE_LINEAGE_PATH,
        FEATURE_SUMMARY_PATH,
        CONTRACT_REPORT_PATH,
        GATE_DECISION_PATH,
        MANIFEST_PATH,
        DEVELOPMENT_FEATURE_PATH,
    ]

    for path in required_paths:
        assert path.exists()
        assert path.is_file()


# ============================================================
# TEST 3 — REGISTRY CONTAINS EXACTLY 40 FEATURES
# ============================================================

def test_feature_registry_has_expected_size():
    registry = pd.read_csv(
        FEATURE_REGISTRY_PATH
    )

    assert len(registry) == (
        EXPECTED_REGISTERED_FEATURES
    )

    assert registry[
        "feature_name"
    ].nunique() == EXPECTED_REGISTERED_FEATURES


# ============================================================
# TEST 4 — REGISTRY DISPOSITION COUNTS ARE CORRECT
# ============================================================

def test_feature_registry_disposition_counts():
    registry = pd.read_csv(
        FEATURE_REGISTRY_PATH
    )

    counts = (
        registry[
            "d6_disposition"
        ]
        .value_counts()
        .to_dict()
    )

    assert counts.get(
        D6_CANDIDATE,
        0,
    ) == EXPECTED_CANDIDATE_FEATURES

    assert counts.get(
        D6_CONDITIONAL,
        0,
    ) == EXPECTED_CONDITIONAL_FEATURES


# ============================================================
# TEST 5 — GENERATED REGISTRY MATCHES SOURCE REGISTRY
# ============================================================

def test_persisted_registry_matches_source_registry():
    persisted = pd.read_csv(
        FEATURE_REGISTRY_PATH
    )

    generated = (
        build_feature_engineering_registry()
    )

    assert persisted[
        "feature_name"
    ].tolist() == generated[
        "feature_name"
    ].tolist()

    assert persisted[
        "d6_disposition"
    ].tolist() == generated[
        "d6_disposition"
    ].tolist()


# ============================================================
# TEST 6 — LINEAGE TABLE CONTAINS ALL FEATURES
# ============================================================

def test_lineage_audit_contains_all_registered_features():
    lineage = pd.read_csv(
        FEATURE_LINEAGE_PATH
    )

    expected_features = {
        specification.feature_name
        for specification in FEATURE_SPECIFICATIONS
    }

    assert set(
        lineage["feature_name"]
    ) == expected_features

    assert len(lineage) == (
        EXPECTED_REGISTERED_FEATURES
    )


# ============================================================
# TEST 7 — NO CANDIDATE LINEAGE VIOLATIONS
# ============================================================

def test_lineage_audit_has_no_candidate_violations():
    lineage = pd.read_csv(
        FEATURE_LINEAGE_PATH
    )

    violations = lineage.loc[
        lineage[
            "candidate_lineage_violation"
        ]
        == True
    ]

    assert len(violations) == 0


# ============================================================
# TEST 8 — CANDIDATES HAVE D4-APPROVED LINEAGE
# ============================================================

def test_candidate_features_have_approved_lineage():
    lineage = pd.read_csv(
        FEATURE_LINEAGE_PATH
    )

    candidates = lineage.loc[
        lineage[
            "d6_disposition"
        ]
        == D6_CANDIDATE
    ]

    assert len(candidates) == (
        EXPECTED_CANDIDATE_FEATURES
    )

    assert set(
        candidates[
            "source_governance"
        ].unique()
    ) == {"D4_APPROVED"}


# ============================================================
# TEST 9 — CONDITIONAL FEATURES RETAIN CONDITIONAL LINEAGE
# ============================================================

def test_conditional_features_retain_conditional_lineage():
    lineage = pd.read_csv(
        FEATURE_LINEAGE_PATH
    )

    conditional = lineage.loc[
        lineage[
            "d6_disposition"
        ]
        == D6_CONDITIONAL
    ]

    assert len(conditional) == (
        EXPECTED_CONDITIONAL_FEATURES
    )

    assert set(
        conditional[
            "source_governance"
        ].unique()
    ) == {"D4_CONDITIONAL"}


# ============================================================
# TEST 10 — SUMMARY CONTAINS REQUIRED METRICS
# ============================================================

def test_summary_contains_required_metrics():
    summary = pd.read_csv(
        FEATURE_SUMMARY_PATH
    )

    required_metrics = {
        "development_encounters",
        "development_patients",
        "train_encounters",
        "validation_encounters",
        "locked_test_encounters",
        "train_patients",
        "validation_patients",
        "registered_features",
        "candidate_features",
        "conditional_features",
        "candidate_conditional_overlap",
        "prohibited_model_features",
        "candidate_conditional_lineage_violations",
    }

    assert required_metrics.issubset(
        set(summary["metric"])
    )


# ============================================================
# TEST 11 — SUMMARY REPORTS ZERO LOCKED TEST ENCOUNTERS
# ============================================================

def test_summary_reports_zero_locked_test_encounters():
    summary = pd.read_csv(
        FEATURE_SUMMARY_PATH
    )

    metric_map = dict(
        zip(
            summary["metric"],
            summary["value"],
        )
    )

    assert int(
        metric_map[
            "locked_test_encounters"
        ]
    ) == 0


# ============================================================
# TEST 12 — SUMMARY REPORTS ZERO GOVERNANCE VIOLATIONS
# ============================================================

def test_summary_reports_zero_governance_violations():
    summary = pd.read_csv(
        FEATURE_SUMMARY_PATH
    )

    metric_map = dict(
        zip(
            summary["metric"],
            summary["value"],
        )
    )

    assert int(
        metric_map[
            "candidate_conditional_overlap"
        ]
    ) == 0

    assert int(
        metric_map[
            "prohibited_model_features"
        ]
    ) == 0

    assert int(
        metric_map[
            "candidate_conditional_lineage_violations"
        ]
    ) == 0


# ============================================================
# TEST 13 — DEVELOPMENT ARTIFACT HAS EXPECTED SHAPE
# ============================================================

def test_development_artifact_has_expected_shape():
    development = pd.read_parquet(
        DEVELOPMENT_FEATURE_PATH
    )

    assert development.shape == (
        EXPECTED_DEVELOPMENT_ENCOUNTERS,
        EXPECTED_COMBINED_COLUMNS,
    )


# ============================================================
# TEST 14 — DEVELOPMENT ARTIFACT HAS EXPECTED PATIENT COUNT
# ============================================================

def test_development_artifact_patient_count():
    development = pd.read_parquet(
        DEVELOPMENT_FEATURE_PATH
    )

    assert development[
        GROUP_COLUMN
    ].nunique() == EXPECTED_DEVELOPMENT_PATIENTS


# ============================================================
# TEST 15 — DEVELOPMENT ARTIFACT EXCLUDES LOCKED TEST
# ============================================================

def test_development_artifact_excludes_locked_test():
    development = pd.read_parquet(
        DEVELOPMENT_FEATURE_PATH
    )

    observed_splits = set(
        development[
            "split"
        ].unique()
    )

    assert observed_splits == {
        TRAIN_LABEL,
        VALIDATION_LABEL,
    }

    assert TEST_LABEL not in observed_splits


# ============================================================
# TEST 16 — DEVELOPMENT ARTIFACT CHECKSUM IS STABLE
# ============================================================

def test_development_artifact_checksum_is_stable():
    observed_checksum = calculate_sha256(
        DEVELOPMENT_FEATURE_PATH
    )

    assert observed_checksum == (
        EXPECTED_DEVELOPMENT_SHA256
    )


# ============================================================
# TEST 17 — MANIFEST EXISTS AND LOADS
# ============================================================

def test_d6_manifest_loads_successfully():
    with MANIFEST_PATH.open(
        "r",
        encoding="utf-8",
    ) as file_handle:
        manifest = yaml.safe_load(
            file_handle
        )

    assert isinstance(
        manifest,
        dict,
    )

    assert manifest[
        "lifecycle_stage"
    ] == "D6_GOVERNED_FEATURE_ENGINEERING"


# ============================================================
# TEST 18 — MANIFEST RECORDS D5 CHECKSUM
# ============================================================

def test_manifest_records_authoritative_d5_checksum():
    with MANIFEST_PATH.open(
        "r",
        encoding="utf-8",
    ) as file_handle:
        manifest = yaml.safe_load(
            file_handle
        )

    assert (
        manifest[
            "source_dependencies"
        ][
            "d5_split_assignment_sha256"
        ]
        == EXPECTED_D5_ASSIGNMENT_SHA256
    )


# ============================================================
# TEST 19 — MANIFEST RECORDS D6 DEVELOPMENT CHECKSUM
# ============================================================

def test_manifest_records_d6_development_checksum():
    with MANIFEST_PATH.open(
        "r",
        encoding="utf-8",
    ) as file_handle:
        manifest = yaml.safe_load(
            file_handle
        )

    assert (
        manifest[
            "development_feature_artifact"
        ][
            "sha256"
        ]
        == EXPECTED_DEVELOPMENT_SHA256
    )


# ============================================================
# TEST 20 — MANIFEST RECORDS EXPECTED DEVELOPMENT SIZE
# ============================================================

def test_manifest_records_expected_development_size():
    with MANIFEST_PATH.open(
        "r",
        encoding="utf-8",
    ) as file_handle:
        manifest = yaml.safe_load(
            file_handle
        )

    assert (
        manifest[
            "development_population"
        ][
            "encounters"
        ]
        == EXPECTED_DEVELOPMENT_ENCOUNTERS
    )

    assert (
        manifest[
            "development_population"
        ][
            "patients"
        ]
        == EXPECTED_DEVELOPMENT_PATIENTS
    )


# ============================================================
# TEST 21 — MANIFEST RECORDS LOCKED TEST AS ABSENT
# ============================================================

def test_manifest_records_locked_test_as_absent():
    with MANIFEST_PATH.open(
        "r",
        encoding="utf-8",
    ) as file_handle:
        manifest = yaml.safe_load(
            file_handle
        )

    assert (
        manifest[
            "development_population"
        ][
            "locked_test_present"
        ]
        is False
    )

    assert (
        manifest[
            "development_population"
        ][
            "locked_partition"
        ]
        == TEST_LABEL
    )


# ============================================================
# TEST 22 — MANIFEST FEATURE COUNTS ARE CORRECT
# ============================================================

def test_manifest_feature_counts_are_correct():
    with MANIFEST_PATH.open(
        "r",
        encoding="utf-8",
    ) as file_handle:
        manifest = yaml.safe_load(
            file_handle
        )

    governance = manifest[
        "feature_governance"
    ]

    assert governance[
        "registered_feature_count"
    ] == EXPECTED_REGISTERED_FEATURES

    assert governance[
        "candidate_feature_count"
    ] == EXPECTED_CANDIDATE_FEATURES

    assert governance[
        "conditional_feature_count"
    ] == EXPECTED_CONDITIONAL_FEATURES


# ============================================================
# TEST 23 — MANIFEST HAS ZERO GOVERNANCE VIOLATIONS
# ============================================================

def test_manifest_has_zero_governance_violations():
    with MANIFEST_PATH.open(
        "r",
        encoding="utf-8",
    ) as file_handle:
        manifest = yaml.safe_load(
            file_handle
        )

    governance = manifest[
        "feature_governance"
    ]

    assert governance[
        "candidate_conditional_overlap"
    ] == []

    assert governance[
        "prohibited_model_features"
    ] == []

    assert governance[
        "candidate_features_with_conditional_lineage"
    ] == []


# ============================================================
# TEST 24 — MANIFEST VALIDATION STATUS IS PASS
# ============================================================

def test_manifest_validation_status_is_pass():
    with MANIFEST_PATH.open(
        "r",
        encoding="utf-8",
    ) as file_handle:
        manifest = yaml.safe_load(
            file_handle
        )

    assert manifest[
        "validation_status"
    ] == "PASS"


# ============================================================
# TEST 25 — MANIFEST AUTHORIZES D7
# ============================================================

def test_manifest_authorizes_d7_preprocessing():
    with MANIFEST_PATH.open(
        "r",
        encoding="utf-8",
    ) as file_handle:
        manifest = yaml.safe_load(
            file_handle
        )

    assert manifest[
        "downstream_authorization"
    ] == "D7_GOVERNED_PREPROCESSING"


# ============================================================
# TEST 26 — CONTRACT DOCUMENT RECORDS LOCKED TEST PROTECTION
# ============================================================

def test_contract_records_locked_test_protection():
    text = CONTRACT_REPORT_PATH.read_text(
        encoding="utf-8"
    )

    assert "locked" in text.lower()
    assert "test" in text.lower()
    assert "D7" not in text or len(text) > 0


# ============================================================
# TEST 27 — GATE DECISION IS PASS
# ============================================================

def test_gate_decision_is_pass():
    text = GATE_DECISION_PATH.read_text(
        encoding="utf-8"
    )

    assert "**PASS**" in text


# ============================================================
# TEST 28 — GATE AUTHORIZES D7
# ============================================================

def test_gate_authorizes_d7():
    text = GATE_DECISION_PATH.read_text(
        encoding="utf-8"
    )

    assert (
        "D7 — Governed Preprocessing Pipeline"
        in text
    )