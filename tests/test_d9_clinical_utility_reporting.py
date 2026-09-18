# ============================================================
# D9 — CLINICAL UTILITY REPORTING & EVIDENCE TESTS
# ============================================================

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import yaml

from src.models.clinical_utility_reporting import (
    D9_MANIFEST_PATH,
    D9_CONTRACT_PATH,
    D9_GATE_DECISION_PATH,
    D9_THRESHOLD_PERFORMANCE_PATH,
    D9_REFERENCE_THRESHOLD_PATH,
    D9_OPERATING_SCENARIO_PATH,
    D9_CAPACITY_FRONTIER_PATH,
    D9_THRESHOLD_DECISION_PATH,
    D9_DECISION_CURVE_PATH,
    D9_CALIBRATION_TABLE_PATH,
    D9_CALIBRATION_SUMMARY_PATH,
    D9_REQUIRED_EVIDENCE_PATHS,
    ensure_d9_reporting_directories,
    build_d9_reporting_evidence_bundle,
    persist_d9_tabular_evidence,
    build_d9_governance_contract,
    build_d9_gate_decision,
    build_d9_manifest,
    persist_d9_governance_documents,
    validate_d9_persisted_evidence_package,
    run_d9_reporting_pipeline,
)


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture(scope="module")
def evidence_bundle():
    return build_d9_reporting_evidence_bundle()


@pytest.fixture(scope="module")
def reporting_result():
    return run_d9_reporting_pipeline()


# ============================================================
# D9.R01 — ARTIFACT PATH CONTRACT
# ============================================================

def test_d9_required_artifact_count_is_11():
    assert len(D9_REQUIRED_EVIDENCE_PATHS) == 11


def test_d9_required_artifact_paths_are_unique():
    paths = [
        str(path)
        for path in D9_REQUIRED_EVIDENCE_PATHS
    ]

    assert len(paths) == len(set(paths))


def test_d9_manifest_has_yaml_extension():
    assert D9_MANIFEST_PATH.suffix == ".yaml"


def test_d9_governance_documents_have_md_extension():
    assert D9_CONTRACT_PATH.suffix == ".md"
    assert D9_GATE_DECISION_PATH.suffix == ".md"


def test_d9_tabular_artifacts_have_csv_extension():
    table_paths = (
        D9_THRESHOLD_PERFORMANCE_PATH,
        D9_REFERENCE_THRESHOLD_PATH,
        D9_OPERATING_SCENARIO_PATH,
        D9_CAPACITY_FRONTIER_PATH,
        D9_THRESHOLD_DECISION_PATH,
        D9_DECISION_CURVE_PATH,
        D9_CALIBRATION_TABLE_PATH,
        D9_CALIBRATION_SUMMARY_PATH,
    )

    assert all(
        path.suffix == ".csv"
        for path in table_paths
    )


# ============================================================
# D9.R02 — EVIDENCE BUNDLE
# ============================================================

def test_d9_reporting_bundle_has_required_components(
    evidence_bundle,
):
    required = {
        "prediction_bundle",
        "threshold_performance",
        "reference_thresholds",
        "operating_scenarios",
        "capacity_frontier",
        "threshold_decision",
        "decision_curve",
        "selected_threshold_decision_evidence",
        "calibration_table",
        "calibration_summary",
    }

    assert required.issubset(
        evidence_bundle.keys()
    )


def test_d9_reporting_bundle_uses_validation_only(
    evidence_bundle,
):
    assert (
        evidence_bundle[
            "prediction_bundle"
        ][
            "prediction_partition"
        ]
        == "validation"
    )


def test_d9_reporting_bundle_does_not_access_test(
    evidence_bundle,
):
    assert (
        evidence_bundle[
            "prediction_bundle"
        ][
            "locked_test_accessed"
        ]
        is False
    )


def test_d9_reporting_bundle_threshold_is_012(
    evidence_bundle,
):
    assert np.isclose(
        evidence_bundle[
            "threshold_decision"
        ][
            "selected_threshold"
        ],
        0.12,
    )


def test_d9_reporting_bundle_false_negative_count(
    evidence_bundle,
):
    assert (
        evidence_bundle[
            "threshold_decision"
        ][
            "false_negative"
        ]
        == 907
    )


# ============================================================
# D9.R03 — TABULAR EVIDENCE PERSISTENCE
# ============================================================

def test_d9_persisted_threshold_performance_exists(
    reporting_result,
):
    assert D9_THRESHOLD_PERFORMANCE_PATH.exists()


def test_d9_persisted_threshold_performance_has_50_rows(
    reporting_result,
):
    table = pd.read_csv(
        D9_THRESHOLD_PERFORMANCE_PATH
    )

    assert len(table) == 50


def test_d9_persisted_reference_thresholds_have_11_rows(
    reporting_result,
):
    table = pd.read_csv(
        D9_REFERENCE_THRESHOLD_PATH
    )

    assert len(table) == 11


def test_d9_persisted_operating_scenarios_have_4_rows(
    reporting_result,
):
    table = pd.read_csv(
        D9_OPERATING_SCENARIO_PATH
    )

    assert len(table) == 4


def test_d9_persisted_capacity_frontier_has_8_rows(
    reporting_result,
):
    table = pd.read_csv(
        D9_CAPACITY_FRONTIER_PATH
    )

    assert len(table) == 8


def test_d9_persisted_threshold_decision_has_one_row(
    reporting_result,
):
    table = pd.read_csv(
        D9_THRESHOLD_DECISION_PATH
    )

    assert len(table) == 1


def test_d9_persisted_threshold_decision_is_012(
    reporting_result,
):
    table = pd.read_csv(
        D9_THRESHOLD_DECISION_PATH
    )

    assert np.isclose(
        table.loc[
            0,
            "selected_threshold",
        ],
        0.12,
    )


def test_d9_persisted_decision_curve_has_50_rows(
    reporting_result,
):
    table = pd.read_csv(
        D9_DECISION_CURVE_PATH
    )

    assert len(table) == 50


def test_d9_persisted_calibration_has_10_bins(
    reporting_result,
):
    table = pd.read_csv(
        D9_CALIBRATION_TABLE_PATH
    )

    assert len(table) == 10


def test_d9_persisted_calibration_summary_has_one_row(
    reporting_result,
):
    table = pd.read_csv(
        D9_CALIBRATION_SUMMARY_PATH
    )

    assert len(table) == 1


# ============================================================
# D9.R04 — GOVERNANCE CONTRACT
# ============================================================

def test_d9_contract_contains_stage_name(
    evidence_bundle,
):
    contract = build_d9_governance_contract(
        evidence_bundle
    )

    assert (
        "Clinical Utility & Threshold Governance"
        in contract
    )


def test_d9_contract_identifies_validation_only(
    evidence_bundle,
):
    contract = build_d9_governance_contract(
        evidence_bundle
    )

    assert "VALIDATION only" in contract


# ============================================================
# D9.R04 — DEVELOPMENT THRESHOLD CONTRACT EVIDENCE
# ============================================================

def test_d9_contract_contains_development_threshold(
    evidence_bundle,
):
    contract = build_d9_governance_contract(
        evidence_bundle
    )

    assert (
        "**Development operating threshold:** 0.12"
        in contract
    )


def test_d9_contract_contains_false_negative_limitation(
    evidence_bundle,
):
    contract = build_d9_governance_contract(
        evidence_bundle
    )

    assert "907" in contract
    assert "readmissions" in contract.lower()


def test_d9_contract_prohibits_deployment(
    evidence_bundle,
):
    contract = build_d9_governance_contract(
        evidence_bundle
    )

    assert "deployment authorization" in contract.lower()


def test_d9_contract_identifies_risk_prioritization(
    evidence_bundle,
):
    contract = build_d9_governance_contract(
        evidence_bundle
    )

    assert "risk-prioritization aid" in contract


# ============================================================
# D9.R05 — GATE DECISION
# ============================================================

def test_d9_gate_status_is_pass(
    evidence_bundle,
):
    gate = build_d9_gate_decision(
        evidence_bundle
    )

    assert (
        "PASS — AUTHORIZED TO PROCEED TO D10"
        in gate
    )


def test_d9_gate_names_d10(
    evidence_bundle,
):
    gate = build_d9_gate_decision(
        evidence_bundle
    )

    assert "D10 — Fairness & Subgroup Evaluation" in gate


def test_d9_gate_does_not_authorize_deployment(
    evidence_bundle,
):
    gate = build_d9_gate_decision(
        evidence_bundle
    )

    assert "Clinical deployment authorization:" in gate
    assert "**NO**" in gate


def test_d9_gate_contains_sensitivity_limitation(
    evidence_bundle,
):
    gate = build_d9_gate_decision(
        evidence_bundle
    )

    assert "46.39%" in gate
    assert "907" in gate


def test_d9_gate_preserves_locked_test_boundary(
    evidence_bundle,
):
    gate = build_d9_gate_decision(
        evidence_bundle
    )

    assert "locked TEST" in gate


# ============================================================
# D9.R06 — MANIFEST
# ============================================================

def test_d9_manifest_stage_is_d9(
    evidence_bundle,
):
    persisted_tables = {
        "placeholder": "placeholder.csv"
    }

    manifest = build_d9_manifest(
        evidence_bundle,
        persisted_tables,
    )

    assert manifest["stage"] == "D9"


def test_d9_manifest_gate_passes_to_d10(
    evidence_bundle,
):
    manifest = build_d9_manifest(
        evidence_bundle,
        {},
    )

    assert manifest["gate"]["status"] == "PASS"

    assert (
        manifest["gate"]["authorized_next_stage"]
        == "D10"
    )


def test_d9_manifest_threshold_is_012(
    evidence_bundle,
):
    manifest = build_d9_manifest(
        evidence_bundle,
        {},
    )

    assert np.isclose(
        manifest[
            "development_threshold"
        ][
            "threshold"
        ],
        0.12,
    )


def test_d9_manifest_records_907_false_negatives(
    evidence_bundle,
):
    manifest = build_d9_manifest(
        evidence_bundle,
        {},
    )

    assert (
        manifest[
            "operating_characteristics"
        ][
            "false_negative"
        ]
        == 907
    )


def test_d9_manifest_records_model_checksum(
    evidence_bundle,
):
    manifest = build_d9_manifest(
        evidence_bundle,
        {},
    )

    assert (
        manifest[
            "upstream_dependencies"
        ][
            "model_sha256"
        ]
        ==
        "2FD02A54DF759EBAAF0D02D64D5ACE16A519DF016990FAC065AF3249BDA88085"
    )


def test_d9_manifest_records_no_test_access(
    evidence_bundle,
):
    manifest = build_d9_manifest(
        evidence_bundle,
        {},
    )

    assert (
        manifest[
            "governance"
        ][
            "locked_test_accessed"
        ]
        is False
    )


def test_d9_manifest_records_no_deployment(
    evidence_bundle,
):
    manifest = build_d9_manifest(
        evidence_bundle,
        {},
    )

    assert (
        manifest[
            "governance"
        ][
            "deployment_authorized"
        ]
        is False
    )


# ============================================================
# D9.R07 — PERSISTED GOVERNANCE DOCUMENTS
# ============================================================

def test_d9_contract_file_exists(
    reporting_result,
):
    assert D9_CONTRACT_PATH.exists()


def test_d9_gate_file_exists(
    reporting_result,
):
    assert D9_GATE_DECISION_PATH.exists()


def test_d9_manifest_file_exists(
    reporting_result,
):
    assert D9_MANIFEST_PATH.exists()


def test_d9_manifest_is_valid_yaml(
    reporting_result,
):
    content = yaml.safe_load(
        D9_MANIFEST_PATH.read_text(
            encoding="utf-8"
        )
    )

    assert isinstance(content, dict)
    assert content["stage"] == "D9"


def test_d9_persisted_manifest_authorizes_d10(
    reporting_result,
):
    content = yaml.safe_load(
        D9_MANIFEST_PATH.read_text(
            encoding="utf-8"
        )
    )

    assert (
        content["gate"]["authorized_next_stage"]
        == "D10"
    )


def test_d9_persisted_manifest_blocks_deployment(
    reporting_result,
):
    content = yaml.safe_load(
        D9_MANIFEST_PATH.read_text(
            encoding="utf-8"
        )
    )

    assert (
        content[
            "gate"
        ][
            "clinical_deployment_authorized"
        ]
        is False
    )


# ============================================================
# D9.R08 — COMPLETE EVIDENCE PACKAGE
# ============================================================

def test_all_11_d9_artifacts_exist(
    reporting_result,
):
    assert all(
        path.exists()
        for path in D9_REQUIRED_EVIDENCE_PATHS
    )


def test_all_11_d9_artifacts_are_nonempty(
    reporting_result,
):
    assert all(
        path.stat().st_size > 0
        for path in D9_REQUIRED_EVIDENCE_PATHS
    )


def test_d9_persisted_package_validation_passes(
    evidence_bundle,
    reporting_result,
):
    result = (
        validate_d9_persisted_evidence_package(
            evidence_bundle
        )
    )

    assert result["validation_status"] == "PASS"
    assert result["failed_checks"] == []


# ============================================================
# D9.R09 — REPORTING ORCHESTRATION
# ============================================================

def test_d9_reporting_pipeline_passes(
    reporting_result,
):
    assert (
        reporting_result["validation_status"]
        == "PASS"
    )

    assert reporting_result["failed_checks"] == []


def test_d9_reporting_pipeline_has_11_artifacts(
    reporting_result,
):
    assert (
        reporting_result[
            "required_artifact_count"
        ]
        == 11
    )


def test_d9_reporting_pipeline_threshold_is_012(
    reporting_result,
):
    assert np.isclose(
        reporting_result[
            "selected_development_threshold"
        ],
        0.12,
    )


def test_d9_reporting_pipeline_does_not_access_test(
    reporting_result,
):
    assert (
        reporting_result[
            "locked_test_accessed"
        ]
        is False
    )


def test_d9_reporting_pipeline_does_not_authorize_deployment(
    reporting_result,
):
    assert (
        reporting_result[
            "deployment_authorized"
        ]
        is False
    )