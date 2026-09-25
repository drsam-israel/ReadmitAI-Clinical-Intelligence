# ============================================================
# D13 — MODEL REGISTRY & ARTIFACT FREEZE TESTS
# ============================================================
# Purpose:
#   Independently test the D13 registry boundary, frozen artifact
#   integrity, source-feature contract, software provenance, formal
#   registry record, freeze manifest, change control, and D13 gate.
#
# Safety boundary:
#   These tests must not retrain, refit, retune, generate predictions,
#   access/evaluate the locked TEST partition, or authorize deployment.
# ============================================================

from __future__ import annotations

import hashlib
import json

import pytest

from src.features import preprocessing as d7
from src.models import registry as d13


# ============================================================
# D13.T01 — STATIC GOVERNANCE CONTRACT
# ============================================================

def test_d13_static_boundary_passes() -> None:
    result = d13.validate_d13_static_registry_boundary()
    assert result["validation_status"] == "PASS"
    assert result["failed_checks"] == []


def test_d13_static_boundary_preserves_test_and_deployment_boundary() -> None:
    result = d13.build_d13_static_registry_boundary()
    assert result["evaluation_partition"] == "NONE"
    assert result["locked_test_accessed"] is False
    assert result["locked_test_evaluated"] is False
    assert result["deployment_authorized"] is False
    assert "locked_test_access" in result["prohibited_activities"]
    assert "locked_test_evaluation" in result["prohibited_activities"]
    assert "deployment_authorization" in result["prohibited_activities"]


def test_d13_static_boundary_points_to_d12_freeze_and_d14_next() -> None:
    result = d13.build_d13_static_registry_boundary()
    assert result["source_lifecycle_stage"] == "D12"
    assert result["source_git_commit"] == "4e995f2"
    assert result["next_lifecycle_stage"] == "D14_LOCKED_TEST_EVALUATION"


# ============================================================
# D13.T02 — FROZEN ARTIFACT IDENTITY
# ============================================================

def test_d13_frozen_artifact_identity_passes() -> None:
    result = d13.validate_d13_frozen_artifact_identity()
    assert result["validation_status"] == "PASS"
    assert result["failed_checks"] == []


@pytest.mark.parametrize(
    ("actual_key", "expected"),
    (
        ("model_sha256", d13.D13_EXPECTED_MODEL_SHA256),
        ("preprocessor_sha256", d13.D13_EXPECTED_D7_PREPROCESSOR_SHA256),
        ("schema_sha256", d13.D13_EXPECTED_D7_SCHEMA_SHA256),
    ),
)
def test_d13_frozen_artifact_hashes_match(
    actual_key: str,
    expected: str,
) -> None:
    result = d13.validate_d13_frozen_artifact_identity()
    assert result[actual_key] == expected


def test_d13_artifact_verification_is_read_only() -> None:
    result = d13.validate_d13_frozen_artifact_identity()
    assert result["artifact_sizes_unchanged"] is True
    assert result["artifact_mtimes_unchanged"] is True
    assert result["model_loaded"] is False
    assert result["model_retrained"] is False
    assert result["preprocessor_loaded"] is False
    assert result["preprocessor_refitted"] is False
    assert result["predictions_generated"] is False
    assert result["threshold_retuned"] is False


# ============================================================
# D13.T03 — REGISTERED CANDIDATE IDENTITY
# ============================================================

def test_d13_registered_candidate_identity_passes() -> None:
    result = d13.validate_d13_registered_candidate_identity()
    assert result["validation_status"] == "PASS"
    assert result["failed_checks"] == []
    assert result["registry_id"] == "DIABETES_READMISSION_XGB_D13_V1"
    assert result["model_version"] == "1.0.0"


def test_d13_model_metadata_hash_is_frozen() -> None:
    result = d13.validate_d13_registered_candidate_identity()
    assert (
        result["model_metadata_sha256"]
        == d13.D13_EXPECTED_D8_MODEL_METADATA_SHA256
    )
    assert result["model_metadata_sha256_verified"] is True
    assert result["model_metadata_size_unchanged"] is True
    assert result["model_metadata_mtime_unchanged"] is True


# ============================================================
# D13.T04 — AUTHORITATIVE SOURCE FEATURE CONTRACT
# ============================================================

def test_d13_source_feature_contract_passes() -> None:
    result = d13.validate_d13_source_feature_contract()
    assert result["validation_status"] == "PASS"
    assert result["failed_checks"] == []


def test_d13_source_features_equal_authoritative_d7_order() -> None:
    result = d13.build_d13_source_feature_contract()
    assert result["primary_candidate_features"] == list(
        d7.PRIMARY_CANDIDATE_FEATURES
    )
    assert result["categorical_features"] == list(d7.CATEGORICAL_FEATURES)
    assert result["numeric_features"] == list(d7.NUMERIC_FEATURES)


def test_d13_source_feature_contract_counts_are_frozen() -> None:
    result = d13.build_d13_source_feature_contract()
    assert result["expected_raw_feature_count"] == 10
    assert result["expected_transformed_feature_count"] == 49
    assert len(result["primary_candidate_features"]) == 10
    assert len(result["categorical_features"]) == 5
    assert len(result["numeric_features"]) == 5


def test_d13_source_feature_contract_hash_is_deterministic() -> None:
    first = d13.build_d13_source_feature_contract()
    second = d13.build_d13_source_feature_contract()
    assert first["source_feature_contract_sha256"] == second[
        "source_feature_contract_sha256"
    ]
    expected = hashlib.sha256(
        first["canonical_contract_json"].encode("utf-8")
    ).hexdigest().upper()
    assert first["source_feature_contract_sha256"] == expected


# ============================================================
# D13.T05 — FINAL SYSTEM IDENTITY
# ============================================================

def test_d13_final_registered_candidate_identity_passes() -> None:
    result = d13.validate_d13_final_registered_candidate_identity()
    assert result["final_validation_status"] == "PASS"
    assert result["final_failed_checks"] == []


def test_d13_final_system_fingerprint_is_deterministic() -> None:
    first = d13.build_d13_final_registered_candidate_identity()
    second = d13.build_d13_final_registered_candidate_identity()
    assert first["candidate_system_sha256"] == second[
        "candidate_system_sha256"
    ]
    expected = hashlib.sha256(
        first["final_identity_material"].encode("utf-8")
    ).hexdigest().upper()
    assert first["candidate_system_sha256"] == expected


def test_d13_final_system_fingerprint_binds_feature_contract() -> None:
    result = d13.validate_d13_final_registered_candidate_identity()
    assert result["feature_contract_bound_to_system_identity"] is True
    assert result["candidate_system_sha256"] != result[
        "intermediate_candidate_system_sha256"
    ]


# ============================================================
# D13.T06 — SOFTWARE ENVIRONMENT PROVENANCE
# ============================================================

def test_d13_software_environment_provenance_passes() -> None:
    result = d13.validate_d13_software_environment_provenance()
    assert result["validation_status"] == "PASS"
    assert result["failed_checks"] == []


def test_d13_software_environment_hash_is_deterministic() -> None:
    result = d13.build_d13_software_environment_provenance()
    expected = hashlib.sha256(
        result["canonical_environment_json"].encode("utf-8")
    ).hexdigest().upper()
    assert result["software_environment_sha256"] == expected


def test_d13_software_environment_contains_verified_components() -> None:
    result = d13.build_d13_software_environment_provenance()
    environment = result["software_environment"]
    assert environment["python"] == "3.13.15"
    assert environment["numpy"] == "2.5.3"
    assert environment["pandas"] == "3.0.5"
    assert environment["scikit_learn"] == "1.9.1"
    assert environment["xgboost"] == "3.4.1"
    assert environment["joblib"] == "1.6.0"
    assert environment["shap"] == "0.52.0"
    assert environment["git"] == "2.55.0.windows.3"


# ============================================================
# D13.T07 — FORMAL REGISTRY EVIDENCE & CHANGE CONTROL
# ============================================================

def test_d13_registry_evidence_bundle_passes() -> None:
    result = d13.validate_d13_registry_evidence_bundle()
    assert result["validation_status"] == "PASS"
    assert result["failed_checks"] == []


def test_d13_artifact_inventory_contains_required_components() -> None:
    result = d13.build_d13_registry_evidence_bundle()
    components = {
        item["component"] for item in result["artifact_inventory"]
    }
    assert components == {
        "selected_model",
        "model_metadata",
        "preprocessor",
        "transformed_feature_schema",
        "source_feature_contract",
    }
    assert all(
        item["frozen"] is True
        for item in result["artifact_inventory"]
    )


def test_d13_change_control_requires_new_identity_after_change() -> None:
    result = d13.build_d13_registry_evidence_bundle()
    change = result["change_control_status"]
    assert change["registered_candidate_mutated"] is False
    assert change["feature_contract_changed"] is False
    assert change["post_freeze_change_requires_new_identity"] is True


def test_d13_formal_registry_record_is_json_serializable() -> None:
    record = d13.build_d13_formal_registry_record()
    serialized = json.dumps(record, sort_keys=True)
    assert serialized
    assert record["evaluation_partition"] == "NONE"


# ============================================================
# D13.T08 — FREEZE MANIFEST & GATE
# ============================================================

def test_d13_freeze_manifest_is_deterministic() -> None:
    first = d13.build_d13_freeze_manifest()
    second = d13.build_d13_freeze_manifest()
    assert first["freeze_manifest_sha256"] == second[
        "freeze_manifest_sha256"
    ]
    expected = hashlib.sha256(
        first["canonical_registry_record_json"].encode("utf-8")
    ).hexdigest().upper()
    assert first["freeze_manifest_sha256"] == expected


def test_d13_gate_passes_for_progression_to_d14_only() -> None:
    result = d13.build_d13_registry_gate_decision()
    assert result["validation_status"] == "PASS"
    assert result["gate_disposition"] == (
        "PASS_PROGRESS_TO_D14_LOCKED_TEST_EVALUATION"
    )
    assert result["progression_to_d14_authorized"] is True
    assert result["deployment_authorized"] is False
    assert result["locked_test_accessed"] is False
    assert result["locked_test_evaluated"] is False
    assert result["failed_checks"] == []


# ============================================================
# D13.T09 — NEGATIVE / TAMPER-DETECTION TESTS
# ============================================================

def test_d13_static_validation_detects_test_access_tamper() -> None:
    boundary = d13.build_d13_static_registry_boundary()
    boundary["locked_test_accessed"] = True
    result = d13.validate_d13_static_registry_boundary(boundary)
    assert result["validation_status"] == "FAIL"
    assert "locked_test_not_accessed" in result["failed_checks"]


def test_d13_feature_contract_validation_detects_count_tamper() -> None:
    contract = d13.build_d13_source_feature_contract()
    contract["primary_candidate_features"] = contract[
        "primary_candidate_features"
    ][:-1]
    result = d13.validate_d13_source_feature_contract(contract)
    assert result["validation_status"] == "FAIL"
    assert "raw_feature_count_matches_d7" in result["failed_checks"]


def test_d13_registry_bundle_validation_detects_test_access_tamper() -> None:
    bundle = d13.build_d13_registry_evidence_bundle()
    bundle["locked_test_accessed"] = True
    result = d13.validate_d13_registry_evidence_bundle(bundle)
    assert result["validation_status"] == "FAIL"
    assert "locked_test_not_accessed" in result["failed_checks"]
