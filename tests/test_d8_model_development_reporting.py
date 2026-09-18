# ============================================================
# TESTS — D8 GOVERNED MODEL DEVELOPMENT & SELECTION REPORTING
# ============================================================
#
# Purpose:
#   Validate the persisted governance evidence produced by D8
#   without rerunning expensive model training or hyperparameter
#   optimization.
#
# These tests verify:
#   - governed candidate architecture;
#   - candidate governance roles;
#   - evidence artifact completeness;
#   - TRAIN-only tuning boundaries;
#   - patient-disjoint cross-validation;
#   - held-out VALIDATION comparison;
#   - governed model selection;
#   - persisted artifact integrity;
#   - locked TEST protection;
#   - absence of threshold/deployment authorization.
# ============================================================

from pathlib import Path

import pandas as pd
import yaml

from src.models.development import (
    MODEL_DUMMY,
    MODEL_LOGISTIC,
    MODEL_RANDOM_FOREST,
    MODEL_XGBOOST,
    build_candidate_model_factory,
)

from src.models.development_reporting import (
    D8_REPORTING_MODEL_ROLES,
    D8_MANIFEST_PATH,
    D8_CONTRACT_REPORT_PATH,
    D8_GATE_REPORT_PATH,
    D8_CANDIDATE_TABLE_PATH,
    D8_CV_TABLE_PATH,
    D8_TUNING_TABLE_PATH,
    D8_VALIDATION_TABLE_PATH,
    D8_SELECTION_TABLE_PATH,
    D8_ARTIFACT_INTEGRITY_TABLE_PATH,
    build_d8_candidate_model_registry,
)


# ============================================================
# SECTION 1 — GOVERNED CANDIDATE ARCHITECTURE
# ============================================================

def test_d8_reporting_model_roles_complete():
    expected_models = {
        MODEL_DUMMY,
        MODEL_LOGISTIC,
        MODEL_RANDOM_FOREST,
        MODEL_XGBOOST,
    }

    assert set(
        D8_REPORTING_MODEL_ROLES
    ) == expected_models


def test_d8_reporting_model_roles_are_unique():
    roles = list(
        D8_REPORTING_MODEL_ROLES.values()
    )

    assert len(roles) == len(
        set(roles)
    )


def test_d8_candidate_registry_contains_four_models():
    table = build_d8_candidate_model_registry(
        build_candidate_model_factory()
    )

    assert len(table) == 4

    assert table[
        "model_name"
    ].is_unique


def test_d8_candidate_registry_contains_expected_models():
    table = build_d8_candidate_model_registry(
        build_candidate_model_factory()
    )

    assert set(
        table["model_name"]
    ) == {
        MODEL_DUMMY,
        MODEL_LOGISTIC,
        MODEL_RANDOM_FOREST,
        MODEL_XGBOOST,
    }


def test_d8_candidate_registry_governance_roles_correct():
    table = build_d8_candidate_model_registry(
        build_candidate_model_factory()
    )

    observed_roles = dict(
        zip(
            table["model_name"],
            table["model_role"],
        )
    )

    assert observed_roles == (
        D8_REPORTING_MODEL_ROLES
    )


def test_d8_candidate_registry_estimator_classes_present():
    table = build_d8_candidate_model_registry(
        build_candidate_model_factory()
    )

    assert table[
        "estimator_class"
    ].notna().all()

    assert (
        table[
            "estimator_class"
        ].str.len()
        > 0
    ).all()


def test_d8_dummy_reference_not_hyperparameter_tuned():
    table = build_d8_candidate_model_registry(
        build_candidate_model_factory()
    )

    row = table.loc[
        table["model_name"]
        == MODEL_DUMMY
    ].iloc[0]

    assert (
        bool(
            row[
                "included_in_hyperparameter_tuning"
            ]
        )
        is False
    )


def test_d8_three_predictive_candidates_are_tunable():
    table = build_d8_candidate_model_registry(
        build_candidate_model_factory()
    )

    tunable_models = set(
        table.loc[
            table[
                "included_in_hyperparameter_tuning"
            ],
            "model_name",
        ]
    )

    assert tunable_models == {
        MODEL_LOGISTIC,
        MODEL_RANDOM_FOREST,
        MODEL_XGBOOST,
    }


def test_d8_candidate_registry_protects_locked_test():
    table = build_d8_candidate_model_registry(
        build_candidate_model_factory()
    )

    assert (
        table[
            "locked_test_access_permitted"
        ]
        == False
    ).all()  # noqa: E712


def test_d8_candidate_registry_prohibits_threshold_selection():
    table = build_d8_candidate_model_registry(
        build_candidate_model_factory()
    )

    assert (
        table[
            "clinical_threshold_selection_permitted"
        ]
        == False
    ).all()  # noqa: E712


def test_d8_candidate_registry_does_not_authorize_deployment():
    table = build_d8_candidate_model_registry(
        build_candidate_model_factory()
    )

    assert (
        table[
            "deployment_authorized"
        ]
        == False
    ).all()  # noqa: E712


# ============================================================
# SECTION 2 — D8 EVIDENCE PACKAGE COMPLETENESS
# ============================================================

def _d8_evidence_paths():
    return [
        D8_MANIFEST_PATH,
        D8_CONTRACT_REPORT_PATH,
        D8_GATE_REPORT_PATH,
        D8_CANDIDATE_TABLE_PATH,
        D8_CV_TABLE_PATH,
        D8_TUNING_TABLE_PATH,
        D8_VALIDATION_TABLE_PATH,
        D8_SELECTION_TABLE_PATH,
        D8_ARTIFACT_INTEGRITY_TABLE_PATH,
    ]


def test_d8_evidence_package_contains_nine_artifacts():
    assert len(
        _d8_evidence_paths()
    ) == 9


def test_all_d8_evidence_artifacts_exist():
    assert all(
        Path(path).exists()
        for path in _d8_evidence_paths()
    )


def test_all_d8_evidence_artifacts_are_nonempty():
    for path in _d8_evidence_paths():

        assert (
            Path(path).stat().st_size
            > 0
        )


# ============================================================
# SECTION 3 — MANIFEST GOVERNANCE
# ============================================================

def _load_d8_manifest():
    with Path(
        D8_MANIFEST_PATH
    ).open(
        "r",
        encoding="utf-8",
    ) as file_handle:

        return yaml.safe_load(
            file_handle
        )


def test_d8_manifest_stage_identity():
    manifest = _load_d8_manifest()

    assert manifest[
        "stage"
    ] == "D8"

    assert manifest[
        "stage_name"
    ] == (
        "Governed Model Development & Selection"
    )


def test_d8_manifest_gate_passes():
    manifest = _load_d8_manifest()

    assert manifest[
        "gate_status"
    ] == "PASS"


def test_d8_manifest_selected_model_is_xgboost():
    manifest = _load_d8_manifest()

    assert (
        manifest[
            "selected_development_model"
        ]
        == MODEL_XGBOOST
    )


def test_d8_manifest_primary_metric_is_validation_pr_auc():
    manifest = _load_d8_manifest()

    assert (
        manifest[
            "selection"
        ][
            "primary_metric"
        ]
        == "validation_pr_auc"
    )


def test_d8_manifest_validation_pr_auc_is_bounded():
    manifest = _load_d8_manifest()

    value = float(
        manifest[
            "selection"
        ][
            "validation_pr_auc"
        ]
    )

    assert 0.0 <= value <= 1.0


def test_d8_manifest_validation_roc_auc_is_bounded():
    manifest = _load_d8_manifest()

    value = float(
        manifest[
            "selection"
        ][
            "validation_roc_auc"
        ]
    )

    assert 0.0 <= value <= 1.0


def test_d8_manifest_runner_up_is_logistic_regression():
    manifest = _load_d8_manifest()

    assert (
        manifest[
            "selection"
        ][
            "runner_up_model"
        ]
        == MODEL_LOGISTIC
    )


def test_d8_manifest_selection_margin_positive():
    manifest = _load_d8_manifest()

    assert (
        float(
            manifest[
                "selection"
            ][
                "pr_auc_margin_vs_runner_up"
            ]
        )
        > 0.0
    )


def test_d8_manifest_fit_partition_is_train():
    manifest = _load_d8_manifest()

    assert (
        manifest[
            "governance"
        ][
            "fit_partition"
        ]
        == "train"
    )


def test_d8_manifest_tuning_partition_is_train():
    manifest = _load_d8_manifest()

    assert (
        manifest[
            "governance"
        ][
            "hyperparameter_tuning_partition"
        ]
        == "train"
    )


def test_d8_manifest_patient_disjoint_cv():
    manifest = _load_d8_manifest()

    assert (
        manifest[
            "governance"
        ][
            "patient_disjoint_cv"
        ]
        is True
    )


def test_d8_manifest_validation_not_used_for_tuning():
    manifest = _load_d8_manifest()

    assert (
        manifest[
            "governance"
        ][
            "validation_used_for_hyperparameter_tuning"
        ]
        is False
    )


def test_d8_manifest_validation_used_for_model_comparison():
    manifest = _load_d8_manifest()

    assert (
        manifest[
            "governance"
        ][
            "validation_used_for_model_comparison"
        ]
        is True
    )


def test_d8_manifest_development_candidate_only():
    manifest = _load_d8_manifest()

    assert (
        manifest[
            "governance"
        ][
            "development_candidate_only"
        ]
        is True
    )


def test_d8_manifest_does_not_claim_clinical_superiority():
    manifest = _load_d8_manifest()

    assert (
        manifest[
            "governance"
        ][
            "clinical_superiority_claimed"
        ]
        is False
    )


def test_d8_manifest_clinical_utility_not_established():
    manifest = _load_d8_manifest()

    assert (
        manifest[
            "governance"
        ][
            "clinical_utility_established"
        ]
        is False
    )


def test_d8_manifest_locked_test_untouched():
    manifest = _load_d8_manifest()

    assert (
        manifest[
            "governance"
        ][
            "locked_test_accessed"
        ]
        is False
    )


def test_d8_manifest_threshold_not_selected():
    manifest = _load_d8_manifest()

    assert (
        manifest[
            "governance"
        ][
            "clinical_threshold_selected"
        ]
        is False
    )


def test_d8_manifest_deployment_not_authorized():
    manifest = _load_d8_manifest()

    assert (
        manifest[
            "governance"
        ][
            "deployment_authorized"
        ]
        is False
    )


# ============================================================
# SECTION 4 — PATIENT-DISJOINT CROSS-VALIDATION EVIDENCE
# ============================================================

def _load_cv_table():
    return pd.read_csv(
        D8_CV_TABLE_PATH
    )


def test_d8_cv_contains_five_folds():
    table = _load_cv_table()

    assert len(table) == 5

    assert set(
        table["fold"]
    ) == {
        1,
        2,
        3,
        4,
        5,
    }


def test_d8_cv_patient_overlap_is_zero():
    table = _load_cv_table()

    assert (
        table[
            "patient_overlap_count"
        ]
        == 0
    ).all()


def test_d8_cv_train_and_validation_patients_present():
    table = _load_cv_table()

    assert (
        table[
            "cv_train_patients"
        ]
        > 0
    ).all()

    assert (
        table[
            "cv_validation_patients"
        ]
        > 0
    ).all()


def test_d8_cv_train_and_validation_encounters_present():
    table = _load_cv_table()

    assert (
        table[
            "cv_train_encounters"
        ]
        > 0
    ).all()

    assert (
        table[
            "cv_validation_encounters"
        ]
        > 0
    ).all()


def test_d8_cv_all_folds_contain_positive_cases():
    table = _load_cv_table()

    assert (
        table[
            "cv_train_positive_count"
        ]
        > 0
    ).all()

    assert (
        table[
            "cv_validation_positive_count"
        ]
        > 0
    ).all()


def test_d8_cv_prevalence_values_are_bounded():
    table = _load_cv_table()

    assert (
        table[
            "cv_train_prevalence"
        ].between(
            0.0,
            1.0,
            inclusive="both",
        )
    ).all()

    assert (
        table[
            "cv_validation_prevalence"
        ].between(
            0.0,
            1.0,
            inclusive="both",
        )
    ).all()


# ============================================================
# SECTION 5 — HYPERPARAMETER OPTIMIZATION EVIDENCE
# ============================================================

def _load_tuning_table():
    return pd.read_csv(
        D8_TUNING_TABLE_PATH
    )


def test_d8_tuning_contains_three_models():
    table = _load_tuning_table()

    assert set(
        table[
            "model_name"
        ]
    ) == {
        MODEL_LOGISTIC,
        MODEL_RANDOM_FOREST,
        MODEL_XGBOOST,
    }


def test_d8_dummy_reference_not_present_in_tuning_results():
    table = _load_tuning_table()

    assert MODEL_DUMMY not in set(
        table[
            "model_name"
        ]
    )


def test_d8_tuning_is_train_only():
    table = _load_tuning_table()

    assert (
        table[
            "fit_partition"
        ]
        == "train"
    ).all()


def test_d8_external_validation_not_used_for_tuning():
    table = _load_tuning_table()

    assert (
        table[
            "external_validation_used_for_tuning"
        ]
        == False
    ).all()  # noqa: E712


def test_d8_locked_test_not_used_for_tuning():
    table = _load_tuning_table()

    assert (
        table[
            "locked_test_accessed"
        ]
        == False
    ).all()  # noqa: E712


def test_d8_threshold_not_selected_during_tuning():
    table = _load_tuning_table()

    assert (
        table[
            "clinical_threshold_selected"
        ]
        == False
    ).all()  # noqa: E712


def test_d8_tuning_uses_five_cv_folds():
    table = _load_tuning_table()

    assert (
        table[
            "cv_folds"
        ]
        == 5
    ).all()


def test_d8_tuning_uses_average_precision():
    table = _load_tuning_table()

    assert (
        table[
            "primary_metric"
        ]
        == "average_precision"
    ).all()


def test_d8_tuning_cv_pr_auc_values_are_bounded():
    table = _load_tuning_table()

    assert (
        table[
            "best_cv_pr_auc"
        ].between(
            0.0,
            1.0,
            inclusive="both",
        )
    ).all()


def test_d8_tuning_best_parameters_are_present():
    table = _load_tuning_table()

    assert table[
        "best_parameters"
    ].notna().all()

    assert (
        table[
            "best_parameters"
        ].astype(str).str.len()
        > 2
    ).all()


# ============================================================
# SECTION 6 — HELD-OUT VALIDATION PERFORMANCE EVIDENCE
# ============================================================

def _load_validation_table():
    return pd.read_csv(
        D8_VALIDATION_TABLE_PATH
    )


def test_d8_validation_contains_three_tuned_models():
    table = _load_validation_table()

    assert set(
        table[
            "model_name"
        ]
    ) == {
        MODEL_LOGISTIC,
        MODEL_RANDOM_FOREST,
        MODEL_XGBOOST,
    }


def test_d8_validation_table_sorted_by_primary_metric():
    table = _load_validation_table()

    values = table[
        "validation_pr_auc"
    ].tolist()

    assert values == sorted(
        values,
        reverse=True,
    )


def test_d8_validation_primary_metric_correct():
    table = _load_validation_table()

    assert (
        table[
            "primary_selection_metric"
        ]
        == "validation_pr_auc"
    ).all()


def test_d8_validation_models_fit_on_train():
    table = _load_validation_table()

    assert (
        table[
            "fit_partition"
        ]
        == "train"
    ).all()


def test_d8_validation_not_used_for_model_fit():
    table = _load_validation_table()

    assert (
        table[
            "validation_used_for_fit"
        ]
        == False
    ).all()  # noqa: E712


def test_d8_validation_locked_test_remains_untouched():
    table = _load_validation_table()

    assert (
        table[
            "locked_test_accessed"
        ]
        == False
    ).all()  # noqa: E712


def test_d8_validation_threshold_not_selected():
    table = _load_validation_table()

    assert (
        table[
            "clinical_threshold_selected"
        ]
        == False
    ).all()  # noqa: E712


def test_d8_validation_pr_auc_values_are_bounded():
    table = _load_validation_table()

    assert (
        table[
            "validation_pr_auc"
        ].between(
            0.0,
            1.0,
            inclusive="both",
        )
    ).all()


def test_d8_validation_roc_auc_values_are_bounded():
    table = _load_validation_table()

    assert (
        table[
            "validation_roc_auc"
        ].between(
            0.0,
            1.0,
            inclusive="both",
        )
    ).all()


def test_d8_xgboost_has_highest_validation_pr_auc():
    table = _load_validation_table()

    selected = table.sort_values(
        by=[
            "validation_pr_auc",
            "validation_roc_auc",
        ],
        ascending=[
            False,
            False,
        ],
    ).iloc[0]

    assert (
        selected[
            "model_name"
        ]
        == MODEL_XGBOOST
    )


# ============================================================
# SECTION 7 — GOVERNED MODEL SELECTION EVIDENCE
# ============================================================

def _load_selection_table():
    return pd.read_csv(
        D8_SELECTION_TABLE_PATH
    )


def test_d8_selection_table_contains_one_model():
    table = _load_selection_table()

    assert len(table) == 1


def test_d8_selected_model_is_xgboost():
    table = _load_selection_table()

    assert (
        table.iloc[0][
            "selected_model"
        ]
        == MODEL_XGBOOST
    )


def test_d8_selected_model_role_is_boosted_tree_challenger():
    table = _load_selection_table()

    assert (
        table.iloc[0][
            "selected_model_role"
        ]
        == "BOOSTED_TREE_CHALLENGER"
    )


def test_d8_selection_metric_is_validation_pr_auc():
    table = _load_selection_table()

    assert (
        table.iloc[0][
            "selection_metric"
        ]
        == "validation_pr_auc"
    )


def test_d8_runner_up_is_logistic_regression():
    table = _load_selection_table()

    assert (
        table.iloc[0][
            "runner_up_model"
        ]
        == MODEL_LOGISTIC
    )


def test_d8_selected_model_has_positive_runner_up_margin():
    table = _load_selection_table()

    assert (
        float(
            table.iloc[0][
                "pr_auc_margin_vs_runner_up"
            ]
        )
        > 0.0
    )


def test_d8_selection_is_development_candidate_only():
    table = _load_selection_table()

    assert (
        bool(
            table.iloc[0][
                "development_candidate_only"
            ]
        )
        is True
    )


def test_d8_selection_does_not_claim_clinical_superiority():
    table = _load_selection_table()

    assert (
        bool(
            table.iloc[0][
                "clinical_superiority_claimed"
            ]
        )
        is False
    )


def test_d8_selection_does_not_establish_clinical_utility():
    table = _load_selection_table()

    assert (
        bool(
            table.iloc[0][
                "clinical_utility_established"
            ]
        )
        is False
    )


def test_d8_selection_keeps_locked_test_untouched():
    table = _load_selection_table()

    assert (
        bool(
            table.iloc[0][
                "locked_test_accessed"
            ]
        )
        is False
    )


def test_d8_selection_does_not_select_threshold():
    table = _load_selection_table()

    assert (
        bool(
            table.iloc[0][
                "clinical_threshold_selected"
            ]
        )
        is False
    )


def test_d8_selection_does_not_authorize_deployment():
    table = _load_selection_table()

    assert (
        bool(
            table.iloc[0][
                "deployment_authorized"
            ]
        )
        is False
    )


# ============================================================
# SECTION 8 — PERSISTED MODEL ARTIFACT INTEGRITY
# ============================================================

def _load_integrity_table():
    return pd.read_csv(
        D8_ARTIFACT_INTEGRITY_TABLE_PATH
    )


def test_d8_integrity_table_contains_one_model():
    table = _load_integrity_table()

    assert len(table) == 1


def test_d8_integrity_selected_model_is_xgboost():
    table = _load_integrity_table()

    assert (
        table.iloc[0][
            "selected_model"
        ]
        == MODEL_XGBOOST
    )


def test_d8_model_artifact_exists():
    table = _load_integrity_table()

    path = Path(
        table.iloc[0][
            "model_artifact_path"
        ]
    )

    assert path.exists()


def test_d8_metadata_artifact_exists():
    table = _load_integrity_table()

    path = Path(
        table.iloc[0][
            "metadata_artifact_path"
        ]
    )

    assert path.exists()


def test_d8_model_checksum_has_sha256_length():
    table = _load_integrity_table()

    checksum = str(
        table.iloc[0][
            "model_sha256"
        ]
    )

    assert len(checksum) == 64


def test_d8_metadata_checksum_has_sha256_length():
    table = _load_integrity_table()

    checksum = str(
        table.iloc[0][
            "metadata_sha256"
        ]
    )

    assert len(checksum) == 64


def test_d8_model_checksum_is_hexadecimal():
    table = _load_integrity_table()

    checksum = str(
        table.iloc[0][
            "model_sha256"
        ]
    )

    int(
        checksum,
        16,
    )


def test_d8_metadata_checksum_is_hexadecimal():
    table = _load_integrity_table()

    checksum = str(
        table.iloc[0][
            "metadata_sha256"
        ]
    )

    int(
        checksum,
        16,
    )


def test_d8_integrity_locked_test_untouched():
    table = _load_integrity_table()

    assert (
        bool(
            table.iloc[0][
                "locked_test_accessed"
            ]
        )
        is False
    )


def test_d8_integrity_threshold_not_selected():
    table = _load_integrity_table()

    assert (
        bool(
            table.iloc[0][
                "clinical_threshold_selected"
            ]
        )
        is False
    )


def test_d8_integrity_deployment_not_authorized():
    table = _load_integrity_table()

    assert (
        bool(
            table.iloc[0][
                "deployment_authorized"
            ]
        )
        is False
    )


# ============================================================
# SECTION 9 — CROSS-ARTIFACT CONSISTENCY
# ============================================================

def test_d8_manifest_and_selection_table_agree_on_model():
    manifest = _load_d8_manifest()
    selection = _load_selection_table()

    assert (
        manifest[
            "selected_development_model"
        ]
        == selection.iloc[0][
            "selected_model"
        ]
    )


def test_d8_manifest_and_selection_table_agree_on_pr_auc():
    manifest = _load_d8_manifest()
    selection = _load_selection_table()

    assert abs(
        float(
            manifest[
                "selection"
            ][
                "validation_pr_auc"
            ]
        )
        -
        float(
            selection.iloc[0][
                "validation_pr_auc"
            ]
        )
    ) < 1e-12


def test_d8_manifest_and_selection_table_agree_on_roc_auc():
    manifest = _load_d8_manifest()
    selection = _load_selection_table()

    assert abs(
        float(
            manifest[
                "selection"
            ][
                "validation_roc_auc"
            ]
        )
        -
        float(
            selection.iloc[0][
                "validation_roc_auc"
            ]
        )
    ) < 1e-12


def test_d8_manifest_and_integrity_table_agree_on_model_hash():
    manifest = _load_d8_manifest()
    integrity = _load_integrity_table()

    assert (
        manifest[
            "artifact_integrity"
        ][
            "model_sha256"
        ]
        == integrity.iloc[0][
            "model_sha256"
        ]
    )


def test_d8_manifest_and_integrity_table_agree_on_metadata_hash():
    manifest = _load_d8_manifest()
    integrity = _load_integrity_table()

    assert (
        manifest[
            "artifact_integrity"
        ][
            "metadata_sha256"
        ]
        == integrity.iloc[0][
            "metadata_sha256"
        ]
    )


def test_d8_selection_matches_highest_validation_pr_auc():
    validation = _load_validation_table()
    selection = _load_selection_table()

    expected_model = (
        validation
        .sort_values(
            by=[
                "validation_pr_auc",
                "validation_roc_auc",
            ],
            ascending=[
                False,
                False,
            ],
        )
        .iloc[0][
            "model_name"
        ]
    )

    assert (
        selection.iloc[0][
            "selected_model"
        ]
        == expected_model
    )


# ============================================================
# SECTION 10 — HUMAN-READABLE GOVERNANCE REPORTS
# ============================================================

def test_d8_contract_contains_train_only_boundary():
    text = Path(
        D8_CONTRACT_REPORT_PATH
    ).read_text(
        encoding="utf-8"
    )

    assert (
        "Model fitting occurs on TRAIN only."
        in text
    )


def test_d8_contract_contains_validation_boundary():
    text = Path(
        D8_CONTRACT_REPORT_PATH
    ).read_text(
        encoding="utf-8"
    )

    assert (
        "VALIDATION is excluded from hyperparameter optimization."
        in text
    )


def test_d8_contract_contains_locked_test_boundary():
    text = Path(
        D8_CONTRACT_REPORT_PATH
    ).read_text(
        encoding="utf-8"
    )

    assert (
        "locked TEST partition is inaccessible"
        in text
    )


def test_d8_contract_does_not_authorize_threshold_selection():
    text = Path(
        D8_CONTRACT_REPORT_PATH
    ).read_text(
        encoding="utf-8"
    )

    assert (
        "No clinical operating threshold is selected during D8."
        in text
    )


def test_d8_gate_decision_is_pass():
    text = Path(
        D8_GATE_REPORT_PATH
    ).read_text(
        encoding="utf-8"
    )

    assert "**PASS**" in text


def test_d8_gate_identifies_xgboost():
    text = Path(
        D8_GATE_REPORT_PATH
    ).read_text(
        encoding="utf-8"
    )

    assert (
        "**Model:** xgboost"
        in text
    )


def test_d8_gate_does_not_claim_clinical_superiority():
    text = Path(
        D8_GATE_REPORT_PATH
    ).read_text(
        encoding="utf-8"
    )

    assert (
        "not interpreted as proof of clinical superiority"
        in text
    )


def test_d8_gate_does_not_authorize_deployment():
    text = Path(
        D8_GATE_REPORT_PATH
    ).read_text(
        encoding="utf-8"
    )

    assert (
        "deployment is not authorized"
        in text
    )


def test_d8_gate_authorizes_progression_to_d9():
    text = Path(
        D8_GATE_REPORT_PATH
    ).read_text(
        encoding="utf-8"
    )

    assert (
        "D9 — Clinical Utility & Threshold Governance"
        in text
    )