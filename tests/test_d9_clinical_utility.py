# ============================================================
# D9 — CLINICAL UTILITY & THRESHOLD GOVERNANCE TESTS
# ============================================================

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.models.clinical_utility import (
    D9_EXPECTED_MODEL_SHA256,
    D9_EXPECTED_SELECTED_MODEL,
    D9_EXPECTED_VALIDATION_ENCOUNTERS,
    D9_EXPECTED_TRANSFORMED_FEATURE_COUNT,
    D9_DEVELOPMENT_MINIMUM_SENSITIVITY,
    D9_DEVELOPMENT_MAXIMUM_ALERTS_PER_100,
    validate_d9_static_contract,
    load_d9_frozen_d8_model,
    build_d9_validation_prediction_bundle,
    validate_d9_validation_prediction_bundle,
    evaluate_d9_threshold,
    build_d9_candidate_threshold_grid,
    build_d9_threshold_performance_table,
    validate_d9_threshold_performance_engine,
    build_d9_reference_threshold_table,
    build_d9_threshold_tradeoff_summary,
    validate_d9_threshold_tradeoff_analysis,
    evaluate_d9_operating_scenarios,
    build_d9_capacity_frontier,
    validate_d9_operating_scenario_analysis,
    select_d9_development_threshold,
    validate_d9_development_threshold_selection,
    calculate_d9_net_benefit,
    build_d9_decision_curve_table,
    build_d9_selected_threshold_decision_evidence,
    validate_d9_decision_curve_analysis,
    build_d9_calibration_table,
    calculate_d9_calibration_intercept_slope,
    build_d9_calibration_summary,
    validate_d9_calibration_assessment,
)


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture(scope="module")
def prediction_bundle():
    return build_d9_validation_prediction_bundle()


@pytest.fixture(scope="module")
def threshold_table(prediction_bundle):
    return build_d9_threshold_performance_table(
        prediction_bundle
    )


# ============================================================
# D9.01 — STATIC GOVERNANCE CONTRACT
# ============================================================

def test_d9_static_contract_passes():
    result = validate_d9_static_contract()

    assert result["validation_status"] == "PASS"
    assert result["failed_checks"] == []


def test_d9_static_contract_blocks_locked_test():
    result = validate_d9_static_contract()

    assert (
        result["locked_test_access_permitted"]
        is False
    )


def test_d9_static_contract_blocks_model_retraining():
    result = validate_d9_static_contract()

    assert (
        result["model_retraining_permitted"]
        is False
    )


def test_d9_static_contract_blocks_retuning():
    result = validate_d9_static_contract()

    assert (
        result["hyperparameter_retuning_permitted"]
        is False
    )


def test_d9_static_contract_blocks_preprocessor_refit():
    result = validate_d9_static_contract()

    assert (
        result["preprocessor_refitting_permitted"]
        is False
    )


def test_d9_static_contract_blocks_deployment():
    result = validate_d9_static_contract()

    assert result["deployment_authorized"] is False


# ============================================================
# D9.02 — FROZEN D8 MODEL BOUNDARY
# ============================================================

def test_d9_loads_expected_model():
    result = load_d9_frozen_d8_model()

    assert (
        result["selected_model"]
        == D9_EXPECTED_SELECTED_MODEL
    )


def test_d9_model_checksum_matches_frozen_d8():
    result = load_d9_frozen_d8_model()

    assert (
        result["model_sha256"]
        == D9_EXPECTED_MODEL_SHA256
    )


def test_d9_model_not_retrained():
    result = load_d9_frozen_d8_model()

    assert result["model_retrained"] is False


def test_d9_model_not_retuned():
    result = load_d9_frozen_d8_model()

    assert result["hyperparameters_retuned"] is False


def test_d9_model_loader_does_not_access_test():
    result = load_d9_frozen_d8_model()

    assert result["locked_test_accessed"] is False


# ============================================================
# D9.03 — VALIDATION PREDICTION BOUNDARY
# ============================================================

def test_d9_validation_encounter_count(prediction_bundle):
    assert (
        prediction_bundle["validation_encounter_count"]
        == D9_EXPECTED_VALIDATION_ENCOUNTERS
    )


def test_d9_validation_feature_count(prediction_bundle):
    assert (
        prediction_bundle["transformed_feature_count"]
        == D9_EXPECTED_TRANSFORMED_FEATURE_COUNT
    )


def test_d9_validation_positive_count(prediction_bundle):
    assert (
        prediction_bundle["validation_positive_count"]
        == 1692
    )


def test_d9_validation_prevalence(prediction_bundle):
    assert np.isclose(
        prediction_bundle["validation_prevalence"],
        0.11241031092213659,
    )


def test_d9_probability_vector_has_expected_length(
    prediction_bundle,
):
    assert (
        len(
            prediction_bundle[
                "validation_probability"
            ]
        )
        == D9_EXPECTED_VALIDATION_ENCOUNTERS
    )


def test_d9_probabilities_are_finite(prediction_bundle):
    probability = prediction_bundle[
        "validation_probability"
    ]

    assert np.isfinite(probability).all()


def test_d9_probabilities_are_bounded(prediction_bundle):
    probability = prediction_bundle[
        "validation_probability"
    ]

    assert (probability >= 0.0).all()
    assert (probability <= 1.0).all()


def test_d9_prediction_bundle_does_not_access_test(
    prediction_bundle,
):
    assert (
        prediction_bundle["locked_test_accessed"]
        is False
    )


def test_d9_prediction_bundle_does_not_refit_preprocessor(
    prediction_bundle,
):
    assert (
        prediction_bundle[
            "preprocessor_refitted_in_d9"
        ]
        is False
    )


def test_d9_prediction_bundle_validation_passes():
    result = validate_d9_validation_prediction_bundle()

    assert result["validation_status"] == "PASS"
    assert result["failed_checks"] == []


# ============================================================
# D9.04 — SINGLE-THRESHOLD ENGINE
# ============================================================

def test_d9_threshold_zero_predicts_everyone_positive():
    y = np.array([0, 1, 0, 1])
    p = np.array([0.1, 0.2, 0.3, 0.4])

    result = evaluate_d9_threshold(
        y,
        p,
        0.0,
    )

    assert result["true_positive"] == 2
    assert result["false_positive"] == 2
    assert result["false_negative"] == 0
    assert result["true_negative"] == 0


def test_d9_threshold_one_handles_no_positive_predictions():
    y = np.array([0, 1, 0, 1])
    p = np.array([0.1, 0.2, 0.3, 0.4])

    result = evaluate_d9_threshold(
        y,
        p,
        1.0,
    )

    assert result["predicted_positive_count"] == 0
    assert result["true_positive"] == 0
    assert np.isinf(
        result["number_needed_to_evaluate"]
    )


def test_d9_threshold_rejects_invalid_threshold():
    with pytest.raises(ValueError):
        evaluate_d9_threshold(
            np.array([0, 1]),
            np.array([0.2, 0.8]),
            1.1,
        )


def test_d9_threshold_rejects_length_mismatch():
    with pytest.raises(ValueError):
        evaluate_d9_threshold(
            np.array([0, 1]),
            np.array([0.2]),
            0.5,
        )


def test_d9_threshold_confusion_matrix_is_complete(
    prediction_bundle,
):
    result = evaluate_d9_threshold(
        prediction_bundle["y_validation"],
        prediction_bundle["validation_probability"],
        0.12,
    )

    total = (
        result["true_positive"]
        + result["false_positive"]
        + result["true_negative"]
        + result["false_negative"]
    )

    assert total == D9_EXPECTED_VALIDATION_ENCOUNTERS


# ============================================================
# D9.05 — THRESHOLD GRID
# ============================================================

def test_d9_threshold_grid_has_50_values():
    grid = build_d9_candidate_threshold_grid()

    assert len(grid) == 50


def test_d9_threshold_grid_bounds():
    grid = build_d9_candidate_threshold_grid()

    assert np.isclose(grid.min(), 0.01)
    assert np.isclose(grid.max(), 0.50)


def test_d9_threshold_grid_is_unique():
    grid = build_d9_candidate_threshold_grid()

    assert len(np.unique(grid)) == len(grid)


def test_d9_threshold_performance_has_50_rows(
    threshold_table,
):
    assert len(threshold_table) == 50


def test_d9_threshold_performance_does_not_select_threshold(
    threshold_table,
):
    assert not threshold_table[
        "threshold_selected"
    ].any()


def test_d9_threshold_engine_validation_passes():
    result = validate_d9_threshold_performance_engine()

    assert result["validation_status"] == "PASS"
    assert result["failed_checks"] == []


# ============================================================
# D9.06 — REFERENCE TRADE-OFF ANALYSIS
# ============================================================

def test_d9_reference_threshold_table_has_11_rows():
    table = build_d9_reference_threshold_table()

    assert len(table) == 11


def test_d9_reference_threshold_table_contains_0125():
    table = build_d9_reference_threshold_table()

    assert np.isclose(
        table["threshold"],
        0.125,
    ).any()


def test_d9_tradeoff_summary_does_not_select_threshold(
    threshold_table,
):
    result = build_d9_threshold_tradeoff_summary(
        threshold_table
    )

    assert result["threshold_selected"] is False


def test_d9_tradeoff_analysis_passes():
    result = validate_d9_threshold_tradeoff_analysis()

    assert result["validation_status"] == "PASS"
    assert result["failed_checks"] == []


# ============================================================
# D9.07 — OPERATING SCENARIOS & CAPACITY FRONTIER
# ============================================================

def test_d9_operating_scenarios_has_four_rows(
    threshold_table,
):
    table = evaluate_d9_operating_scenarios(
        threshold_table
    )

    assert len(table) == 4


def test_d9_balanced_scenario_has_two_feasible_thresholds(
    threshold_table,
):
    table = evaluate_d9_operating_scenarios(
        threshold_table
    )

    row = table.loc[
        table["scenario"]
        == "BALANCED_EXPLORATORY"
    ].iloc[0]

    assert row["feasible_threshold_count"] == 2


def test_d9_capacity_frontier_has_eight_rows(
    threshold_table,
):
    table = build_d9_capacity_frontier(
        threshold_table
    )

    assert len(table) == 8


def test_d9_capacity_frontier_does_not_select_threshold(
    threshold_table,
):
    table = build_d9_capacity_frontier(
        threshold_table
    )

    assert not table["threshold_selected"].any()


def test_d9_operating_scenario_validation_passes():
    result = validate_d9_operating_scenario_analysis()

    assert result["validation_status"] == "PASS"
    assert result["failed_checks"] == []


# ============================================================
# D9.08 — DEVELOPMENT THRESHOLD SELECTION
# ============================================================

def test_d9_development_threshold_is_012(
    threshold_table,
):
    result = select_d9_development_threshold(
        threshold_table
    )

    assert np.isclose(
        result["selected_threshold"],
        0.12,
    )


def test_d9_threshold_meets_sensitivity_constraint(
    threshold_table,
):
    result = select_d9_development_threshold(
        threshold_table
    )

    assert (
        result["sensitivity"]
        >= D9_DEVELOPMENT_MINIMUM_SENSITIVITY
    )


def test_d9_threshold_meets_alert_constraint(
    threshold_table,
):
    result = select_d9_development_threshold(
        threshold_table
    )

    assert (
        result["alerts_per_100_patients"]
        <= D9_DEVELOPMENT_MAXIMUM_ALERTS_PER_100
    )


def test_d9_selected_threshold_confusion_matrix(
    threshold_table,
):
    result = select_d9_development_threshold(
        threshold_table
    )

    assert result["true_positive"] == 785
    assert result["false_positive"] == 3924
    assert result["true_negative"] == 9436
    assert result["false_negative"] == 907


def test_d9_threshold_is_development_only(
    threshold_table,
):
    result = select_d9_development_threshold(
        threshold_table
    )

    assert (
        result["development_threshold_selected"]
        is True
    )

    assert (
        result["institutional_approval_obtained"]
        is False
    )

    assert result["deployment_authorized"] is False


def test_d9_threshold_selection_validation_passes():
    result = validate_d9_development_threshold_selection()

    assert result["validation_status"] == "PASS"
    assert result["failed_checks"] == []


# ============================================================
# D9.09 — DECISION-CURVE ANALYSIS
# ============================================================

def test_d9_decision_curve_has_50_rows():
    table = build_d9_decision_curve_table()

    assert len(table) == 50


def test_d9_selected_threshold_net_benefit_positive():
    result = (
        build_d9_selected_threshold_decision_evidence()
    )

    assert result["model_net_benefit"] > 0.0


def test_d9_selected_threshold_beats_treat_all():
    result = (
        build_d9_selected_threshold_decision_evidence()
    )

    assert (
        result["model_net_benefit"]
        > result["treat_all_net_benefit"]
    )


def test_d9_selected_threshold_beats_treat_none():
    result = (
        build_d9_selected_threshold_decision_evidence()
    )

    assert (
        result["model_net_benefit"]
        > result["treat_none_net_benefit"]
    )


def test_d9_net_benefit_rejects_zero_threshold():
    with pytest.raises(ValueError):
        calculate_d9_net_benefit(
            np.array([0, 1]),
            np.array([0.2, 0.8]),
            0.0,
        )


def test_d9_decision_curve_validation_passes():
    result = validate_d9_decision_curve_analysis()

    assert result["validation_status"] == "PASS"
    assert result["failed_checks"] == []


# ============================================================
# D9.10 — CALIBRATION ASSESSMENT
# ============================================================

def test_d9_calibration_table_has_ten_bins():
    table = build_d9_calibration_table()

    assert len(table) == 10


def test_d9_calibration_table_accounts_for_all_encounters():
    table = build_d9_calibration_table()

    assert (
        table["encounter_count"].sum()
        == D9_EXPECTED_VALIDATION_ENCOUNTERS
    )


def test_d9_calibration_intercept_is_near_zero():
    result = (
        calculate_d9_calibration_intercept_slope()
    )

    assert abs(
        result["calibration_intercept"]
    ) < 0.05


def test_d9_calibration_slope_is_near_one():
    result = (
        calculate_d9_calibration_intercept_slope()
    )

    assert abs(
        result["calibration_slope"] - 1.0
    ) < 0.10


def test_d9_brier_score_is_finite():
    result = build_d9_calibration_summary()

    assert np.isfinite(
        result["brier_score"]
    )


def test_d9_no_recalibration_performed():
    result = build_d9_calibration_summary()

    assert result["model_recalibrated"] is False


def test_d9_calibration_does_not_claim_deployment():
    result = build_d9_calibration_summary()

    assert result["deployment_authorized"] is False


def test_d9_calibration_validation_passes():
    result = validate_d9_calibration_assessment()

    assert result["validation_status"] == "PASS"
    assert result["failed_checks"] == []


# ============================================================
# D9.11 — FINAL LIFECYCLE SAFETY ASSERTIONS
# ============================================================

def test_d9_locked_test_remains_untouched(
    prediction_bundle,
):
    assert (
        prediction_bundle["locked_test_accessed"]
        is False
    )


def test_d9_never_authorizes_deployment(
    threshold_table,
):
    result = select_d9_development_threshold(
        threshold_table
    )

    assert result["deployment_authorized"] is False