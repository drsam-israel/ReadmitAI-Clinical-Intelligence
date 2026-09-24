
# D12 — EXPLAINABILITY & MODEL INTERPRETATION GOVERNANCE TESTS
# ============================================================

from __future__ import annotations

import numpy as np
import pytest

from src.models import explainability as d12


# ============================================================
# D12-T.01 — STATIC GOVERNANCE BOUNDARY
# ============================================================

@pytest.fixture(scope="module")
def static_boundary():
    return d12.build_d12_static_system_boundary()


@pytest.fixture(scope="module")
def static_validation(static_boundary):
    return d12.validate_d12_static_system_boundary(static_boundary)


def test_d12_static_boundary_passes(static_validation):
    assert static_validation["validation_status"] == "PASS"
    assert static_validation["failed_checks"] == []


def test_d12_static_boundary_identity(static_boundary):
    assert static_boundary["stage_id"] == "D12"
    assert static_boundary["model_name"] == "xgboost"
    assert static_boundary["development_threshold"] == pytest.approx(0.12)
    assert static_boundary["validation_encounters"] == 15052
    assert static_boundary["validation_positives"] == 1692
    assert static_boundary["validation_negatives"] == 13360
    assert static_boundary["transformed_feature_count"] == 49


def test_d12_static_boundary_hashes(static_boundary):
    assert static_boundary["expected_model_sha256"] == (
        "2FD02A54DF759EBAAF0D02D64D5ACE16A519DF016990FAC065AF3249BDA88085"
    )
    assert static_boundary["expected_d7_preprocessor_sha256"] == (
        "076878C0BD7C9B80897F3AA06157719A1E311165299549D83213C789CA1ECEAC"
    )
    assert static_boundary["expected_d7_schema_sha256"] == (
        "69E0E7F19C64350A6995830E875C1303E5D14F55FD7CDA4A7D845CCDE7B756ED"
    )


def test_d12_static_boundary_preserves_lifecycle_controls(static_boundary):
    assert static_boundary["model_retrained"] is False
    assert static_boundary["preprocessor_refitted"] is False
    assert static_boundary["threshold_retuned"] is False
    assert static_boundary["locked_test_accessed"] is False
    assert static_boundary["deployment_authorized"] is False


# ============================================================
# D12-T.02 — FROZEN RUNTIME BOUNDARY
# ============================================================

@pytest.fixture(scope="module")
def runtime_boundary():
    return d12.build_d12_frozen_runtime_boundary()


@pytest.fixture(scope="module")
def runtime_validation(runtime_boundary):
    return d12.validate_d12_frozen_runtime_boundary(runtime_boundary)


def test_d12_runtime_boundary_passes(runtime_validation):
    assert runtime_validation["validation_status"] == "PASS"
    assert runtime_validation["failed_checks"] == []


def test_d12_runtime_boundary_shape(runtime_validation):
    assert runtime_validation["validation_encounters"] == 15052
    assert runtime_validation["validation_positives"] == 1692
    assert runtime_validation["validation_negatives"] == 13360
    assert runtime_validation["transformed_feature_count"] == 49


def test_d12_runtime_threshold_is_frozen(runtime_boundary, runtime_validation):
    assert runtime_validation["selected_development_threshold"] == pytest.approx(0.12)
    assert runtime_boundary["d9_threshold_selection_status"] == "PASS"
    assert runtime_validation["threshold_matches_d9"] is True


def test_d12_runtime_model_identity_is_frozen(runtime_boundary, runtime_validation):
    assert runtime_boundary["model_sha256"] == d12.D12_EXPECTED_MODEL_SHA256
    assert runtime_validation["model_sha_matches_d9"] is True
    assert runtime_validation["model_sha256_unchanged"] is True
    assert runtime_validation["model_mtime_unchanged"] is True


def test_d12_runtime_cross_stage_identity(runtime_validation):
    assert runtime_validation["outcomes_match_d7_d9"] is True
    assert runtime_validation["feature_names_match_d7_d9"] is True
    assert runtime_validation["transformed_matrices_match_d7_d9"] is True
    assert runtime_validation["probabilities_match_d9"] is True


def test_d12_runtime_does_not_mutate_system(runtime_boundary):
    assert runtime_boundary["model_retrained"] is False
    assert runtime_boundary["preprocessor_refitted"] is False
    assert runtime_boundary["threshold_retuned"] is False
    assert runtime_boundary["locked_test_accessed"] is False
    assert runtime_boundary["deployment_authorized"] is False


# ============================================================
# D12-T.03 — EXPLAINABILITY FOUNDATION
# ============================================================

@pytest.fixture(scope="module")
def method_governance():
    return d12.build_d12_explainability_method_governance()


@pytest.fixture(scope="module")
def shap_compatibility():
    return d12.validate_d12_shap_compatibility(sample_size=10)


@pytest.fixture(scope="module")
def shap_additivity():
    return d12.validate_d12_shap_additivity(sample_size=100)


def test_d12_method_governance_is_tree_shap(method_governance):
    assert method_governance["method_name"] == "SHAP TreeExplainer"
    assert method_governance["explainer_family"] == "TreeExplainer"
    assert method_governance["model_output_space"] == "raw"
    assert method_governance["feature_attribution_is_causal"] is False


def test_d12_shap_compatibility_passes(shap_compatibility):
    assert shap_compatibility["validation_status"] == "PASS"
    assert shap_compatibility["failed_checks"] == []
    assert shap_compatibility["explainer_type"] == "TreeExplainer"
    assert tuple(shap_compatibility["shap_values_shape"]) == (10, 49)
    assert tuple(shap_compatibility["data_shape"]) == (10, 49)
    assert shap_compatibility["feature_count"] == 49
    assert shap_compatibility["finite_shap"] is True


def test_d12_shap_additivity_passes(shap_additivity):
    assert shap_additivity["validation_status"] == "PASS"
    assert shap_additivity["failed_checks"] == []
    assert shap_additivity["model_output"] == "raw"
    assert shap_additivity["max_probability_reconstruction_error"] <= 1e-6
    assert shap_additivity["shap_values_are_probability_point_changes"] is False
    assert shap_additivity["feature_attribution_is_causal"] is False


# ============================================================
# D12-T.04 — FULL VALIDATION ATTRIBUTION DATASET
# ============================================================

@pytest.fixture(scope="module")
def attribution():
    return d12.build_d12_governed_attribution_dataset()


def test_d12_full_validation_attribution_shape(attribution):
    assert attribution["encounter_count"] == 15052
    assert attribution["feature_count"] == 49
    assert np.asarray(attribution["shap_values"]).shape == (15052, 49)


def test_d12_full_validation_attribution_is_finite(attribution):
    assert np.isfinite(np.asarray(attribution["shap_values"], dtype=float)).all()
    assert attribution["shap_values_finite"] is True


def test_d12_full_validation_probability_reconstruction(attribution):
    assert attribution["max_probability_reconstruction_error"] <= 1e-6


def test_d12_full_validation_respects_boundary(attribution):
    assert attribution["locked_test_accessed"] is False
    assert attribution["deployment_authorized"] is False


# ============================================================
# D12-T.05 — GLOBAL ATTRIBUTION & SOURCE-FAMILY MAPPING
# ============================================================

@pytest.fixture(scope="module")
def global_evidence():
    return d12.build_d12_global_shap_attribution()


@pytest.fixture(scope="module")
def global_validation(global_evidence):
    return d12.validate_d12_global_shap_attribution(global_evidence)


def test_d12_global_attribution_passes(global_validation):
    assert global_validation["validation_status"] == "PASS"
    assert global_validation["failed_checks"] == []


def test_d12_global_attribution_counts(global_evidence):
    assert global_evidence["encounter_count"] == 15052
    assert global_evidence["transformed_feature_count"] == 49
    assert global_evidence["source_feature_family_count"] == 10


def test_d12_source_family_registry_exact():
    assert tuple(d12.D12_SOURCE_FEATURE_FAMILIES) == (
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
    )


@pytest.mark.parametrize(
    ("transformed_feature", "expected_family"),
    [
        ("numeric__prior_inpatient_use", "prior_inpatient_use"),
        ("numeric__prior_utilization_intensity", "prior_utilization_intensity"),
        ("categorical__age_[70-80)", "age"),
        ("categorical__admission_source_id_7", "admission_source_id"),
        ("categorical__race_Caucasian", "race"),
        ("categorical__gender_Female", "gender"),
    ],
)
def test_d12_transformed_feature_mapping(transformed_feature, expected_family):
    assert (
        d12.map_d12_transformed_feature_to_source_family(transformed_feature)
        == expected_family
    )


def test_d12_global_source_family_shares_sum_to_one(global_evidence):
    shares = [
        row["absolute_attribution_share"]
        for row in global_evidence["source_family_attribution"]
    ]
    assert sum(shares) == pytest.approx(1.0, abs=1e-10)


def test_d12_prior_utilization_is_dominant_global_signal(global_evidence):
    assert global_evidence["prior_utilization_absolute_attribution_percent"] > 60.0
    assert global_evidence["prior_utilization_absolute_attribution_percent"] < 80.0


def test_d12_global_attribution_not_causal(global_evidence):
    assert global_evidence["feature_attribution_is_causal"] is False
    assert global_evidence["shap_values_are_probability_point_changes"] is False
    assert global_evidence["locked_test_accessed"] is False
    assert global_evidence["deployment_authorized"] is False


# ============================================================
# D12-T.06 — DIRECTIONALITY / DEPENDENCE
# ============================================================

@pytest.fixture(scope="module")
def directionality():
    return d12.build_d12_feature_directionality_evidence()


@pytest.fixture(scope="module")
def directionality_validation(directionality):
    return d12.validate_d12_feature_directionality_evidence(directionality)


def test_d12_directionality_passes(directionality_validation):
    assert directionality_validation["validation_status"] == "PASS"
    assert directionality_validation["failed_checks"] == []


def test_d12_directionality_contains_focus_families(directionality):
    expected = {
        "prior_inpatient_use",
        "prior_utilization_intensity",
        "prior_utilization_domain_count",
        "prior_outpatient_use",
        "age",
        "admission_source_id",
    }
    assert expected.issubset(set(directionality["feature_evidence"]))


def test_d12_directionality_support_is_conserved(directionality):
    for evidence in directionality["feature_evidence"].values():
        assert sum(row["support"] for row in evidence["rows"]) == 15052


def test_d12_directionality_preserves_interpretation_controls(directionality):
    assert directionality["feature_attribution_is_causal"] is False
    assert directionality["case_mix_may_contribute"] is True
    assert directionality["model_feature_dependence_may_contribute"] is True
    assert directionality["locked_test_accessed"] is False
    assert directionality["deployment_authorized"] is False


# ============================================================
# D12-T.07 — LOCAL PATIENT EXPLANATIONS
# ============================================================

@pytest.fixture(scope="module")
def local_evidence():
    return d12.build_d12_local_patient_explanation_evidence()


@pytest.fixture(scope="module")
def local_validation(local_evidence):
    return d12.validate_d12_local_patient_explanation_evidence(local_evidence)


def test_d12_local_explanations_pass(local_validation):
    assert local_validation["validation_status"] == "PASS"
    assert local_validation["failed_checks"] == []


def test_d12_local_case_registry_exact(local_evidence):
    assert local_evidence["case_count"] == 5
    assert tuple(case["case_type"] for case in local_evidence["cases"]) == (
        "true_negative_low_probability",
        "false_negative_highest_probability",
        "true_positive_nearest_threshold",
        "false_positive_nearest_threshold",
        "true_positive_high_probability",
    )


def test_d12_local_cases_are_unique(local_evidence):
    positions = [
        case["validation_row_position"]
        for case in local_evidence["cases"]
    ]
    assert len(positions) == len(set(positions)) == 5


def test_d12_local_probability_reconstruction(local_evidence):
    assert local_evidence["max_probability_reconstruction_error"] <= 1e-6


def test_d12_local_explanations_are_not_causal_or_generalizable(local_evidence):
    for case in local_evidence["cases"]:
        assert case["feature_attribution_is_causal"] is False
        assert case["local_explanation_generalizable_to_population"] is False
    assert local_evidence["locked_test_accessed"] is False
    assert local_evidence["deployment_authorized"] is False


# ============================================================
# D12-T.08 — ATTRIBUTION STABILITY & SLICE ANALYSIS
# ============================================================

@pytest.fixture(scope="module")
def stability():
    return d12.build_d12_attribution_stability_slice_evidence()


@pytest.fixture(scope="module")
def stability_validation(stability):
    return d12.validate_d12_attribution_stability_slice_evidence(stability)


def test_d12_stability_passes(stability_validation):
    assert stability_validation["validation_status"] == "PASS"
    assert stability_validation["failed_checks"] == []


def test_d12_stability_slice_counts(stability):
    assert stability["slice_count"] == 42
    assert stability["adequate_support_slice_count"] == 34
    assert stability["low_support_slice_count"] == 8


def test_d12_stability_slice_dimensions_exact(stability):
    observed = {row["slice_dimension"] for row in stability["slice_rows"]}
    assert observed == set(d12.D12_STABILITY_SLICE_REGISTRY)


def test_d12_stability_support_flags_are_governed(stability):
    for row in stability["slice_rows"]:
        assert row["support_adequate"] == (
            row["support"] >= d12.D12_SLICE_MINIMUM_ADEQUATE_SUPPORT
        )


def test_d12_stability_metrics_are_bounded(stability):
    for row in stability["slice_rows"]:
        assert 0.0 <= row["total_variation_distance"] <= 1.0
        assert -1.0 <= row["spearman_rank_correlation"] <= 1.0
        assert 0.0 <= row["top_k_jaccard"] <= 1.0


def test_d12_stability_does_not_invent_material_cutoff(stability):
    assert stability["material_instability_threshold_defined"] is False
    assert stability["automatic_bias_labeling"] is False
    assert stability["automatic_mitigation_applied"] is False


def test_d12_stability_retains_case_mix_and_noncausal_controls(stability):
    assert stability["feature_attribution_is_causal"] is False
    assert stability["slice_differences_may_reflect_case_mix"] is True
    assert stability["locked_test_accessed"] is False
    assert stability["deployment_authorized"] is False


# ============================================================
# D12-T.09 — CLINICAL PLAUSIBILITY & D11 CARRY-FORWARD
# ============================================================

def test_d12_clinical_plausibility_register():
    review = d12.build_d12_clinical_plausibility_review()
    assert review["validation_status"] == "PASS"
    assert review["review_item_count"] == 6
    assert review["clinical_plausibility_supported"] is True
    assert review["clinical_appropriateness_established"] is False
    assert review["causal_mechanism_established"] is False
    assert review["fairness_established"] is False
    assert review["external_validation_established"] is False
    assert review["deployment_authorized"] is False


def test_d12_d11_carry_forward_register():
    register = d12.build_d12_d11_carry_forward_resolution_register()
    assert register["validation_status"] == "PASS"
    assert register["resolution_count"] == 6
    assert register["all_d11_questions_accounted_for"] is True
    assert register["locked_test_reassessment_preserved_for_d14"] is True
    assert register["deployment_authorized"] is False


def test_d12_d11_carry_forward_ids_are_complete():
    register = d12.build_d12_d11_carry_forward_resolution_register()
    assert [row["carry_forward_id"] for row in register["resolution_rows"]] == [
        "D11-CF-01",
        "D11-CF-02",
        "D11-CF-03",
        "D11-CF-04",
        "D11-CF-05",
        "D11-CF-06",
    ]


# ============================================================
# D12-T.10 — LIMITATIONS REGISTER
# ============================================================

def test_d12_limitations_register_complete():
    register = d12.build_d12_explainability_limitations_register()
    assert register["validation_status"] == "PASS"
    assert register["limitation_count"] == 8
    assert [row["limitation_id"] for row in register["limitations"]] == [
        "D12-LIM-01",
        "D12-LIM-02",
        "D12-LIM-03",
        "D12-LIM-04",
        "D12-LIM-05",
        "D12-LIM-06",
        "D12-LIM-07",
        "D12-LIM-08",
    ]


def test_d12_limitations_preserve_interpretation_prohibitions():
    register = d12.build_d12_explainability_limitations_register()
    assert register["causal_claim_prohibited"] is True
    assert register["probability_point_interpretation_prohibited"] is True
    assert register["low_support_overinterpretation_prohibited"] is True
    assert register["external_transportability_claim_prohibited"] is True
    assert register["deployment_inference_prohibited"] is True
    assert register["deployment_authorized"] is False


# ============================================================
# D12-T.11 — FINAL GOVERNANCE DISPOSITION
# ============================================================

@pytest.fixture(scope="module")
def disposition():
    return d12.build_d12_governance_disposition()


@pytest.fixture(scope="module")
def disposition_validation(disposition):
    return d12.validate_d12_governance_disposition(disposition)


def test_d12_final_disposition_passes(disposition_validation):
    assert disposition_validation["validation_status"] == "PASS"
    assert disposition_validation["failed_checks"] == []


def test_d12_progression_is_to_d13_only(disposition):
    assert disposition["governance_disposition"] == (
        "CONDITIONAL_PASS_PROGRESS_TO_D13_WITH_EXPLAINABILITY_LIMITATIONS"
    )
    assert disposition["progression_authorized"] is True
    assert disposition["next_lifecycle_stage"] == (
        "D13_MODEL_REGISTRY_AND_ARTIFACT_FREEZE"
    )


def test_d12_final_disposition_does_not_overclaim(disposition):
    assert disposition["clinical_appropriateness_established"] is False
    assert disposition["fairness_established"] is False
    assert disposition["causality_established"] is False
    assert disposition["external_validation_established"] is False
    assert disposition["prospective_effectiveness_established"] is False


def test_d12_final_disposition_preserves_d14_test_boundary(disposition):
    assert disposition["locked_test_reassessment_required_in_d14"] is True
    assert disposition["locked_test_accessed"] is False


def test_d12_final_disposition_preserves_immutable_system(disposition):
    assert disposition["model_retrained"] is False
    assert disposition["hyperparameters_retuned"] is False
    assert disposition["preprocessor_refitted"] is False
    assert disposition["features_reengineered"] is False
    assert disposition["feature_selection_changed"] is False
    assert disposition["threshold_retuned"] is False
    assert disposition["probabilities_recalibrated"] is False
    assert disposition["subgroup_specific_thresholds_created"] is False
    assert disposition["automatic_mitigation_applied"] is False
    assert disposition["autonomous_clinical_decision_authorized"] is False
    assert disposition["deployment_authorized"] is False
