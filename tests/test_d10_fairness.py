
# D10 — FAIRNESS & SUBGROUP EVALUATION TESTS
# ============================================================
#
# Purpose:
#   Protect the frozen D10 analytical and governance contract.
#   These tests verify lifecycle boundaries, cross-stage identity,
#   subgroup evidence completeness, uncertainty, calibration, and
#   governance findings without authorizing deployment or TEST use.
# ============================================================

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.models import fairness as d10


# ============================================================
# D10 TEST FIXTURES — SESSION-SCOPED EVIDENCE
# ============================================================

@pytest.fixture(scope="session")
def static_contract():
    return d10.validate_d10_static_contract()


@pytest.fixture(scope="session")
def cross_stage_alignment():
    return d10.validate_d10_cross_stage_alignment()


@pytest.fixture(scope="session")
def fairness_frame():
    return d10.build_d10_fairness_evaluation_frame()


@pytest.fixture(scope="session")
def fairness_frame_validation():
    return d10.validate_d10_fairness_evaluation_frame()


@pytest.fixture(scope="session")
def stability_validation():
    return d10.validate_d10_stability_policy()


@pytest.fixture(scope="session")
def subgroup_table():
    return d10.build_d10_subgroup_performance_table()


@pytest.fixture(scope="session")
def subgroup_validation():
    return d10.validate_d10_subgroup_performance_table()


@pytest.fixture(scope="session")
def disparity_population():
    return d10.build_d10_primary_disparity_population()


@pytest.fixture(scope="session")
def disparity_summary():
    return d10.build_d10_disparity_summary()


@pytest.fixture(scope="session")
def disparity_validation():
    return d10.validate_d10_disparity_analysis()


@pytest.fixture(scope="session")
def uncertainty_table():
    return d10.build_d10_subgroup_uncertainty_table()


@pytest.fixture(scope="session")
def uncertainty_validation():
    return d10.validate_d10_subgroup_uncertainty()


@pytest.fixture(scope="session")
def calibration_bins():
    return d10.build_d10_subgroup_calibration_table()


@pytest.fixture(scope="session")
def calibration_summary():
    return d10.build_d10_subgroup_calibration_summary()


@pytest.fixture(scope="session")
def calibration_validation():
    return d10.validate_d10_subgroup_calibration()


@pytest.fixture(scope="session")
def findings_registry():
    return d10.build_d10_governance_findings_registry()


@pytest.fixture(scope="session")
def findings_validation():
    return d10.validate_d10_governance_findings_registry()


# ============================================================
# D10.01 — STATIC LIFECYCLE & GOVERNANCE CONTRACT
# ============================================================

def test_d10_stage_identity_is_frozen():
    assert d10.D10_STAGE == "D10"
    assert d10.D10_STAGE_NAME == "Fairness & Subgroup Evaluation"
    assert d10.D10_TARGET == "readmitted_30d"
    assert d10.D10_SOURCE_MODEL_STAGE == "D8"
    assert d10.D10_SOURCE_THRESHOLD_STAGE == "D9"
    assert d10.D10_EVALUATION_PARTITION == "validation"
    assert d10.D10_LOCKED_TEST_EVALUATION_STAGE == "D14"


def test_d10_upstream_model_identity_is_frozen():
    assert d10.D10_EXPECTED_SELECTED_MODEL == "xgboost"
    assert d10.D10_EXPECTED_MODEL_SHA256 == (
        "2FD02A54DF759EBAAF0D02D64D5ACE16A519DF016990FAC065AF3249BDA88085"
    )
    assert d10.D10_EXPECTED_TRANSFORMED_FEATURE_COUNT == 49


def test_d10_validation_population_is_frozen():
    assert d10.D10_EXPECTED_VALIDATION_ENCOUNTERS == 15052
    assert d10.D10_EXPECTED_VALIDATION_POSITIVES == 1692


def test_d10_threshold_is_frozen_at_d9_operating_point():
    assert np.isclose(d10.D10_EXPECTED_DEVELOPMENT_THRESHOLD, 0.12)
    assert d10.D10_THRESHOLD_RETUNING_PERMITTED is False
    assert d10.D10_SUBGROUP_SPECIFIC_THRESHOLDS_PERMITTED is False


def test_d10_governance_prohibitions_remain_enforced():
    assert d10.D10_MODEL_RETRAINING_PERMITTED is False
    assert d10.D10_HYPERPARAMETER_RETUNING_PERMITTED is False
    assert d10.D10_PREPROCESSOR_REFITTING_PERMITTED is False
    assert d10.D10_LOCKED_TEST_ACCESS_PERMITTED is False
    assert d10.D10_AUTOMATIC_FAIRNESS_MITIGATION_PERMITTED is False
    assert d10.D10_AUTONOMOUS_CLINICAL_DECISION_PERMITTED is False
    assert d10.D10_DEPLOYMENT_AUTHORIZED is False


def test_d10_primary_subgroups_are_frozen():
    assert d10.D10_PRIMARY_SUBGROUP_VARIABLES == ("race", "gender", "age")


def test_d10_required_metric_contract_has_23_metrics():
    assert len(d10.D10_REQUIRED_SUBGROUP_METRICS) == 23
    assert len(set(d10.D10_REQUIRED_SUBGROUP_METRICS)) == 23


def test_d10_static_contract_passes(static_contract):
    assert static_contract["validation_status"] == "PASS"
    assert static_contract["failed_checks"] == []
    assert static_contract["locked_test_access_permitted"] is False
    assert static_contract["deployment_authorized"] is False


# ============================================================
# D10.02 — CROSS-STAGE ALIGNMENT & EVALUATION BOUNDARY
# ============================================================

def test_d10_cross_stage_alignment_passes(cross_stage_alignment):
    assert cross_stage_alignment["validation_status"] == "PASS"
    assert cross_stage_alignment["failed_checks"] == []
    assert cross_stage_alignment["locked_test_accessed"] is False


def test_d10_cross_stage_counts_match_frozen_contract(cross_stage_alignment):
    assert cross_stage_alignment["validation_encounter_count"] == 15052
    assert cross_stage_alignment["validation_positive_count"] == 1692
    assert cross_stage_alignment["validation_negative_count"] == 13360
    assert cross_stage_alignment["probability_count"] == 15052


def test_d10_cross_stage_model_and_outcomes_match(cross_stage_alignment):
    assert cross_stage_alignment["selected_model"] == "xgboost"
    assert cross_stage_alignment["model_sha256"] == d10.D10_EXPECTED_MODEL_SHA256
    assert cross_stage_alignment["d7_d9_outcomes_match_elementwise"] is True
    assert cross_stage_alignment["prediction_partition"] == "validation"


def test_d10_fairness_frame_has_expected_population(fairness_frame, fairness_frame_validation):
    assert len(fairness_frame) == 15052
    assert int(fairness_frame[d10.D10_TARGET].sum()) == 1692
    assert fairness_frame.index.is_unique
    assert fairness_frame_validation["validation_status"] == "PASS"
    assert fairness_frame_validation["locked_test_accessed"] is False


def test_d10_fairness_frame_contains_required_subgroups(fairness_frame):
    for column in d10.D10_PRIMARY_SUBGROUP_VARIABLES:
        assert column in fairness_frame.columns


# ============================================================
# D10.03 — SUPPORT / ANALYTICAL STABILITY POLICY
# ============================================================

def test_d10_stability_policy_values_are_frozen():
    assert d10.D10_MIN_SUBGROUP_ENCOUNTERS == 100
    assert d10.D10_MIN_POSITIVE_OUTCOMES == 20
    assert d10.D10_MIN_NEGATIVE_OUTCOMES == 20


def test_d10_stability_policy_is_not_a_fairness_standard(stability_validation):
    assert stability_validation["validation_status"] == "PASS"
    assert stability_validation["fairness_standard"] is False
    assert stability_validation["clinical_threshold"] is False
    assert stability_validation["regulatory_threshold"] is False
    assert stability_validation["low_support_groups_retained"] is True
    assert stability_validation["low_support_excluded_from_primary_disparity_summary"] is True


# ============================================================
# D10.04 — SUBGROUP PERFORMANCE
# ============================================================

def test_d10_subgroup_performance_validation_passes(subgroup_validation):
    assert subgroup_validation["validation_status"] == "PASS"
    assert subgroup_validation["failed_checks"] == []
    assert subgroup_validation["locked_test_accessed"] is False


def test_d10_subgroup_table_has_expected_rows(subgroup_table, subgroup_validation):
    assert len(subgroup_table) == 18
    assert subgroup_validation["race_subgroups"] == 6
    assert subgroup_validation["gender_subgroups"] == 2
    assert subgroup_validation["age_subgroups"] == 10


def test_d10_subgroup_support_counts_are_frozen(subgroup_table, subgroup_validation):
    assert subgroup_validation["adequate_support_rows"] == 14
    assert subgroup_validation["low_support_rows"] == 4
    counts = subgroup_table["support_classification"].value_counts().to_dict()
    assert counts.get("ADEQUATE_SUPPORT", 0) == 14
    assert counts.get("LOW_SUPPORT", 0) == 4


def test_d10_each_subgroup_dimension_reconciles_to_validation_population(subgroup_validation):
    for subgroup in d10.D10_PRIMARY_SUBGROUP_VARIABLES:
        assert subgroup_validation["encounter_total_per_subgroup_dimension"][subgroup] == 15052
        assert subgroup_validation["positive_total_per_subgroup_dimension"][subgroup] == 1692
        assert subgroup_validation["predicted_positive_total_per_subgroup_dimension"][subgroup] == 4709


def test_d10_unknown_race_is_retained_in_full_evidence(subgroup_table):
    unknown = subgroup_table[
        (subgroup_table["subgroup"] == "race")
        & (subgroup_table["subgroup_value"].astype(str) == "?")
    ]
    assert len(unknown) == 1
    assert int(unknown.iloc[0]["encounter_count"]) == 345


def test_d10_known_low_support_groups_are_retained(subgroup_table):
    low = set(
        subgroup_table.loc[
            subgroup_table["support_classification"] == "LOW_SUPPORT",
            ["subgroup", "subgroup_value"],
        ].itertuples(index=False, name=None)
    )
    assert low == {
        ("race", "Asian"),
        ("race", "Other"),
        ("age", "[0-10)"),
        ("age", "[10-20)"),
    }


def test_d10_threshold_dependent_counts_reconcile(subgroup_table):
    assert (subgroup_table["true_positive"] >= 0).all()
    assert (subgroup_table["false_positive"] >= 0).all()
    assert (subgroup_table["true_negative"] >= 0).all()
    assert (subgroup_table["false_negative"] >= 0).all()
    assert np.allclose(
        subgroup_table["predicted_positive_count"],
        subgroup_table["true_positive"] + subgroup_table["false_positive"],
    )


# ============================================================
# D10.05 — GOVERNED DISPARITY ANALYSIS
# ============================================================

def test_d10_disparity_validation_passes(disparity_validation):
    assert disparity_validation["validation_status"] == "PASS"
    assert disparity_validation["failed_checks"] == []
    assert disparity_validation["fairness_threshold_applied"] is False
    assert disparity_validation["subgroup_specific_thresholds_created"] is False
    assert disparity_validation["automatic_mitigation_applied"] is False
    assert disparity_validation["locked_test_accessed"] is False


def test_d10_disparity_summary_shape_is_frozen(disparity_summary, disparity_validation):
    assert len(disparity_summary) == 39
    assert disparity_validation["primary_disparity_metric_count"] == 13
    assert disparity_validation["eligible_group_counts"] == {"age": 8, "gender": 2, "race": 3}


def test_d10_unknown_race_excluded_from_primary_disparity(
    disparity_population,
    disparity_validation,
):
    assert disparity_validation["unknown_race_excluded"] is True

    unknown = disparity_population[
        (disparity_population["subgroup"] == "race")
        & (disparity_population["subgroup_value"].astype(str) == "?")
    ]

    assert len(unknown) == 1
    assert bool(unknown.iloc[0]["primary_disparity_eligible"]) is False


def test_d10_low_support_groups_excluded_from_primary_disparity(
    disparity_population,
    disparity_validation,
):
    assert disparity_validation["low_support_groups_excluded"] is True

    low_support = disparity_population[
        disparity_population["support_classification"] == "LOW_SUPPORT"
    ]

    assert len(low_support) == 4
    assert (~low_support["primary_disparity_eligible"].astype(bool)).all()

    eligible = disparity_population[
        disparity_population["primary_disparity_eligible"].astype(bool)
    ]

    assert (eligible["support_classification"] == "ADEQUATE_SUPPORT").all()


# ============================================================
# D10.06 — SUBGROUP UNCERTAINTY
# ============================================================

def test_d10_uncertainty_validation_passes(uncertainty_validation):
    assert uncertainty_validation["validation_status"] == "PASS"
    assert uncertainty_validation["failed_checks"] == []
    assert uncertainty_validation["subgroup_rows"] == 18
    assert uncertainty_validation["interval_metric_count"] == 8
    assert np.isclose(uncertainty_validation["confidence_level"], 0.95)
    assert uncertainty_validation["interval_method"] == "Wilson score interval"


def test_d10_wilson_intervals_are_bounded(uncertainty_table):
    lower_cols = [c for c in uncertainty_table.columns if c.endswith("_ci_lower")]
    upper_cols = [c for c in uncertainty_table.columns if c.endswith("_ci_upper")]
    assert len(lower_cols) == 8
    assert len(upper_cols) == 8
    for column in lower_cols + upper_cols:
        finite = uncertainty_table[column].dropna()
        assert finite.between(0.0, 1.0).all()


def test_d10_uncertainty_retains_low_support_without_changing_threshold(uncertainty_validation):
    assert uncertainty_validation["low_support_rows_retained"] == 4
    assert uncertainty_validation["fairness_threshold_applied"] is False
    assert uncertainty_validation["threshold_retuned"] is False
    assert uncertainty_validation["locked_test_accessed"] is False


# ============================================================
# D10.07 — SUBGROUP CALIBRATION
# ============================================================

def test_d10_calibration_validation_passes(calibration_validation):
    assert calibration_validation["validation_status"] == "PASS"
    assert calibration_validation["failed_checks"] == []
    assert calibration_validation["subgroup_summary_rows"] == 18
    assert calibration_validation["calibration_bin_rows"] == 90
    assert calibration_validation["requested_bins_per_subgroup"] == 5


def test_d10_calibration_method_is_frozen(calibration_validation):
    assert d10.D10_CALIBRATION_BIN_COUNT == 5
    assert d10.D10_CALIBRATION_METHOD == "within_subgroup_equal_frequency_quantile_bins"
    assert calibration_validation["calibration_method"] == d10.D10_CALIBRATION_METHOD


def test_d10_calibration_does_not_recalibrate_model(calibration_validation):
    assert calibration_validation["model_recalibrated"] is False
    assert calibration_validation["probability_calibration_established"] is False
    assert calibration_validation["fairness_threshold_applied"] is False
    assert calibration_validation["threshold_retuned"] is False
    assert calibration_validation["locked_test_accessed"] is False


def test_d10_calibration_retains_all_subgroups(calibration_summary):
    assert len(calibration_summary) == 18
    assert int((calibration_summary["support_classification"] == "LOW_SUPPORT").sum()) == 4
    assert ((calibration_summary["brier_score"] >= 0.0) & (calibration_summary["brier_score"] <= 1.0)).all()


def test_d10_calibration_bins_reconcile_to_subgroup_counts(
    calibration_bins,
    calibration_summary,
):
    observed = (
        calibration_bins.groupby(
            ["subgroup", "subgroup_value"],
            dropna=False,
        )["encounter_count"]
        .sum()
        .sort_index()
    )

    expected = (
        calibration_summary
        .set_index(["subgroup", "subgroup_value"])["encounter_count"]
        .sort_index()
    )

    pd.testing.assert_series_equal(
        observed.astype(int),
        expected.astype(int),
        check_names=False,
    )


# ============================================================
# D10.08 — GOVERNANCE FINDINGS & REVIEW TRIGGERS
# ============================================================

def test_d10_governance_findings_validation_passes(findings_validation):
    assert findings_validation["validation_status"] == "PASS"
    assert findings_validation["failed_checks"] == []
    assert findings_validation["governance_finding_count"] == 7


def test_d10_governance_finding_ids_are_frozen(findings_registry):
    assert tuple(findings_registry["finding_id"].tolist()) == d10.D10_GOVERNANCE_FINDING_IDS
    assert tuple(findings_registry["finding_id"].tolist()) == (
        "D10-F01", "D10-F02", "D10-F03", "D10-F04",
        "D10-F05", "D10-F06", "D10-F07",
    )


def test_d10_governance_dispositions_match_validated_registry(findings_validation):
    assert findings_validation["disposition_counts"] == {
        "REVIEW_REQUIRED": 2,
        "CLINICAL_REVIEW_REQUIRED": 1,
        "MONITOR": 1,
        "MONITOR_AND_REVIEW": 1,
        "INSUFFICIENT_EVIDENCE": 1,
        "DATA_GOVERNANCE_REVIEW": 1,
    }


def test_d10_findings_do_not_declare_fairness_violation_or_causal_bias(findings_registry, findings_validation):
    assert findings_validation["fairness_violation_determined"] is False
    assert findings_validation["causal_bias_determined"] is False
    assert (~findings_registry["fairness_violation_determined"]).all()
    assert (~findings_registry["causal_bias_determined"]).all()


def test_d10_findings_do_not_authorize_automatic_intervention(findings_registry, findings_validation):
    assert findings_validation["subgroup_specific_thresholds_created"] is False
    assert findings_validation["automatic_mitigation_applied"] is False
    assert findings_validation["model_recalibrated"] is False
    assert (~findings_registry["subgroup_threshold_change_authorized"]).all()
    assert (~findings_registry["automatic_mitigation_authorized"]).all()
    assert (~findings_registry["model_recalibration_authorized"]).all()


def test_d10_findings_do_not_authorize_deployment_or_test_access(findings_registry, findings_validation):
    assert findings_validation["deployment_authorized"] is False
    assert findings_validation["locked_test_accessed"] is False
    assert (~findings_registry["deployment_authorized"]).all()
    assert (~findings_registry["locked_test_accessed"]).all()


def test_d10_f01_is_clinical_review_required(findings_registry):
    row = findings_registry.set_index("finding_id").loc["D10-F01"]
    assert row["domain"] == "clinical_utility_and_safety"
    assert row["disposition"] == "CLINICAL_REVIEW_REQUIRED"
    assert row["deployment_implication"] == "UNRESOLVED_BEFORE_DEPLOYMENT"


def test_d10_f06_preserves_insufficient_evidence_conclusion(findings_registry):
    row = findings_registry.set_index("finding_id").loc["D10-F06"]
    assert row["domain"] == "subgroup_evidence_sufficiency"
    assert row["disposition"] == "INSUFFICIENT_EVIDENCE"
    assert row["deployment_implication"] == "EVIDENCE_LIMITATION_TO_CARRY_FORWARD"


def test_d10_f07_is_data_governance_review(findings_registry):
    row = findings_registry.set_index("finding_id").loc["D10-F07"]
    assert row["domain"] == "demographic_data_quality"
    assert row["affected_population"] == "race=?"
    assert row["disposition"] == "DATA_GOVERNANCE_REVIEW"
    assert row["deployment_implication"] == "DATA_QUALITY_ACTION_REQUIRED"
