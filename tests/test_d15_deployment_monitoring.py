# ============================================================
# D15 — DEPLOYMENT & MONITORING DESIGN
# CONTROLLED INFERENCE SERVICE TESTS
# ============================================================
#
# Purpose:
# Verify that the D15 controlled inference service:
#
#   - executes the frozen inference chain correctly;
#   - preserves frozen candidate identity;
#   - enforces the D6 feature-governance contract;
#   - uses frozen D7 preprocessing without refitting;
#   - uses the frozen D8 model;
#   - preserves the D9 operating threshold;
#   - produces advisory-only output;
#   - emits audit and monitoring evidence;
#   - fails closed for invalid inference requests.
#
# These tests do NOT authorize production deployment.
# ============================================================

import math

import numpy as np
import pandas as pd
import pytest

import src.models.deployment_monitoring as d15


# ============================================================
# SECTION 01 — GOVERNED TEST FIXTURES
# ============================================================


@pytest.fixture
def valid_inference_record():
    """
    Plausible technical smoke-test record.

    This record is used only to test the governed inference
    pathway. It is not a clinical validation case.
    """

    return {
        "race": "Caucasian",
        "gender": "Female",
        "age": "[70-80)",
        "admission_type_id": 1,
        "admission_source_id": 7,
        "number_outpatient": 0,
        "number_emergency": 0,
        "number_inpatient": 1,
    }


@pytest.fixture
def zero_utilization_record():
    return {
        "race": "Caucasian",
        "gender": "Male",
        "age": "[60-70)",
        "admission_type_id": 1,
        "admission_source_id": 7,
        "number_outpatient": 0,
        "number_emergency": 0,
        "number_inpatient": 0,
    }


# ============================================================
# SECTION 02 — ARCHITECTURE CONTRACT TESTS
# ============================================================


def test_d15_architecture_gate_passes():
    evidence = (
        d15.validate_d15_deployment_architecture()
    )

    assert evidence["overall_pass"] is True
    assert evidence["validation_status"] == "PASS"
    assert (
        evidence[
            "production_deployment_authorized"
        ]
        is False
    )


def test_d15_architecture_has_twelve_layers():
    assert len(
        d15.D15_ARCHITECTURE_LAYERS
    ) == 12


def test_d15_inference_flow_is_frozen():
    assert d15.D15_INFERENCE_FLOW == (
        "INPUT_CAPTURE",
        "INPUT_VALIDATION",
        "GOVERNED_FEATURE_ENGINEERING",
        "FROZEN_PREPROCESSING",
        "FROZEN_MODEL_INFERENCE",
        "FROZEN_OPERATING_POINT",
        "ADVISORY_OUTPUT",
    )


def test_d15_production_remains_unauthorized():
    assert (
        d15.D15_PRODUCTION_DEPLOYMENT_AUTHORIZED
        is False
    )


# ============================================================
# SECTION 03 — FROZEN ARTIFACT IDENTITY TESTS
# ============================================================


def test_d15_frozen_artifact_identity_passes():
    evidence = (
        d15.validate_d15_frozen_artifact_identity()
    )

    assert evidence["overall_pass"] is True
    assert evidence["validation_status"] == "PASS"


def test_d15_preprocessor_hash_is_frozen():
    snapshot = (
        d15.snapshot_d15_frozen_artifacts()
    )

    assert (
        snapshot["preprocessor_sha256"]
        == d15.D15_EXPECTED_D7_PREPROCESSOR_SHA256
    )


def test_d15_schema_hash_is_frozen():
    snapshot = (
        d15.snapshot_d15_frozen_artifacts()
    )

    assert (
        snapshot["schema_sha256"]
        == d15.D15_EXPECTED_D7_SCHEMA_SHA256
    )


def test_d15_model_hash_is_frozen():
    snapshot = (
        d15.snapshot_d15_frozen_artifacts()
    )

    assert (
        snapshot["model_sha256"]
        == d15.D15_EXPECTED_D8_MODEL_SHA256
    )


def test_d15_metadata_hash_is_frozen():
    snapshot = (
        d15.snapshot_d15_frozen_artifacts()
    )

    assert (
        snapshot["metadata_sha256"]
        == d15.D15_EXPECTED_D8_METADATA_SHA256
    )


def test_d15_artifact_identity_detects_wrong_hash():
    snapshot = (
        d15.snapshot_d15_frozen_artifacts()
    )

    snapshot["model_sha256"] = (
        "0" * 64
    )

    evidence = (
        d15.validate_d15_frozen_artifact_identity(
            snapshot
        )
    )

    assert evidence["overall_pass"] is False

    assert (
        evidence["checks"][
            "model_sha256_valid"
        ]
        is False
    )


# ============================================================
# SECTION 04 — RAW INPUT VALIDATION TESTS
# ============================================================


def test_d15_valid_input_passes(
    valid_inference_record,
):
    df = pd.DataFrame(
        [valid_inference_record]
    )

    evidence = (
        d15.validate_d15_inference_input(
            df
        )
    )

    assert evidence["overall_pass"] is True


def test_d15_missing_required_input_fails(
    valid_inference_record,
):
    record = valid_inference_record.copy()

    record.pop(
        "number_inpatient"
    )

    df = pd.DataFrame(
        [record]
    )

    evidence = (
        d15.validate_d15_inference_input(
            df
        )
    )

    assert evidence["overall_pass"] is False

    assert (
        evidence["checks"][
            "all_required_inputs_present"
        ]
        is False
    )


def test_d15_missing_value_fails(
    valid_inference_record,
):
    record = valid_inference_record.copy()

    record["race"] = None

    df = pd.DataFrame(
        [record]
    )

    evidence = (
        d15.validate_d15_inference_input(
            df
        )
    )

    assert evidence["overall_pass"] is False


def test_d15_negative_utilization_fails(
    valid_inference_record,
):
    record = valid_inference_record.copy()

    record["number_inpatient"] = -1

    df = pd.DataFrame(
        [record]
    )

    evidence = (
        d15.validate_d15_inference_input(
            df
        )
    )

    assert evidence["overall_pass"] is False

    assert (
        evidence["checks"][
            "utilization_counts_nonnegative"
        ]
        is False
    )


def test_d15_fractional_utilization_fails(
    valid_inference_record,
):
    record = valid_inference_record.copy()

    record["number_emergency"] = 1.5

    df = pd.DataFrame(
        [record]
    )

    evidence = (
        d15.validate_d15_inference_input(
            df
        )
    )

    assert evidence["overall_pass"] is False

    assert (
        evidence["checks"][
            "utilization_counts_integer_like"
        ]
        is False
    )


def test_d15_non_numeric_utilization_fails(
    valid_inference_record,
):
    record = valid_inference_record.copy()

    record["number_outpatient"] = "invalid"

    df = pd.DataFrame(
        [record]
    )

    evidence = (
        d15.validate_d15_inference_input(
            df
        )
    )

    assert evidence["overall_pass"] is False


def test_d15_multiple_encounters_fail(
    valid_inference_record,
):
    df = pd.DataFrame(
        [
            valid_inference_record,
            valid_inference_record,
        ]
    )

    evidence = (
        d15.validate_d15_inference_input(
            df
        )
    )

    assert evidence["overall_pass"] is False

    assert (
        evidence["checks"][
            "exactly_one_encounter"
        ]
        is False
    )


# ============================================================
# SECTION 05 — D6 GOVERNED FEATURE TESTS
# ============================================================


def test_d15_d6_primary_feature_count(
    valid_inference_record,
):
    df = pd.DataFrame(
        [valid_inference_record]
    )

    bundle = (
        d15.build_d15_governed_primary_features(
            df
        )
    )

    assert (
        bundle[
            "primary_features"
        ].shape
        == (1, 10)
    )

    assert (
        bundle[
            "candidate_feature_count"
        ]
        == 10
    )


def test_d15_d6_conditional_features_excluded(
    valid_inference_record,
):
    df = pd.DataFrame(
        [valid_inference_record]
    )

    bundle = (
        d15.build_d15_governed_primary_features(
            df
        )
    )

    assert (
        bundle[
            "conditional_features_in_primary_matrix"
        ]
        == []
    )


def test_d15_d6_registry_reconciles(
    valid_inference_record,
):
    df = pd.DataFrame(
        [valid_inference_record]
    )

    bundle = (
        d15.build_d15_governed_primary_features(
            df
        )
    )

    assert (
        bundle["candidate_feature_count"]
        == 10
    )

    assert (
        bundle["conditional_feature_count"]
        == 30
    )

    assert (
        bundle["registered_feature_count"]
        == 40
    )


def test_d15_utilization_engineering_one_domain(
    valid_inference_record,
):
    df = pd.DataFrame(
        [valid_inference_record]
    )

    bundle = (
        d15.build_d15_governed_primary_features(
            df
        )
    )

    row = bundle[
        "primary_features"
    ].iloc[0]

    assert (
        row["prior_outpatient_use"]
        == 0
    )

    assert (
        row["prior_emergency_use"]
        == 0
    )

    assert (
        row["prior_inpatient_use"]
        == 1
    )

    assert (
        row["prior_utilization_intensity"]
        == 1
    )

    assert (
        row[
            "prior_utilization_domain_count"
        ]
        == 1
    )


def test_d15_zero_utilization_engineering(
    zero_utilization_record,
):
    df = pd.DataFrame(
        [zero_utilization_record]
    )

    bundle = (
        d15.build_d15_governed_primary_features(
            df
        )
    )

    row = bundle[
        "primary_features"
    ].iloc[0]

    assert (
        row["prior_utilization_intensity"]
        == 0
    )

    assert (
        row[
            "prior_utilization_domain_count"
        ]
        == 0
    )


# ============================================================
# SECTION 06 — FROZEN PREPROCESSING TESTS
# ============================================================


def test_d15_preprocessing_produces_49_features(
    valid_inference_record,
):
    df = pd.DataFrame(
        [valid_inference_record]
    )

    features = (
        d15.build_d15_governed_primary_features(
            df
        )
    )

    bundle = (
        d15.transform_d15_with_frozen_preprocessor(
            features[
                "primary_features"
            ]
        )
    )

    assert (
        bundle[
            "transformed_features"
        ].shape
        == (1, 49)
    )


def test_d15_preprocessor_is_not_refitted(
    valid_inference_record,
):
    df = pd.DataFrame(
        [valid_inference_record]
    )

    features = (
        d15.build_d15_governed_primary_features(
            df
        )
    )

    bundle = (
        d15.transform_d15_with_frozen_preprocessor(
            features[
                "primary_features"
            ]
        )
    )

    assert (
        bundle["preprocessor_refitted"]
        is False
    )

    assert (
        bundle["schema_modified"]
        is False
    )


def test_d15_transformed_values_are_finite(
    valid_inference_record,
):
    df = pd.DataFrame(
        [valid_inference_record]
    )

    features = (
        d15.build_d15_governed_primary_features(
            df
        )
    )

    bundle = (
        d15.transform_d15_with_frozen_preprocessor(
            features[
                "primary_features"
            ]
        )
    )

    values = (
        bundle[
            "transformed_features"
        ].to_numpy(
            dtype=float
        )
    )

    assert (
        pd.notna(values).all()
    )

    assert (
        np.isfinite(
            values
        ).all()
    )


# ============================================================
# SECTION 07 — FROZEN OPERATING-POINT TESTS
# ============================================================


def test_d15_probability_below_threshold():
    flag = (
        d15.build_d15_advisory_flag(
            0.119999
        )
    )

    assert (
        flag
        == "NO_MODEL_PRIORITY_FLAG"
    )


def test_d15_probability_at_threshold():
    flag = (
        d15.build_d15_advisory_flag(
            0.12
        )
    )

    assert (
        flag
        == "PRIORITIZE_FOR_HUMAN_REVIEW"
    )


def test_d15_probability_above_threshold():
    flag = (
        d15.build_d15_advisory_flag(
            0.120001
        )
    )

    assert (
        flag
        == "PRIORITIZE_FOR_HUMAN_REVIEW"
    )


def test_d15_threshold_remains_frozen():
    assert (
        d15.D15_FROZEN_OPERATING_THRESHOLD
        == 0.12
    )


# ============================================================
# SECTION 08 — END-TO-END SERVICE TESTS
# ============================================================


def test_d15_controlled_inference_passes(
    valid_inference_record,
):
    evidence = (
        d15.run_d15_controlled_inference(
            valid_inference_record
        )
    )

    assert (
        evidence[
            "service_validation"
        ][
            "overall_pass"
        ]
        is True
    )

    assert (
        evidence[
            "service_validation"
        ][
            "validation_status"
        ]
        == "PASS"
    )


def test_d15_probability_is_valid(
    valid_inference_record,
):
    evidence = (
        d15.run_d15_controlled_inference(
            valid_inference_record
        )
    )

    probability = evidence[
        "advisory_output"
    ][
        "prediction_probability"
    ]

    assert math.isfinite(
        probability
    )

    assert (
        0.0
        <= probability
        <= 1.0
    )


def test_d15_smoke_test_probability_is_reproducible(
    valid_inference_record,
):
    evidence = (
        d15.run_d15_controlled_inference(
            valid_inference_record
        )
    )

    probability = evidence[
        "advisory_output"
    ][
        "prediction_probability"
    ]

    assert probability == pytest.approx(
        0.13454879820346832,
        abs=1e-12,
    )


def test_d15_smoke_test_crosses_frozen_threshold(
    valid_inference_record,
):
    evidence = (
        d15.run_d15_controlled_inference(
            valid_inference_record
        )
    )

    assert (
        evidence[
            "advisory_output"
        ][
            "advisory_flag"
        ]
        == "PRIORITIZE_FOR_HUMAN_REVIEW"
    )


def test_d15_output_is_advisory(
    valid_inference_record,
):
    evidence = (
        d15.run_d15_controlled_inference(
            valid_inference_record
        )
    )

    output = evidence[
        "advisory_output"
    ]

    assert (
        output["output_classification"]
        == "CLINICAL_DECISION_SUPPORT_ADVISORY"
    )

    assert (
        output["human_review_required"]
        is True
    )


def test_d15_output_does_not_authorize_deployment(
    valid_inference_record,
):
    evidence = (
        d15.run_d15_controlled_inference(
            valid_inference_record
        )
    )

    assert (
        evidence[
            "production_deployment_authorized"
        ]
        is False
    )

    assert (
        evidence[
            "advisory_output"
        ][
            "deployment_authorized"
        ]
        is False
    )


def test_d15_model_not_modified(
    valid_inference_record,
):
    before = (
        d15.snapshot_d15_frozen_artifacts()
    )

    evidence = (
        d15.run_d15_controlled_inference(
            valid_inference_record
        )
    )

    after = (
        d15.snapshot_d15_frozen_artifacts()
    )

    assert before == after

    assert (
        evidence[
            "model_retrained"
        ]
        is False
    )

    assert (
        evidence[
            "model_retuned"
        ]
        is False
    )

    assert (
        evidence[
            "model_recalibrated"
        ]
        is False
    )

    assert (
        evidence[
            "threshold_retuned"
        ]
        is False
    )


# ============================================================
# SECTION 09 — FAIL-CLOSED SERVICE TESTS
# ============================================================


def test_d15_service_blocks_missing_input(
    valid_inference_record,
):
    record = valid_inference_record.copy()

    record.pop(
        "race"
    )

    with pytest.raises(
        d15.D15InferenceBlockedError
    ):
        d15.run_d15_controlled_inference(
            record
        )


def test_d15_service_blocks_negative_utilization(
    valid_inference_record,
):
    record = valid_inference_record.copy()

    record["number_inpatient"] = -1

    with pytest.raises(
        d15.D15InferenceBlockedError
    ):
        d15.run_d15_controlled_inference(
            record
        )


def test_d15_service_blocks_fractional_utilization(
    valid_inference_record,
):
    record = valid_inference_record.copy()

    record["number_emergency"] = 0.5

    with pytest.raises(
        d15.D15InferenceBlockedError
    ):
        d15.run_d15_controlled_inference(
            record
        )


def test_d15_service_blocks_multiple_encounters(
    valid_inference_record,
):
    df = pd.DataFrame(
        [
            valid_inference_record,
            valid_inference_record,
        ]
    )

    with pytest.raises(
        d15.D15InferenceBlockedError
    ):
        d15.run_d15_controlled_inference(
            df
        )


def test_d15_service_blocks_invalid_input_type():
    with pytest.raises(
        d15.D15InferenceBlockedError
    ):
        d15.run_d15_controlled_inference(
            "not-a-valid-input"
        )


# ============================================================
# SECTION 10 — AUDIT CONTRACT TESTS
# ============================================================


def test_d15_audit_event_is_emitted(
    valid_inference_record,
):
    evidence = (
        d15.run_d15_controlled_inference(
            valid_inference_record
        )
    )

    audit = evidence[
        "audit_event"
    ]

    assert (
        audit["event_type"]
        == "INFERENCE_COMPLETED"
    )

    assert (
        audit["inference_status"]
        == "COMPLETED"
    )


def test_d15_audit_contains_required_fields(
    valid_inference_record,
):
    evidence = (
        d15.run_d15_controlled_inference(
            valid_inference_record
        )
    )

    audit = evidence[
        "audit_event"
    ]

    assert set(
        d15.D15_REQUIRED_AUDIT_FIELDS
    ).issubset(
        set(
            audit.keys()
        )
    )


def test_d15_audit_preserves_frozen_identity(
    valid_inference_record,
):
    evidence = (
        d15.run_d15_controlled_inference(
            valid_inference_record
        )
    )

    audit = evidence[
        "audit_event"
    ]

    assert (
        audit["registry_id"]
        == d15.D15_EXPECTED_REGISTRY_ID
    )

    assert (
        audit["model_version"]
        == d15.D15_EXPECTED_MODEL_VERSION
    )

    assert (
        audit["frozen_threshold"]
        == 0.12
    )


# ============================================================
# SECTION 11 — MONITORING TELEMETRY TESTS
# ============================================================


def test_d15_monitoring_telemetry_emitted(
    valid_inference_record,
):
    evidence = (
        d15.run_d15_controlled_inference(
            valid_inference_record
        )
    )

    telemetry = evidence[
        "monitoring_telemetry"
    ]

    assert (
        telemetry["registry_id"]
        == d15.D15_EXPECTED_REGISTRY_ID
    )

    assert (
        telemetry["model_version"]
        == d15.D15_EXPECTED_MODEL_VERSION
    )


def test_d15_monitoring_contains_probability(
    valid_inference_record,
):
    evidence = (
        d15.run_d15_controlled_inference(
            valid_inference_record
        )
    )

    telemetry = evidence[
        "monitoring_telemetry"
    ]

    assert (
        0.0
        <= telemetry[
            "prediction_probability"
        ]
        <= 1.0
    )


def test_d15_monitoring_contains_utilization_controls(
    valid_inference_record,
):
    evidence = (
        d15.run_d15_controlled_inference(
            valid_inference_record
        )
    )

    telemetry = evidence[
        "monitoring_telemetry"
    ]

    assert (
        telemetry[
            "prior_utilization_intensity"
        ]
        == 1.0
    )

    assert (
        telemetry[
            "prior_utilization_domain_count"
        ]
        == 1
    )


# ============================================================
# SECTION 12 — GOVERNANCE BOUNDARY TESTS
# ============================================================


def test_d15_no_subgroup_threshold_created(
    valid_inference_record,
):
    evidence = (
        d15.run_d15_controlled_inference(
            valid_inference_record
        )
    )

    assert (
        evidence[
            "subgroup_threshold_created"
        ]
        is False
    )


def test_d15_human_review_remains_required(
    valid_inference_record,
):
    evidence = (
        d15.run_d15_controlled_inference(
            valid_inference_record
        )
    )

    assert (
        evidence[
            "advisory_output"
        ][
            "human_review_required"
        ]
        is True
    )


def test_d15_external_validation_not_established():
    contract = (
        d15.build_d15_governance_contract()
    )

    assert (
        contract.external_validation_established
        is False
    )


def test_d15_clinical_effectiveness_not_established():
    contract = (
        d15.build_d15_governance_contract()
    )

    assert (
        contract.clinical_effectiveness_established
        is False
    )


# ============================================================
# END OF D15 CONTROLLED INFERENCE SERVICE TESTS
# ============================================================