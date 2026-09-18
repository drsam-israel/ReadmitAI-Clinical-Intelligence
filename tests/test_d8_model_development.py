# ============================================================
# TESTS — D8 GOVERNED MODEL DEVELOPMENT & SELECTION ENGINE
# ============================================================
#
# Purpose:
#   Validate the executable D8 model-development controls
#   without repeatedly rerunning expensive hyperparameter
#   optimization.
#
# Scope:
#   - D8 lifecycle contract;
#   - frozen D7 -> D8 development boundary;
#   - candidate-model architecture;
#   - model-input compatibility;
#   - patient-group recovery;
#   - patient-disjoint TRAIN CV;
#   - persisted selected-model integrity.
#
# Expensive TRAIN-CV hyperparameter optimization is validated
# through the persisted D8 evidence package and reporting tests.
# ============================================================

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import src.models.development as d


# ============================================================
# SECTION 1 — SESSION-SCOPED D8 FIXTURES
# ============================================================

@pytest.fixture(scope="session")
def d8_matrices():
    """
    Build the frozen D7 -> D8 development matrices once for the
    entire test session.
    """

    return d.build_d8_model_development_matrices()


@pytest.fixture(scope="session")
def d8_group_bundle(d8_matrices):
    """
    Recover TRAIN patient groups once.
    """

    return d.build_d8_train_patient_groups(
        matrices=d8_matrices
    )


@pytest.fixture(scope="session")
def d8_cv_bundle(
    d8_matrices,
    d8_group_bundle,
):
    """
    Build patient-disjoint TRAIN CV folds once.
    """

    return d.build_d8_group_aware_cv_folds(
        matrices=d8_matrices,
        group_bundle=d8_group_bundle,
    )


@pytest.fixture(scope="session")
def d8_candidate_factory():
    """
    Build governed D8 candidate estimators once.
    """

    return d.build_candidate_model_factory()


# ============================================================
# SECTION 2 — D8 LIFECYCLE CONTRACT
# ============================================================

def test_d8_model_development_contract_passes():
    result = (
        d.validate_d8_model_development_contract()
    )

    assert result[
        "validation_status"
    ] == "PASS"


def test_d8_stage_identity():
    assert d.D8_STAGE == "D8"

    assert d.D8_STAGE_NAME == (
        "Governed Model Development & Selection"
    )


def test_d8_target_is_readmitted_30d():
    assert d.D8_TARGET == "readmitted_30d"


def test_d8_fit_partition_is_train():
    assert d.D8_FIT_PARTITION == "train"


def test_d8_selection_partition_is_validation():
    assert (
        d.D8_SELECTION_PARTITION
        == "validation"
    )


def test_d8_locked_test_access_prohibited():
    assert (
        d.D8_LOCKED_TEST_ACCESS_PERMITTED
        is False
    )


def test_d8_clinical_threshold_selection_prohibited():
    assert (
        d.D8_CLINICAL_THRESHOLD_SELECTION_PERMITTED
        is False
    )


def test_d8_deployment_not_authorized():
    assert (
        d.D8_CLINICAL_DEPLOYMENT_AUTHORIZED
        is False
    )


# ============================================================
# SECTION 3 — D7 -> D8 DEVELOPMENT MATRIX BOUNDARY
# ============================================================

def test_d8_model_development_matrices_pass(
    d8_matrices,
):
    result = (
        d.validate_d8_model_development_matrices(
            d8_matrices
        )
    )

    assert result[
        "validation_status"
    ] == "PASS"


def test_d8_train_encounter_count(
    d8_matrices,
):
    assert (
        d8_matrices[
            "X_train"
        ].shape[0]
        == 70024
    )


def test_d8_validation_encounter_count(
    d8_matrices,
):
    assert (
        d8_matrices[
            "X_validation"
        ].shape[0]
        == 15052
    )


def test_d8_train_transformed_feature_count(
    d8_matrices,
):
    assert (
        d8_matrices[
            "X_train"
        ].shape[1]
        == 49
    )


def test_d8_validation_transformed_feature_count(
    d8_matrices,
):
    assert (
        d8_matrices[
            "X_validation"
        ].shape[1]
        == 49
    )


def test_d8_train_and_validation_schema_identical(
    d8_matrices,
):
    assert list(
        d8_matrices[
            "X_train"
        ].columns
    ) == list(
        d8_matrices[
            "X_validation"
        ].columns
    )


def test_d8_train_target_count_matches_X(
    d8_matrices,
):
    assert len(
        d8_matrices[
            "y_train"
        ]
    ) == len(
        d8_matrices[
            "X_train"
        ]
    )


def test_d8_validation_target_count_matches_X(
    d8_matrices,
):
    assert len(
        d8_matrices[
            "y_validation"
        ]
    ) == len(
        d8_matrices[
            "X_validation"
        ]
    )


def test_d8_train_features_have_no_missing_values(
    d8_matrices,
):
    assert not (
        d8_matrices[
            "X_train"
        ].isna().any().any()
    )


def test_d8_validation_features_have_no_missing_values(
    d8_matrices,
):
    assert not (
        d8_matrices[
            "X_validation"
        ].isna().any().any()
    )


def test_d8_train_features_are_finite(
    d8_matrices,
):
    values = d8_matrices[
        "X_train"
    ].to_numpy(
        dtype=float
    )

    assert np.isfinite(
        values
    ).all()


def test_d8_validation_features_are_finite(
    d8_matrices,
):
    values = d8_matrices[
        "X_validation"
    ].to_numpy(
        dtype=float
    )

    assert np.isfinite(
        values
    ).all()


def test_d8_train_target_is_binary(
    d8_matrices,
):
    assert set(
        pd.Series(
            d8_matrices[
                "y_train"
            ]
        ).unique()
    ).issubset(
        {0, 1}
    )


def test_d8_validation_target_is_binary(
    d8_matrices,
):
    assert set(
        pd.Series(
            d8_matrices[
                "y_validation"
            ]
        ).unique()
    ).issubset(
        {0, 1}
    )


def test_d8_locked_test_not_present_in_matrices(
    d8_matrices,
):
    forbidden_keys = {
        "X_test",
        "y_test",
        "test",
        "test_df",
        "test_matrix",
    }

    assert forbidden_keys.isdisjoint(
        set(
            d8_matrices.keys()
        )
    )


# ============================================================
# SECTION 4 — CANDIDATE MODEL FACTORY
# ============================================================

def test_d8_candidate_factory_validation_passes():
    result = (
        d.validate_candidate_model_factory()
    )

    assert result[
        "validation_status"
    ] == "PASS"


def test_d8_candidate_factory_contains_four_models(
    d8_candidate_factory,
):
    assert len(
        d8_candidate_factory
    ) == 4


def test_d8_candidate_factory_contains_expected_models(
    d8_candidate_factory,
):
    assert set(
        d8_candidate_factory
    ) == {
        d.MODEL_DUMMY,
        d.MODEL_LOGISTIC,
        d.MODEL_RANDOM_FOREST,
        d.MODEL_XGBOOST,
    }


def test_d8_candidate_models_are_distinct_objects(
    d8_candidate_factory,
):
    object_ids = {
        id(estimator)
        for estimator
        in d8_candidate_factory.values()
    }

    assert len(
        object_ids
    ) == 4


def test_d8_dummy_estimator_class(
    d8_candidate_factory,
):
    assert (
        d8_candidate_factory[
            d.MODEL_DUMMY
        ].__class__.__name__
        == "DummyClassifier"
    )


def test_d8_logistic_estimator_class(
    d8_candidate_factory,
):
    assert (
        d8_candidate_factory[
            d.MODEL_LOGISTIC
        ].__class__.__name__
        == "LogisticRegression"
    )


def test_d8_random_forest_estimator_class(
    d8_candidate_factory,
):
    assert (
        d8_candidate_factory[
            d.MODEL_RANDOM_FOREST
        ].__class__.__name__
        == "RandomForestClassifier"
    )


def test_d8_xgboost_estimator_class(
    d8_candidate_factory,
):
    assert (
        d8_candidate_factory[
            d.MODEL_XGBOOST
        ].__class__.__name__
        == "XGBClassifier"
    )


# ============================================================
# SECTION 5 — MODEL INPUT COMPATIBILITY ADAPTER
# ============================================================

def test_d8_model_input_adapter_passes(
    d8_matrices,
):
    result = (
        d.validate_model_input_adapter(
            d8_matrices
        )
    )

    assert result[
        "validation_status"
    ] == "PASS"


def test_d8_xgboost_adapter_returns_numpy(
    d8_matrices,
):
    adapted = d.prepare_model_input(
        d.MODEL_XGBOOST,
        d8_matrices[
            "X_train"
        ],
    )

    assert isinstance(
        adapted,
        np.ndarray,
    )


def test_d8_xgboost_adapter_preserves_shape(
    d8_matrices,
):
    source = d8_matrices[
        "X_train"
    ]

    adapted = d.prepare_model_input(
        d.MODEL_XGBOOST,
        source,
    )

    assert adapted.shape == (
        source.shape
    )


def test_d8_xgboost_adapter_preserves_values(
    d8_matrices,
):
    source = d8_matrices[
        "X_train"
    ]

    adapted = d.prepare_model_input(
        d.MODEL_XGBOOST,
        source,
    )

    np.testing.assert_array_equal(
        adapted,
        source.to_numpy(
            dtype=np.float64
        ),
    )


@pytest.mark.parametrize(
    "model_name",
    [
        d.MODEL_DUMMY,
        d.MODEL_LOGISTIC,
        d.MODEL_RANDOM_FOREST,
    ],
)
def test_d8_non_xgboost_models_keep_dataframe(
    d8_matrices,
    model_name,
):
    source = d8_matrices[
        "X_train"
    ]

    adapted = d.prepare_model_input(
        model_name,
        source,
    )

    assert isinstance(
        adapted,
        pd.DataFrame,
    )

    assert adapted is source


# ============================================================
# SECTION 6 — TRAIN PATIENT GROUP RECOVERY
# ============================================================

def test_d8_train_patient_groups_are_present(
    d8_group_bundle,
):
    assert d8_group_bundle is not None

    assert isinstance(
        d8_group_bundle,
        dict,
    )

    assert len(
        d8_group_bundle
    ) > 0


def test_d8_train_patient_group_bundle_has_no_test_key(
    d8_group_bundle,
):
    forbidden_keys = {
        "test",
        "test_groups",
        "test_patient_nbr",
        "test_patient_ids",
    }

    assert forbidden_keys.isdisjoint(
        set(
            d8_group_bundle.keys()
        )
    )


# ============================================================
# SECTION 7 — PATIENT-DISJOINT TRAIN CROSS-VALIDATION
# ============================================================

def test_d8_group_aware_cv_validation_passes(
    d8_cv_bundle,
):
    result = (
        d.validate_d8_group_aware_cv_folds(
            d8_cv_bundle
        )
    )

    assert result[
        "validation_status"
    ] == "PASS"


def test_d8_cv_bundle_contains_fold_summary(
    d8_cv_bundle,
):
    assert (
        "fold_summary"
        in d8_cv_bundle
    )


def test_d8_cv_contains_five_folds(
    d8_cv_bundle,
):
    table = d8_cv_bundle[
        "fold_summary"
    ]

    assert len(
        table
    ) == 5


def test_d8_cv_fold_numbers_are_complete(
    d8_cv_bundle,
):
    table = d8_cv_bundle[
        "fold_summary"
    ]

    assert set(
        table[
            "fold"
        ]
    ) == {
        1,
        2,
        3,
        4,
        5,
    }


def test_d8_cv_has_zero_patient_overlap(
    d8_cv_bundle,
):
    table = d8_cv_bundle[
        "fold_summary"
    ]

    assert (
        table[
            "patient_overlap_count"
        ]
        == 0
    ).all()


def test_d8_cv_train_encounters_present(
    d8_cv_bundle,
):
    table = d8_cv_bundle[
        "fold_summary"
    ]

    assert (
        table[
            "cv_train_encounters"
        ]
        > 0
    ).all()


def test_d8_cv_validation_encounters_present(
    d8_cv_bundle,
):
    table = d8_cv_bundle[
        "fold_summary"
    ]

    assert (
        table[
            "cv_validation_encounters"
        ]
        > 0
    ).all()


def test_d8_cv_train_patients_present(
    d8_cv_bundle,
):
    table = d8_cv_bundle[
        "fold_summary"
    ]

    assert (
        table[
            "cv_train_patients"
        ]
        > 0
    ).all()


def test_d8_cv_validation_patients_present(
    d8_cv_bundle,
):
    table = d8_cv_bundle[
        "fold_summary"
    ]

    assert (
        table[
            "cv_validation_patients"
        ]
        > 0
    ).all()


def test_d8_cv_train_positive_cases_present(
    d8_cv_bundle,
):
    table = d8_cv_bundle[
        "fold_summary"
    ]

    assert (
        table[
            "cv_train_positive_count"
        ]
        > 0
    ).all()


def test_d8_cv_validation_positive_cases_present(
    d8_cv_bundle,
):
    table = d8_cv_bundle[
        "fold_summary"
    ]

    assert (
        table[
            "cv_validation_positive_count"
        ]
        > 0
    ).all()


def test_d8_cv_prevalence_is_bounded(
    d8_cv_bundle,
):
    table = d8_cv_bundle[
        "fold_summary"
    ]

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
# SECTION 8 — HYPERPARAMETER OPTIMIZATION CONTRACT
# ============================================================

def test_d8_hyperparameter_contract_passes():
    result = (
        d.validate_d8_hyperparameter_optimization_contract()
    )

    assert result[
        "validation_status"
    ] == "PASS"


def test_d8_tuning_partition_is_train():
    assert (
        d.D8_TUNING_PARTITION
        == "train"
    )


def test_d8_tuning_metric_is_average_precision():
    assert (
        d.D8_TUNING_PRIMARY_METRIC
        == "average_precision"
    )


def test_d8_tuning_uses_five_folds():
    assert (
        d.D8_TUNING_CV_FOLDS
        == 5
    )


def test_d8_tuning_validation_access_prohibited():
    assert (
        d.D8_TUNING_VALIDATION_ACCESS_PERMITTED
        is False
    )


def test_d8_tuning_locked_test_access_prohibited():
    assert (
        d.D8_TUNING_LOCKED_TEST_ACCESS_PERMITTED
        is False
    )


def test_d8_tuning_threshold_selection_prohibited():
    assert (
        d.D8_TUNING_CLINICAL_THRESHOLD_SELECTION_PERMITTED
        is False
    )


def test_d8_tunable_candidate_set():
    assert set(
        d.TUNABLE_MODEL_CANDIDATES
    ) == {
        d.MODEL_LOGISTIC,
        d.MODEL_RANDOM_FOREST,
        d.MODEL_XGBOOST,
    }


def test_d8_dummy_not_in_tunable_candidate_set():
    assert (
        d.MODEL_DUMMY
        not in d.TUNABLE_MODEL_CANDIDATES
    )


# ============================================================
# SECTION 9 — PERSISTED DEVELOPMENT MODEL
# ============================================================

def test_d8_selected_model_artifact_exists():
    assert Path(
        d.D8_SELECTED_MODEL_ARTIFACT_PATH
    ).exists()


def test_d8_selected_model_metadata_exists():
    assert Path(
        d.D8_SELECTED_MODEL_METADATA_PATH
    ).exists()


def test_d8_selected_development_model_declared_xgboost():
    assert (
        d.D8_SELECTED_DEVELOPMENT_MODEL
        == d.MODEL_XGBOOST
    )


# ============================================================
# SECTION 10 — DEVELOPMENT-SELECTION GOVERNANCE BOUNDARY
# ============================================================

def test_d8_primary_selection_metric_is_validation_pr_auc():
    """
    Verify that held-out VALIDATION PR-AUC is the governed
    primary development-model selection metric.
    """

    assert (
        d.PRIMARY_SELECTION_METRIC
        == "validation_pr_auc"
    )


def test_d8_secondary_selection_metrics_are_governed():
    """
    Verify that VALIDATION ROC-AUC is retained as the governed
    secondary discrimination metric.

    SECONDARY_SELECTION_METRICS is intentionally represented
    as a tuple so the governance contract can support more than
    one secondary metric if required in a future lifecycle
    revision.
    """

    assert isinstance(
        d.SECONDARY_SELECTION_METRICS,
        tuple,
    )

    assert (
        d.SECONDARY_SELECTION_METRICS
        == (
            "validation_roc_auc",
        )
    )


def test_d8_primary_metric_not_replaced_by_accuracy():
    """
    Confirm that accuracy is not the governed primary
    development-model selection criterion.
    """

    assert (
        d.PRIMARY_SELECTION_METRIC
        != "validation_accuracy"
    )

    assert (
        "accuracy"
        not in d.PRIMARY_SELECTION_METRIC.lower()
    )


def test_d8_secondary_metric_contains_validation_roc_auc():
    """
    Explicitly verify the expected secondary discrimination
    evidence.
    """

    assert (
        "validation_roc_auc"
        in d.SECONDARY_SELECTION_METRICS
    )


def test_d8_selection_rule_does_not_claim_clinical_superiority():
    """
    The D8 selection rule must preserve the distinction between
    statistical development-stage selection and demonstrated
    clinical superiority.
    """

    rule = (
        d.D8_MODEL_SELECTION_RULE.lower()
    )

    assert (
        "clinical superiority"
        in rule
    )


def test_d8_selection_rule_mentions_locked_test():
    """
    The selection rule must explicitly preserve the locked-test
    lifecycle boundary.
    """

    rule = (
        d.D8_MODEL_SELECTION_RULE.lower()
    )

    assert (
        "locked-test"
        in rule
        or
        "locked test"
        in rule
    )


# ============================================================
# SECTION 11 — FINAL D8 ENGINE SAFETY BOUNDARY
# ============================================================

def test_d8_engine_has_no_test_feature_matrix(
    d8_matrices,
):
    """
    D8 must not expose the locked TEST feature matrix.
    """

    assert (
        "X_test"
        not in d8_matrices
    )


def test_d8_engine_has_no_test_target_vector(
    d8_matrices,
):
    """
    D8 must not expose the locked TEST outcome vector.
    """

    assert (
        "y_test"
        not in d8_matrices
    )


def test_d8_engine_remains_pre_threshold():
    """
    Clinical operating-threshold selection belongs to D9,
    not D8.
    """

    assert (
        d.D8_CLINICAL_THRESHOLD_SELECTION_PERMITTED
        is False
    )


def test_d8_engine_remains_pre_deployment():
    """
    Successful D8 model selection does not constitute
    deployment authorization.
    """

    assert (
        d.D8_CLINICAL_DEPLOYMENT_AUTHORIZED
        is False
    )

# ============================================================
# SECTION 11 — FINAL D8 ENGINE SAFETY BOUNDARY
# ============================================================

def test_d8_engine_has_no_test_feature_matrix(
    d8_matrices,
):
    assert (
        "X_test"
        not in d8_matrices
    )


def test_d8_engine_has_no_test_target_vector(
    d8_matrices,
):
    assert (
        "y_test"
        not in d8_matrices
    )


def test_d8_engine_remains_pre_threshold():
    assert (
        d.D8_CLINICAL_THRESHOLD_SELECTION_PERMITTED
        is False
    )


def test_d8_engine_remains_pre_deployment():
    assert (
        d.D8_CLINICAL_DEPLOYMENT_AUTHORIZED
        is False
    )