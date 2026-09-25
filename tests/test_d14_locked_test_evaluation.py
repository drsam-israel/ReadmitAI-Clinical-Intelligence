# ============================================================
# D14 — LOCKED-TEST EVALUATION
# Pre-Access Governance Contract Tests
# ============================================================
#
# Purpose:
# Verify the D14 governance boundary BEFORE any locked TEST
# access, transformation, prediction, or evaluation occurs.
#
# These tests intentionally do NOT:
#   - load TEST rows,
#   - transform TEST features,
#   - generate TEST predictions,
#   - calculate TEST metrics,
#   - retrain or retune the model,
#   - refit preprocessing,
#   - change the operating threshold,
#   - authorize deployment.
# ============================================================


from dataclasses import replace

import pytest

from src.models.locked_test_evaluation import (
    D14_STAGE_ID,
    D14_STAGE_NAME,
    D14_SOURCE_LIFECYCLE_STAGE,
    D14_SOURCE_GIT_COMMIT,
    D14_NEXT_LIFECYCLE_STAGE,
    D14_EVALUATION_PARTITION,
    D14_EVALUATION_MODE,
    D14_DEPLOYMENT_AUTHORIZED,
    D14_EXPECTED_REGISTRY_ID,
    D14_EXPECTED_MODEL_VERSION,
    D14_EXPECTED_CANDIDATE_SYSTEM_SHA256,
    D14_EXPECTED_FEATURE_CONTRACT_SHA256,
    D14_EXPECTED_SOFTWARE_ENVIRONMENT_SHA256,
    D14_EXPECTED_FREEZE_MANIFEST_SHA256,
    D14_EXPECTED_MODEL_SHA256,
    D14_EXPECTED_PREPROCESSOR_SHA256,
    D14_EXPECTED_TRANSFORMED_SCHEMA_SHA256,
    D14_EXPECTED_MODEL_METADATA_SHA256,
    D14_EXPECTED_DEVELOPMENT_THRESHOLD,
    D14_THRESHOLD_CLASSIFICATION,
    D14_THRESHOLD_SOURCE_STAGE,
    D14_THRESHOLD_RETUNING_ALLOWED,
    D14_RECALIBRATION_ALLOWED,
    D14_SUBGROUP_THRESHOLD_OPTIMIZATION_ALLOWED,
    D14_EXPECTED_TEST_ENCOUNTERS,
    D14_EXPECTED_TEST_PATIENTS,
    D14_EXPECTED_TEST_POSITIVES,
    D14_EXPECTED_TEST_NEGATIVES,
    D14_EXPECTED_SOURCE_FEATURE_COUNT,
    D14_EXPECTED_TRANSFORMED_FEATURE_COUNT,
    D14_LOCKED_TEST_ACCESSED,
    D14_LOCKED_TEST_EVALUATED,
    D14_LOCKED_TEST_PREDICTIONS_GENERATED,
    D14_MODEL_RETRAINED,
    D14_MODEL_RETUNED,
    D14_PREPROCESSOR_REFITTED,
    D14_FEATURE_ENGINEERING_CHANGED,
    D14_FEATURE_SET_CHANGED,
    D14_THRESHOLD_RETUNED,
    D14_MODEL_RECALIBRATED,
    D14_SUBGROUP_THRESHOLD_CREATED,
    D14_TEST_DRIVEN_MODEL_SELECTION,
    D14_TEST_DRIVEN_REDESIGN,
    D14_DEPLOYMENT_AUTHORIZED_PRE_EVALUATION,
    D14_PROHIBITED_ACTIVITIES,
    D14_PRIMARY_EVALUATION_DOMAINS,
    D14_CONFIRMATORY_EVALUATION_DOMAINS,
    D14_INTERPRETATION_RULES,
    D14PreAccessGovernanceContract,
    build_d14_pre_access_governance_contract,
    validate_d14_pre_access_governance_contract,
)


# ============================================================
# D14.00 — LIFECYCLE IDENTITY TESTS
# ============================================================


def test_d14_stage_identity_is_frozen():
    assert D14_STAGE_ID == "D14"
    assert D14_STAGE_NAME == "Locked-Test Evaluation"
    assert D14_SOURCE_LIFECYCLE_STAGE == "D13"
    assert D14_SOURCE_GIT_COMMIT == "b4118f9"


def test_d14_progression_target_is_d15():
    assert (
        D14_NEXT_LIFECYCLE_STAGE
        == "D15_DEPLOYMENT_AND_MONITORING_DESIGN"
    )


def test_d14_partition_is_locked_test():
    assert D14_EVALUATION_PARTITION == "LOCKED_TEST"


def test_d14_evaluation_mode_is_one_time_confirmatory():
    assert (
        D14_EVALUATION_MODE
        == "ONE_TIME_CONFIRMATORY_EVALUATION"
    )


def test_d14_does_not_authorize_deployment():
    assert D14_DEPLOYMENT_AUTHORIZED is False


# ============================================================
# D14.01 — FROZEN CANDIDATE IDENTITY TESTS
# ============================================================


def test_d14_registry_identity_matches_d13_freeze():
    assert (
        D14_EXPECTED_REGISTRY_ID
        == "DIABETES_READMISSION_XGB_D13_V1"
    )
    assert D14_EXPECTED_MODEL_VERSION == "1.0.0"


def test_d14_candidate_system_hash_matches_d13():
    assert (
        D14_EXPECTED_CANDIDATE_SYSTEM_SHA256
        == "9349A52C715517666540C0D5B1EDB148D48709C0FC2CC77BE9B53F10FE373679"
    )


def test_d14_feature_contract_hash_matches_d13():
    assert (
        D14_EXPECTED_FEATURE_CONTRACT_SHA256
        == "277CCC7C847B2FE6882A4072EA991B1FEF701D0222471B8B1F583DE06924C0BC"
    )


def test_d14_environment_hash_matches_d13():
    assert (
        D14_EXPECTED_SOFTWARE_ENVIRONMENT_SHA256
        == "D008029639FF03569910412173B84B557C3694A12B24ED8198E06F38616A6E7E"
    )


def test_d14_freeze_manifest_hash_matches_d13():
    assert (
        D14_EXPECTED_FREEZE_MANIFEST_SHA256
        == "0F278573E2C4D139E6D0968DD624AB7C1304825D3B805B6FEF288162051B6119"
    )


def test_d14_component_hashes_are_bound():
    assert (
        D14_EXPECTED_MODEL_SHA256
        == "2FD02A54DF759EBAAF0D02D64D5ACE16A519DF016990FAC065AF3249BDA88085"
    )
    assert (
        D14_EXPECTED_PREPROCESSOR_SHA256
        == "076878C0BD7C9B80897F3AA06157719A1E311165299549D83213C789CA1ECEAC"
    )
    assert (
        D14_EXPECTED_TRANSFORMED_SCHEMA_SHA256
        == "69E0E7F19C64350A6995830E875C1303E5D14F55FD7CDA4A7D845CCDE7B756ED"
    )
    assert (
        D14_EXPECTED_MODEL_METADATA_SHA256
        == "5838A6C77F05BB183F90B9AA4B0ED9F0AE5B0FBF2E3E1B1326A79A3A67A1AC76"
    )


# ============================================================
# D14.02 — OPERATING-POINT TESTS
# ============================================================


def test_d14_threshold_is_frozen_at_development_value():
    assert D14_EXPECTED_DEVELOPMENT_THRESHOLD == pytest.approx(
        0.12
    )
    assert (
        D14_THRESHOLD_CLASSIFICATION
        == "FROZEN_DEVELOPMENT_STAGE_OPERATING_THRESHOLD"
    )
    assert D14_THRESHOLD_SOURCE_STAGE == "D9"


def test_d14_threshold_optimization_is_prohibited():
    assert D14_THRESHOLD_RETUNING_ALLOWED is False
    assert D14_RECALIBRATION_ALLOWED is False
    assert (
        D14_SUBGROUP_THRESHOLD_OPTIMIZATION_ALLOWED
        is False
    )


# ============================================================
# D14.03 — EXPECTED LOCKED-TEST CONTRACT TESTS
# ============================================================


def test_d14_expected_test_partition_identity():
    assert D14_EXPECTED_TEST_ENCOUNTERS == 15_038
    assert D14_EXPECTED_TEST_PATIENTS == 10_568
    assert D14_EXPECTED_TEST_POSITIVES == 1_707
    assert D14_EXPECTED_TEST_NEGATIVES == 13_331


def test_d14_expected_test_class_counts_reconcile():
    assert (
        D14_EXPECTED_TEST_POSITIVES
        + D14_EXPECTED_TEST_NEGATIVES
        == D14_EXPECTED_TEST_ENCOUNTERS
    )


def test_d14_expected_feature_dimensions():
    assert D14_EXPECTED_SOURCE_FEATURE_COUNT == 10
    assert D14_EXPECTED_TRANSFORMED_FEATURE_COUNT == 49


# ============================================================
# D14.04 — PRE-ACCESS STATE TESTS
# ============================================================


def test_d14_locked_test_has_not_been_accessed():
    assert D14_LOCKED_TEST_ACCESSED is False


def test_d14_locked_test_has_not_been_evaluated():
    assert D14_LOCKED_TEST_EVALUATED is False


def test_d14_locked_test_predictions_do_not_exist():
    assert D14_LOCKED_TEST_PREDICTIONS_GENERATED is False


def test_d14_candidate_has_not_been_modified():
    assert D14_MODEL_RETRAINED is False
    assert D14_MODEL_RETUNED is False
    assert D14_PREPROCESSOR_REFITTED is False
    assert D14_FEATURE_ENGINEERING_CHANGED is False
    assert D14_FEATURE_SET_CHANGED is False
    assert D14_THRESHOLD_RETUNED is False
    assert D14_MODEL_RECALIBRATED is False
    assert D14_SUBGROUP_THRESHOLD_CREATED is False
    assert D14_TEST_DRIVEN_MODEL_SELECTION is False
    assert D14_TEST_DRIVEN_REDESIGN is False


def test_d14_pre_access_state_does_not_authorize_deployment():
    assert D14_DEPLOYMENT_AUTHORIZED_PRE_EVALUATION is False


# ============================================================
# D14.05 — PROHIBITED-ACTIVITY TESTS
# ============================================================


@pytest.mark.parametrize(
    "activity",
    [
        "MODEL_RETRAINING",
        "HYPERPARAMETER_RETUNING",
        "PREPROCESSOR_REFITTING",
        "FEATURE_ENGINEERING_CHANGE",
        "FEATURE_SET_CHANGE",
        "MODEL_RESELECTION",
        "THRESHOLD_RETUNING",
        "PROBABILITY_RECALIBRATION",
        "SUBGROUP_SPECIFIC_THRESHOLD_OPTIMIZATION",
        "TEST_DRIVEN_MODEL_SELECTION",
        "TEST_DRIVEN_FEATURE_SELECTION",
        "TEST_DRIVEN_MODEL_REDESIGN",
        "TEST_TO_VALIDATION_OPTIMIZATION_LOOP",
        "AUTONOMOUS_CLINICAL_DECISION_MAKING",
        "DEPLOYMENT_AUTHORIZATION_FROM_PRE_ACCESS_CONTRACT",
    ],
)
def test_d14_required_prohibited_activity_is_declared(activity):
    assert activity in D14_PROHIBITED_ACTIVITIES


# ============================================================
# D14.06 — PRE-SPECIFIED PRIMARY METRIC TESTS
# ============================================================


def test_d14_discrimination_metrics_are_prespecified():
    metrics = D14_PRIMARY_EVALUATION_DOMAINS[
        "discrimination"
    ]

    assert "PR_AUC" in metrics
    assert "ROC_AUC" in metrics


def test_d14_calibration_metrics_are_prespecified():
    metrics = D14_PRIMARY_EVALUATION_DOMAINS[
        "calibration"
    ]

    assert "BRIER_SCORE" in metrics
    assert "LOG_LOSS" in metrics


def test_d14_operating_metrics_are_prespecified():
    metrics = D14_PRIMARY_EVALUATION_DOMAINS[
        "frozen_threshold_operating_performance"
    ]

    expected_metrics = {
        "TRUE_POSITIVES",
        "FALSE_POSITIVES",
        "TRUE_NEGATIVES",
        "FALSE_NEGATIVES",
        "SENSITIVITY",
        "SPECIFICITY",
        "PRECISION_PPV",
        "NEGATIVE_PREDICTIVE_VALUE",
        "F1_SCORE",
        "ALERT_COUNT",
        "ALERT_RATE",
        "ALERTS_PER_100_ENCOUNTERS",
        "NUMBER_NEEDED_TO_EVALUATE",
    }

    assert expected_metrics.issubset(set(metrics))


# ============================================================
# D14.07 — CONFIRMATORY DOMAIN TESTS
# ============================================================


def test_d14_subgroup_domains_are_prespecified():
    domains = D14_CONFIRMATORY_EVALUATION_DOMAINS[
        "subgroup_performance"
    ]

    assert domains == (
        "RACE",
        "GENDER",
        "AGE",
    )


def test_d14_robustness_domains_are_prespecified():
    domains = D14_CONFIRMATORY_EVALUATION_DOMAINS[
        "robustness_transportability"
    ]

    assert "PRIOR_UTILIZATION" in domains
    assert "ADMISSION_CONTEXT" in domains
    assert "AGE_STRUCTURE" in domains


def test_d14_explainability_confirmation_is_prespecified():
    domains = D14_CONFIRMATORY_EVALUATION_DOMAINS[
        "explainability_confirmation"
    ]

    assert "GLOBAL_FEATURE_CONTRIBUTION" in domains
    assert "PRIOR_UTILIZATION_DEPENDENCE" in domains
    assert "LOCAL_EXPLANATION_CONSISTENCY" in domains


# ============================================================
# D14.08 — INTERPRETATION-RULE TESTS
# ============================================================


def test_d14_unfavorable_results_must_be_retained():
    assert (
        "UNFAVORABLE_RESULTS_MUST_BE_RETAINED_AND_REPORTED"
        in D14_INTERPRETATION_RULES
    )


def test_d14_favorable_results_do_not_authorize_deployment():
    assert (
        "FAVORABLE_RESULTS_DO_NOT_AUTOMATICALLY_AUTHORIZE_DEPLOYMENT"
        in D14_INTERPRETATION_RULES
    )


def test_d14_internal_test_is_not_external_validation():
    assert (
        "INTERNAL_TEST_VALIDATION_IS_NOT_EXTERNAL_VALIDATION"
        in D14_INTERPRETATION_RULES
    )


def test_d14_validation_is_not_clinical_effectiveness():
    assert (
        "TECHNICAL_VALIDATION_IS_NOT_CLINICAL_EFFECTIVENESS"
        in D14_INTERPRETATION_RULES
    )


def test_d14_validation_is_not_deployment_authorization():
    assert (
        "CLINICAL_VALIDATION_IS_NOT_DEPLOYMENT_AUTHORIZATION"
        in D14_INTERPRETATION_RULES
    )


# ============================================================
# D14.09 — CONTRACT CONSTRUCTION TESTS
# ============================================================


def test_d14_contract_builds_successfully():
    contract = build_d14_pre_access_governance_contract()

    assert isinstance(
        contract,
        D14PreAccessGovernanceContract,
    )


def test_d14_contract_is_bound_to_frozen_candidate():
    contract = build_d14_pre_access_governance_contract()

    assert (
        contract.registry_id
        == D14_EXPECTED_REGISTRY_ID
    )
    assert (
        contract.candidate_system_sha256
        == D14_EXPECTED_CANDIDATE_SYSTEM_SHA256
    )
    assert (
        contract.feature_contract_sha256
        == D14_EXPECTED_FEATURE_CONTRACT_SHA256
    )


def test_d14_contract_preserves_pre_access_state():
    contract = build_d14_pre_access_governance_contract()

    assert contract.locked_test_accessed is False
    assert contract.locked_test_evaluated is False
    assert contract.predictions_generated is False

    assert contract.model_retrained is False
    assert contract.model_retuned is False
    assert contract.preprocessor_refitted is False
    assert contract.threshold_retuned is False
    assert contract.model_recalibrated is False

    assert contract.deployment_authorized is False


def test_d14_contract_is_immutable():
    contract = build_d14_pre_access_governance_contract()

    with pytest.raises(Exception):
        contract.stage_id = "ALTERED"


# ============================================================
# D14.10 — CONTRACT VALIDATION TESTS
# ============================================================


def test_d14_valid_contract_passes():
    contract = build_d14_pre_access_governance_contract()

    result = validate_d14_pre_access_governance_contract(
        contract
    )

    assert result["overall_pass"] is True
    assert result["validation_status"] == "PASS"

    assert (
        result["next_controlled_action"]
        == "D14_LOCKED_TEST_ACCESS_IMPLEMENTATION"
    )


def test_d14_validation_confirms_test_is_unopened():
    result = validate_d14_pre_access_governance_contract()

    assert result["locked_test_accessed"] is False
    assert result["locked_test_evaluated"] is False
    assert result["predictions_generated"] is False


def test_d14_validation_confirms_deployment_not_authorized():
    result = validate_d14_pre_access_governance_contract()

    assert result["deployment_authorized"] is False


# ============================================================
# D14.11 — FAIL-CLOSED TAMPER TESTS
# ============================================================


def test_d14_fails_if_source_commit_is_changed():
    contract = build_d14_pre_access_governance_contract()

    tampered = replace(
        contract,
        source_git_commit="INVALID_COMMIT",
    )

    result = validate_d14_pre_access_governance_contract(
        tampered
    )

    assert result["overall_pass"] is False
    assert (
        result["checks"]["stage_identity_valid"]
        is False
    )


def test_d14_fails_if_candidate_identity_is_changed():
    contract = build_d14_pre_access_governance_contract()

    tampered = replace(
        contract,
        candidate_system_sha256="INVALID_SHA256",
    )

    result = validate_d14_pre_access_governance_contract(
        tampered
    )

    assert result["overall_pass"] is False
    assert (
        result["checks"]["candidate_identity_bound"]
        is False
    )


def test_d14_fails_if_threshold_is_changed():
    contract = build_d14_pre_access_governance_contract()

    tampered = replace(
        contract,
        development_threshold=0.20,
    )

    result = validate_d14_pre_access_governance_contract(
        tampered
    )

    assert result["overall_pass"] is False
    assert result["checks"]["threshold_frozen"] is False


def test_d14_fails_if_test_is_marked_accessed_early():
    contract = build_d14_pre_access_governance_contract()

    tampered = replace(
        contract,
        locked_test_accessed=True,
    )

    result = validate_d14_pre_access_governance_contract(
        tampered
    )

    assert result["overall_pass"] is False
    assert (
        result["checks"]["locked_test_not_accessed"]
        is False
    )


def test_d14_fails_if_test_is_marked_evaluated_early():
    contract = build_d14_pre_access_governance_contract()

    tampered = replace(
        contract,
        locked_test_evaluated=True,
    )

    result = validate_d14_pre_access_governance_contract(
        tampered
    )

    assert result["overall_pass"] is False
    assert (
        result["checks"]["locked_test_not_evaluated"]
        is False
    )


def test_d14_fails_if_predictions_are_marked_generated_early():
    contract = build_d14_pre_access_governance_contract()

    tampered = replace(
        contract,
        predictions_generated=True,
    )

    result = validate_d14_pre_access_governance_contract(
        tampered
    )

    assert result["overall_pass"] is False
    assert (
        result["checks"][
            "locked_test_predictions_not_generated"
        ]
        is False
    )


def test_d14_fails_if_model_is_marked_retrained():
    contract = build_d14_pre_access_governance_contract()

    tampered = replace(
        contract,
        model_retrained=True,
    )

    result = validate_d14_pre_access_governance_contract(
        tampered
    )

    assert result["overall_pass"] is False
    assert result["checks"]["model_not_retrained"] is False


def test_d14_fails_if_preprocessor_is_marked_refitted():
    contract = build_d14_pre_access_governance_contract()

    tampered = replace(
        contract,
        preprocessor_refitted=True,
    )

    result = validate_d14_pre_access_governance_contract(
        tampered
    )

    assert result["overall_pass"] is False
    assert (
        result["checks"]["preprocessor_not_refitted"]
        is False
    )


def test_d14_fails_if_threshold_is_marked_retuned():
    contract = build_d14_pre_access_governance_contract()

    tampered = replace(
        contract,
        threshold_retuned=True,
    )

    result = validate_d14_pre_access_governance_contract(
        tampered
    )

    assert result["overall_pass"] is False
    assert result["checks"]["threshold_not_retuned"] is False


def test_d14_fails_if_test_driven_redesign_is_marked_true():
    contract = build_d14_pre_access_governance_contract()

    tampered = replace(
        contract,
        test_driven_redesign=True,
    )

    result = validate_d14_pre_access_governance_contract(
        tampered
    )

    assert result["overall_pass"] is False
    assert (
        result["checks"]["no_test_driven_redesign"]
        is False
    )


def test_d14_fails_if_deployment_is_marked_authorized():
    contract = build_d14_pre_access_governance_contract()

    tampered = replace(
        contract,
        deployment_authorized=True,
    )

    result = validate_d14_pre_access_governance_contract(
        tampered
    )

    assert result["overall_pass"] is False
    assert (
        result["checks"]["deployment_not_authorized"]
        is False
    )