# ============================================================
# D13 — MODEL REGISTRY & ARTIFACT FREEZE REPORTING TESTS
# ============================================================
# Purpose:
#   Verify the D13 reporting layer and persisted governance evidence.
#   These tests must not access/evaluate locked TEST, retrain/refit,
#   retune the threshold, or authorize deployment.
# ============================================================

from __future__ import annotations

import csv
import json
from pathlib import Path

from src.models import registry as d13
from src.models import registry_reporting as reporting


# ============================================================
# D13.RT01 — REPORTING BUNDLE
# ============================================================

def test_d13_reporting_bundle_passes() -> None:
    result = reporting.validate_d13_reporting_bundle()
    assert result["reporting_validation_status"] == "PASS"
    assert result["reporting_failed_checks"] == []
    assert result["locked_test_accessed"] is False
    assert result["locked_test_evaluated"] is False
    assert result["deployment_authorized"] is False


def test_d13_reporting_bundle_preserves_candidate_identity() -> None:
    result = reporting.validate_d13_reporting_bundle()
    assert (
        result["system_identity"]["candidate_system_sha256"]
        == "9349A52C715517666540C0D5B1EDB148D48709C0FC2CC77BE9B53F10FE373679"
    )
    assert (
        result["gate_decision"]["candidate_system_sha256"]
        == result["system_identity"]["candidate_system_sha256"]
    )


# ============================================================
# D13.RT02 — PERSIST EVIDENCE PACKAGE
# ============================================================

def test_d13_persist_reporting_evidence_passes() -> None:
    result = reporting.persist_d13_reporting_evidence()
    assert result["validation_status"] == "PASS"
    assert result["artifact_count"] == 10
    assert result["locked_test_accessed"] is False
    assert result["locked_test_evaluated"] is False
    assert result["deployment_authorized"] is False


def test_d13_all_expected_reporting_artifacts_exist() -> None:
    reporting.persist_d13_reporting_evidence()
    expected = [
        reporting.D13_REGISTRY_RECORD_PATH,
        reporting.D13_FREEZE_MANIFEST_PATH,
        reporting.D13_CONTRACT_PATH,
        reporting.D13_GATE_DECISION_PATH,
        reporting.D13_REGISTERED_CANDIDATE_TABLE_PATH,
        reporting.D13_ARTIFACT_INVENTORY_PATH,
        reporting.D13_SOFTWARE_ENVIRONMENT_PATH,
        reporting.D13_FEATURE_CONTRACT_PATH,
        reporting.D13_CHANGE_CONTROL_PATH,
        reporting.D13_LIFECYCLE_PROVENANCE_PATH,
    ]
    assert all(Path(path).exists() for path in expected)
    assert all(Path(path).stat().st_size > 0 for path in expected)


# ============================================================
# D13.RT03 — FORMAL REGISTRY JSON
# ============================================================

def test_d13_persisted_registry_record_identity() -> None:
    reporting.persist_d13_reporting_evidence()
    record = json.loads(
        reporting.D13_REGISTRY_RECORD_PATH.read_text(encoding="utf-8")
    )
    assert record["registry_id"] == "DIABETES_READMISSION_XGB_D13_V1"
    assert record["model_version"] == "1.0.0"
    assert record["candidate_system_sha256"] == (
        "9349A52C715517666540C0D5B1EDB148D48709C0FC2CC77BE9B53F10FE373679"
    )
    assert record["source_feature_contract_sha256"] == (
        "277CCC7C847B2FE6882A4072EA991B1FEF701D0222471B8B1F583DE06924C0BC"
    )
    assert record["software_environment_sha256"] == (
        "D008029639FF03569910412173B84B557C3694A12B24ED8198E06F38616A6E7E"
    )
    assert record["evaluation_partition"] == "NONE"
    assert record["locked_test_accessed"] is False
    assert record["locked_test_evaluated"] is False
    assert record["deployment_authorized"] is False


# ============================================================
# D13.RT04 — FREEZE MANIFEST
# ============================================================

def test_d13_persisted_freeze_manifest_identity() -> None:
    reporting.persist_d13_reporting_evidence()
    manifest = json.loads(
        reporting.D13_FREEZE_MANIFEST_PATH.read_text(encoding="utf-8")
    )
    assert manifest["freeze_status"] == "FROZEN_PENDING_D14_LOCKED_TEST"
    assert manifest["freeze_manifest_sha256"] == (
        "0F278573E2C4D139E6D0968DD624AB7C1304825D3B805B6FEF288162051B6119"
    )
    assert manifest["candidate_system_sha256"] == (
        "9349A52C715517666540C0D5B1EDB148D48709C0FC2CC77BE9B53F10FE373679"
    )
    assert manifest["post_freeze_change_requires_new_identity"] is True
    assert manifest["locked_test_accessed"] is False
    assert manifest["locked_test_evaluated"] is False
    assert manifest["deployment_authorized"] is False


# ============================================================
# D13.RT05 — REGISTERED CANDIDATE TABLE
# ============================================================

def test_d13_registered_candidate_table_contains_one_candidate() -> None:
    reporting.persist_d13_reporting_evidence()
    with reporting.D13_REGISTERED_CANDIDATE_TABLE_PATH.open(
        encoding="utf-8",
        newline="",
    ) as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 1
    row = rows[0]
    assert row["registry_id"] == "DIABETES_READMISSION_XGB_D13_V1"
    assert row["candidate_system_sha256"] == (
        "9349A52C715517666540C0D5B1EDB148D48709C0FC2CC77BE9B53F10FE373679"
    )
    assert row["development_operating_threshold"] == "0.12"
    assert row["source_feature_count"] == "10"
    assert row["transformed_feature_count"] == "49"
    assert row["locked_test_accessed"] == "False"
    assert row["deployment_authorized"] == "False"


# ============================================================
# D13.RT06 — ARTIFACT INVENTORY
# ============================================================

def test_d13_artifact_inventory_has_five_frozen_components() -> None:
    reporting.persist_d13_reporting_evidence()
    with reporting.D13_ARTIFACT_INVENTORY_PATH.open(
        encoding="utf-8",
        newline="",
    ) as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 5
    assert {row["component"] for row in rows} == {
        "selected_model",
        "model_metadata",
        "preprocessor",
        "transformed_feature_schema",
        "source_feature_contract",
    }
    assert all(row["frozen"] == "True" for row in rows)
    assert all(len(row["sha256"]) == 64 for row in rows)


# ============================================================
# D13.RT07 — SOFTWARE ENVIRONMENT
# ============================================================

def test_d13_software_environment_table_contains_verified_stack() -> None:
    reporting.persist_d13_reporting_evidence()
    with reporting.D13_SOFTWARE_ENVIRONMENT_PATH.open(
        encoding="utf-8",
        newline="",
    ) as handle:
        rows = list(csv.DictReader(handle))

    environment = {
        row["component"]: row["version_or_value"]
        for row in rows
    }
    assert environment["python"] == "3.13.15"
    assert environment["numpy"] == "2.5.3"
    assert environment["pandas"] == "3.0.5"
    assert environment["scikit_learn"] == "1.9.1"
    assert environment["xgboost"] == "3.4.1"
    assert environment["joblib"] == "1.6.0"
    assert environment["shap"] == "0.52.0"
    assert environment["git"] == "2.55.0.windows.3"


# ============================================================
# D13.RT08 — FEATURE CONTRACT
# ============================================================

def test_d13_feature_contract_table_preserves_order_and_types() -> None:
    reporting.persist_d13_reporting_evidence()
    with reporting.D13_FEATURE_CONTRACT_PATH.open(
        encoding="utf-8",
        newline="",
    ) as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 10
    assert [row["feature_name"] for row in rows] == [
        "race",
        "gender",
        "age",
        "admission_type_id",
        "admission_source_id",
        "prior_outpatient_use",
        "prior_emergency_use",
        "prior_inpatient_use",
        "prior_utilization_intensity",
        "prior_utilization_domain_count",
    ]
    assert [row["feature_type"] for row in rows[:5]] == [
        "categorical"
    ] * 5
    assert [row["feature_type"] for row in rows[5:]] == [
        "numeric"
    ] * 5
    assert all(
        row["authorized_for_primary_pathway"] == "True"
        for row in rows
    )
    assert all(
        row["source_feature_contract_sha256"]
        == "277CCC7C847B2FE6882A4072EA991B1FEF701D0222471B8B1F583DE06924C0BC"
        for row in rows
    )


# ============================================================
# D13.RT09 — CHANGE CONTROL & LIFECYCLE PROVENANCE
# ============================================================

def test_d13_change_control_record_blocks_silent_mutation() -> None:
    reporting.persist_d13_reporting_evidence()
    with reporting.D13_CHANGE_CONTROL_PATH.open(
        encoding="utf-8",
        newline="",
    ) as handle:
        rows = list(csv.DictReader(handle))

    controls = {row["control"]: row["value"] for row in rows}
    assert controls["registered_candidate_mutated"] == "False"
    assert controls["model_retrained"] == "False"
    assert controls["preprocessor_refitted"] == "False"
    assert controls["feature_contract_changed"] == "False"
    assert controls["threshold_retuned"] == "False"
    assert controls["probability_recalibrated"] == "False"
    assert controls["locked_test_accessed"] == "False"
    assert controls["locked_test_evaluated"] == "False"
    assert controls["deployment_authorized"] == "False"
    assert controls["post_freeze_change_requires_new_identity"] == "True"


def test_d13_lifecycle_provenance_reaches_d13_and_points_to_d14() -> None:
    reporting.persist_d13_reporting_evidence()
    with reporting.D13_LIFECYCLE_PROVENANCE_PATH.open(
        encoding="utf-8",
        newline="",
    ) as handle:
        rows = list(csv.DictReader(handle))

    provenance = {
        row["stage_or_reference"]: row["provenance"]
        for row in rows
    }
    assert provenance["D12"] == (
        "explainability_and_model_interpretation_governance"
    )
    assert provenance["D13"] == "model_registry_and_artifact_freeze"
    assert provenance["D13_source_git_commit"] == "4e995f2"
    assert provenance["next_stage"] == "D14_LOCKED_TEST_EVALUATION"


# ============================================================
# D13.RT10 — GOVERNANCE DOCUMENTS
# ============================================================

def test_d13_contract_documents_safety_boundary() -> None:
    reporting.persist_d13_reporting_evidence()
    text = reporting.D13_CONTRACT_PATH.read_text(encoding="utf-8")
    assert "9349A52C715517666540C0D5B1EDB148D48709C0FC2CC77BE9B53F10FE373679" in text
    assert "Locked TEST accessed in D13: **False**" in text
    assert "Deployment authorized: **False**" in text
    assert "does not authorize clinical deployment" in text


def test_d13_gate_document_authorizes_d14_not_deployment() -> None:
    reporting.persist_d13_reporting_evidence()
    text = reporting.D13_GATE_DECISION_PATH.read_text(encoding="utf-8")
    assert "PASS_PROGRESS_TO_D14_LOCKED_TEST_EVALUATION" in text
    assert "Progression to D14 authorized: `True`" in text
    assert "Locked TEST accessed: `False`" in text
    assert "Deployment authorized: `False`" in text


# ============================================================
# D13.RT11 — CROSS-LAYER IDENTITY CONSISTENCY
# ============================================================

def test_d13_runtime_and_persisted_evidence_share_same_identity() -> None:
    reporting.persist_d13_reporting_evidence()

    runtime = d13.validate_d13_final_registered_candidate_identity()
    record = json.loads(
        reporting.D13_REGISTRY_RECORD_PATH.read_text(encoding="utf-8")
    )
    manifest = json.loads(
        reporting.D13_FREEZE_MANIFEST_PATH.read_text(encoding="utf-8")
    )

    expected = runtime["candidate_system_sha256"]
    assert record["candidate_system_sha256"] == expected
    assert manifest["candidate_system_sha256"] == expected


def test_d13_runtime_gate_and_persisted_manifest_share_freeze_hash() -> None:
    reporting.persist_d13_reporting_evidence()

    runtime_gate = d13.build_d13_registry_gate_decision()
    manifest = json.loads(
        reporting.D13_FREEZE_MANIFEST_PATH.read_text(encoding="utf-8")
    )
    assert (
        manifest["freeze_manifest_sha256"]
        == runtime_gate["freeze_manifest_sha256"]
    )
