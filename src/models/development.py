# ============================================================
# D8 — MODEL DEVELOPMENT & SELECTION
# ============================================================
"""
Governed model-development framework for the Diabetes
30-Day Readmission Clinical AI project.

D8 PURPOSE
----------
Develop and compare candidate predictive models using the frozen
D7 preprocessing pathway.

DEVELOPMENT BOUNDARY
--------------------
TRAIN:
    Model fitting and TRAIN-derived fitted state.

VALIDATION:
    Model comparison and selection evidence only.

LOCKED TEST:
    Inaccessible during D8.

D8 DOES NOT
-----------
- redefine the clinical cohort;
- redefine the prediction target;
- redesign D4 feature authorization;
- refit D5 partitions;
- introduce D6-CONDITIONAL features;
- refit preprocessing using validation;
- access the locked test partition;
- select the final clinical operating threshold;
- authorize clinical deployment.

The output of D8 is a governed candidate-model comparison and
selection decision for progression to downstream clinical
evaluation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    average_precision_score,
    roc_auc_score,
)

from src.features.preprocessing import (
    PRIMARY_CANDIDATE_FEATURES,
    EXPECTED_D7_RAW_FEATURE_COUNT,
    EXPECTED_D7_TRANSFORMED_FEATURE_COUNT,
    EXPECTED_D7_TRAIN_ENCOUNTERS,
    EXPECTED_D7_VALIDATION_ENCOUNTERS,
    build_persisted_d7_primary_preprocessor,
)

from pathlib import Path

from sklearn.model_selection import StratifiedGroupKFold


from sklearn.model_selection import (
    GridSearchCV,
    RandomizedSearchCV,
)

# ============================================================
# D8 — ARTIFACT PERSISTENCE IMPORTS
# ============================================================

import hashlib
import json
import joblib
# ============================================================
# D8.01 — GOVERNED MODEL-DEVELOPMENT CONTRACT
# ============================================================

D8_STAGE = "D8"

D8_STAGE_NAME = (
    "Governed Model Development & Selection"
)

D8_TARGET = "readmitted_30d"

D8_FIT_PARTITION = "train"

D8_SELECTION_PARTITION = "validation"

D8_LOCKED_TEST_ACCESS_PERMITTED = False

D8_CLINICAL_THRESHOLD_SELECTION_PERMITTED = False

D8_CLINICAL_DEPLOYMENT_AUTHORIZED = False


# ============================================================
# D8.02 — CANDIDATE MODEL IDENTIFIERS
# ============================================================

MODEL_DUMMY = "dummy_prevalence"

MODEL_LOGISTIC = "logistic_regression"

MODEL_RANDOM_FOREST = "random_forest"

MODEL_XGBOOST = "xgboost"

EXPECTED_MODEL_CANDIDATES = (
    MODEL_DUMMY,
    MODEL_LOGISTIC,
    MODEL_RANDOM_FOREST,
    MODEL_XGBOOST,
)


# ============================================================
# D8.03 — MODEL ROLE REGISTRY
# ============================================================

MODEL_ROLES = {
    MODEL_DUMMY:
        "NO_SKILL_REFERENCE",

    MODEL_LOGISTIC:
        "INTERPRETABLE_BASELINE",

    MODEL_RANDOM_FOREST:
        "NONLINEAR_CHALLENGER",

    MODEL_XGBOOST:
        "BOOSTED_TREE_CHALLENGER",
}


# ============================================================
# D8.04 — GOVERNED MODEL SEEDS
# ============================================================

D8_RANDOM_STATE = 42


# ============================================================
# D8.05 — MODEL-SELECTION METRIC CONTRACT
# ============================================================

PRIMARY_SELECTION_METRIC = (
    "validation_pr_auc"
)

SECONDARY_SELECTION_METRICS = (
    "validation_roc_auc",
)

DIAGNOSTIC_METRICS = (
    "sensitivity",
    "specificity",
    "precision",
    "negative_predictive_value",
    "f1_score",
)

MODEL_SELECTION_RULE = (
    "Candidate model comparison is primarily based on "
    "VALIDATION PR-AUC. ROC-AUC is a secondary discrimination "
    "metric. Threshold-dependent metrics are diagnostic during "
    "D8 and must not be treated as the final clinical operating "
    "threshold decision."
)


# ============================================================
# D8.06 — CLASS-IMBALANCE GOVERNANCE
# ============================================================

CLASS_IMBALANCE_POLICY = {
    "target":
        D8_TARGET,

    "primary_metric":
        PRIMARY_SELECTION_METRIC,

    "accuracy_as_primary_metric":
        False,

    "synthetic_oversampling_permitted":
        False,

    "validation_resampling_permitted":
        False,

    "locked_test_resampling_permitted":
        False,

    "class_weighting":
        (
            "May be evaluated only as an explicitly governed "
            "model configuration."
        ),
}


# ============================================================
# D8.07 — MODEL DEVELOPMENT CONTRACT
# ============================================================

@dataclass(frozen=True)
class ModelDevelopmentContract:
    """
    Immutable D8 model-development governance contract.
    """

    stage: str = D8_STAGE

    target: str = D8_TARGET

    fit_partition: str = D8_FIT_PARTITION

    selection_partition: str = (
        D8_SELECTION_PARTITION
    )

    primary_selection_metric: str = (
        PRIMARY_SELECTION_METRIC
    )

    locked_test_access_permitted: bool = (
        D8_LOCKED_TEST_ACCESS_PERMITTED
    )

    clinical_threshold_selection_permitted: bool = (
        D8_CLINICAL_THRESHOLD_SELECTION_PERMITTED
    )

    clinical_deployment_authorized: bool = (
        D8_CLINICAL_DEPLOYMENT_AUTHORIZED
    )


D8_MODEL_DEVELOPMENT_CONTRACT = (
    ModelDevelopmentContract()
)


# ============================================================
# D8.08 — VALIDATE MODEL-DEVELOPMENT CONTRACT
# ============================================================

def validate_d8_model_development_contract(
) -> dict[str, Any]:
    """
    Validate the static governance rules that must hold before
    candidate-model development may begin.
    """

    candidate_models_unique = (
        len(
            EXPECTED_MODEL_CANDIDATES
        )
        == len(
            set(
                EXPECTED_MODEL_CANDIDATES
            )
        )
    )

    candidate_roles_complete = (
        set(
            EXPECTED_MODEL_CANDIDATES
        )
        == set(
            MODEL_ROLES
        )
    )

    primary_features_unique = (
        len(
            PRIMARY_CANDIDATE_FEATURES
        )
        == len(
            set(
                PRIMARY_CANDIDATE_FEATURES
            )
        )
    )

    checks = {
        "stage":
            D8_STAGE,

        "target":
            D8_TARGET,

        "candidate_model_count":
            len(
                EXPECTED_MODEL_CANDIDATES
            ),

        "candidate_models_unique":
            candidate_models_unique,

        "candidate_roles_complete":
            candidate_roles_complete,

        "raw_feature_count":
            len(
                PRIMARY_CANDIDATE_FEATURES
            ),

        "expected_raw_feature_count":
            EXPECTED_D7_RAW_FEATURE_COUNT,

        "expected_transformed_feature_count":
            EXPECTED_D7_TRANSFORMED_FEATURE_COUNT,

        "primary_features_unique":
            primary_features_unique,

        "fit_partition":
            D8_FIT_PARTITION,

        "selection_partition":
            D8_SELECTION_PARTITION,

        "primary_selection_metric":
            PRIMARY_SELECTION_METRIC,

        "accuracy_as_primary_metric":
            False,

        "synthetic_oversampling_permitted":
            False,

        "validation_resampling_permitted":
            False,

        "locked_test_access_permitted":
            D8_LOCKED_TEST_ACCESS_PERMITTED,

        "clinical_threshold_selection_permitted":
            D8_CLINICAL_THRESHOLD_SELECTION_PERMITTED,

        "clinical_deployment_authorized":
            D8_CLINICAL_DEPLOYMENT_AUTHORIZED,
    }

    passed = (
        checks[
            "stage"
        ]
        == "D8"

        and checks[
            "target"
        ]
        == "readmitted_30d"

        and checks[
            "candidate_model_count"
        ]
        == 4

        and candidate_models_unique

        and candidate_roles_complete

        and checks[
            "raw_feature_count"
        ]
        == EXPECTED_D7_RAW_FEATURE_COUNT

        and primary_features_unique

        and checks[
            "fit_partition"
        ]
        == "train"

        and checks[
            "selection_partition"
        ]
        == "validation"

        and checks[
            "primary_selection_metric"
        ]
        == "validation_pr_auc"

        and (
            checks[
                "accuracy_as_primary_metric"
            ]
            is False
        )

        and (
            checks[
                "synthetic_oversampling_permitted"
            ]
            is False
        )

        and (
            checks[
                "validation_resampling_permitted"
            ]
            is False
        )

        and (
            checks[
                "locked_test_access_permitted"
            ]
            is False
        )

        and (
            checks[
                "clinical_threshold_selection_permitted"
            ]
            is False
        )

        and (
            checks[
                "clinical_deployment_authorized"
            ]
            is False
        )
    )

    checks["validation_status"] = (
        "PASS"
        if passed
        else "FAIL"
    )

    return checks

# ============================================================
# D8.09 — BUILD AUTHORITATIVE MODEL-DEVELOPMENT MATRICES
# ============================================================

def build_d8_model_development_matrices(
) -> dict[str, Any]:
    """
    Load the frozen D7 preprocessing state and expose only the
    governed TRAIN and VALIDATION matrices permitted during D8.

    TRAIN:
        Candidate-model fitting.

    VALIDATION:
        Candidate-model comparison and selection.

    LOCKED TEST:
        Not loaded and not accessible through this function.
    """

    d7_workflow = (
        build_persisted_d7_primary_preprocessor()
    )

    fitted_bundle = (
        d7_workflow[
            "fitted_bundle"
        ]
    )

    persistence_validation = (
        d7_workflow[
            "persistence_validation"
        ]
    )

    if (
        persistence_validation[
            "validation_status"
        ]
        != "PASS"
    ):
        raise RuntimeError(
            "D8 model development blocked because "
            "the frozen D7 preprocessing gate did not pass."
        )

    X_train = (
        fitted_bundle[
            "X_train_transformed"
        ]
        .copy()
    )

    X_validation = (
        fitted_bundle[
            "X_validation_transformed"
        ]
        .copy()
    )

    y_train = (
        fitted_bundle[
            "y_train"
        ]
        .copy()
    )

    y_validation = (
        fitted_bundle[
            "y_validation"
        ]
        .copy()
    )

    transformed_feature_names = (
        fitted_bundle[
            "transformed_feature_names"
        ]
    )

    return {
        "X_train":
            X_train,

        "y_train":
            y_train,

        "X_validation":
            X_validation,

        "y_validation":
            y_validation,

        "transformed_feature_names":
            transformed_feature_names,

        "d7_preprocessor_sha256":
            d7_workflow[
                "persistence_result"
            ][
                "preprocessor_sha256"
            ],

        "d7_schema_sha256":
            d7_workflow[
                "persistence_result"
            ][
                "schema_sha256"
            ],

        "fit_partition":
            D8_FIT_PARTITION,

        "selection_partition":
            D8_SELECTION_PARTITION,

        "validation_contributed_to_preprocessing_fit":
            False,

        "locked_test_accessed":
            False,
    }


# ============================================================
# D8.10 — VALIDATE MODEL-DEVELOPMENT MATRICES
# ============================================================

def validate_d8_model_development_matrices(
    matrices: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Validate the exact D8 TRAIN / VALIDATION modeling boundary
    before candidate-model fitting is permitted.
    """

    if matrices is None:
        matrices = (
            build_d8_model_development_matrices()
        )

    X_train = matrices["X_train"]
    X_validation = matrices["X_validation"]

    y_train = matrices["y_train"]
    y_validation = matrices["y_validation"]

    transformed_feature_names = (
        matrices[
            "transformed_feature_names"
        ]
    )

    train_feature_order_correct = (
        list(X_train.columns)
        == transformed_feature_names
    )

    validation_feature_order_correct = (
        list(X_validation.columns)
        == transformed_feature_names
    )

    transformed_schema_identical = (
        list(X_train.columns)
        == list(X_validation.columns)
    )

    transformed_feature_names_unique = (
        len(
            transformed_feature_names
        )
        == len(
            set(
                transformed_feature_names
            )
        )
    )

    train_target_values = sorted(
        pd.Series(
            y_train
        )
        .dropna()
        .unique()
        .tolist()
    )

    validation_target_values = sorted(
        pd.Series(
            y_validation
        )
        .dropna()
        .unique()
        .tolist()
    )

    train_missing_values = int(
        X_train
        .isna()
        .sum()
        .sum()
    )

    validation_missing_values = int(
        X_validation
        .isna()
        .sum()
        .sum()
    )

    train_nonfinite_values = int(
        (
            ~np.isfinite(
                X_train.to_numpy(
                    dtype=float
                )
            )
        )
        .sum()
    )

    validation_nonfinite_values = int(
        (
            ~np.isfinite(
                X_validation.to_numpy(
                    dtype=float
                )
            )
        )
        .sum()
    )

    train_positive_count = int(
        pd.Series(
            y_train
        ).sum()
    )

    validation_positive_count = int(
        pd.Series(
            y_validation
        ).sum()
    )

    train_prevalence = float(
        pd.Series(
            y_train
        ).mean()
    )

    validation_prevalence = float(
        pd.Series(
            y_validation
        ).mean()
    )

    checks = {
        "X_train_shape":
            X_train.shape,

        "X_validation_shape":
            X_validation.shape,

        "y_train_rows":
            len(y_train),

        "y_validation_rows":
            len(y_validation),

        "transformed_feature_count":
            len(
                transformed_feature_names
            ),

        "train_feature_order_correct":
            train_feature_order_correct,

        "validation_feature_order_correct":
            validation_feature_order_correct,

        "transformed_schema_identical":
            transformed_schema_identical,

        "transformed_feature_names_unique":
            transformed_feature_names_unique,

        "train_target_values":
            train_target_values,

        "validation_target_values":
            validation_target_values,

        "train_positive_count":
            train_positive_count,

        "validation_positive_count":
            validation_positive_count,

        "train_prevalence":
            train_prevalence,

        "validation_prevalence":
            validation_prevalence,

        "train_missing_values":
            train_missing_values,

        "validation_missing_values":
            validation_missing_values,

        "train_nonfinite_values":
            train_nonfinite_values,

        "validation_nonfinite_values":
            validation_nonfinite_values,

        "fit_partition":
            matrices[
                "fit_partition"
            ],

        "selection_partition":
            matrices[
                "selection_partition"
            ],

        "validation_contributed_to_preprocessing_fit":
            matrices[
                "validation_contributed_to_preprocessing_fit"
            ],

        "locked_test_accessed":
            matrices[
                "locked_test_accessed"
            ],

        "d7_preprocessor_sha256":
            matrices[
                "d7_preprocessor_sha256"
            ],

        "d7_schema_sha256":
            matrices[
                "d7_schema_sha256"
            ],
    }

    passed = (
        X_train.shape
        == (
            EXPECTED_D7_TRAIN_ENCOUNTERS,
            EXPECTED_D7_TRANSFORMED_FEATURE_COUNT,
        )

        and X_validation.shape
        == (
            EXPECTED_D7_VALIDATION_ENCOUNTERS,
            EXPECTED_D7_TRANSFORMED_FEATURE_COUNT,
        )

        and len(y_train)
        == EXPECTED_D7_TRAIN_ENCOUNTERS

        and len(y_validation)
        == EXPECTED_D7_VALIDATION_ENCOUNTERS

        and train_feature_order_correct

        and validation_feature_order_correct

        and transformed_schema_identical

        and transformed_feature_names_unique

        and train_target_values
        == [0, 1]

        and validation_target_values
        == [0, 1]

        and train_missing_values
        == 0

        and validation_missing_values
        == 0

        and train_nonfinite_values
        == 0

        and validation_nonfinite_values
        == 0

        and matrices[
            "fit_partition"
        ]
        == "train"

        and matrices[
            "selection_partition"
        ]
        == "validation"

        and matrices[
            "validation_contributed_to_preprocessing_fit"
        ]
        is False

        and matrices[
            "locked_test_accessed"
        ]
        is False
    )

    checks[
        "validation_status"
    ] = (
        "PASS"
        if passed
        else "FAIL"
    )

    return checks

# ============================================================
# D8.11 — XGBOOST AVAILABILITY
# ============================================================

try:
    from xgboost import XGBClassifier

    XGBOOST_AVAILABLE = True

except ImportError:
    XGBClassifier = None

    XGBOOST_AVAILABLE = False


# ============================================================
# D8.12 — GOVERNED CANDIDATE MODEL SPECIFICATIONS
# ============================================================

MODEL_SPECIFICATIONS = {
    MODEL_DUMMY: {
        "role":
            MODEL_ROLES[
                MODEL_DUMMY
            ],

        "estimator":
            "DummyClassifier",

        "parameters": {
            "strategy":
                "prior",

            "random_state":
                D8_RANDOM_STATE,
        },
    },

    MODEL_LOGISTIC: {
        "role":
            MODEL_ROLES[
                MODEL_LOGISTIC
            ],

        "estimator":
            "LogisticRegression",

        "parameters": {
            # scikit-learn 1.8+ compatible representation
            # of L2 regularization.
            "C":
                1.0,

            "l1_ratio":
                0.0,

            "solver":
                "liblinear",

            "max_iter":
                1000,

            "class_weight":
                None,

            "random_state":
                D8_RANDOM_STATE,
        },
    },

    MODEL_RANDOM_FOREST: {
        "role":
            MODEL_ROLES[
                MODEL_RANDOM_FOREST
            ],

        "estimator":
            "RandomForestClassifier",

        "parameters": {
            "n_estimators":
                500,

            "criterion":
                "gini",

            "max_depth":
                None,

            "min_samples_split":
                2,

            "min_samples_leaf":
                1,

            "max_features":
                "sqrt",

            "class_weight":
                None,

            "n_jobs":
                -1,

            "random_state":
                D8_RANDOM_STATE,
        },
    },

    MODEL_XGBOOST: {
        "role":
            MODEL_ROLES[
                MODEL_XGBOOST
            ],

        "estimator":
            "XGBClassifier",

        "parameters": {
            "n_estimators":
                300,

            "max_depth":
                4,

            "learning_rate":
                0.05,

            "subsample":
                0.8,

            "colsample_bytree":
                0.8,

            "objective":
                "binary:logistic",

            "eval_metric":
                "logloss",

            "tree_method":
                "hist",

            "n_jobs":
                -1,

            "random_state":
                D8_RANDOM_STATE,
        },
    },
}


# ============================================================
# D8.13 — BUILD GOVERNED CANDIDATE MODEL FACTORY
# ============================================================

def build_candidate_model_factory(
) -> dict[str, BaseEstimator]:
    """
    Instantiate the governed D8 candidate models.

    This function defines model objects only.

    It does NOT:
    - fit any model;
    - access validation outcomes for fitting;
    - access the locked test partition;
    - perform hyperparameter tuning;
    - select a clinical threshold.
    """

    if not XGBOOST_AVAILABLE:
        raise RuntimeError(
            "XGBoost is required for the governed D8 "
            "candidate set but is not installed."
        )

    models = {
        MODEL_DUMMY:
            DummyClassifier(
                **MODEL_SPECIFICATIONS[
                    MODEL_DUMMY
                ][
                    "parameters"
                ]
            ),

        MODEL_LOGISTIC:
            LogisticRegression(
                **MODEL_SPECIFICATIONS[
                    MODEL_LOGISTIC
                ][
                    "parameters"
                ]
            ),

        MODEL_RANDOM_FOREST:
            RandomForestClassifier(
                **MODEL_SPECIFICATIONS[
                    MODEL_RANDOM_FOREST
                ][
                    "parameters"
                ]
            ),

        MODEL_XGBOOST:
            XGBClassifier(
                **MODEL_SPECIFICATIONS[
                    MODEL_XGBOOST
                ][
                    "parameters"
                ]
            ),
    }

    return models


# ============================================================
# D8.14 — VALIDATE CANDIDATE MODEL FACTORY
# ============================================================

def validate_candidate_model_factory(
) -> dict[str, Any]:
    """
    Validate the candidate-model factory before model fitting.
    """

    models = (
        build_candidate_model_factory()
    )

    model_names = tuple(
        models.keys()
    )

    estimator_classes = {
        name:
            estimator.__class__.__name__

        for name, estimator
        in models.items()
    }

    all_estimators_unfitted = all(
        not hasattr(
            estimator,
            "classes_",
        )

        for estimator
        in models.values()
    )

    expected_estimator_classes = {
        MODEL_DUMMY:
            "DummyClassifier",

        MODEL_LOGISTIC:
            "LogisticRegression",

        MODEL_RANDOM_FOREST:
            "RandomForestClassifier",

        MODEL_XGBOOST:
            "XGBClassifier",
    }

    checks = {
        "xgboost_available":
            XGBOOST_AVAILABLE,

        "candidate_model_count":
            len(models),

        "candidate_model_names":
            list(
                model_names
            ),

        "candidate_set_exact":
            model_names
            == EXPECTED_MODEL_CANDIDATES,

        "estimator_classes":
            estimator_classes,

        "estimator_classes_correct":
            estimator_classes
            == expected_estimator_classes,

        "all_estimators_unfitted":
            all_estimators_unfitted,

        "random_state":
            D8_RANDOM_STATE,

        "fit_performed":
            False,

        "validation_used_for_fit":
            False,

        "locked_test_accessed":
            False,

        "clinical_threshold_selected":
            False,
    }

    passed = (
        checks[
            "xgboost_available"
        ]
        is True

        and checks[
            "candidate_model_count"
        ]
        == 4

        and checks[
            "candidate_set_exact"
        ]
        is True

        and checks[
            "estimator_classes_correct"
        ]
        is True

        and checks[
            "all_estimators_unfitted"
        ]
        is True

        and checks[
            "fit_performed"
        ]
        is False

        and checks[
            "validation_used_for_fit"
        ]
        is False

        and checks[
            "locked_test_accessed"
        ]
        is False

        and checks[
            "clinical_threshold_selected"
        ]
        is False
    )

    checks[
        "validation_status"
    ] = (
        "PASS"
        if passed
        else "FAIL"
    )

    return checks


# ============================================================
# D8.14A — MODEL-SPECIFIC INPUT COMPATIBILITY POLICY
# ============================================================

MODEL_INPUT_COMPATIBILITY_POLICY = {
    MODEL_DUMMY:
        "PANDAS_DATAFRAME",

    MODEL_LOGISTIC:
        "PANDAS_DATAFRAME",

    MODEL_RANDOM_FOREST:
        "PANDAS_DATAFRAME",

    MODEL_XGBOOST:
        "ORDERED_NUMPY_ARRAY",
}

XGBOOST_INPUT_ADAPTER_REASON = (
    "XGBoost 3.x rejects pandas feature names containing "
    "characters such as '[', ']' or '<'. The frozen D7 "
    "schema legitimately contains one-hot encoded age-category "
    "feature names with square brackets. XGBoost therefore "
    "receives the identical ordered 49-column numeric matrix "
    "as a NumPy array. Feature values, order, count, D7 "
    "authorization and preprocessing state remain unchanged."
)


# ============================================================
# D8.14B — MODEL-SPECIFIC INPUT ADAPTER
# ============================================================

def prepare_model_input(
    model_name: str,
    X: pd.DataFrame,
) -> pd.DataFrame | np.ndarray:
    """
    Prepare estimator-specific model input without changing the
    governed D7 feature values, order, count or preprocessing
    state.

    XGBoost compatibility control
    ------------------------------
    XGBoost 3.x rejects pandas feature names containing certain
    characters such as '[', ']' and '<'.

    The frozen D7 transformed schema legitimately contains
    one-hot encoded age-category names with square brackets.

    XGBoost therefore receives the exact same 49-column numeric
    matrix as a NumPy array.

    This function does NOT:
    - rename D7 features;
    - change feature order;
    - change feature values;
    - change feature count;
    - refit preprocessing;
    - use validation for fitting;
    - access the locked test partition.
    """

    if model_name not in EXPECTED_MODEL_CANDIDATES:
        raise ValueError(
            f"Unknown D8 candidate model: {model_name}"
        )

    if not isinstance(
        X,
        pd.DataFrame,
    ):
        raise TypeError(
            "D8 governed model input must originate from "
            "a pandas DataFrame containing the frozen D7 "
            "transformed schema."
        )

    if (
        X.shape[1]
        != EXPECTED_D7_TRANSFORMED_FEATURE_COUNT
    ):
        raise RuntimeError(
            "D8 model input does not contain the expected "
            f"{EXPECTED_D7_TRANSFORMED_FEATURE_COUNT} "
            "transformed features."
        )

    if model_name == MODEL_XGBOOST:

        adapted = X.to_numpy(
            dtype=np.float64,
            copy=True,
        )

        if adapted.shape != X.shape:
            raise RuntimeError(
                "XGBoost input adaptation changed "
                "the governed matrix shape."
            )

        if not np.isfinite(
            adapted
        ).all():
            raise RuntimeError(
                "XGBoost adapted matrix contains "
                "non-finite values."
            )

        return adapted

    return X


# ============================================================
# D8.14C — VALIDATE MODEL-SPECIFIC INPUT ADAPTER
# ============================================================

def validate_model_input_adapter(
    matrices: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Validate that estimator-specific input adaptation preserves
    the frozen D7 matrix exactly.

    The XGBoost adapter may change only the container type:
        pandas DataFrame -> NumPy ndarray

    It may not change:
    - number of encounters;
    - number of features;
    - feature order;
    - numeric values.
    """

    if matrices is None:
        matrices = (
            build_d8_model_development_matrices()
        )

    X_train = matrices[
        "X_train"
    ]

    X_validation = matrices[
        "X_validation"
    ]

    xgb_train = (
        prepare_model_input(
            MODEL_XGBOOST,
            X_train,
        )
    )

    xgb_validation = (
        prepare_model_input(
            MODEL_XGBOOST,
            X_validation,
        )
    )

    train_reference = (
        X_train.to_numpy(
            dtype=np.float64,
            copy=True,
        )
    )

    validation_reference = (
        X_validation.to_numpy(
            dtype=np.float64,
            copy=True,
        )
    )

    non_xgb_identity_preserved = all(
        prepare_model_input(
            model_name,
            X_train,
        )
        is X_train

        for model_name
        in (
            MODEL_DUMMY,
            MODEL_LOGISTIC,
            MODEL_RANDOM_FOREST,
        )
    )

    checks = {
        "xgboost_policy":
            MODEL_INPUT_COMPATIBILITY_POLICY[
                MODEL_XGBOOST
            ],

        "xgboost_train_type":
            type(
                xgb_train
            ).__name__,

        "xgboost_validation_type":
            type(
                xgb_validation
            ).__name__,

        "xgboost_train_shape":
            xgb_train.shape,

        "xgboost_validation_shape":
            xgb_validation.shape,

        "train_shape_preserved":
            xgb_train.shape
            == X_train.shape,

        "validation_shape_preserved":
            xgb_validation.shape
            == X_validation.shape,

        "train_values_preserved_exactly":
            np.array_equal(
                xgb_train,
                train_reference,
            ),

        "validation_values_preserved_exactly":
            np.array_equal(
                xgb_validation,
                validation_reference,
            ),

        "train_values_finite":
            np.isfinite(
                xgb_train
            ).all(),

        "validation_values_finite":
            np.isfinite(
                xgb_validation
            ).all(),

        "non_xgboost_identity_preserved":
            non_xgb_identity_preserved,

        "d7_feature_count":
            X_train.shape[1],

        "xgboost_feature_count":
            xgb_train.shape[1],

        "d7_schema_modified":
            False,

        "feature_values_modified":
            False,

        "feature_order_modified":
            False,

        "locked_test_accessed":
            False,
    }

    passed = (
        checks[
            "xgboost_train_type"
        ]
        == "ndarray"

        and checks[
            "xgboost_validation_type"
        ]
        == "ndarray"

        and checks[
            "train_shape_preserved"
        ]
        is True

        and checks[
            "validation_shape_preserved"
        ]
        is True

        and checks[
            "train_values_preserved_exactly"
        ]
        is True

        and checks[
            "validation_values_preserved_exactly"
        ]
        is True

        and checks[
            "train_values_finite"
        ]

        and checks[
            "validation_values_finite"
        ]

        and checks[
            "non_xgboost_identity_preserved"
        ]
        is True

        and checks[
            "d7_feature_count"
        ]
        == EXPECTED_D7_TRANSFORMED_FEATURE_COUNT

        and checks[
            "xgboost_feature_count"
        ]
        == EXPECTED_D7_TRANSFORMED_FEATURE_COUNT

        and checks[
            "d7_schema_modified"
        ]
        is False

        and checks[
            "feature_values_modified"
        ]
        is False

        and checks[
            "feature_order_modified"
        ]
        is False

        and checks[
            "locked_test_accessed"
        ]
        is False
    )

    checks[
        "validation_status"
    ] = (
        "PASS"
        if passed
        else "FAIL"
    )

    return checks


# ============================================================
# D8.15 — GOVERNED CANDIDATE MODEL TRAINING
# ============================================================

def fit_d8_candidate_models(
    matrices: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Fit the governed D8 candidate models using TRAIN only.

    VALIDATION:
        Used only to generate out-of-sample development
        predictions for later model comparison.

    LOCKED TEST:
        Not loaded and not accessed.

    No clinical operating threshold is selected here.
    """

    if matrices is None:
        matrices = (
            build_d8_model_development_matrices()
        )

    matrix_validation = (
        validate_d8_model_development_matrices(
            matrices
        )
    )

    if (
        matrix_validation[
            "validation_status"
        ]
        != "PASS"
    ):
        raise RuntimeError(
            "D8 candidate-model training blocked because "
            "the model-development matrix gate did not pass."
        )

    adapter_validation = (
        validate_model_input_adapter(
            matrices
        )
    )

    if (
        adapter_validation[
            "validation_status"
        ]
        != "PASS"
    ):
        raise RuntimeError(
            "D8 candidate-model training blocked because "
            "the estimator input-adapter gate did not pass."
        )

    X_train = matrices[
        "X_train"
    ]

    y_train = matrices[
        "y_train"
    ]

    X_validation = matrices[
        "X_validation"
    ]

    y_validation = matrices[
        "y_validation"
    ]

    models = (
        build_candidate_model_factory()
    )

    fitted_models = {}

    train_probabilities = {}

    validation_probabilities = {}

    training_records = []

    for model_name, model in models.items():

        # ----------------------------------------------------
        # MODEL-SPECIFIC INPUT ADAPTATION
        # ----------------------------------------------------

        X_train_model = (
            prepare_model_input(
                model_name,
                X_train,
            )
        )

        X_validation_model = (
            prepare_model_input(
                model_name,
                X_validation,
            )
        )

        # ----------------------------------------------------
        # FIT — TRAIN ONLY
        # ----------------------------------------------------

        model.fit(
            X_train_model,
            y_train,
        )

        # ----------------------------------------------------
        # TRAIN PROBABILITY PREDICTIONS
        # ----------------------------------------------------

        train_probability = (
            model.predict_proba(
                X_train_model
            )[:, 1]
        )

        # ----------------------------------------------------
        # VALIDATION PROBABILITY PREDICTIONS
        # ----------------------------------------------------

        validation_probability = (
            model.predict_proba(
                X_validation_model
            )[:, 1]
        )

        fitted_models[
            model_name
        ] = model

        train_probabilities[
            model_name
        ] = train_probability

        validation_probabilities[
            model_name
        ] = validation_probability

        training_records.append(
            {
                "model_name":
                    model_name,

                "model_role":
                    MODEL_ROLES[
                        model_name
                    ],

                "estimator_class":
                    model.__class__.__name__,

                "input_container":
                    (
                        "ndarray"
                        if model_name
                        == MODEL_XGBOOST
                        else "DataFrame"
                    ),

                "input_compatibility_policy":
                    MODEL_INPUT_COMPATIBILITY_POLICY[
                        model_name
                    ],

                "fit_partition":
                    "train",

                "fit_encounters":
                    int(
                        len(
                            X_train
                        )
                    ),

                "fit_positive_count":
                    int(
                        pd.Series(
                            y_train
                        ).sum()
                    ),

                "validation_prediction_encounters":
                    int(
                        len(
                            X_validation
                        )
                    ),

                "validation_used_for_fit":
                    False,

                "locked_test_accessed":
                    False,

                "clinical_threshold_selected":
                    False,
            }
        )

    training_registry = (
        pd.DataFrame(
            training_records
        )
    )

    return {
        "fitted_models":
            fitted_models,

        "train_probabilities":
            train_probabilities,

        "validation_probabilities":
            validation_probabilities,

        "training_registry":
            training_registry,

        "y_train":
            y_train.copy(),

        "y_validation":
            y_validation.copy(),

        "xgboost_input_adapter_applied":
            True,

        "d7_schema_modified":
            False,

        "fit_partition":
            "train",

        "validation_used_for_fit":
            False,

        "locked_test_accessed":
            False,

        "clinical_threshold_selected":
            False,
    }


# ============================================================
# D8.16 — VALIDATE CANDIDATE MODEL TRAINING
# ============================================================

def validate_d8_candidate_model_training(
    training_bundle: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Validate that every governed candidate model was fitted
    correctly and that probability predictions are structurally
    valid before performance comparison is permitted.
    """

    if training_bundle is None:
        training_bundle = (
            fit_d8_candidate_models()
        )

    fitted_models = (
        training_bundle[
            "fitted_models"
        ]
    )

    train_probabilities = (
        training_bundle[
            "train_probabilities"
        ]
    )

    validation_probabilities = (
        training_bundle[
            "validation_probabilities"
        ]
    )

    training_registry = (
        training_bundle[
            "training_registry"
        ]
    )

    expected_models = set(
        EXPECTED_MODEL_CANDIDATES
    )

    fitted_model_names = set(
        fitted_models
    )

    train_prediction_models = set(
        train_probabilities
    )

    validation_prediction_models = set(
        validation_probabilities
    )

    all_models_fitted = all(
        hasattr(
            model,
            "classes_",
        )

        for model
        in fitted_models.values()
    )

    train_prediction_lengths_correct = all(
        len(
            probabilities
        )
        == EXPECTED_D7_TRAIN_ENCOUNTERS

        for probabilities
        in train_probabilities.values()
    )

    validation_prediction_lengths_correct = all(
        len(
            probabilities
        )
        == EXPECTED_D7_VALIDATION_ENCOUNTERS

        for probabilities
        in validation_probabilities.values()
    )

    train_probabilities_finite = all(
        np.isfinite(
            probabilities
        ).all()

        for probabilities
        in train_probabilities.values()
    )

    validation_probabilities_finite = all(
        np.isfinite(
            probabilities
        ).all()

        for probabilities
        in validation_probabilities.values()
    )

    train_probabilities_in_range = all(
        (
            (
                probabilities
                >= 0.0
            ).all()

            and

            (
                probabilities
                <= 1.0
            ).all()
        )

        for probabilities
        in train_probabilities.values()
    )

    validation_probabilities_in_range = all(
        (
            (
                probabilities
                >= 0.0
            ).all()

            and

            (
                probabilities
                <= 1.0
            ).all()
        )

        for probabilities
        in validation_probabilities.values()
    )

    training_registry_models = set(
        training_registry[
            "model_name"
        ].tolist()
    )

    training_registry_complete = (
        training_registry_models
        == expected_models
    )

    xgboost_registry_row = (
        training_registry.loc[
            training_registry[
                "model_name"
            ]
            == MODEL_XGBOOST
        ]
    )

    xgboost_adapter_recorded = (
        len(
            xgboost_registry_row
        )
        == 1

        and xgboost_registry_row[
            "input_container"
        ].iloc[0]
        == "ndarray"

        and xgboost_registry_row[
            "input_compatibility_policy"
        ].iloc[0]
        == "ORDERED_NUMPY_ARRAY"
    )

    non_xgboost_dataframe_recorded = (
        training_registry.loc[
            training_registry[
                "model_name"
            ]
            != MODEL_XGBOOST,
            "input_container",
        ]
        .eq(
            "DataFrame"
        )
        .all()
    )

    checks = {
        "expected_candidate_count":
            len(
                EXPECTED_MODEL_CANDIDATES
            ),

        "fitted_candidate_count":
            len(
                fitted_models
            ),

        "fitted_candidate_names":
            list(
                fitted_models.keys()
            ),

        "candidate_set_complete":
            fitted_model_names
            == expected_models,

        "train_prediction_set_complete":
            train_prediction_models
            == expected_models,

        "validation_prediction_set_complete":
            validation_prediction_models
            == expected_models,

        "all_models_fitted":
            all_models_fitted,

        "train_prediction_lengths_correct":
            train_prediction_lengths_correct,

        "validation_prediction_lengths_correct":
            validation_prediction_lengths_correct,

        "train_probabilities_finite":
            train_probabilities_finite,

        "validation_probabilities_finite":
            validation_probabilities_finite,

        "train_probabilities_in_range":
            train_probabilities_in_range,

        "validation_probabilities_in_range":
            validation_probabilities_in_range,

        "training_registry_complete":
            training_registry_complete,

        "xgboost_input_adapter_applied":
            training_bundle[
                "xgboost_input_adapter_applied"
            ],

        "xgboost_adapter_recorded":
            xgboost_adapter_recorded,

        "non_xgboost_dataframe_recorded":
            non_xgboost_dataframe_recorded,

        "d7_schema_modified":
            training_bundle[
                "d7_schema_modified"
            ],

        "fit_partition":
            training_bundle[
                "fit_partition"
            ],

        "validation_used_for_fit":
            training_bundle[
                "validation_used_for_fit"
            ],

        "locked_test_accessed":
            training_bundle[
                "locked_test_accessed"
            ],

        "clinical_threshold_selected":
            training_bundle[
                "clinical_threshold_selected"
            ],
    }

    # ============================================================
# D8.16A — FINAL CANDIDATE-TRAINING GATE
# ============================================================

    passed = all(
        [
            checks[
                "fitted_candidate_count"
            ]
            == 4,

            bool(
                checks[
                    "candidate_set_complete"
                ]
            ),

            bool(
                checks[
                    "train_prediction_set_complete"
                ]
            ),

            bool(
                checks[
                    "validation_prediction_set_complete"
                ]
            ),

            bool(
                checks[
                    "all_models_fitted"
                ]
            ),

            bool(
                checks[
                    "train_prediction_lengths_correct"
                ]
            ),

            bool(
                checks[
                    "validation_prediction_lengths_correct"
                ]
            ),

            bool(
                checks[
                    "train_probabilities_finite"
                ]
            ),

            bool(
                checks[
                    "validation_probabilities_finite"
                ]
            ),

            bool(
                checks[
                    "train_probabilities_in_range"
                ]
            ),

            bool(
                checks[
                    "validation_probabilities_in_range"
                ]
            ),

            bool(
                checks[
                    "training_registry_complete"
                ]
            ),

            bool(
                checks[
                    "xgboost_input_adapter_applied"
                ]
            ),

            bool(
                checks[
                    "xgboost_adapter_recorded"
                ]
            ),

            bool(
                checks[
                    "non_xgboost_dataframe_recorded"
                ]
            ),

            checks[
                "d7_schema_modified"
            ]
            is False,

            checks[
                "fit_partition"
            ]
            == "train",

            checks[
                "validation_used_for_fit"
            ]
            is False,

            checks[
                "locked_test_accessed"
            ]
            is False,

            checks[
                "clinical_threshold_selected"
            ]
            is False,
        ]
    )

    checks[
        "validation_status"
    ] = (
        "PASS"
        if passed
        else "FAIL"
    )

    return checks

# ============================================================
# D8.17 — GOVERNED MODEL DISCRIMINATION EVALUATION
# ============================================================

def evaluate_d8_candidate_discrimination(
    training_bundle: dict[str, Any] | None = None,
) -> pd.DataFrame:
    """
    Evaluate threshold-independent discrimination performance
    for every governed D8 candidate model.

    PRIMARY METRIC:
        VALIDATION PR-AUC / Average Precision.

    SECONDARY METRIC:
        VALIDATION ROC-AUC.

    TRAIN metrics are retained as generalization evidence.

    This function does NOT:
    - access the locked test partition;
    - optimize a classification threshold;
    - select a clinical operating point;
    - authorize deployment.
    """

    if training_bundle is None:
        training_bundle = (
            fit_d8_candidate_models()
        )

    training_validation = (
        validate_d8_candidate_model_training(
            training_bundle
        )
    )

    if (
        training_validation[
            "validation_status"
        ]
        != "PASS"
    ):
        raise RuntimeError(
            "D8 discrimination evaluation blocked because "
            "candidate-model training validation did not pass."
        )

    y_train = np.asarray(
        training_bundle[
            "y_train"
        ]
    )

    y_validation = np.asarray(
        training_bundle[
            "y_validation"
        ]
    )

    train_probabilities = (
        training_bundle[
            "train_probabilities"
        ]
    )

    validation_probabilities = (
        training_bundle[
            "validation_probabilities"
        ]
    )

    records = []

    for model_name in EXPECTED_MODEL_CANDIDATES:

        train_probability = np.asarray(
            train_probabilities[
                model_name
            ]
        )

        validation_probability = np.asarray(
            validation_probabilities[
                model_name
            ]
        )

        # ----------------------------------------------------
        # THRESHOLD-INDEPENDENT TRAIN METRICS
        # ----------------------------------------------------

        train_pr_auc = float(
            average_precision_score(
                y_train,
                train_probability,
            )
        )

        train_roc_auc = float(
            roc_auc_score(
                y_train,
                train_probability,
            )
        )

        # ----------------------------------------------------
        # THRESHOLD-INDEPENDENT VALIDATION METRICS
        # ----------------------------------------------------

        validation_pr_auc = float(
            average_precision_score(
                y_validation,
                validation_probability,
            )
        )

        validation_roc_auc = float(
            roc_auc_score(
                y_validation,
                validation_probability,
            )
        )

        # ----------------------------------------------------
        # GENERALIZATION GAPS
        # Positive value means TRAIN > VALIDATION.
        # ----------------------------------------------------

        pr_auc_generalization_gap = float(
            train_pr_auc
            - validation_pr_auc
        )

        roc_auc_generalization_gap = float(
            train_roc_auc
            - validation_roc_auc
        )

        records.append(
            {
                "model_name":
                    model_name,

                "model_role":
                    MODEL_ROLES[
                        model_name
                    ],

                "train_pr_auc":
                    train_pr_auc,

                "validation_pr_auc":
                    validation_pr_auc,

                "pr_auc_generalization_gap":
                    pr_auc_generalization_gap,

                "train_roc_auc":
                    train_roc_auc,

                "validation_roc_auc":
                    validation_roc_auc,

                "roc_auc_generalization_gap":
                    roc_auc_generalization_gap,

                "primary_selection_metric":
                    (
                        PRIMARY_SELECTION_METRIC
                    ),

                "locked_test_accessed":
                    False,

                "clinical_threshold_selected":
                    False,
            }
        )

    performance_table = (
        pd.DataFrame(
            records
        )
    )

    return performance_table


# ============================================================
# D8.18 — VALIDATE MODEL DISCRIMINATION EVIDENCE
# ============================================================

def validate_d8_candidate_discrimination(
    performance_table: pd.DataFrame | None = None,
) -> dict[str, Any]:
    """
    Validate the D8 candidate-model discrimination evidence
    before any governed model-selection decision is permitted.
    """

    if performance_table is None:
        performance_table = (
            evaluate_d8_candidate_discrimination()
        )

    required_columns = {
        "model_name",
        "model_role",
        "train_pr_auc",
        "validation_pr_auc",
        "pr_auc_generalization_gap",
        "train_roc_auc",
        "validation_roc_auc",
        "roc_auc_generalization_gap",
        "primary_selection_metric",
        "locked_test_accessed",
        "clinical_threshold_selected",
    }

    required_columns_present = (
        required_columns
        .issubset(
            performance_table.columns
        )
    )

    candidate_set_complete = (
        set(
            performance_table[
                "model_name"
            ].tolist()
        )
        == set(
            EXPECTED_MODEL_CANDIDATES
        )
    )

    candidate_rows_unique = (
        performance_table[
            "model_name"
        ]
        .is_unique
    )

    metric_columns = [
        "train_pr_auc",
        "validation_pr_auc",
        "pr_auc_generalization_gap",
        "train_roc_auc",
        "validation_roc_auc",
        "roc_auc_generalization_gap",
    ]

    metric_values_finite = bool(
        np.isfinite(
            performance_table[
                metric_columns
            ].to_numpy(
                dtype=float
            )
        ).all()
    )

    bounded_metric_columns = [
        "train_pr_auc",
        "validation_pr_auc",
        "train_roc_auc",
        "validation_roc_auc",
    ]

    bounded_metrics_valid = bool(
        (
            performance_table[
                bounded_metric_columns
            ]
            .ge(0.0)
            .all()
            .all()
        )

        and

        (
            performance_table[
                bounded_metric_columns
            ]
            .le(1.0)
            .all()
            .all()
        )
    )

    generalization_gap_math_correct = bool(
        np.allclose(
            performance_table[
                "pr_auc_generalization_gap"
            ].to_numpy(
                dtype=float
            ),

            (
                performance_table[
                    "train_pr_auc"
                ]
                -
                performance_table[
                    "validation_pr_auc"
                ]
            ).to_numpy(
                dtype=float
            ),
        )

        and

        np.allclose(
            performance_table[
                "roc_auc_generalization_gap"
            ].to_numpy(
                dtype=float
            ),

            (
                performance_table[
                    "train_roc_auc"
                ]
                -
                performance_table[
                    "validation_roc_auc"
                ]
            ).to_numpy(
                dtype=float
            ),
        )
    )

    primary_metric_correct = bool(
        performance_table[
            "primary_selection_metric"
        ]
        .eq(
            PRIMARY_SELECTION_METRIC
        )
        .all()
    )

    locked_test_untouched = bool(
        performance_table[
            "locked_test_accessed"
        ]
        .eq(False)
        .all()
    )

    threshold_not_selected = bool(
        performance_table[
            "clinical_threshold_selected"
        ]
        .eq(False)
        .all()
    )

    checks = {
        "candidate_row_count":
            int(
                len(
                    performance_table
                )
            ),

        "required_columns_present":
            required_columns_present,

        "candidate_set_complete":
            candidate_set_complete,

        "candidate_rows_unique":
            bool(
                candidate_rows_unique
            ),

        "metric_values_finite":
            metric_values_finite,

        "bounded_metrics_valid":
            bounded_metrics_valid,

        "generalization_gap_math_correct":
            generalization_gap_math_correct,

        "primary_selection_metric":
            PRIMARY_SELECTION_METRIC,

        "primary_metric_correct":
            primary_metric_correct,

        "locked_test_accessed":
            not locked_test_untouched,

        "clinical_threshold_selected":
            not threshold_not_selected,
    }

    passed = all(
        [
            checks[
                "candidate_row_count"
            ]
            == 4,

            bool(
                checks[
                    "required_columns_present"
                ]
            ),

            bool(
                checks[
                    "candidate_set_complete"
                ]
            ),

            bool(
                checks[
                    "candidate_rows_unique"
                ]
            ),

            bool(
                checks[
                    "metric_values_finite"
                ]
            ),

            bool(
                checks[
                    "bounded_metrics_valid"
                ]
            ),

            bool(
                checks[
                    "generalization_gap_math_correct"
                ]
            ),

            bool(
                checks[
                    "primary_metric_correct"
                ]
            ),

            checks[
                "locked_test_accessed"
            ]
            is False,

            checks[
                "clinical_threshold_selected"
            ]
            is False,
        ]
    )

    checks[
        "validation_status"
    ] = (
        "PASS"
        if passed
        else "FAIL"
    )

    return checks

# ============================================================
# D8.19 — TRAIN-ONLY HYPERPARAMETER OPTIMIZATION CONTRACT
# ============================================================

TUNABLE_MODEL_CANDIDATES = (
    MODEL_LOGISTIC,
    MODEL_RANDOM_FOREST,
    MODEL_XGBOOST,
)

D8_TUNING_PARTITION = "train"

D8_TUNING_PRIMARY_METRIC = "average_precision"

D8_TUNING_CV_FOLDS = 5

D8_TUNING_VALIDATION_ACCESS_PERMITTED = False

D8_TUNING_LOCKED_TEST_ACCESS_PERMITTED = False

D8_TUNING_CLINICAL_THRESHOLD_SELECTION_PERMITTED = False


@dataclass(frozen=True)
class HyperparameterOptimizationContract:
    """
    Immutable governance contract for D8 hyperparameter
    optimization.

    Hyperparameter search is restricted to TRAIN.

    VALIDATION is reserved for post-tuning candidate-model
    comparison.

    LOCKED TEST remains inaccessible.
    """

    stage: str = D8_STAGE

    tuning_partition: str = (
        D8_TUNING_PARTITION
    )

    tunable_models: tuple[str, ...] = (
        TUNABLE_MODEL_CANDIDATES
    )

    primary_metric: str = (
        D8_TUNING_PRIMARY_METRIC
    )

    cv_folds: int = (
        D8_TUNING_CV_FOLDS
    )

    validation_access_permitted: bool = (
        D8_TUNING_VALIDATION_ACCESS_PERMITTED
    )

    locked_test_access_permitted: bool = (
        D8_TUNING_LOCKED_TEST_ACCESS_PERMITTED
    )

    clinical_threshold_selection_permitted: bool = (
        D8_TUNING_CLINICAL_THRESHOLD_SELECTION_PERMITTED
    )


D8_HYPERPARAMETER_OPTIMIZATION_CONTRACT = (
    HyperparameterOptimizationContract()
)


# ============================================================
# D8.20 — GOVERNED HYPERPARAMETER SEARCH SPACES
# ============================================================

D8_HYPERPARAMETER_SEARCH_SPACES = {

    MODEL_LOGISTIC: {
        "C": [
            0.01,
            0.1,
            1.0,
            10.0,
        ],

        "class_weight": [
            None,
            "balanced",
        ],
    },

    MODEL_RANDOM_FOREST: {
        "n_estimators": [
            300,
            500,
        ],

        "max_depth": [
            8,
            12,
            None,
        ],

        "min_samples_leaf": [
            1,
            5,
            10,
        ],

        "class_weight": [
            None,
            "balanced",
        ],
    },

    MODEL_XGBOOST: {
        "n_estimators": [
            200,
            300,
            500,
        ],

        "max_depth": [
            3,
            4,
            6,
        ],

        "learning_rate": [
            0.03,
            0.05,
            0.1,
        ],

        "subsample": [
            0.8,
            1.0,
        ],

        "colsample_bytree": [
            0.8,
            1.0,
        ],
    },
}


# ============================================================
# D8.21 — VALIDATE HYPERPARAMETER OPTIMIZATION CONTRACT
# ============================================================

def validate_d8_hyperparameter_optimization_contract(
) -> dict[str, Any]:
    """
    Validate the governance boundary before any hyperparameter
    optimization is permitted.
    """

    contract = (
        D8_HYPERPARAMETER_OPTIMIZATION_CONTRACT
    )

    tunable_models_unique = (
        len(
            contract.tunable_models
        )
        == len(
            set(
                contract.tunable_models
            )
        )
    )

    dummy_excluded_from_tuning = (
        MODEL_DUMMY
        not in contract.tunable_models
    )

    tunable_model_set_correct = (
        set(
            contract.tunable_models
        )
        == {
            MODEL_LOGISTIC,
            MODEL_RANDOM_FOREST,
            MODEL_XGBOOST,
        }
    )

    search_spaces_complete = (
        set(
            D8_HYPERPARAMETER_SEARCH_SPACES
        )
        == set(
            contract.tunable_models
        )
    )

    search_spaces_nonempty = all(
        bool(
            search_space
        )

        for search_space
        in D8_HYPERPARAMETER_SEARCH_SPACES.values()
    )

    parameter_values_nonempty = all(
        len(
            values
        )
        > 0

        for search_space
        in D8_HYPERPARAMETER_SEARCH_SPACES.values()

        for values
        in search_space.values()
    )

    checks = {
        "stage":
            contract.stage,

        "tuning_partition":
            contract.tuning_partition,

        "tunable_model_count":
            len(
                contract.tunable_models
            ),

        "tunable_models":
            list(
                contract.tunable_models
            ),

        "tunable_models_unique":
            tunable_models_unique,

        "dummy_excluded_from_tuning":
            dummy_excluded_from_tuning,

        "tunable_model_set_correct":
            tunable_model_set_correct,

        "search_spaces_complete":
            search_spaces_complete,

        "search_spaces_nonempty":
            search_spaces_nonempty,

        "parameter_values_nonempty":
            parameter_values_nonempty,

        "primary_metric":
            contract.primary_metric,

        "cv_folds":
            contract.cv_folds,

        "validation_access_permitted":
            contract.validation_access_permitted,

        "locked_test_access_permitted":
            contract.locked_test_access_permitted,

        "clinical_threshold_selection_permitted":
            contract.clinical_threshold_selection_permitted,
    }

    passed = all(
        [
            checks[
                "stage"
            ]
            == "D8",

            checks[
                "tuning_partition"
            ]
            == "train",

            checks[
                "tunable_model_count"
            ]
            == 3,

            bool(
                checks[
                    "tunable_models_unique"
                ]
            ),

            bool(
                checks[
                    "dummy_excluded_from_tuning"
                ]
            ),

            bool(
                checks[
                    "tunable_model_set_correct"
                ]
            ),

            bool(
                checks[
                    "search_spaces_complete"
                ]
            ),

            bool(
                checks[
                    "search_spaces_nonempty"
                ]
            ),

            bool(
                checks[
                    "parameter_values_nonempty"
                ]
            ),

            checks[
                "primary_metric"
            ]
            == "average_precision",

            checks[
                "cv_folds"
            ]
            == 5,

            checks[
                "validation_access_permitted"
            ]
            is False,

            checks[
                "locked_test_access_permitted"
            ]
            is False,

            checks[
                "clinical_threshold_selection_permitted"
            ]
            is False,
        ]
    )

    checks[
        "validation_status"
    ] = (
        "PASS"
        if passed
        else "FAIL"
    )

    return checks

# ============================================================
# D8.22 — AUTHORITATIVE TRAIN PATIENT-GROUP RECOVERY
# ============================================================

D8_DEVELOPMENT_ENGINEERED_PATH = Path(
    "data/interim/D6_development_engineered.parquet"
)

D8_GROUP_IDENTIFIER = "patient_nbr"

D8_SPLIT_COLUMN = "split"

D8_TRAIN_SPLIT_LABEL = "train"


def build_d8_train_patient_groups(
    matrices: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Recover authoritative patient-group identifiers for the
    frozen D8 TRAIN matrix.

    Source:
        D6 development-only engineered artifact.

    Purpose:
        Support patient-disjoint cross-validation entirely
        within TRAIN.

    Governance:
        - VALIDATION is not used for CV fitting/tuning.
        - LOCKED TEST is not present in the D6 development
          artifact and is not accessed.
        - patient_nbr is used only as a grouping identifier.
        - patient_nbr is never supplied as a model feature.
    """

    if matrices is None:
        matrices = (
            build_d8_model_development_matrices()
        )

    if not D8_DEVELOPMENT_ENGINEERED_PATH.exists():
        raise FileNotFoundError(
            "Authoritative D6 development artifact not found: "
            f"{D8_DEVELOPMENT_ENGINEERED_PATH}"
        )

    development_df = pd.read_parquet(
        D8_DEVELOPMENT_ENGINEERED_PATH
    )

    required_columns = {
        "encounter_id",
        D8_GROUP_IDENTIFIER,
        D8_TARGET,
        D8_SPLIT_COLUMN,
    }

    missing_columns = (
        required_columns
        - set(
            development_df.columns
        )
    )

    if missing_columns:
        raise RuntimeError(
            "D8 group recovery blocked because required D6 "
            f"columns are missing: {sorted(missing_columns)}"
        )

    train_governance = (
        development_df.loc[
            development_df[
                D8_SPLIT_COLUMN
            ]
            == D8_TRAIN_SPLIT_LABEL,
            [
                "encounter_id",
                D8_GROUP_IDENTIFIER,
                D8_TARGET,
                D8_SPLIT_COLUMN,
            ],
        ]
        .copy()
        .reset_index(
            drop=True
        )
    )

    if len(
        train_governance
    ) != len(
        matrices[
            "X_train"
        ]
    ):
        raise RuntimeError(
            "D8 TRAIN patient-group recovery does not align "
            "with the frozen D7 TRAIN encounter count."
        )

    recovered_target = (
        train_governance[
            D8_TARGET
        ]
        .to_numpy()
    )

    governed_target = np.asarray(
        matrices[
            "y_train"
        ]
    )

    if not np.array_equal(
        recovered_target,
        governed_target,
    ):
        raise RuntimeError(
            "D8 TRAIN patient-group recovery target order "
            "does not align with the frozen D7 TRAIN target."
        )

    groups = (
        train_governance[
            D8_GROUP_IDENTIFIER
        ]
        .to_numpy()
    )

    return {
        "train_governance":
            train_governance,

        "groups":
            groups,

        "encounter_ids":
            train_governance[
                "encounter_id"
            ]
            .to_numpy(),

        "y_train":
            governed_target.copy(),

        "group_identifier":
            D8_GROUP_IDENTIFIER,

        "split_column":
            D8_SPLIT_COLUMN,

        "split_label":
            D8_TRAIN_SPLIT_LABEL,

        "validation_used":
            False,

        "locked_test_accessed":
            False,

        "patient_identifier_used_as_feature":
            False,
    }


# ============================================================
# D8.23 — BUILD PATIENT-DISJOINT TRAIN CV FOLDS
# ============================================================

def build_d8_group_aware_cv_folds(
    matrices: dict[str, Any] | None = None,
    group_bundle: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Build deterministic 5-fold stratified group cross-validation
    entirely within TRAIN.

    Stratification:
        readmitted_30d

    Group:
        patient_nbr

    Requirement:
        No patient may appear in both the CV-training and
        CV-validation portion of the same fold.
    """

    if matrices is None:
        matrices = (
            build_d8_model_development_matrices()
        )

    if group_bundle is None:
        group_bundle = (
            build_d8_train_patient_groups(
                matrices
            )
        )

    X_train = matrices[
        "X_train"
    ]

    y_train = np.asarray(
        matrices[
            "y_train"
        ]
    )

    groups = np.asarray(
        group_bundle[
            "groups"
        ]
    )

    splitter = StratifiedGroupKFold(
        n_splits=D8_TUNING_CV_FOLDS,
        shuffle=True,
        random_state=D8_RANDOM_STATE,
    )

    cv_splits = []

    fold_records = []

    for fold_number, (
        cv_train_index,
        cv_validation_index,
    ) in enumerate(
        splitter.split(
            X_train,
            y_train,
            groups,
        ),
        start=1,
    ):

        cv_train_groups = set(
            groups[
                cv_train_index
            ].tolist()
        )

        cv_validation_groups = set(
            groups[
                cv_validation_index
            ].tolist()
        )

        patient_overlap = (
            cv_train_groups
            & cv_validation_groups
        )

        cv_train_y = (
            y_train[
                cv_train_index
            ]
        )

        cv_validation_y = (
            y_train[
                cv_validation_index
            ]
        )

        cv_splits.append(
            (
                cv_train_index,
                cv_validation_index,
            )
        )

        fold_records.append(
            {
                "fold":
                    fold_number,

                "cv_train_encounters":
                    int(
                        len(
                            cv_train_index
                        )
                    ),

                "cv_validation_encounters":
                    int(
                        len(
                            cv_validation_index
                        )
                    ),

                "cv_train_patients":
                    int(
                        len(
                            cv_train_groups
                        )
                    ),

                "cv_validation_patients":
                    int(
                        len(
                            cv_validation_groups
                        )
                    ),

                "patient_overlap_count":
                    int(
                        len(
                            patient_overlap
                        )
                    ),

                "cv_train_positive_count":
                    int(
                        cv_train_y.sum()
                    ),

                "cv_validation_positive_count":
                    int(
                        cv_validation_y.sum()
                    ),

                "cv_train_prevalence":
                    float(
                        cv_train_y.mean()
                    ),

                "cv_validation_prevalence":
                    float(
                        cv_validation_y.mean()
                    ),
            }
        )

    fold_summary = pd.DataFrame(
        fold_records
    )

    return {
        "cv_splits":
            cv_splits,

        "fold_summary":
            fold_summary,

        "groups":
            groups,

        "n_splits":
            D8_TUNING_CV_FOLDS,

        "random_state":
            D8_RANDOM_STATE,

        "shuffle":
            True,

        "stratification_target":
            D8_TARGET,

        "group_identifier":
            D8_GROUP_IDENTIFIER,

        "source_partition":
            "train",

        "validation_used_for_cv":
            False,

        "locked_test_accessed":
            False,

        "patient_identifier_used_as_feature":
            False,
    }


# ============================================================
# D8.24 — VALIDATE PATIENT-DISJOINT TRAIN CV
# ============================================================

def validate_d8_group_aware_cv_folds(
    cv_bundle: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Validate the TRAIN-only group-aware CV structure before
    hyperparameter optimization is permitted.
    """

    if cv_bundle is None:
        cv_bundle = (
            build_d8_group_aware_cv_folds()
        )

    cv_splits = (
        cv_bundle[
            "cv_splits"
        ]
    )

    fold_summary = (
        cv_bundle[
            "fold_summary"
        ]
    )

    groups = np.asarray(
        cv_bundle[
            "groups"
        ]
    )

    fold_count_correct = (
        len(
            cv_splits
        )
        == D8_TUNING_CV_FOLDS
    )

    all_patient_overlaps_zero = bool(
        fold_summary[
            "patient_overlap_count"
        ]
        .eq(0)
        .all()
    )

    all_folds_have_positive_cases = bool(
        (
            fold_summary[
                "cv_train_positive_count"
            ]
            > 0
        )
        .all()

        and

        (
            fold_summary[
                "cv_validation_positive_count"
            ]
            > 0
        )
        .all()
    )

    all_folds_nonempty = bool(
        (
            fold_summary[
                "cv_train_encounters"
            ]
            > 0
        )
        .all()

        and

        (
            fold_summary[
                "cv_validation_encounters"
            ]
            > 0
        )
        .all()
    )

    every_encounter_validated_once = (
        np.zeros(
            len(groups),
            dtype=int,
        )
    )

    indices_in_range = True

    train_validation_index_overlap_zero = True

    for (
        cv_train_index,
        cv_validation_index,
    ) in cv_splits:

        if (
            cv_train_index.min() < 0
            or cv_validation_index.min() < 0
            or cv_train_index.max() >= len(groups)
            or cv_validation_index.max() >= len(groups)
        ):
            indices_in_range = False

        if np.intersect1d(
            cv_train_index,
            cv_validation_index,
        ).size != 0:
            train_validation_index_overlap_zero = False

        every_encounter_validated_once[
            cv_validation_index
        ] += 1

    every_encounter_validated_once_check = bool(
        np.all(
            every_encounter_validated_once
            == 1
        )
    )

    unique_train_patients = int(
        pd.Series(
            groups
        )
        .nunique()
    )

    checks = {
        "cv_method":
            "StratifiedGroupKFold",

        "cv_fold_count":
            len(
                cv_splits
            ),

        "expected_cv_fold_count":
            D8_TUNING_CV_FOLDS,

        "fold_count_correct":
            fold_count_correct,

        "train_encounter_count":
            int(
                len(
                    groups
                )
            ),

        "unique_train_patients":
            unique_train_patients,

        "all_patient_overlaps_zero":
            all_patient_overlaps_zero,

        "all_folds_have_positive_cases":
            all_folds_have_positive_cases,

        "all_folds_nonempty":
            all_folds_nonempty,

        "indices_in_range":
            bool(
                indices_in_range
            ),

        "train_validation_index_overlap_zero":
            bool(
                train_validation_index_overlap_zero
            ),

        "every_encounter_validated_once":
            every_encounter_validated_once_check,

        "source_partition":
            cv_bundle[
                "source_partition"
            ],

        "validation_used_for_cv":
            cv_bundle[
                "validation_used_for_cv"
            ],

        "locked_test_accessed":
            cv_bundle[
                "locked_test_accessed"
            ],

        "patient_identifier_used_as_feature":
            cv_bundle[
                "patient_identifier_used_as_feature"
            ],
    }

    passed = all(
        [
            bool(
                checks[
                    "fold_count_correct"
                ]
            ),

            checks[
                "train_encounter_count"
            ]
            == EXPECTED_D7_TRAIN_ENCOUNTERS,

            checks[
                "unique_train_patients"
            ]
            > 0,

            bool(
                checks[
                    "all_patient_overlaps_zero"
                ]
            ),

            bool(
                checks[
                    "all_folds_have_positive_cases"
                ]
            ),

            bool(
                checks[
                    "all_folds_nonempty"
                ]
            ),

            bool(
                checks[
                    "indices_in_range"
                ]
            ),

            bool(
                checks[
                    "train_validation_index_overlap_zero"
                ]
            ),

            bool(
                checks[
                    "every_encounter_validated_once"
                ]
            ),

            checks[
                "source_partition"
            ]
            == "train",

            checks[
                "validation_used_for_cv"
            ]
            is False,

            checks[
                "locked_test_accessed"
            ]
            is False,

            checks[
                "patient_identifier_used_as_feature"
            ]
            is False,
        ]
    )

    checks[
        "validation_status"
    ] = (
        "PASS"
        if passed
        else "FAIL"
    )

    return checks

# ============================================================
# D8.25 — GOVERNED TRAIN-ONLY HYPERPARAMETER OPTIMIZATION
# ============================================================

D8_RANDOM_FOREST_SEARCH_ITERATIONS = 18
D8_XGBOOST_SEARCH_ITERATIONS = 24


def tune_d8_candidate_models(
    matrices: dict[str, Any] | None = None,
    cv_bundle: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Tune predictive D8 candidate models exclusively within TRAIN.

    Logistic Regression:
        Exhaustive GridSearchCV.

    Random Forest:
        RandomizedSearchCV.

    XGBoost:
        RandomizedSearchCV.

    Primary optimization metric:
        Average Precision / PR-AUC.

    Governance:
        - Uses only frozen TRAIN matrix.
        - Uses patient-disjoint TRAIN CV folds.
        - External VALIDATION does not participate in tuning.
        - LOCKED TEST remains inaccessible.
        - No clinical threshold is selected.
    """

    contract_validation = (
        validate_d8_hyperparameter_optimization_contract()
    )

    if contract_validation["validation_status"] != "PASS":
        raise RuntimeError(
            "D8 tuning blocked because the hyperparameter "
            "optimization contract did not pass."
        )

    if matrices is None:
        matrices = build_d8_model_development_matrices()

    matrix_validation = (
        validate_d8_model_development_matrices(
            matrices
        )
    )

    if matrix_validation["validation_status"] != "PASS":
        raise RuntimeError(
            "D8 tuning blocked because model-development "
            "matrix validation did not pass."
        )

    if cv_bundle is None:
        cv_bundle = build_d8_group_aware_cv_folds(
            matrices=matrices
        )

    cv_validation = (
        validate_d8_group_aware_cv_folds(
            cv_bundle
        )
    )

    if cv_validation["validation_status"] != "PASS":
        raise RuntimeError(
            "D8 tuning blocked because patient-disjoint "
            "TRAIN CV validation did not pass."
        )

    X_train = matrices["X_train"]

    y_train = np.asarray(
        matrices["y_train"]
    )

    cv_splits = cv_bundle["cv_splits"]

    candidate_estimators = (
        build_candidate_model_factory()
    )

    best_estimators = {}
    best_parameters = {}
    best_cv_scores = {}
    search_objects = {}
    tuning_records = []

    # ========================================================
    # LOGISTIC REGRESSION — EXHAUSTIVE GRID SEARCH
    # ========================================================

    logistic_estimator = candidate_estimators[
        MODEL_LOGISTIC
    ]

    logistic_search = GridSearchCV(
        estimator=logistic_estimator,
        param_grid=(
            D8_HYPERPARAMETER_SEARCH_SPACES[
                MODEL_LOGISTIC
            ]
        ),
        scoring=D8_TUNING_PRIMARY_METRIC,
        cv=cv_splits,
        refit=True,
        n_jobs=-1,
        return_train_score=True,
        error_score="raise",
    )

    logistic_search.fit(
        X_train,
        y_train,
    )

    best_estimators[
        MODEL_LOGISTIC
    ] = logistic_search.best_estimator_

    best_parameters[
        MODEL_LOGISTIC
    ] = logistic_search.best_params_

    best_cv_scores[
        MODEL_LOGISTIC
    ] = float(
        logistic_search.best_score_
    )

    search_objects[
        MODEL_LOGISTIC
    ] = logistic_search

    tuning_records.append(
        {
            "model_name":
                MODEL_LOGISTIC,

            "search_method":
                "GridSearchCV",

            "search_iterations":
                int(
                    len(
                        logistic_search.cv_results_[
                            "params"
                        ]
                    )
                ),

            "cv_folds":
                D8_TUNING_CV_FOLDS,

            "primary_metric":
                D8_TUNING_PRIMARY_METRIC,

            "best_cv_pr_auc":
                float(
                    logistic_search.best_score_
                ),

            "best_parameters":
                str(
                    logistic_search.best_params_
                ),

            "fit_partition":
                "train",

            "external_validation_used_for_tuning":
                False,

            "locked_test_accessed":
                False,

            "clinical_threshold_selected":
                False,
        }
    )

    # ========================================================
    # RANDOM FOREST — RANDOMIZED SEARCH
    # ========================================================

    random_forest_estimator = (
        candidate_estimators[
            MODEL_RANDOM_FOREST
        ]
    )

    random_forest_search = RandomizedSearchCV(
        estimator=random_forest_estimator,
        param_distributions=(
            D8_HYPERPARAMETER_SEARCH_SPACES[
                MODEL_RANDOM_FOREST
            ]
        ),
        n_iter=D8_RANDOM_FOREST_SEARCH_ITERATIONS,
        scoring=D8_TUNING_PRIMARY_METRIC,
        cv=cv_splits,
        refit=True,
        random_state=D8_RANDOM_STATE,
        n_jobs=-1,
        return_train_score=True,
        error_score="raise",
    )

    random_forest_search.fit(
        X_train,
        y_train,
    )

    best_estimators[
        MODEL_RANDOM_FOREST
    ] = (
        random_forest_search.best_estimator_
    )

    best_parameters[
        MODEL_RANDOM_FOREST
    ] = (
        random_forest_search.best_params_
    )

    best_cv_scores[
        MODEL_RANDOM_FOREST
    ] = float(
        random_forest_search.best_score_
    )

    search_objects[
        MODEL_RANDOM_FOREST
    ] = random_forest_search

    tuning_records.append(
        {
            "model_name":
                MODEL_RANDOM_FOREST,

            "search_method":
                "RandomizedSearchCV",

            "search_iterations":
                int(
                    len(
                        random_forest_search.cv_results_[
                            "params"
                        ]
                    )
                ),

            "cv_folds":
                D8_TUNING_CV_FOLDS,

            "primary_metric":
                D8_TUNING_PRIMARY_METRIC,

            "best_cv_pr_auc":
                float(
                    random_forest_search.best_score_
                ),

            "best_parameters":
                str(
                    random_forest_search.best_params_
                ),

            "fit_partition":
                "train",

            "external_validation_used_for_tuning":
                False,

            "locked_test_accessed":
                False,

            "clinical_threshold_selected":
                False,
        }
    )

    # ========================================================
    # XGBOOST — RANDOMIZED SEARCH
    # ========================================================

    xgboost_estimator = candidate_estimators[
        MODEL_XGBOOST
    ]

    X_train_xgboost = prepare_model_input(
        MODEL_XGBOOST,
        X_train,
    )

    xgboost_search = RandomizedSearchCV(
        estimator=xgboost_estimator,
        param_distributions=(
            D8_HYPERPARAMETER_SEARCH_SPACES[
                MODEL_XGBOOST
            ]
        ),
        n_iter=D8_XGBOOST_SEARCH_ITERATIONS,
        scoring=D8_TUNING_PRIMARY_METRIC,
        cv=cv_splits,
        refit=True,
        random_state=D8_RANDOM_STATE,
        n_jobs=-1,
        return_train_score=True,
        error_score="raise",
    )

    xgboost_search.fit(
        X_train_xgboost,
        y_train,
    )

    best_estimators[
        MODEL_XGBOOST
    ] = (
        xgboost_search.best_estimator_
    )

    best_parameters[
        MODEL_XGBOOST
    ] = (
        xgboost_search.best_params_
    )

    best_cv_scores[
        MODEL_XGBOOST
    ] = float(
        xgboost_search.best_score_
    )

    search_objects[
        MODEL_XGBOOST
    ] = xgboost_search

    tuning_records.append(
        {
            "model_name":
                MODEL_XGBOOST,

            "search_method":
                "RandomizedSearchCV",

            "search_iterations":
                int(
                    len(
                        xgboost_search.cv_results_[
                            "params"
                        ]
                    )
                ),

            "cv_folds":
                D8_TUNING_CV_FOLDS,

            "primary_metric":
                D8_TUNING_PRIMARY_METRIC,

            "best_cv_pr_auc":
                float(
                    xgboost_search.best_score_
                ),

            "best_parameters":
                str(
                    xgboost_search.best_params_
                ),

            "fit_partition":
                "train",

            "external_validation_used_for_tuning":
                False,

            "locked_test_accessed":
                False,

            "clinical_threshold_selected":
                False,
        }
    )

    tuning_summary = pd.DataFrame(
        tuning_records
    )

    return {
        "best_estimators":
            best_estimators,

        "best_parameters":
            best_parameters,

        "best_cv_scores":
            best_cv_scores,

        "search_objects":
            search_objects,

        "tuning_summary":
            tuning_summary,

        "fit_partition":
            "train",

        "cv_method":
            "StratifiedGroupKFold",

        "primary_metric":
            D8_TUNING_PRIMARY_METRIC,

        "external_validation_used_for_tuning":
            False,

        "locked_test_accessed":
            False,

        "clinical_threshold_selected":
            False,
    }


# ============================================================
# D8.26 — VALIDATE HYPERPARAMETER OPTIMIZATION RESULTS
# ============================================================

def validate_d8_hyperparameter_optimization(
    tuning_bundle: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Validate governed TRAIN-only hyperparameter optimization.
    """

    if tuning_bundle is None:
        tuning_bundle = tune_d8_candidate_models()

    expected_models = set(
        TUNABLE_MODEL_CANDIDATES
    )

    best_estimators = tuning_bundle[
        "best_estimators"
    ]

    best_parameters = tuning_bundle[
        "best_parameters"
    ]

    best_cv_scores = tuning_bundle[
        "best_cv_scores"
    ]

    tuning_summary = tuning_bundle[
        "tuning_summary"
    ]

    tuned_model_set_complete = (
        set(best_estimators)
        == expected_models
    )

    best_parameter_set_complete = (
        set(best_parameters)
        == expected_models
    )

    best_score_set_complete = (
        set(best_cv_scores)
        == expected_models
    )

    all_best_estimators_fitted = all(
        hasattr(
            estimator,
            "classes_",
        )
        for estimator
        in best_estimators.values()
    )

    cv_scores_finite = bool(
        np.isfinite(
            np.asarray(
                list(
                    best_cv_scores.values()
                ),
                dtype=float,
            )
        ).all()
    )

    cv_scores_in_range = bool(
        all(
            0.0 <= float(score) <= 1.0
            for score
            in best_cv_scores.values()
        )
    )

    summary_model_set_complete = (
        set(
            tuning_summary[
                "model_name"
            ].tolist()
        )
        == expected_models
    )

    summary_rows_unique = bool(
        tuning_summary[
            "model_name"
        ].is_unique
    )

    no_external_validation_tuning = bool(
        tuning_summary[
            "external_validation_used_for_tuning"
        ]
        .eq(False)
        .all()
    )

    no_locked_test_access = bool(
        tuning_summary[
            "locked_test_accessed"
        ]
        .eq(False)
        .all()
    )

    no_threshold_selection = bool(
        tuning_summary[
            "clinical_threshold_selected"
        ]
        .eq(False)
        .all()
    )

    checks = {
        "expected_tuned_model_count":
            3,

        "tuned_model_count":
            len(
                best_estimators
            ),

        "tuned_models":
            list(
                best_estimators.keys()
            ),

        "tuned_model_set_complete":
            tuned_model_set_complete,

        "best_parameter_set_complete":
            best_parameter_set_complete,

        "best_score_set_complete":
            best_score_set_complete,

        "all_best_estimators_fitted":
            all_best_estimators_fitted,

        "cv_scores_finite":
            cv_scores_finite,

        "cv_scores_in_range":
            cv_scores_in_range,

        "summary_model_set_complete":
            summary_model_set_complete,

        "summary_rows_unique":
            summary_rows_unique,

        "fit_partition":
            tuning_bundle[
                "fit_partition"
            ],

        "cv_method":
            tuning_bundle[
                "cv_method"
            ],

        "primary_metric":
            tuning_bundle[
                "primary_metric"
            ],

        "external_validation_used_for_tuning":
            not no_external_validation_tuning,

        "locked_test_accessed":
            not no_locked_test_access,

        "clinical_threshold_selected":
            not no_threshold_selection,
    }

    passed = all(
        [
            checks["tuned_model_count"] == 3,
            bool(checks["tuned_model_set_complete"]),
            bool(checks["best_parameter_set_complete"]),
            bool(checks["best_score_set_complete"]),
            bool(checks["all_best_estimators_fitted"]),
            bool(checks["cv_scores_finite"]),
            bool(checks["cv_scores_in_range"]),
            bool(checks["summary_model_set_complete"]),
            bool(checks["summary_rows_unique"]),

            checks["fit_partition"] == "train",

            checks["cv_method"]
            == "StratifiedGroupKFold",

            checks["primary_metric"]
            == "average_precision",

            checks[
                "external_validation_used_for_tuning"
            ]
            is False,

            checks[
                "locked_test_accessed"
            ]
            is False,

            checks[
                "clinical_threshold_selected"
            ]
            is False,
        ]
    )

    checks["validation_status"] = (
        "PASS"
        if passed
        else "FAIL"
    )

    return checks

# ============================================================
# D8.27 — TUNED-CANDIDATE HELD-OUT VALIDATION EVALUATION
# ============================================================

def evaluate_d8_tuned_candidates_on_validation(
    tuning_bundle: dict[str, Any] | None = None,
    matrices: dict[str, Any] | None = None,
) -> pd.DataFrame:
    """
    Evaluate TRAIN-CV-tuned candidate models on the external
    held-out VALIDATION partition.

    This is the post-tuning model-comparison evaluation.

    Governance:
        - Hyperparameters were selected using TRAIN CV only.
        - VALIDATION is used only for evaluation.
        - No estimator is fitted on VALIDATION.
        - LOCKED TEST remains inaccessible.
        - No clinical threshold is selected.
    """

    if matrices is None:
        matrices = build_d8_model_development_matrices()

    matrix_validation = (
        validate_d8_model_development_matrices(
            matrices
        )
    )

    if matrix_validation["validation_status"] != "PASS":
        raise RuntimeError(
            "D8 tuned-candidate validation evaluation blocked "
            "because development-matrix validation did not pass."
        )

    if tuning_bundle is None:
        tuning_bundle = tune_d8_candidate_models(
            matrices=matrices
        )

    tuning_validation = (
        validate_d8_hyperparameter_optimization(
            tuning_bundle
        )
    )

    if tuning_validation["validation_status"] != "PASS":
        raise RuntimeError(
            "D8 tuned-candidate validation evaluation blocked "
            "because hyperparameter optimization validation "
            "did not pass."
        )

    X_train = matrices["X_train"]
    X_validation = matrices["X_validation"]

    y_train = np.asarray(
        matrices["y_train"]
    )

    y_validation = np.asarray(
        matrices["y_validation"]
    )

    best_estimators = tuning_bundle[
        "best_estimators"
    ]

    best_parameters = tuning_bundle[
        "best_parameters"
    ]

    best_cv_scores = tuning_bundle[
        "best_cv_scores"
    ]

    records = []

    for model_name in TUNABLE_MODEL_CANDIDATES:

        estimator = best_estimators[
            model_name
        ]

        X_train_model = prepare_model_input(
            model_name,
            X_train,
        )

        X_validation_model = prepare_model_input(
            model_name,
            X_validation,
        )

        # ----------------------------------------------------
        # IMPORTANT:
        # Estimator is already fitted/refitted on TRAIN by the
        # governed CV search. No .fit() occurs here.
        # ----------------------------------------------------

        train_probability = (
            estimator.predict_proba(
                X_train_model
            )[:, 1]
        )

        validation_probability = (
            estimator.predict_proba(
                X_validation_model
            )[:, 1]
        )

        train_pr_auc = float(
            average_precision_score(
                y_train,
                train_probability,
            )
        )

        validation_pr_auc = float(
            average_precision_score(
                y_validation,
                validation_probability,
            )
        )

        train_roc_auc = float(
            roc_auc_score(
                y_train,
                train_probability,
            )
        )

        validation_roc_auc = float(
            roc_auc_score(
                y_validation,
                validation_probability,
            )
        )

        records.append(
            {
                "model_name":
                    model_name,

                "model_role":
                    MODEL_ROLES[
                        model_name
                    ],

                "best_train_cv_pr_auc":
                    float(
                        best_cv_scores[
                            model_name
                        ]
                    ),

                "train_pr_auc":
                    train_pr_auc,

                "validation_pr_auc":
                    validation_pr_auc,

                "pr_auc_generalization_gap":
                    float(
                        train_pr_auc
                        - validation_pr_auc
                    ),

                "train_roc_auc":
                    train_roc_auc,

                "validation_roc_auc":
                    validation_roc_auc,

                "roc_auc_generalization_gap":
                    float(
                        train_roc_auc
                        - validation_roc_auc
                    ),

                "best_parameters":
                    str(
                        best_parameters[
                            model_name
                        ]
                    ),

                "primary_selection_metric":
                    PRIMARY_SELECTION_METRIC,

                "fit_partition":
                    "train",

                "validation_used_for_fit":
                    False,

                "locked_test_accessed":
                    False,

                "clinical_threshold_selected":
                    False,
            }
        )

    return pd.DataFrame(
        records
    )


# ============================================================
# D8.28 — VALIDATE TUNED-CANDIDATE VALIDATION EVIDENCE
# ============================================================

def validate_d8_tuned_candidate_validation(
    performance_table: pd.DataFrame | None = None,
) -> dict[str, Any]:
    """
    Validate post-tuning held-out VALIDATION performance
    evidence before model-selection logic is permitted.
    """

    if performance_table is None:
        performance_table = (
            evaluate_d8_tuned_candidates_on_validation()
        )

    expected_models = set(
        TUNABLE_MODEL_CANDIDATES
    )

    required_columns = {
        "model_name",
        "model_role",
        "best_train_cv_pr_auc",
        "train_pr_auc",
        "validation_pr_auc",
        "pr_auc_generalization_gap",
        "train_roc_auc",
        "validation_roc_auc",
        "roc_auc_generalization_gap",
        "best_parameters",
        "primary_selection_metric",
        "fit_partition",
        "validation_used_for_fit",
        "locked_test_accessed",
        "clinical_threshold_selected",
    }

    required_columns_present = (
        required_columns.issubset(
            performance_table.columns
        )
    )

    candidate_set_complete = (
        set(
            performance_table[
                "model_name"
            ].tolist()
        )
        == expected_models
    )

    candidate_rows_unique = bool(
        performance_table[
            "model_name"
        ].is_unique
    )

    bounded_metric_columns = [
        "best_train_cv_pr_auc",
        "train_pr_auc",
        "validation_pr_auc",
        "train_roc_auc",
        "validation_roc_auc",
    ]

    metrics_finite = bool(
        np.isfinite(
            performance_table[
                bounded_metric_columns
            ].to_numpy(
                dtype=float
            )
        ).all()
    )

    metrics_in_range = bool(
        performance_table[
            bounded_metric_columns
        ]
        .ge(0.0)
        .all()
        .all()

        and

        performance_table[
            bounded_metric_columns
        ]
        .le(1.0)
        .all()
        .all()
    )

    pr_gap_correct = bool(
        np.allclose(
            performance_table[
                "pr_auc_generalization_gap"
            ].to_numpy(
                dtype=float
            ),

            (
                performance_table[
                    "train_pr_auc"
                ]
                -
                performance_table[
                    "validation_pr_auc"
                ]
            ).to_numpy(
                dtype=float
            ),
        )
    )

    roc_gap_correct = bool(
        np.allclose(
            performance_table[
                "roc_auc_generalization_gap"
            ].to_numpy(
                dtype=float
            ),

            (
                performance_table[
                    "train_roc_auc"
                ]
                -
                performance_table[
                    "validation_roc_auc"
                ]
            ).to_numpy(
                dtype=float
            ),
        )
    )

    primary_metric_correct = bool(
        performance_table[
            "primary_selection_metric"
        ]
        .eq(
            PRIMARY_SELECTION_METRIC
        )
        .all()
    )

    train_only_fit = bool(
        performance_table[
            "fit_partition"
        ]
        .eq("train")
        .all()
    )

    validation_not_used_for_fit = bool(
        performance_table[
            "validation_used_for_fit"
        ]
        .eq(False)
        .all()
    )

    locked_test_untouched = bool(
        performance_table[
            "locked_test_accessed"
        ]
        .eq(False)
        .all()
    )

    threshold_not_selected = bool(
        performance_table[
            "clinical_threshold_selected"
        ]
        .eq(False)
        .all()
    )

    checks = {
        "expected_candidate_count":
            3,

        "candidate_count":
            int(
                len(
                    performance_table
                )
            ),

        "required_columns_present":
            required_columns_present,

        "candidate_set_complete":
            candidate_set_complete,

        "candidate_rows_unique":
            candidate_rows_unique,

        "metrics_finite":
            metrics_finite,

        "metrics_in_range":
            metrics_in_range,

        "pr_auc_generalization_gap_correct":
            pr_gap_correct,

        "roc_auc_generalization_gap_correct":
            roc_gap_correct,

        "primary_selection_metric":
            PRIMARY_SELECTION_METRIC,

        "primary_metric_correct":
            primary_metric_correct,

        "fit_partition":
            "train",

        "train_only_fit":
            train_only_fit,

        "validation_used_for_fit":
            not validation_not_used_for_fit,

        "locked_test_accessed":
            not locked_test_untouched,

        "clinical_threshold_selected":
            not threshold_not_selected,
    }

    passed = all(
        [
            checks["candidate_count"] == 3,

            bool(
                checks[
                    "required_columns_present"
                ]
            ),

            bool(
                checks[
                    "candidate_set_complete"
                ]
            ),

            bool(
                checks[
                    "candidate_rows_unique"
                ]
            ),

            bool(
                checks[
                    "metrics_finite"
                ]
            ),

            bool(
                checks[
                    "metrics_in_range"
                ]
            ),

            bool(
                checks[
                    "pr_auc_generalization_gap_correct"
                ]
            ),

            bool(
                checks[
                    "roc_auc_generalization_gap_correct"
                ]
            ),

            bool(
                checks[
                    "primary_metric_correct"
                ]
            ),

            bool(
                checks[
                    "train_only_fit"
                ]
            ),

            checks[
                "validation_used_for_fit"
            ]
            is False,

            checks[
                "locked_test_accessed"
            ]
            is False,

            checks[
                "clinical_threshold_selected"
            ]
            is False,
        ]
    )

    checks["validation_status"] = (
        "PASS"
        if passed
        else "FAIL"
    )

    return checks

# ============================================================
# D8.29 — GOVERNED DEVELOPMENT MODEL SELECTION
# ============================================================

D8_SELECTED_DEVELOPMENT_MODEL = MODEL_XGBOOST

D8_MODEL_SELECTION_RULE = (
    "Highest held-out validation PR-AUC among TRAIN-CV-tuned "
    "candidate models; validation ROC-AUC retained as secondary "
    "discrimination evidence. Selection does not constitute "
    "clinical superiority, deployment approval, or locked-test "
    "performance confirmation."
)


def select_d8_development_model(
    performance_table: pd.DataFrame,
    tuning_bundle: dict[str, Any],
) -> dict[str, Any]:
    """
    Apply the pre-specified D8 model-selection rule.

    Primary criterion:
        Highest held-out VALIDATION PR-AUC.

    Secondary evidence:
        VALIDATION ROC-AUC and generalization behavior.

    The resulting estimator is a DEVELOPMENT candidate only.

    This function does NOT:
        - access TEST;
        - select a clinical threshold;
        - establish clinical utility;
        - authorize deployment.
    """

    validation = (
        validate_d8_tuned_candidate_validation(
            performance_table
        )
    )

    if validation["validation_status"] != "PASS":
        raise RuntimeError(
            "D8 model selection blocked because tuned-candidate "
            "validation evidence did not pass."
        )

    ranked = (
        performance_table
        .sort_values(
            by=[
                "validation_pr_auc",
                "validation_roc_auc",
            ],
            ascending=[
                False,
                False,
            ],
            kind="mergesort",
        )
        .reset_index(drop=True)
    )

    selected_row = ranked.iloc[0]

    selected_model_name = str(
        selected_row["model_name"]
    )

    if selected_model_name != D8_SELECTED_DEVELOPMENT_MODEL:
        raise RuntimeError(
            "Observed model-selection result does not match "
            "the governed D8 selection declaration."
        )

    selected_estimator = (
        tuning_bundle[
            "best_estimators"
        ][
            selected_model_name
        ]
    )

    runner_up_row = ranked.iloc[1]

    pr_auc_margin_vs_runner_up = float(
        selected_row[
            "validation_pr_auc"
        ]
        -
        runner_up_row[
            "validation_pr_auc"
        ]
    )

    return {
        "selected_model_name":
            selected_model_name,

        "selected_model_role":
            str(
                selected_row[
                    "model_role"
                ]
            ),

        "selected_estimator":
            selected_estimator,

        "selected_parameters":
            tuning_bundle[
                "best_parameters"
            ][
                selected_model_name
            ],

        "best_train_cv_pr_auc":
            float(
                selected_row[
                    "best_train_cv_pr_auc"
                ]
            ),

        "train_pr_auc":
            float(
                selected_row[
                    "train_pr_auc"
                ]
            ),

        "validation_pr_auc":
            float(
                selected_row[
                    "validation_pr_auc"
                ]
            ),

        "validation_roc_auc":
            float(
                selected_row[
                    "validation_roc_auc"
                ]
            ),

        "pr_auc_generalization_gap":
            float(
                selected_row[
                    "pr_auc_generalization_gap"
                ]
            ),

        "roc_auc_generalization_gap":
            float(
                selected_row[
                    "roc_auc_generalization_gap"
                ]
            ),

        "runner_up_model":
            str(
                runner_up_row[
                    "model_name"
                ]
            ),

        "runner_up_validation_pr_auc":
            float(
                runner_up_row[
                    "validation_pr_auc"
                ]
            ),

        "pr_auc_margin_vs_runner_up":
            pr_auc_margin_vs_runner_up,

        "selection_rule":
            D8_MODEL_SELECTION_RULE,

        "selection_metric":
            "validation_pr_auc",

        "development_candidate_only":
            True,

        "clinical_superiority_claimed":
            False,

        "clinical_utility_established":
            False,

        "locked_test_accessed":
            False,

        "clinical_threshold_selected":
            False,

        "deployment_authorized":
            False,
    }


# ============================================================
# D8.30 — VALIDATE GOVERNED MODEL-SELECTION DECISION
# ============================================================

def validate_d8_development_model_selection(
    selection_bundle: dict[str, Any],
) -> dict[str, Any]:
    """
    Validate the D8 development-model selection decision.
    """

    selected_model = (
        selection_bundle[
            "selected_model_name"
        ]
    )

    selected_estimator = (
        selection_bundle[
            "selected_estimator"
        ]
    )

    selected_model_correct = (
        selected_model
        == D8_SELECTED_DEVELOPMENT_MODEL
    )

    estimator_fitted = hasattr(
        selected_estimator,
        "classes_",
    )

    primary_metric_correct = (
        selection_bundle[
            "selection_metric"
        ]
        == "validation_pr_auc"
    )

    positive_selection_margin = (
        selection_bundle[
            "pr_auc_margin_vs_runner_up"
        ]
        > 0.0
    )

    checks = {
        "selected_model":
            selected_model,

        "expected_selected_model":
            D8_SELECTED_DEVELOPMENT_MODEL,

        "selected_model_correct":
            selected_model_correct,

        "selected_estimator_fitted":
            estimator_fitted,

        "selection_metric":
            selection_bundle[
                "selection_metric"
            ],

        "primary_metric_correct":
            primary_metric_correct,

        "validation_pr_auc":
            selection_bundle[
                "validation_pr_auc"
            ],

        "validation_roc_auc":
            selection_bundle[
                "validation_roc_auc"
            ],

        "runner_up_model":
            selection_bundle[
                "runner_up_model"
            ],

        "pr_auc_margin_vs_runner_up":
            selection_bundle[
                "pr_auc_margin_vs_runner_up"
            ],

        "positive_selection_margin":
            positive_selection_margin,

        "development_candidate_only":
            selection_bundle[
                "development_candidate_only"
            ],

        "clinical_superiority_claimed":
            selection_bundle[
                "clinical_superiority_claimed"
            ],

        "clinical_utility_established":
            selection_bundle[
                "clinical_utility_established"
            ],

        "locked_test_accessed":
            selection_bundle[
                "locked_test_accessed"
            ],

        "clinical_threshold_selected":
            selection_bundle[
                "clinical_threshold_selected"
            ],

        "deployment_authorized":
            selection_bundle[
                "deployment_authorized"
            ],
    }

    passed = all(
        [
            bool(
                checks[
                    "selected_model_correct"
                ]
            ),

            bool(
                checks[
                    "selected_estimator_fitted"
                ]
            ),

            bool(
                checks[
                    "primary_metric_correct"
                ]
            ),

            bool(
                checks[
                    "positive_selection_margin"
                ]
            ),

            checks[
                "development_candidate_only"
            ]
            is True,

            checks[
                "clinical_superiority_claimed"
            ]
            is False,

            checks[
                "clinical_utility_established"
            ]
            is False,

            checks[
                "locked_test_accessed"
            ]
            is False,

            checks[
                "clinical_threshold_selected"
            ]
            is False,

            checks[
                "deployment_authorized"
            ]
            is False,
        ]
    )

    checks["validation_status"] = (
        "PASS"
        if passed
        else "FAIL"
    )

    return checks

# ============================================================
# D8.31 — SELECTED DEVELOPMENT MODEL PERSISTENCE
# ============================================================

D8_MODEL_ARTIFACT_DIRECTORY = Path(
    "artifacts/models"
)

D8_SELECTED_MODEL_ARTIFACT_PATH = (
    D8_MODEL_ARTIFACT_DIRECTORY
    / "D8_selected_development_model.joblib"
)

D8_SELECTED_MODEL_METADATA_PATH = (
    D8_MODEL_ARTIFACT_DIRECTORY
    / "D8_selected_development_model_metadata.json"
)


def _sha256_file(
    path: Path,
) -> str:
    """
    Calculate SHA256 for a persisted D8 artifact.
    """

    sha256 = hashlib.sha256()

    with path.open("rb") as file_handle:

        for block in iter(
            lambda: file_handle.read(
                1024 * 1024
            ),
            b"",
        ):
            sha256.update(block)

    return sha256.hexdigest().upper()


def persist_d8_selected_development_model(
    selection_bundle: dict[str, Any],
) -> dict[str, Any]:
    """
    Persist the governed D8 selected development estimator
    and machine-readable metadata.

    Persistence does not:
        - access locked TEST;
        - select a clinical threshold;
        - authorize deployment.
    """

    selection_validation = (
        validate_d8_development_model_selection(
            selection_bundle
        )
    )

    if (
        selection_validation[
            "validation_status"
        ]
        != "PASS"
    ):
        raise RuntimeError(
            "D8 selected-model persistence blocked because "
            "the model-selection gate did not pass."
        )

    D8_MODEL_ARTIFACT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    selected_estimator = (
        selection_bundle[
            "selected_estimator"
        ]
    )

    joblib.dump(
        selected_estimator,
        D8_SELECTED_MODEL_ARTIFACT_PATH,
    )

    model_sha256 = _sha256_file(
        D8_SELECTED_MODEL_ARTIFACT_PATH
    )

    metadata = {
        "stage":
            D8_STAGE,

        "stage_name":
            D8_STAGE_NAME,

        "selected_model":
            selection_bundle[
                "selected_model_name"
            ],

        "selected_model_role":
            selection_bundle[
                "selected_model_role"
            ],

        "selected_parameters":
            selection_bundle[
                "selected_parameters"
            ],

        "best_train_cv_pr_auc":
            selection_bundle[
                "best_train_cv_pr_auc"
            ],

        "train_pr_auc":
            selection_bundle[
                "train_pr_auc"
            ],

        "validation_pr_auc":
            selection_bundle[
                "validation_pr_auc"
            ],

        "validation_roc_auc":
            selection_bundle[
                "validation_roc_auc"
            ],

        "pr_auc_generalization_gap":
            selection_bundle[
                "pr_auc_generalization_gap"
            ],

        "roc_auc_generalization_gap":
            selection_bundle[
                "roc_auc_generalization_gap"
            ],

        "runner_up_model":
            selection_bundle[
                "runner_up_model"
            ],

        "runner_up_validation_pr_auc":
            selection_bundle[
                "runner_up_validation_pr_auc"
            ],

        "pr_auc_margin_vs_runner_up":
            selection_bundle[
                "pr_auc_margin_vs_runner_up"
            ],

        "selection_metric":
            selection_bundle[
                "selection_metric"
            ],

        "selection_rule":
            selection_bundle[
                "selection_rule"
            ],

        "model_artifact_path":
            str(
                D8_SELECTED_MODEL_ARTIFACT_PATH
            ),

        "model_sha256":
            model_sha256,

        "development_candidate_only":
            True,

        "clinical_superiority_claimed":
            False,

        "clinical_utility_established":
            False,

        "locked_test_accessed":
            False,

        "clinical_threshold_selected":
            False,

        "deployment_authorized":
            False,
    }

    with D8_SELECTED_MODEL_METADATA_PATH.open(
        "w",
        encoding="utf-8",
    ) as file_handle:

        json.dump(
            metadata,
            file_handle,
            indent=2,
            sort_keys=True,
        )

    metadata_sha256 = _sha256_file(
        D8_SELECTED_MODEL_METADATA_PATH
    )

    return {
        "model_artifact_path":
            str(
                D8_SELECTED_MODEL_ARTIFACT_PATH
            ),

        "metadata_artifact_path":
            str(
                D8_SELECTED_MODEL_METADATA_PATH
            ),

        "model_sha256":
            model_sha256,

        "metadata_sha256":
            metadata_sha256,

        "selected_model":
            selection_bundle[
                "selected_model_name"
            ],

        "locked_test_accessed":
            False,

        "clinical_threshold_selected":
            False,

        "deployment_authorized":
            False,
    }


# ============================================================
# D8.32 — VALIDATE SELECTED MODEL PERSISTENCE
# ============================================================

def validate_d8_selected_model_persistence(
    persistence_bundle: dict[str, Any],
) -> dict[str, Any]:
    """
    Validate persisted selected-model integrity and exact
    reloadability.
    """

    model_path = Path(
        persistence_bundle[
            "model_artifact_path"
        ]
    )

    metadata_path = Path(
        persistence_bundle[
            "metadata_artifact_path"
        ]
    )

    model_artifact_exists = (
        model_path.exists()
    )

    metadata_artifact_exists = (
        metadata_path.exists()
    )

    model_checksum_matches = (
        model_artifact_exists
        and
        _sha256_file(
            model_path
        )
        == persistence_bundle[
            "model_sha256"
        ]
    )

    metadata_checksum_matches = (
        metadata_artifact_exists
        and
        _sha256_file(
            metadata_path
        )
        == persistence_bundle[
            "metadata_sha256"
        ]
    )

    reloaded_estimator = (
        joblib.load(
            model_path
        )
        if model_artifact_exists
        else None
    )

    reloaded_estimator_fitted = (
        reloaded_estimator is not None
        and
        hasattr(
            reloaded_estimator,
            "classes_",
        )
    )

    with metadata_path.open(
        "r",
        encoding="utf-8",
    ) as file_handle:

        metadata = json.load(
            file_handle
        )

    metadata_selected_model_correct = (
        metadata[
            "selected_model"
        ]
        == D8_SELECTED_DEVELOPMENT_MODEL
    )

    metadata_model_checksum_correct = (
        metadata[
            "model_sha256"
        ]
        == persistence_bundle[
            "model_sha256"
        ]
    )

    checks = {
        "model_artifact_exists":
            model_artifact_exists,

        "metadata_artifact_exists":
            metadata_artifact_exists,

        "model_checksum_matches":
            model_checksum_matches,

        "metadata_checksum_matches":
            metadata_checksum_matches,

        "reloaded_estimator_fitted":
            reloaded_estimator_fitted,

        "selected_model":
            persistence_bundle[
                "selected_model"
            ],

        "metadata_selected_model_correct":
            metadata_selected_model_correct,

        "metadata_model_checksum_correct":
            metadata_model_checksum_correct,

        "model_sha256":
            persistence_bundle[
                "model_sha256"
            ],

        "metadata_sha256":
            persistence_bundle[
                "metadata_sha256"
            ],

        "locked_test_accessed":
            persistence_bundle[
                "locked_test_accessed"
            ],

        "clinical_threshold_selected":
            persistence_bundle[
                "clinical_threshold_selected"
            ],

        "deployment_authorized":
            persistence_bundle[
                "deployment_authorized"
            ],
    }

    passed = all(
        [
            bool(
                checks[
                    "model_artifact_exists"
                ]
            ),

            bool(
                checks[
                    "metadata_artifact_exists"
                ]
            ),

            bool(
                checks[
                    "model_checksum_matches"
                ]
            ),

            bool(
                checks[
                    "metadata_checksum_matches"
                ]
            ),

            bool(
                checks[
                    "reloaded_estimator_fitted"
                ]
            ),

            bool(
                checks[
                    "metadata_selected_model_correct"
                ]
            ),

            bool(
                checks[
                    "metadata_model_checksum_correct"
                ]
            ),

            checks[
                "locked_test_accessed"
            ]
            is False,

            checks[
                "clinical_threshold_selected"
            ]
            is False,

            checks[
                "deployment_authorized"
            ]
            is False,
        ]
    )

    checks["validation_status"] = (
        "PASS"
        if passed
        else "FAIL"
    )

    return checks