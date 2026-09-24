# ============================================================
# D11 — ROBUSTNESS & TRANSPORTABILITY RUNTIME TEST SUITE
# ============================================================
"""
Regression tests for:

D11 — Robustness & Transportability

Purpose
-------
These tests verify that D11 evaluates the already-frozen clinical
AI development system without changing the governed lifecycle state.

The suite protects:

1. frozen upstream artifact identities;
2. authoritative D9 validation baseline reproduction;
3. D7-compatible unknown-category normalization;
4. stress-test registry integrity;
5. synthetic perturbation execution;
6. observed-slice robustness assessment;
7. D11.15 comparison/degradation governance;
8. D11.16 lifecycle disposition;
9. locked-TEST isolation;
10. prohibition of retraining, refitting, retuning, recalibration,
    unsupported transportability claims, and deployment authorization.

IMPORTANT
---------
D11 is development-stage internal robustness evidence.

It does NOT establish:
- external validation;
- temporal validation;
- geographic transportability;
- institutional transportability;
- prospective validation;
- clinical deployment authorization.
"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd
import pytest

from src.models import robustness as d11


# ============================================================
# SECTION 01 — GOVERNED EXPECTED VALUES
# ============================================================

EXPECTED_D7_PREPROCESSOR_SHA256 = (
    "076878C0BD7C9B80897F3AA06157719A1E311165299549D83213C789CA1ECEAC"
)

EXPECTED_D7_SCHEMA_SHA256 = (
    "69E0E7F19C64350A6995830E875C1303E5D14F55FD7CDA4A7D845CCDE7B756ED"
)

EXPECTED_MODEL_SHA256 = (
    "2FD02A54DF759EBAAF0D02D64D5ACE16A519DF016990FAC065AF3249BDA88085"
)

EXPECTED_THRESHOLD = 0.12

EXPECTED_VALIDATION_ENCOUNTERS = 15052
EXPECTED_VALIDATION_POSITIVES = 1692
EXPECTED_VALIDATION_NEGATIVES = 13360
EXPECTED_TRANSFORMED_FEATURES = 49

EXPECTED_PREDICTED_POSITIVES = 4709
EXPECTED_PREDICTED_POSITIVE_RATE = 0.3128487908583577

EXPECTED_MEAN_PROBABILITY = 0.11372116307581723
EXPECTED_MIN_PROBABILITY = 0.02802971936762333
EXPECTED_MAX_PROBABILITY = 0.5256381630897522

EXPECTED_SYNTHETIC_ASSESSMENTS = 2
EXPECTED_OBSERVED_SLICE_ASSESSMENTS = 35
EXPECTED_TOTAL_ASSESSMENTS = 37

EXPECTED_SYNTHETIC_REVIEW_COUNT = 0
EXPECTED_HETEROGENEITY_REVIEW_COUNT = 6
EXPECTED_LOW_SUPPORT_COUNT = 12
EXPECTED_CARRY_FORWARD_ACTION_COUNT = 6

EXPECTED_DISPOSITION = (
    "CONDITIONAL_PASS_PROGRESS_WITH_DOCUMENTED_ROBUSTNESS_FINDINGS"
)

EXPECTED_HETEROGENEITY_SLICES = {
    ("D11-STRESS-004", "admission_source_id=6"),
    ("D11-STRESS-005", "prior_utilization_domain_count=0"),
    ("D11-STRESS-006", "prior_utilization_domain_count=1"),
    ("D11-STRESS-007", "prior_utilization_domain_count>=2"),
    ("D11-STRESS-008", "prior_utilization_intensity>=3"),
    ("D11-STRESS-009", "age=[20-30)"),
}


# ============================================================
# SECTION 02 — SHARED TEST HELPERS
# ============================================================

def assert_close(
    observed: float,
    expected: float,
    *,
    abs_tol: float = 1e-12,
) -> None:
    """Assert deterministic floating-point agreement."""

    assert math.isclose(
        float(observed),
        float(expected),
        rel_tol=0.0,
        abs_tol=abs_tol,
    )


def assert_false_governance_flags(result: dict) -> None:
    """
    Assert lifecycle mutation / unsupported-claim flags remain False.

    Only keys actually present in the supplied result are tested so
    the helper can be reused across D11 runtime layers.
    """

    prohibited_flags = (
        "model_retrained",
        "hyperparameters_retuned",
        "preprocessor_refitted",
        "threshold_retuned",
        "model_recalibrated",
        "locked_test_accessed",
        "external_validation_established",
        "temporal_validation_established",
        "geographic_transportability_established",
        "institutional_transportability_established",
        "prospective_validation_established",
        "deployment_authorized",
    )

    for key in prohibited_flags:
        if key in result:
            assert result[key] is False, (
                f"D11 governance violation: {key} must remain False."
            )


# ============================================================
# SECTION 03 — STATIC GOVERNANCE CONTRACT
# ============================================================

def test_d11_stage_identity():
    assert d11.D11_STAGE == "D11"


def test_d11_frozen_d7_preprocessor_identity():
    assert (
        d11.D11_EXPECTED_D7_PREPROCESSOR_SHA256
        == EXPECTED_D7_PREPROCESSOR_SHA256
    )


def test_d11_frozen_d7_schema_identity():
    assert (
        d11.D11_EXPECTED_D7_SCHEMA_SHA256
        == EXPECTED_D7_SCHEMA_SHA256
    )


def test_d11_frozen_model_identity():
    assert d11.D11_EXPECTED_MODEL_SHA256 == EXPECTED_MODEL_SHA256


def test_d11_frozen_threshold_identity():
    assert_close(
        d11.D11_EXPECTED_DEVELOPMENT_THRESHOLD,
        EXPECTED_THRESHOLD,
    )


def test_d11_disposition_constant_is_frozen():
    assert d11.D11_ROBUSTNESS_DISPOSITION == EXPECTED_DISPOSITION


def test_d11_expected_review_counts_are_frozen():
    assert d11.D11_EXPECTED_SYNTHETIC_REVIEW_COUNT == 0
    assert (
        d11.D11_EXPECTED_OBSERVED_HETEROGENEITY_REVIEW_COUNT
        == 6
    )
    assert d11.D11_EXPECTED_LOW_SUPPORT_LIMITATION_COUNT == 12


def test_d11_next_stage_is_d12_explainability():
    assert d11.D11_NEXT_LIFECYCLE_STAGE == "D12"
    assert d11.D11_NEXT_LIFECYCLE_STAGE_NAME == "Explainability"


def test_d11_has_exactly_six_mandatory_carry_forward_actions():
    actions = d11.D11_MANDATORY_CARRY_FORWARD_ACTIONS

    assert isinstance(actions, tuple)
    assert len(actions) == EXPECTED_CARRY_FORWARD_ACTION_COUNT
    assert len(set(actions)) == EXPECTED_CARRY_FORWARD_ACTION_COUNT


def test_d11_stress_test_prohibited_claims_include_deployment():
    assert (
        "deployment_authorized"
        in d11.D11_STRESS_TEST_PROHIBITED_CLAIMS
    )


def test_d11_stress_test_prohibited_claims_cover_transportability():
    expected = {
        "external_validation_established",
        "temporal_validation_established",
        "geographic_transportability_established",
        "institutional_transportability_established",
        "prospective_validation_established",
        "deployment_authorized",
    }

    assert expected.issubset(
        set(d11.D11_STRESS_TEST_PROHIBITED_CLAIMS)
    )


# ============================================================
# SECTION 04 — STRESS-TEST REGISTRY
# ============================================================

def test_d11_stress_registry_has_nine_scenarios():
    assert len(d11.D11_STRESS_TEST_REGISTRY) == 9


def test_d11_stress_registry_scenario_ids_are_unique():
    scenario_ids = [
        row["scenario_id"]
        for row in d11.D11_STRESS_TEST_REGISTRY
    ]

    assert len(scenario_ids) == len(set(scenario_ids))


def test_d11_stress_registry_contains_expected_ids():
    observed = {
        row["scenario_id"]
        for row in d11.D11_STRESS_TEST_REGISTRY
    }

    expected = {
        f"D11-STRESS-{i:03d}"
        for i in range(1, 10)
    }

    assert observed == expected


def test_d11_first_two_stress_scenarios_are_synthetic():
    registry = d11.D11_STRESS_TEST_REGISTRY

    assert (
        registry[0]["perturbation_type"]
        == "controlled_unknown_category_injection"
    )
    assert (
        registry[1]["perturbation_type"]
        == "controlled_unknown_category_injection"
    )


def test_d11_synthetic_stress_levels_are_ten_percent():
    registry = d11.D11_STRESS_TEST_REGISTRY

    assert_close(registry[0]["perturbation_level"], 0.10)
    assert_close(registry[1]["perturbation_level"], 0.10)


def test_d11_synthetic_stress_features_are_race_and_gender():
    registry = d11.D11_STRESS_TEST_REGISTRY

    assert registry[0]["feature_scope"] == ("race",)
    assert registry[1]["feature_scope"] == ("gender",)


# ============================================================
# SECTION 05 — D7-COMPATIBLE UNKNOWN NORMALIZATION
# ============================================================

def test_d11_unknown_normalization_maps_governed_source_values():
    columns = list(d11.D11_STRESS_TEST_FEATURES)

    row = {
        column: 0
        for column in columns
    }

    row["race"] = "?"
    row["gender"] = "Unknown/Invalid"
    row["age"] = "[70-80)"

    frame = pd.DataFrame([row], columns=columns)
    original = frame.copy(deep=True)

    normalized = d11.normalize_d11_source_unknown_categories(
        frame
    )

    assert normalized.loc[0, "race"] == d11.D11_UNKNOWN_CATEGORY_VALUE
    assert (
        normalized.loc[0, "gender"]
        == d11.D11_UNKNOWN_CATEGORY_VALUE
    )
    assert normalized.loc[0, "age"] == "[70-80)"

    pd.testing.assert_frame_equal(frame, original)


def test_d11_unknown_normalization_preserves_row_count_and_index():
    columns = list(d11.D11_STRESS_TEST_FEATURES)

    rows = []

    for i in range(3):
        row = {
            column: 0
            for column in columns
        }

        row["race"] = "?" if i == 0 else "Caucasian"
        row["gender"] = (
            "Unknown/Invalid"
            if i == 1
            else "Female"
        )
        row["age"] = "[60-70)"

        rows.append(row)

    frame = pd.DataFrame(
        rows,
        columns=columns,
        index=[101, 205, 999],
    )

    normalized = d11.normalize_d11_source_unknown_categories(
        frame
    )

    assert len(normalized) == len(frame)
    assert normalized.index.equals(frame.index)
    assert list(normalized.columns) == list(frame.columns)


def test_d11_unknown_normalization_rejects_wrong_feature_order():
    columns = list(d11.D11_STRESS_TEST_FEATURES)

    frame = pd.DataFrame(
        [{column: 0 for column in reversed(columns)}]
    )

    with pytest.raises(RuntimeError):
        d11.normalize_d11_source_unknown_categories(frame)


# ============================================================
# SECTION 06 — AUTHORITATIVE FROZEN SYSTEM BOUNDARY
# ============================================================

@pytest.fixture(scope="module")
def frozen_boundary():
    return d11.build_d11_frozen_system_boundary()


def test_d11_frozen_boundary_uses_expected_model(frozen_boundary):
    assert frozen_boundary["model_sha256"] == EXPECTED_MODEL_SHA256


def test_d11_frozen_boundary_uses_expected_d7_preprocessor(
    frozen_boundary,
):
    assert (
        frozen_boundary["d7_preprocessor_sha256"]
        == EXPECTED_D7_PREPROCESSOR_SHA256
    )


def test_d11_frozen_boundary_uses_expected_d7_schema(
    frozen_boundary,
):
    assert (
        frozen_boundary["d7_schema_sha256"]
        == EXPECTED_D7_SCHEMA_SHA256
    )


def test_d11_frozen_boundary_threshold_is_unchanged(
    frozen_boundary,
):
    assert_close(
        frozen_boundary["development_threshold"],
        EXPECTED_THRESHOLD,
    )


def test_d11_frozen_boundary_validation_population(
    frozen_boundary,
):
    assert (
        frozen_boundary["validation_encounter_count"]
        == EXPECTED_VALIDATION_ENCOUNTERS
    )

    assert (
        frozen_boundary["validation_positive_count"]
        == EXPECTED_VALIDATION_POSITIVES
    )


def test_d11_frozen_boundary_transformed_feature_count(
    frozen_boundary,
):
    assert (
        frozen_boundary["transformed_feature_count"]
        == EXPECTED_TRANSFORMED_FEATURES
    )


def test_d11_frozen_boundary_probability_vector(
    frozen_boundary,
):
    probabilities = np.asarray(
        frozen_boundary["probabilities"],
        dtype=float,
    )

    assert probabilities.shape == (
        EXPECTED_VALIDATION_ENCOUNTERS,
    )

    assert np.isfinite(probabilities).all()
    assert (probabilities >= 0.0).all()
    assert (probabilities <= 1.0).all()

    assert_close(
        probabilities.mean(),
        EXPECTED_MEAN_PROBABILITY,
    )

    assert_close(
        probabilities.min(),
        EXPECTED_MIN_PROBABILITY,
    )

    assert_close(
        probabilities.max(),
        EXPECTED_MAX_PROBABILITY,
    )


def test_d11_frozen_boundary_outcomes_are_binary(
    frozen_boundary,
):
    y = np.asarray(
        frozen_boundary["y_validation"],
        dtype=int,
    )

    assert len(y) == EXPECTED_VALIDATION_ENCOUNTERS
    assert int(y.sum()) == EXPECTED_VALIDATION_POSITIVES
    assert set(np.unique(y)).issubset({0, 1})


def test_d11_frozen_boundary_preserves_governance_prohibitions(
    frozen_boundary,
):
    assert_false_governance_flags(frozen_boundary)


# ============================================================
# SECTION 07 — BASELINE METRIC REPRODUCTION
# ============================================================

@pytest.fixture(scope="module")
def baseline():
    return d11.build_d11_baseline_metric_reference()


def test_d11_baseline_identity(baseline):
    assert baseline["stage"] == "D11"
    assert baseline["reference_type"] == "AUTHORITATIVE_D11_BASELINE"


def test_d11_baseline_population_counts(baseline):
    assert baseline["encounter_count"] == EXPECTED_VALIDATION_ENCOUNTERS
    assert baseline["positive_count"] == EXPECTED_VALIDATION_POSITIVES
    assert baseline["negative_count"] == EXPECTED_VALIDATION_NEGATIVES


def test_d11_baseline_threshold_is_frozen(baseline):
    assert_close(
        baseline["threshold"],
        EXPECTED_THRESHOLD,
    )


def test_d11_baseline_predicted_positive_count(baseline):
    assert (
        baseline["predicted_positive_count"]
        == EXPECTED_PREDICTED_POSITIVES
    )


def test_d11_baseline_predicted_positive_rate(baseline):
    assert_close(
        baseline["predicted_positive_rate"],
        EXPECTED_PREDICTED_POSITIVE_RATE,
    )


def test_d11_baseline_mean_probability(baseline):
    assert_close(
        baseline["mean_predicted_probability"],
        EXPECTED_MEAN_PROBABILITY,
    )


def test_d11_baseline_confusion_matrix_sums_to_population(
    baseline,
):
    total = (
        baseline["true_positive"]
        + baseline["false_positive"]
        + baseline["true_negative"]
        + baseline["false_negative"]
    )

    assert total == EXPECTED_VALIDATION_ENCOUNTERS


def test_d11_baseline_expected_confusion_matrix(baseline):
    assert baseline["true_positive"] == 785
    assert baseline["false_positive"] == 3924
    assert baseline["true_negative"] == 9436
    assert baseline["false_negative"] == 907


def test_d11_baseline_expected_sensitivity(baseline):
    assert_close(
        baseline["sensitivity"],
        0.4639479905437352,
    )


def test_d11_baseline_expected_specificity(baseline):
    assert_close(
        baseline["specificity"],
        0.7062874251497006,
    )


def test_d11_baseline_expected_precision(baseline):
    assert_close(
        baseline["precision"],
        0.16670205988532596,
    )


def test_d11_baseline_expected_alert_rate(baseline):
    assert_close(
        baseline["alerts_per_100_patients"],
        31.28487908583577,
    )


def test_d11_baseline_expected_number_needed_to_evaluate(
    baseline,
):
    assert_close(
        baseline["number_needed_to_evaluate"],
        5.998726114649681,
    )


# ============================================================
# SECTION 08 — D11.15 ROBUSTNESS COMPARISON ASSESSMENT
# ============================================================

@pytest.fixture(scope="module")
def comparison_assessment():
    return d11.validate_d11_robustness_comparison_assessment()


def test_d11_comparison_assessment_passes(comparison_assessment):
    assert comparison_assessment["validation_status"] == "PASS"
    assert comparison_assessment["failed_checks"] == []


def test_d11_comparison_assessment_counts(comparison_assessment):
    assert (
        comparison_assessment["synthetic_assessment_count"]
        == EXPECTED_SYNTHETIC_ASSESSMENTS
    )

    assert (
        comparison_assessment["observed_slice_assessment_count"]
        == EXPECTED_OBSERVED_SLICE_ASSESSMENTS
    )

    total = (
        len(comparison_assessment["synthetic_assessments"])
        + len(comparison_assessment["observed_slice_assessments"])
    )

    assert total == EXPECTED_TOTAL_ASSESSMENTS


def test_d11_synthetic_assessments_have_no_review_trigger(
    comparison_assessment,
):
    assert (
        comparison_assessment["synthetic_review_count"]
        == EXPECTED_SYNTHETIC_REVIEW_COUNT
    )

    for row in comparison_assessment["synthetic_assessments"]:
        assert (
            row["review_classification"]
            == "NO_PRE_SPECIFIED_REVIEW_TRIGGER"
        )


def test_d11_synthetic_direct_baseline_comparison_is_permitted(
    comparison_assessment,
):
    assert all(
        row["direct_baseline_degradation_comparison_permitted"]
        is True
        for row in comparison_assessment["synthetic_assessments"]
    )


def test_d11_observed_direct_degradation_comparison_is_prohibited(
    comparison_assessment,
):
    assert all(
        row["direct_baseline_degradation_comparison_permitted"]
        is False
        for row in comparison_assessment[
            "observed_slice_assessments"
        ]
    )


def test_d11_observed_low_support_count(comparison_assessment):
    assert (
        comparison_assessment["observed_low_support_count"]
        == EXPECTED_LOW_SUPPORT_COUNT
    )


def test_d11_observed_heterogeneity_review_count(
    comparison_assessment,
):
    assert (
        comparison_assessment["observed_review_signal_count"]
        == EXPECTED_HETEROGENEITY_REVIEW_COUNT
    )


def test_d11_comparison_assessment_governance_flags(
    comparison_assessment,
):
    assert_false_governance_flags(comparison_assessment)


# ============================================================
# SECTION 09 — D11.16 GOVERNANCE FINDINGS
# ============================================================

@pytest.fixture(scope="module")
def governance_findings():
    return d11.validate_d11_robustness_governance_disposition()


def test_d11_governance_disposition_passes(governance_findings):
    assert governance_findings["validation_status"] == "PASS"
    assert governance_findings["failed_checks"] == []


def test_d11_governance_disposition_is_conditional_pass(
    governance_findings,
):
    assert (
        governance_findings["disposition"]
        == EXPECTED_DISPOSITION
    )


def test_d11_progression_to_d12_is_authorized(
    governance_findings,
):
    assert governance_findings["progression_authorized"] is True
    assert governance_findings["next_lifecycle_stage"] == "D12"
    assert (
        governance_findings["next_lifecycle_stage_name"]
        == "Explainability"
    )


def test_d11_deployment_is_not_authorized(
    governance_findings,
):
    assert governance_findings["deployment_authorized"] is False


def test_d11_governance_expected_evidence_profile(
    governance_findings,
):
    assert governance_findings["synthetic_review_count"] == 0

    assert (
        governance_findings["observed_heterogeneity_review_count"]
        == 6
    )

    assert governance_findings["low_support_limitation_count"] == 12

    assert (
        governance_findings["mandatory_carry_forward_action_count"]
        == 6
    )


def test_d11_exact_heterogeneity_findings(
    governance_findings,
):
    observed = {
        (
            row["scenario_id"],
            row["slice_name"],
        )
        for row in governance_findings[
            "observed_heterogeneity_findings"
        ]
    }

    assert observed == EXPECTED_HETEROGENEITY_SLICES


def test_d11_all_heterogeneity_findings_have_adequate_support(
    governance_findings,
):
    findings = governance_findings[
        "observed_heterogeneity_findings"
    ]

    assert len(findings) == 6

    assert all(
        row["support_status"] == "ADEQUATE_SUPPORT"
        for row in findings
    )


def test_d11_all_heterogeneity_findings_have_review_signals(
    governance_findings,
):
    findings = governance_findings[
        "observed_heterogeneity_findings"
    ]

    assert all(
        len(row["review_signals"]) >= 1
        for row in findings
    )


def test_d11_low_support_rows_are_kept_as_limitations(
    governance_findings,
):
    limitations = governance_findings[
        "low_support_limitations"
    ]

    assert len(limitations) == 12

    assert all(
        row["support_status"] != "ADEQUATE_SUPPORT"
        for row in limitations
    )

    assert all(
        row["limitation"]
        == "LOW_SUPPORT_LIMITS_STRONG_INTERPRETATION"
        for row in limitations
    )


def test_d11_mandatory_actions_match_frozen_contract(
    governance_findings,
):
    assert (
        governance_findings["mandatory_carry_forward_actions"]
        == list(d11.D11_MANDATORY_CARRY_FORWARD_ACTIONS)
    )


def test_d11_observed_slice_degradation_claim_is_prohibited(
    governance_findings,
):
    assert (
        governance_findings[
            "direct_observed_slice_degradation_claim_permitted"
        ]
        is False
    )


def test_d11_causal_interpretation_is_prohibited(
    governance_findings,
):
    assert (
        governance_findings["causal_interpretation_permitted"]
        is False
    )


def test_d11_governance_mutation_flags_remain_false(
    governance_findings,
):
    assert_false_governance_flags(governance_findings)


# ============================================================
# SECTION 10 — TRANSPORTABILITY CLAIM BOUNDARY
# ============================================================

@pytest.mark.parametrize(
    "claim_key",
    [
        "external_validation_established",
        "temporal_validation_established",
        "geographic_transportability_established",
        "institutional_transportability_established",
        "prospective_validation_established",
    ],
)
def test_d11_does_not_establish_external_transportability(
    governance_findings,
    claim_key,
):
    assert governance_findings[claim_key] is False


def test_d11_disposition_interpretation_preserves_external_boundary(
    governance_findings,
):
    interpretation = governance_findings[
        "disposition_interpretation"
    ].lower()

    assert "not deployment authorization" in interpretation
    assert "external" in interpretation
    assert "temporal" in interpretation
    assert "geographic" in interpretation
    assert "institutional" in interpretation
    assert "prospective" in interpretation


# ============================================================
# SECTION 11 — FINAL LIFECYCLE SAFETY REGRESSION
# ============================================================

def test_d11_does_not_retrain_model(governance_findings):
    assert governance_findings["model_retrained"] is False


def test_d11_does_not_retune_hyperparameters(governance_findings):
    assert governance_findings["hyperparameters_retuned"] is False


def test_d11_does_not_refit_preprocessor(governance_findings):
    assert governance_findings["preprocessor_refitted"] is False


def test_d11_does_not_retune_threshold(governance_findings):
    assert governance_findings["threshold_retuned"] is False


def test_d11_does_not_recalibrate_model(governance_findings):
    assert governance_findings["model_recalibrated"] is False


def test_d11_does_not_access_locked_test(governance_findings):
    assert governance_findings["locked_test_accessed"] is False


def test_d11_does_not_authorize_deployment(governance_findings):
    assert governance_findings["deployment_authorized"] is False


def test_d11_progression_is_only_to_explainability(
    governance_findings,
):
    assert governance_findings["progression_authorized"] is True
    assert governance_findings["next_lifecycle_stage"] == "D12"
    assert governance_findings["deployment_authorized"] is False