# ============================================================
# D14 — LOCKED-TEST POST-ACCESS GOVERNANCE TESTS
# ============================================================
#
# Purpose:
# Validate the controlled post-access D14 evidence chain:
#
#   locked TEST reconstruction
#       -> frozen D7 transformation
#       -> frozen model inference
#       -> confirmatory performance
#       -> subgroup confirmation
#       -> robustness confirmation
#       -> explainability confirmation
#       -> integrated governance disposition
#
# Historical pre-access contract tests remain preserved in:
# tests/test_d14_locked_test_evaluation.py
# ============================================================


from __future__ import annotations

import numpy as np
import pytest

import src.models.locked_test_evaluation as d14


# ============================================================
# FIXTURES — EXPENSIVE EVIDENCE BUILT ONCE PER MODULE
# ============================================================


@pytest.fixture(scope="module")
def access_evidence():
    return d14.build_d14_locked_test_access_evidence()


@pytest.fixture(scope="module")
def transformed_bundle():
    return d14.transform_d14_locked_test_with_frozen_d7()


@pytest.fixture(scope="module")
def prediction_bundle(transformed_bundle):
    return d14.generate_d14_frozen_test_predictions(
        transformed_bundle
    )


@pytest.fixture(scope="module")
def performance_evidence():
    return d14.build_d14_confirmatory_performance_evidence()


@pytest.fixture(scope="module")
def subgroup_evidence():
    return d14.build_d14_subgroup_confirmation_evidence()


@pytest.fixture(scope="module")
def robustness_evidence():
    return d14.build_d14_robustness_confirmation_evidence()


@pytest.fixture(scope="module")
def explainability_evidence():
    return d14.build_d14_explainability_confirmation_evidence()


@pytest.fixture(scope="module")
def residual_risks():
    return d14.build_d14_residual_risk_register()


@pytest.fixture(scope="module")
def integrated_evidence(
    performance_evidence,
    subgroup_evidence,
    robustness_evidence,
    explainability_evidence,
    residual_risks,
):
    return {
        "registry_id":
            d14.D14_EXPECTED_REGISTRY_ID,

        "candidate_system_sha256":
            d14.D14_EXPECTED_CANDIDATE_SYSTEM_SHA256,

        "evaluation_partition":
            d14.D14_EVALUATION_PARTITION,

        "evaluation_mode":
            d14.D14_EVALUATION_MODE,

        "performance_evidence":
            performance_evidence,

        "subgroup_evidence":
            subgroup_evidence,

        "robustness_evidence":
            robustness_evidence,

        "explainability_evidence":
            explainability_evidence,

        "residual_risks":
            residual_risks,

        "residual_risk_count":
            len(residual_risks),

        "unresolved_residual_risk_count":
            sum(
                not risk["resolved"]
                for risk in residual_risks
            ),

        "external_validation_completed":
            False,

        "clinical_effectiveness_established":
            False,

        "deployment_authorized":
            False,
    }


@pytest.fixture(scope="module")
def integrated_gate(integrated_evidence):
    return d14.evaluate_d14_integrated_governance_gate(
        integrated_evidence
    )


@pytest.fixture(scope="module")
def disposition_validation(integrated_gate):
    return (
        d14.validate_d14_integrated_governance_disposition(
            integrated_gate
        )
    )


# ============================================================
# D14 CONTROLLED TEST ACCESS
# ============================================================


def test_d14_test_access_is_now_controlled_and_recorded(
    access_evidence,
):
    assert access_evidence[
        "test_accessed"
    ] is True


def test_d14_test_not_evaluated_during_access_only(
    access_evidence,
):
    assert access_evidence[
        "test_evaluated"
    ] is False


def test_d14_predictions_not_generated_during_access_only(
    access_evidence,
):
    assert access_evidence[
        "predictions_generated"
    ] is False


def test_d14_model_not_loaded_during_access_only(
    access_evidence,
):
    assert access_evidence[
        "model_loaded_for_inference"
    ] is False


def test_d14_preprocessor_not_loaded_during_access_only(
    access_evidence,
):
    assert access_evidence[
        "preprocessor_loaded_for_inference"
    ] is False


def test_d14_test_not_transformed_during_access_only(
    access_evidence,
):
    assert access_evidence[
        "test_features_transformed"
    ] is False


def test_d14_partition_validation_passes(
    access_evidence,
):
    assert access_evidence[
        "partition_validation"
    ][
        "overall_pass"
    ] is True


def test_d14_test_population_matches_frozen_contract(
    access_evidence,
):
    validation = access_evidence[
        "partition_validation"
    ]

    assert validation[
        "actual_test_encounters"
    ] == d14.D14_EXPECTED_TEST_ENCOUNTERS

    assert validation[
        "actual_test_patients"
    ] == d14.D14_EXPECTED_TEST_PATIENTS

    assert validation[
        "actual_test_positives"
    ] == d14.D14_EXPECTED_TEST_POSITIVES

    assert validation[
        "actual_test_negatives"
    ] == d14.D14_EXPECTED_TEST_NEGATIVES


def test_d14_test_partition_has_no_train_overlap(
    access_evidence,
):
    assert access_evidence[
        "partition_validation"
    ][
        "train_test_patient_overlap"
    ] == 0


def test_d14_test_partition_has_no_validation_overlap(
    access_evidence,
):
    assert access_evidence[
        "partition_validation"
    ][
        "validation_test_patient_overlap"
    ] == 0


def test_d14_access_source_feature_shape_is_governed(
    access_evidence,
):
    assert tuple(
        access_evidence[
            "partition_validation"
        ][
            "source_feature_shape"
        ]
    ) == (
        d14.D14_EXPECTED_TEST_ENCOUNTERS,
        d14.D14_EXPECTED_SOURCE_FEATURE_COUNT,
    )


def test_d14_access_does_not_authorize_deployment(
    access_evidence,
):
    assert access_evidence[
        "deployment_authorized"
    ] is False


# ============================================================
# D14 FROZEN D7 TRANSFORMATION
# ============================================================


def test_d14_transformation_validation_passes(
    prediction_bundle,
):
    assert prediction_bundle[
        "transformation_validation"
    ][
        "overall_pass"
    ] is True


def test_d14_transformation_uses_expected_test_rows(
    transformed_bundle,
):
    assert transformed_bundle[
        "transformed_test"
    ].shape[0] == (
        d14.D14_EXPECTED_TEST_ENCOUNTERS
    )


def test_d14_transformation_has_49_features(
    transformed_bundle,
):
    assert transformed_bundle[
        "transformed_test"
    ].shape[1] == (
        d14.D14_EXPECTED_TRANSFORMED_FEATURE_COUNT
    )


def test_d14_transformed_schema_has_49_features(
    transformed_bundle,
):
    assert len(
        transformed_bundle[
            "transformed_schema"
        ]
    ) == d14.D14_EXPECTED_TRANSFORMED_FEATURE_COUNT


def test_d14_transformed_test_is_finite(
    transformed_bundle,
):
    X_test = np.asarray(
        transformed_bundle[
            "transformed_test"
        ],
        dtype=float,
    )

    assert np.isfinite(
        X_test
    ).all()


def test_d14_preprocessor_was_not_refitted(
    transformed_bundle,
):
    assert transformed_bundle[
        "preprocessor_refitted"
    ] is False


def test_d14_schema_was_not_modified(
    transformed_bundle,
):
    assert transformed_bundle[
        "schema_modified"
    ] is False


def test_d14_frozen_d7_artifact_identity_is_unchanged(
    transformed_bundle,
):
    assert transformed_bundle[
        "artifact_identity_unchanged"
    ] is True


def test_d14_frozen_preprocessor_hash_valid_before_transform(
    transformed_bundle,
):
    assert transformed_bundle[
        "before_artifact_checks"
    ][
        "preprocessor_sha256_valid"
    ] is True


def test_d14_frozen_preprocessor_hash_valid_after_transform(
    transformed_bundle,
):
    assert transformed_bundle[
        "after_artifact_checks"
    ][
        "preprocessor_sha256_valid"
    ] is True


def test_d14_frozen_schema_hash_valid_before_transform(
    transformed_bundle,
):
    assert transformed_bundle[
        "before_artifact_checks"
    ][
        "schema_sha256_valid"
    ] is True


def test_d14_frozen_schema_hash_valid_after_transform(
    transformed_bundle,
):
    assert transformed_bundle[
        "after_artifact_checks"
    ][
        "schema_sha256_valid"
    ] is True


def test_d14_transformation_marks_locked_test_transformed(
    transformed_bundle,
):
    assert transformed_bundle[
        "locked_test_transformed"
    ] is True


def test_d14_transformation_does_not_evaluate_test(
    transformed_bundle,
):
    assert transformed_bundle[
        "locked_test_evaluated"
    ] is False


def test_d14_transformation_does_not_generate_predictions(
    transformed_bundle,
):
    assert transformed_bundle[
        "predictions_generated"
    ] is False


def test_d14_transformation_does_not_retune_threshold(
    transformed_bundle,
):
    assert transformed_bundle[
        "threshold_retuned"
    ] is False


def test_d14_transformation_does_not_authorize_deployment(
    transformed_bundle,
):
    assert transformed_bundle[
        "deployment_authorized"
    ] is False


# ============================================================
# D14 FROZEN MODEL INFERENCE
# ============================================================


def test_d14_model_loaded_for_inference(
    prediction_bundle,
):
    assert prediction_bundle[
        "model_loaded"
    ] is True


def test_d14_predictions_generated(
    prediction_bundle,
):
    assert prediction_bundle[
        "predictions_generated"
    ] is True


def test_d14_test_not_yet_marked_evaluated_inside_inference(
    prediction_bundle,
):
    assert prediction_bundle[
        "locked_test_evaluated"
    ] is False


def test_d14_prediction_count_matches_test_population(
    prediction_bundle,
):
    probabilities = np.asarray(
        prediction_bundle[
            "positive_probabilities"
        ]
    )

    assert len(
        probabilities
    ) == d14.D14_EXPECTED_TEST_ENCOUNTERS


def test_d14_probabilities_are_finite(
    prediction_bundle,
):
    probabilities = np.asarray(
        prediction_bundle[
            "positive_probabilities"
        ],
        dtype=float,
    )

    assert np.isfinite(
        probabilities
    ).all()


def test_d14_probabilities_are_valid(
    prediction_bundle,
):
    probabilities = np.asarray(
        prediction_bundle[
            "positive_probabilities"
        ],
        dtype=float,
    )

    assert (
        probabilities >= 0.0
    ).all()

    assert (
        probabilities <= 1.0
    ).all()


def test_d14_frozen_threshold_predictions_are_binary(
    prediction_bundle,
):
    predictions = np.asarray(
        prediction_bundle[
            "frozen_threshold_predictions"
        ]
    )

    assert set(
        np.unique(
            predictions
        ).tolist()
    ).issubset(
        {0, 1}
    )


def test_d14_frozen_threshold_predictions_match_threshold_rule(
    prediction_bundle,
):
    probabilities = np.asarray(
        prediction_bundle[
            "positive_probabilities"
        ]
    )

    predictions = np.asarray(
        prediction_bundle[
            "frozen_threshold_predictions"
        ]
    )

    expected = (
        probabilities
        >= d14.D14_EXPECTED_DEVELOPMENT_THRESHOLD
    ).astype(int)

    assert np.array_equal(
        predictions,
        expected,
    )


def test_d14_model_not_retrained_for_test_inference(
    prediction_bundle,
):
    assert prediction_bundle[
        "model_retrained"
    ] is False


def test_d14_model_not_retuned_for_test_inference(
    prediction_bundle,
):
    assert prediction_bundle[
        "model_retuned"
    ] is False


def test_d14_model_not_recalibrated_for_test_inference(
    prediction_bundle,
):
    assert prediction_bundle[
        "model_recalibrated"
    ] is False


def test_d14_threshold_not_retuned_for_test_inference(
    prediction_bundle,
):
    assert prediction_bundle[
        "threshold_retuned"
    ] is False


def test_d14_preprocessor_not_refitted_for_inference(
    prediction_bundle,
):
    assert prediction_bundle[
        "preprocessor_refitted"
    ] is False


def test_d14_model_artifact_identity_unchanged_after_inference(
    prediction_bundle,
):
    assert prediction_bundle[
        "model_artifact_identity_unchanged"
    ] is True


def test_d14_model_hash_valid_before_inference(
    prediction_bundle,
):
    assert prediction_bundle[
        "before_model_checks"
    ][
        "model_sha256_valid"
    ] is True


def test_d14_model_hash_valid_after_inference(
    prediction_bundle,
):
    assert prediction_bundle[
        "after_model_checks"
    ][
        "model_sha256_valid"
    ] is True


def test_d14_metadata_hash_valid_before_inference(
    prediction_bundle,
):
    assert prediction_bundle[
        "before_model_checks"
    ][
        "metadata_sha256_valid"
    ] is True


def test_d14_metadata_hash_valid_after_inference(
    prediction_bundle,
):
    assert prediction_bundle[
        "after_model_checks"
    ][
        "metadata_sha256_valid"
    ] is True


def test_d14_inference_does_not_authorize_deployment(
    prediction_bundle,
):
    assert prediction_bundle[
        "deployment_authorized"
    ] is False


# ============================================================
# D14 CONFIRMATORY PERFORMANCE
# ============================================================


def test_d14_performance_validation_passes(
    performance_evidence,
):
    assert performance_evidence[
        "evaluation_validation"
    ][
        "overall_pass"
    ] is True


def test_d14_internal_locked_test_validation_completed(
    performance_evidence,
):
    assert performance_evidence[
        "internal_locked_test_validation_completed"
    ] is True


def test_d14_test_pr_auc_is_preserved(
    performance_evidence,
):
    assert performance_evidence[
        "test_result"
    ][
        "pr_auc"
    ] == pytest.approx(
        0.182040618234,
        abs=1e-12,
    )


def test_d14_test_roc_auc_is_preserved(
    performance_evidence,
):
    assert performance_evidence[
        "test_result"
    ][
        "roc_auc"
    ] == pytest.approx(
        0.623405163566,
        abs=1e-12,
    )


def test_d14_test_brier_score_is_preserved(
    performance_evidence,
):
    assert performance_evidence[
        "test_result"
    ][
        "brier_score"
    ] == pytest.approx(
        0.098257477438,
        abs=1e-12,
    )


def test_d14_test_confusion_matrix_is_preserved(
    performance_evidence,
):
    result = performance_evidence[
        "test_result"
    ]

    assert result[
        "true_positives"
    ] == 832

    assert result[
        "false_positives"
    ] == 3927

    assert result[
        "true_negatives"
    ] == 9404

    assert result[
        "false_negatives"
    ] == 875


def test_d14_test_sensitivity_is_preserved(
    performance_evidence,
):
    assert performance_evidence[
        "test_result"
    ][
        "sensitivity"
    ] == pytest.approx(
        0.487404803749,
        abs=1e-12,
    )


def test_d14_test_alert_count_is_preserved(
    performance_evidence,
):
    assert performance_evidence[
        "test_result"
    ][
        "alert_count"
    ] == 4759


def test_d14_performance_does_not_claim_external_validation(
    performance_evidence,
):
    assert performance_evidence[
        "external_validation_completed"
    ] is False


def test_d14_performance_does_not_claim_clinical_effectiveness(
    performance_evidence,
):
    assert performance_evidence[
        "clinical_effectiveness_established"
    ] is False


def test_d14_performance_does_not_authorize_deployment(
    performance_evidence,
):
    assert performance_evidence[
        "deployment_authorized"
    ] is False


# ============================================================
# D14 SUBGROUP CONFIRMATION
# ============================================================


def test_d14_subgroup_validation_passes(
    subgroup_evidence,
):
    assert subgroup_evidence[
        "validation"
    ][
        "overall_pass"
    ] is True


def test_d14_subgroup_dimensions_are_preserved(
    subgroup_evidence,
):
    assert set(
        subgroup_evidence[
            "subgroup_dimensions"
        ]
    ) == {
        "race",
        "gender",
        "age",
    }


def test_d14_subgroup_threshold_optimization_not_performed(
    subgroup_evidence,
):
    assert subgroup_evidence[
        "subgroup_threshold_optimization"
    ] is False


def test_d14_subgroup_model_not_modified(
    subgroup_evidence,
):
    assert subgroup_evidence[
        "model_modified"
    ] is False


def test_d14_subgroup_analysis_does_not_claim_causal_fairness(
    subgroup_evidence,
):
    assert subgroup_evidence[
        "causal_fairness_claim"
    ] is False


def test_d14_subgroup_analysis_does_not_authorize_deployment(
    subgroup_evidence,
):
    assert subgroup_evidence[
        "deployment_authorized"
    ] is False


# ============================================================
# D14 ROBUSTNESS CONFIRMATION
# ============================================================


def test_d14_robustness_validation_passes(
    robustness_evidence,
):
    assert robustness_evidence[
        "validation"
    ][
        "overall_pass"
    ] is True


def test_d14_robustness_scenarios_are_pre_specified(
    robustness_evidence,
):
    assert robustness_evidence[
        "scenario_source"
    ] == (
        "PRE_SPECIFIED_D11_OBSERVED_SLICE_DEFINITIONS"
    )


def test_d14_no_test_driven_robustness_slices_created(
    robustness_evidence,
):
    assert robustness_evidence[
        "test_driven_slices_created"
    ] is False


def test_d14_robustness_threshold_not_retuned(
    robustness_evidence,
):
    assert robustness_evidence[
        "threshold_retuned"
    ] is False


def test_d14_robustness_model_not_modified(
    robustness_evidence,
):
    assert robustness_evidence[
        "model_modified"
    ] is False


def test_d14_robustness_does_not_claim_external_transportability(
    robustness_evidence,
):
    assert robustness_evidence[
        "external_transportability_established"
    ] is False


def test_d14_robustness_does_not_authorize_deployment(
    robustness_evidence,
):
    assert robustness_evidence[
        "deployment_authorized"
    ] is False


# ============================================================
# D14 EXPLAINABILITY CONFIRMATION
# ============================================================


def test_d14_explainability_validation_passes(
    explainability_evidence,
):
    assert explainability_evidence[
        "overall_pass"
    ] is True


def test_d14_explainability_uses_registered_candidate(
    explainability_evidence,
):
    assert explainability_evidence[
        "registry_id"
    ] == d14.D14_EXPECTED_REGISTRY_ID

    assert explainability_evidence[
        "candidate_system_sha256"
    ] == d14.D14_EXPECTED_CANDIDATE_SYSTEM_SHA256


def test_d14_source_family_additivity_is_preserved(
    explainability_evidence,
):
    assert explainability_evidence[
        "family_evidence"
    ][
        "family_additivity_match"
    ] is True


def test_d14_explainability_does_not_claim_causality(
    explainability_evidence,
):
    assert explainability_evidence[
        "clinical_causality_established"
    ] is False


def test_d14_explainability_does_not_claim_external_validation(
    explainability_evidence,
):
    assert explainability_evidence[
        "external_explainability_validation"
    ] is False


def test_d14_explainability_does_not_authorize_deployment(
    explainability_evidence,
):
    assert explainability_evidence[
        "deployment_authorized"
    ] is False


# ============================================================
# D14 RESIDUAL-RISK GOVERNANCE
# ============================================================


def test_d14_seven_residual_risks_are_registered(
    residual_risks,
):
    assert len(
        residual_risks
    ) == 7


def test_d14_all_residual_risks_remain_unresolved(
    residual_risks,
):
    assert all(
        risk[
            "resolved"
        ] is False
        for risk in residual_risks
    )


@pytest.mark.parametrize(
    "risk_id, expected_classification",
    [
        (
            "D14-RISK-001",
            "MATERIAL",
        ),
        (
            "D14-RISK-002",
            "MATERIAL",
        ),
        (
            "D14-RISK-005",
            "MATERIAL",
        ),
        (
            "D14-RISK-006",
            "UNRESOLVED",
        ),
        (
            "D14-RISK-007",
            "UNRESOLVED",
        ),
    ],
)
def test_d14_residual_risk_classifications_are_preserved(
    residual_risks,
    risk_id,
    expected_classification,
):
    risk = next(
        item
        for item in residual_risks
        if item[
            "risk_id"
        ] == risk_id
    )

    assert risk[
        "severity_classification"
    ] == expected_classification


# ============================================================
# D14 INTEGRATED GOVERNANCE GATE
# ============================================================


def test_d14_integrated_gate_passes(
    integrated_gate,
):
    assert integrated_gate[
        "overall_gate_integrity_pass"
    ] is True

    assert integrated_gate[
        "gate_integrity_status"
    ] == "PASS"


def test_d14_integrated_gate_preserves_conditional_disposition(
    integrated_gate,
):
    assert integrated_gate[
        "disposition"
    ] == d14.D14_FINAL_DISPOSITION


def test_d14_integrated_gate_progresses_to_d15(
    integrated_gate,
):
    assert integrated_gate[
        "next_lifecycle_stage"
    ] == d14.D14_FINAL_NEXT_STAGE


def test_d14_integrated_gate_does_not_authorize_deployment(
    integrated_gate,
):
    assert integrated_gate[
        "deployment_authorized"
    ] is False


def test_d14_integrated_gate_retains_external_validation_boundary(
    integrated_gate,
):
    assert integrated_gate[
        "external_validation_status"
    ] == "NOT_ESTABLISHED"


def test_d14_integrated_gate_retains_clinical_effectiveness_boundary(
    integrated_gate,
):
    assert integrated_gate[
        "clinical_effectiveness_status"
    ] == "NOT_ESTABLISHED"


def test_d14_final_disposition_validation_passes(
    disposition_validation,
):
    assert disposition_validation[
        "overall_pass"
    ] is True

    assert disposition_validation[
        "validation_status"
    ] == "PASS"


# ============================================================
# D14 FAIL-CLOSED GOVERNANCE TESTS
# ============================================================


def test_d14_gate_fails_if_candidate_identity_changes(
    integrated_evidence,
):
    tampered = dict(
        integrated_evidence
    )

    tampered[
        "candidate_system_sha256"
    ] = "TAMPERED"

    gate = (
        d14.evaluate_d14_integrated_governance_gate(
            tampered
        )
    )

    assert gate[
        "overall_gate_integrity_pass"
    ] is False


def test_d14_gate_fails_if_external_validation_is_claimed(
    integrated_evidence,
):
    tampered = dict(
        integrated_evidence
    )

    tampered[
        "external_validation_completed"
    ] = True

    gate = (
        d14.evaluate_d14_integrated_governance_gate(
            tampered
        )
    )

    assert gate[
        "overall_gate_integrity_pass"
    ] is False


def test_d14_gate_fails_if_clinical_effectiveness_is_claimed(
    integrated_evidence,
):
    tampered = dict(
        integrated_evidence
    )

    tampered[
        "clinical_effectiveness_established"
    ] = True

    gate = (
        d14.evaluate_d14_integrated_governance_gate(
            tampered
        )
    )

    assert gate[
        "overall_gate_integrity_pass"
    ] is False


def test_d14_gate_fails_if_deployment_is_authorized(
    integrated_evidence,
):
    tampered = dict(
        integrated_evidence
    )

    tampered[
        "deployment_authorized"
    ] = True

    gate = (
        d14.evaluate_d14_integrated_governance_gate(
            tampered
        )
    )

    assert gate[
        "overall_gate_integrity_pass"
    ] is False


def test_d14_gate_fails_if_residual_risks_are_removed(
    integrated_evidence,
):
    tampered = dict(
        integrated_evidence
    )

    tampered[
        "residual_risk_count"
    ] = 0

    tampered[
        "unresolved_residual_risk_count"
    ] = 0

    gate = (
        d14.evaluate_d14_integrated_governance_gate(
            tampered
        )
    )

    assert gate[
        "overall_gate_integrity_pass"
    ] is False