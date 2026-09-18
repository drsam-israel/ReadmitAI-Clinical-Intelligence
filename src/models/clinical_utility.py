# ============================================================
# D9 — CLINICAL UTILITY & THRESHOLD GOVERNANCE
# ============================================================
#
# Purpose:
#   Evaluate the clinical and operational consequences of using
#   the frozen D8 development model at candidate probability
#   thresholds.
#
# D9 translates discrimination performance into clinically
# interpretable operating characteristics.
#
# D9 DOES:
#   - use the frozen D8 selected development model;
#   - use held-out VALIDATION for threshold development;
#   - evaluate threshold-dependent clinical performance;
#   - quantify false-negative and false-positive consequences;
#   - evaluate alert/intervention burden;
#   - support governed threshold selection;
#   - preserve evidence for the D9 lifecycle decision.
#
# D9 DOES NOT:
#   - retrain the D8 model;
#   - retune D8 hyperparameters;
#   - modify the frozen D7 preprocessor;
#   - access the locked TEST partition;
#   - claim locked-test generalization;
#   - establish deployment readiness;
#   - authorize autonomous clinical decision-making.
#
# The locked TEST partition remains reserved for D14.
# ============================================================

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from sklearn.metrics import (
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
)


from sklearn.metrics import brier_score_loss, log_loss
from sklearn.linear_model import LogisticRegression

# ============================================================
# D9.01 — LIFECYCLE & GOVERNANCE CONTRACT
# ============================================================

D9_STAGE = "D9"

D9_STAGE_NAME = (
    "Clinical Utility & Threshold Governance"
)

D9_SOURCE_STAGE = "D8"

D9_TARGET = "readmitted_30d"

D9_MODEL_SELECTION_STATUS = (
    "FROZEN_D8_DEVELOPMENT_CANDIDATE"
)

D9_THRESHOLD_DEVELOPMENT_PARTITION = (
    "validation"
)

D9_LOCKED_TEST_ACCESS_PERMITTED = False

D9_MODEL_RETRAINING_PERMITTED = False

D9_HYPERPARAMETER_RETUNING_PERMITTED = False

D9_PREPROCESSOR_REFITTING_PERMITTED = False

D9_AUTONOMOUS_CLINICAL_DECISION_PERMITTED = False

D9_DEPLOYMENT_AUTHORIZED = False

D9_LOCKED_TEST_EVALUATION_STAGE = "D14"


# ============================================================
# D9.02 — CLINICAL INTENDED-USE DEFINITION
# ============================================================

D9_CLINICAL_INTENDED_USE = (
    "Support clinician-reviewed identification of hospitalized "
    "patients with diabetes who may benefit from intensified "
    "30-day readmission-prevention planning before discharge."
)

D9_PRIMARY_USERS = (
    "discharge_planning",
    "care_management",
    "treating_clinicians",
)

D9_MODEL_ACTION = (
    "Prioritize patients for clinician-reviewed readmission-"
    "prevention assessment and intervention."
)

D9_PROHIBITED_ACTION = (
    "The model must not autonomously determine discharge, "
    "treatment, admission, denial of care, or other clinical "
    "management decisions."
)


# ============================================================
# D9.03 — THRESHOLD GOVERNANCE PRINCIPLES
# ============================================================

D9_THRESHOLD_GOVERNANCE_PRINCIPLES = (
    "Threshold selection must be based on explicit clinical and "
    "operational trade-offs rather than an arbitrary default "
    "probability threshold.",

    "Sensitivity must be evaluated because false-negative "
    "predictions may leave higher-risk patients without "
    "additional readmission-prevention review.",

    "Precision and alert burden must be evaluated because false "
    "positive alerts consume clinical and care-management "
    "capacity.",

    "Specificity and negative predictive value must be retained "
    "as complementary operating characteristics.",

    "Threshold-dependent performance must be evaluated on the "
    "held-out VALIDATION partition during D9.",

    "The locked TEST partition must remain inaccessible until "
    "the authorized locked-test lifecycle stage.",

    "A D9 threshold is a development-stage operating threshold "
    "and does not constitute deployment authorization.",
)


# ============================================================
# D9.04 — REQUIRED THRESHOLD METRICS
# ============================================================

D9_REQUIRED_THRESHOLD_METRICS = (
    "threshold",
    "true_positive",
    "false_positive",
    "true_negative",
    "false_negative",
    "sensitivity",
    "specificity",
    "precision",
    "negative_predictive_value",
    "f1_score",
    "predicted_positive_count",
    "predicted_positive_rate",
    "alerts_per_100_patients",
    "number_needed_to_evaluate",
)


# ============================================================
# D9.05 — CLINICAL CONSEQUENCE DEFINITIONS
# ============================================================

D9_FALSE_NEGATIVE_CONSEQUENCE = (
    "A patient who experiences 30-day readmission is not "
    "identified by the model for additional clinician-reviewed "
    "readmission-prevention prioritization."
)

D9_FALSE_POSITIVE_CONSEQUENCE = (
    "A patient who does not experience 30-day readmission is "
    "flagged for additional review, increasing clinical or "
    "care-management workload."
)

D9_TRUE_POSITIVE_INTERPRETATION = (
    "A patient who experiences 30-day readmission was identified "
    "for additional clinician-reviewed prevention assessment."
)

D9_TRUE_NEGATIVE_INTERPRETATION = (
    "A patient who does not experience 30-day readmission was "
    "not flagged for additional model-driven prioritization."
)


# ============================================================
# D9.06 — STATIC GOVERNANCE CONTRACT VALIDATION
# ============================================================

def validate_d9_static_contract() -> dict[str, Any]:
    """
    Validate the non-negotiable D9 lifecycle boundaries before
    any threshold analysis is permitted.
    """

    checks = {
        "stage_is_d9":
            D9_STAGE == "D9",

        "source_stage_is_d8":
            D9_SOURCE_STAGE == "D8",

        "target_is_readmitted_30d":
            D9_TARGET == "readmitted_30d",

        "threshold_partition_is_validation":
            D9_THRESHOLD_DEVELOPMENT_PARTITION
            == "validation",

        "locked_test_access_prohibited":
            D9_LOCKED_TEST_ACCESS_PERMITTED
            is False,

        "model_retraining_prohibited":
            D9_MODEL_RETRAINING_PERMITTED
            is False,

        "hyperparameter_retuning_prohibited":
            D9_HYPERPARAMETER_RETUNING_PERMITTED
            is False,

        "preprocessor_refitting_prohibited":
            D9_PREPROCESSOR_REFITTING_PERMITTED
            is False,

        "autonomous_clinical_decision_prohibited":
            D9_AUTONOMOUS_CLINICAL_DECISION_PERMITTED
            is False,

        "deployment_not_authorized":
            D9_DEPLOYMENT_AUTHORIZED
            is False,

        "locked_test_reserved_for_d14":
            D9_LOCKED_TEST_EVALUATION_STAGE
            == "D14",

        "required_threshold_metrics_complete":
            len(D9_REQUIRED_THRESHOLD_METRICS)
            == 14,

        "clinical_users_defined":
            len(D9_PRIMARY_USERS) >= 1,

        "threshold_principles_defined":
            len(D9_THRESHOLD_GOVERNANCE_PRINCIPLES)
            >= 5,
    }

    failed_checks = [
        check_name
        for check_name, passed
        in checks.items()
        if not bool(passed)
    ]

    status = (
        "PASS"
        if not failed_checks
        else "FAIL"
    )

    result = {
        "stage":
            D9_STAGE,

        "stage_name":
            D9_STAGE_NAME,

        "source_stage":
            D9_SOURCE_STAGE,

        "threshold_development_partition":
            D9_THRESHOLD_DEVELOPMENT_PARTITION,

        "locked_test_access_permitted":
            D9_LOCKED_TEST_ACCESS_PERMITTED,

        "model_retraining_permitted":
            D9_MODEL_RETRAINING_PERMITTED,

        "hyperparameter_retuning_permitted":
            D9_HYPERPARAMETER_RETUNING_PERMITTED,

        "preprocessor_refitting_permitted":
            D9_PREPROCESSOR_REFITTING_PERMITTED,

        "deployment_authorized":
            D9_DEPLOYMENT_AUTHORIZED,

        "required_threshold_metric_count":
            len(D9_REQUIRED_THRESHOLD_METRICS),

        "failed_checks":
            failed_checks,

        "validation_status":
            status,
    }

    if status != "PASS":
        raise RuntimeError(
            "D9 static governance contract failed: "
            f"{failed_checks}"
        )

    return result

# ============================================================
# D9.07 — FROZEN D8 MODEL ARTIFACT CONTRACT
# ============================================================

import hashlib
import joblib

from src.features.preprocessing import (
    build_persisted_d7_primary_preprocessor,
)


D9_FROZEN_MODEL_PATH = Path(
    "artifacts/models/D8_selected_development_model.joblib"
)

D9_FROZEN_MODEL_METADATA_PATH = Path(
    "artifacts/models/D8_selected_development_model_metadata.json"
)

D9_EXPECTED_MODEL_SHA256 = (
    "2FD02A54DF759EBAAF0D02D64D5ACE16A519DF016990FAC065AF3249BDA88085"
)

D9_EXPECTED_SELECTED_MODEL = "xgboost"

D9_EXPECTED_VALIDATION_ENCOUNTERS = 15052

D9_EXPECTED_TRANSFORMED_FEATURE_COUNT = 49


# ============================================================
# D9.08 — FILE SHA256 INTEGRITY HELPER
# ============================================================

def _d9_sha256_file(
    path: Path,
) -> str:
    """
    Calculate SHA256 for a persisted D9 dependency artifact.
    """

    sha256 = hashlib.sha256()

    with path.open("rb") as file_handle:

        for block in iter(
            lambda: file_handle.read(1024 * 1024),
            b"",
        ):
            sha256.update(block)

    return sha256.hexdigest().upper()


# ============================================================
# D9.09 — LOAD FROZEN D8 MODEL
# ============================================================

def load_d9_frozen_d8_model() -> dict[str, Any]:
    """
    Load the persisted D8 development model without fitting,
    tuning, or modifying it.

    The artifact checksum must match the D8-frozen checksum
    before D9 is allowed to use the estimator.
    """

    if not D9_FROZEN_MODEL_PATH.exists():
        raise FileNotFoundError(
            "Frozen D8 model artifact is missing: "
            f"{D9_FROZEN_MODEL_PATH}"
        )

    if not D9_FROZEN_MODEL_METADATA_PATH.exists():
        raise FileNotFoundError(
            "Frozen D8 model metadata is missing: "
            f"{D9_FROZEN_MODEL_METADATA_PATH}"
        )

    observed_sha256 = _d9_sha256_file(
        D9_FROZEN_MODEL_PATH
    )

    if observed_sha256 != D9_EXPECTED_MODEL_SHA256:
        raise RuntimeError(
            "Frozen D8 model checksum mismatch. "
            f"Expected={D9_EXPECTED_MODEL_SHA256}, "
            f"Observed={observed_sha256}"
        )

    model = joblib.load(
        D9_FROZEN_MODEL_PATH
    )

    metadata = pd.read_json(
        D9_FROZEN_MODEL_METADATA_PATH,
        typ="series",
    ).to_dict()

    metadata_selected_model = metadata.get(
        "selected_model"
    )

    if metadata_selected_model != D9_EXPECTED_SELECTED_MODEL:
        raise RuntimeError(
            "D8 model metadata does not identify the expected "
            "frozen development candidate. "
            f"Expected={D9_EXPECTED_SELECTED_MODEL}, "
            f"Observed={metadata_selected_model}"
        )

    return {
        "model":
            model,

        "selected_model":
            metadata_selected_model,

        "model_sha256":
            observed_sha256,

        "model_artifact_path":
            str(D9_FROZEN_MODEL_PATH),

        "metadata_artifact_path":
            str(D9_FROZEN_MODEL_METADATA_PATH),

        "model_loaded":
            True,

        "model_retrained":
            False,

        "hyperparameters_retuned":
            False,

        "locked_test_accessed":
            False,

        "validation_status":
            "PASS",
    }


# ============================================================
# D9.10 — BUILD VALIDATION-ONLY PREDICTION BUNDLE
# ============================================================

def build_d9_validation_prediction_bundle() -> dict[str, Any]:
    """
    Generate D9 probability predictions for the held-out
    VALIDATION partition using the frozen D8 model.

    No model fitting occurs here.

    The frozen D7 preprocessing workflow supplies the governed
    transformed VALIDATION representation through its fitted
    preprocessing bundle.

    Locked TEST is not requested or accessed.
    """

    # --------------------------------------------------------
    # Load checksum-verified frozen D8 development model
    # --------------------------------------------------------

    model_bundle = load_d9_frozen_d8_model()

    # --------------------------------------------------------
    # Load frozen D7 preprocessing workflow
    # --------------------------------------------------------

    preprocessing_bundle = (
        build_persisted_d7_primary_preprocessor()
    )

    required_top_level_keys = {
        "fitted_bundle",
        "persistence_validation",
        "persistence_result",
    }

    missing_top_level_keys = (
        required_top_level_keys
        - set(preprocessing_bundle)
    )

    if missing_top_level_keys:
        raise RuntimeError(
            "D9 received an incomplete D7 preprocessing bundle. "
            f"Missing={sorted(missing_top_level_keys)}"
        )

    fitted_bundle = preprocessing_bundle[
        "fitted_bundle"
    ]

    persistence_validation = preprocessing_bundle[
        "persistence_validation"
    ]

    persistence_result = preprocessing_bundle[
        "persistence_result"
    ]

    # --------------------------------------------------------
    # Validate frozen D7 persistence boundary
    # --------------------------------------------------------

    if persistence_validation.get(
        "validation_status"
    ) != "PASS":
        raise RuntimeError(
            "D9 cannot proceed because D7 persisted "
            "preprocessing validation is not PASS."
        )

    required_fitted_keys = {
        "X_validation_transformed",
        "y_validation",
        "transformed_feature_names",
    }

    missing_fitted_keys = (
        required_fitted_keys
        - set(fitted_bundle)
    )

    if missing_fitted_keys:
        raise RuntimeError(
            "D9 received an incomplete D7 fitted bundle. "
            f"Missing={sorted(missing_fitted_keys)}"
        )

    # --------------------------------------------------------
    # Extract VALIDATION only
    # --------------------------------------------------------

    X_validation = fitted_bundle[
        "X_validation_transformed"
    ]

    y_validation = fitted_bundle[
        "y_validation"
    ]

    transformed_feature_names = fitted_bundle[
        "transformed_feature_names"
    ]

    # --------------------------------------------------------
    # Validate expected governed dimensions
    # --------------------------------------------------------

    if X_validation.shape != (
        D9_EXPECTED_VALIDATION_ENCOUNTERS,
        D9_EXPECTED_TRANSFORMED_FEATURE_COUNT,
    ):
        raise RuntimeError(
            "Unexpected D9 VALIDATION matrix shape. "
            f"Expected="
            f"({D9_EXPECTED_VALIDATION_ENCOUNTERS}, "
            f"{D9_EXPECTED_TRANSFORMED_FEATURE_COUNT}), "
            f"Observed={X_validation.shape}"
        )

    if len(
        y_validation
    ) != D9_EXPECTED_VALIDATION_ENCOUNTERS:
        raise RuntimeError(
            "Unexpected D9 VALIDATION target length. "
            f"Expected={D9_EXPECTED_VALIDATION_ENCOUNTERS}, "
            f"Observed={len(y_validation)}"
        )

    if len(
        transformed_feature_names
    ) != D9_EXPECTED_TRANSFORMED_FEATURE_COUNT:
        raise RuntimeError(
            "Unexpected transformed feature count. "
            f"Expected={D9_EXPECTED_TRANSFORMED_FEATURE_COUNT}, "
            f"Observed={len(transformed_feature_names)}"
        )

    # --------------------------------------------------------
    # Verify D7 artifact integrity remains available
    # --------------------------------------------------------

    d7_preprocessor_sha256 = persistence_result.get(
        "preprocessor_sha256"
    )

    d7_schema_sha256 = persistence_result.get(
        "schema_sha256"
    )

    if not d7_preprocessor_sha256:
        raise RuntimeError(
            "D9 could not recover the frozen D7 "
            "preprocessor checksum."
        )

    if not d7_schema_sha256:
        raise RuntimeError(
            "D9 could not recover the frozen D7 "
            "transformed-schema checksum."
        )

    # --------------------------------------------------------
    # Prepare XGBoost-compatible input
    # --------------------------------------------------------
    #
    # D8 established this compatibility boundary because the
    # governed D7 transformed feature names contain characters
    # that XGBoost does not accept as pandas feature names.
    #
    # Conversion to an ordered NumPy array preserves:
    #   - row order;
    #   - column order;
    #   - feature values;
    #   - feature count.
    #
    # It does not refit or transform the data again.
    # --------------------------------------------------------

    X_validation_model = np.asarray(
        X_validation,
        dtype=np.float64,
    )

    if X_validation_model.shape != (
        D9_EXPECTED_VALIDATION_ENCOUNTERS,
        D9_EXPECTED_TRANSFORMED_FEATURE_COUNT,
    ):
        raise RuntimeError(
            "D9 XGBoost compatibility conversion changed "
            "the governed VALIDATION matrix dimensions."
        )

    if not np.isfinite(
        X_validation_model
    ).all():
        raise RuntimeError(
            "D9 VALIDATION model matrix contains "
            "non-finite values."
        )

    # --------------------------------------------------------
    # Generate probabilities — prediction only
    # --------------------------------------------------------

    model = model_bundle[
        "model"
    ]

    validation_probability = model.predict_proba(
        X_validation_model
    )[:, 1]

    validation_probability = np.asarray(
        validation_probability,
        dtype=np.float64,
    )

    y_validation_array = np.asarray(
        y_validation,
        dtype=np.int64,
    )

    # --------------------------------------------------------
    # Validate probability output
    # --------------------------------------------------------

    if validation_probability.shape != (
        D9_EXPECTED_VALIDATION_ENCOUNTERS,
    ):
        raise RuntimeError(
            "Unexpected D9 VALIDATION probability shape. "
            f"Observed={validation_probability.shape}"
        )

    if not np.isfinite(
        validation_probability
    ).all():
        raise RuntimeError(
            "D9 VALIDATION probabilities contain "
            "non-finite values."
        )

    if (
        (validation_probability < 0.0).any()
        or
        (validation_probability > 1.0).any()
    ):
        raise RuntimeError(
            "D9 VALIDATION probabilities fall "
            "outside [0, 1]."
        )

    if not set(
        np.unique(y_validation_array)
    ).issubset({0, 1}):
        raise RuntimeError(
            "D9 VALIDATION target is not binary."
        )

    # --------------------------------------------------------
    # Return governed D9 prediction bundle
    # --------------------------------------------------------

    return {
        "selected_model":
            model_bundle[
                "selected_model"
            ],

        "model_sha256":
            model_bundle[
                "model_sha256"
            ],

        "d7_preprocessor_sha256":
            d7_preprocessor_sha256,

        "d7_schema_sha256":
            d7_schema_sha256,

        "X_validation":
            X_validation_model,

        "y_validation":
            y_validation_array,

        "validation_probability":
            validation_probability,

        "transformed_feature_names":
            tuple(
                transformed_feature_names
            ),

        "validation_encounter_count":
            int(
                len(y_validation_array)
            ),

        "validation_positive_count":
            int(
                y_validation_array.sum()
            ),

        "validation_prevalence":
            float(
                y_validation_array.mean()
            ),

        "transformed_feature_count":
            int(
                X_validation_model.shape[1]
            ),

        "prediction_partition":
            "validation",

        "model_retrained":
            False,

        "hyperparameters_retuned":
            False,

        "preprocessor_refitted_in_d9":
            False,

        "validation_used_for_threshold_development":
            True,

        "locked_test_accessed":
            False,

        "clinical_threshold_selected":
            False,

        "deployment_authorized":
            False,

        "validation_status":
            "PASS",
    }


# ============================================================
# D9.11 — VALIDATE VALIDATION-PREDICTION BOUNDARY
# ============================================================

def validate_d9_validation_prediction_bundle(
    prediction_bundle: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Validate that D9 prediction generation respects the frozen
    D8/D7 lifecycle boundary.
    """

    if prediction_bundle is None:
        prediction_bundle = (
            build_d9_validation_prediction_bundle()
        )

    checks = {
        "selected_model_is_frozen_xgboost":
            prediction_bundle[
                "selected_model"
            ]
            == D9_EXPECTED_SELECTED_MODEL,

        "model_checksum_matches_d8":
            prediction_bundle[
                "model_sha256"
            ]
            == D9_EXPECTED_MODEL_SHA256,

        "validation_encounter_count_correct":
            prediction_bundle[
                "validation_encounter_count"
            ]
            == D9_EXPECTED_VALIDATION_ENCOUNTERS,

        "transformed_feature_count_correct":
            prediction_bundle[
                "transformed_feature_count"
            ]
            == D9_EXPECTED_TRANSFORMED_FEATURE_COUNT,

        "model_not_retrained":
            prediction_bundle[
                "model_retrained"
            ]
            is False,

        "hyperparameters_not_retuned":
            prediction_bundle[
                "hyperparameters_retuned"
            ]
            is False,

        "preprocessor_not_refitted_in_d9":
            prediction_bundle[
                "preprocessor_refitted_in_d9"
            ]
            is False,

        "locked_test_not_accessed":
            prediction_bundle[
                "locked_test_accessed"
            ]
            is False,

        "clinical_threshold_not_selected":
            prediction_bundle[
                "clinical_threshold_selected"
            ]
            is False,

        "deployment_not_authorized":
            prediction_bundle[
                "deployment_authorized"
            ]
            is False,
    }

    failed_checks = [
        check_name
        for check_name, passed
        in checks.items()
        if not bool(passed)
    ]

    status = (
        "PASS"
        if not failed_checks
        else "FAIL"
    )

    result = {
        "selected_model":
            prediction_bundle[
                "selected_model"
            ],

        "model_sha256":
            prediction_bundle[
                "model_sha256"
            ],

        "validation_encounter_count":
            prediction_bundle[
                "validation_encounter_count"
            ],

        "validation_positive_count":
            prediction_bundle[
                "validation_positive_count"
            ],

        "validation_prevalence":
            prediction_bundle[
                "validation_prevalence"
            ],

        "transformed_feature_count":
            prediction_bundle[
                "transformed_feature_count"
            ],

        "model_retrained":
            prediction_bundle[
                "model_retrained"
            ],

        "hyperparameters_retuned":
            prediction_bundle[
                "hyperparameters_retuned"
            ],

        "preprocessor_refitted_in_d9":
            prediction_bundle[
                "preprocessor_refitted_in_d9"
            ],

        "locked_test_accessed":
            prediction_bundle[
                "locked_test_accessed"
            ],

        "clinical_threshold_selected":
            prediction_bundle[
                "clinical_threshold_selected"
            ],

        "deployment_authorized":
            prediction_bundle[
                "deployment_authorized"
            ],

        "failed_checks":
            failed_checks,

        "validation_status":
            status,
    }

    if status != "PASS":
        raise RuntimeError(
            "D9 VALIDATION prediction boundary failed: "
            f"{failed_checks}"
        )

    return result

# ============================================================
# D9.12 — SINGLE-THRESHOLD CLINICAL UTILITY EVALUATION
# ============================================================

def evaluate_d9_threshold(
    y_true: np.ndarray,
    y_probability: np.ndarray,
    threshold: float,
) -> dict[str, Any]:
    """
    Evaluate the clinical and operational consequences of one
    candidate probability threshold.

    This function evaluates a threshold only. It does not select
    or authorize a clinical operating threshold.
    """

    y_true = np.asarray(
        y_true,
        dtype=np.int64,
    )

    y_probability = np.asarray(
        y_probability,
        dtype=np.float64,
    )

    threshold = float(threshold)

    # --------------------------------------------------------
    # Input validation
    # --------------------------------------------------------

    if y_true.ndim != 1:
        raise ValueError(
            "D9 threshold evaluation requires a 1-D target."
        )

    if y_probability.ndim != 1:
        raise ValueError(
            "D9 threshold evaluation requires a 1-D "
            "probability vector."
        )

    if len(y_true) != len(y_probability):
        raise ValueError(
            "D9 target and probability vectors must have "
            "identical lengths."
        )

    if len(y_true) == 0:
        raise ValueError(
            "D9 threshold evaluation received no observations."
        )

    if not set(
        np.unique(y_true)
    ).issubset({0, 1}):
        raise ValueError(
            "D9 threshold evaluation requires a binary target."
        )

    if not np.isfinite(
        y_probability
    ).all():
        raise ValueError(
            "D9 threshold evaluation received non-finite "
            "probabilities."
        )

    if (
        (y_probability < 0.0).any()
        or
        (y_probability > 1.0).any()
    ):
        raise ValueError(
            "D9 probabilities must fall within [0, 1]."
        )

    if not np.isfinite(threshold):
        raise ValueError(
            "D9 threshold must be finite."
        )

    if not 0.0 <= threshold <= 1.0:
        raise ValueError(
            "D9 threshold must fall within [0, 1]."
        )

    # --------------------------------------------------------
    # Apply candidate threshold
    # --------------------------------------------------------

    y_predicted = (
        y_probability >= threshold
    ).astype(np.int64)

    tn, fp, fn, tp = confusion_matrix(
        y_true,
        y_predicted,
        labels=[0, 1],
    ).ravel()

    tn = int(tn)
    fp = int(fp)
    fn = int(fn)
    tp = int(tp)

    total = int(len(y_true))

    predicted_positive_count = (
        tp + fp
    )

    predicted_negative_count = (
        tn + fn
    )

    # --------------------------------------------------------
    # Clinically interpretable operating characteristics
    # --------------------------------------------------------

    sensitivity = (
        tp / (tp + fn)
        if (tp + fn) > 0
        else np.nan
    )

    specificity = (
        tn / (tn + fp)
        if (tn + fp) > 0
        else np.nan
    )

    precision = (
        tp / (tp + fp)
        if (tp + fp) > 0
        else np.nan
    )

    negative_predictive_value = (
        tn / (tn + fn)
        if (tn + fn) > 0
        else np.nan
    )

    f1 = (
        2.0
        * precision
        * sensitivity
        / (precision + sensitivity)
        if (
            np.isfinite(precision)
            and np.isfinite(sensitivity)
            and (precision + sensitivity) > 0
        )
        else 0.0
    )

    predicted_positive_rate = (
        predicted_positive_count / total
    )

    alerts_per_100_patients = (
        100.0 * predicted_positive_rate
    )

    number_needed_to_evaluate = (
        predicted_positive_count / tp
        if tp > 0
        else np.inf
    )

    false_negative_rate = (
        fn / (fn + tp)
        if (fn + tp) > 0
        else np.nan
    )

    false_positive_rate = (
        fp / (fp + tn)
        if (fp + tn) > 0
        else np.nan
    )

    # --------------------------------------------------------
    # Governed result
    # --------------------------------------------------------

    return {
        "threshold":
            threshold,

        "true_positive":
            tp,

        "false_positive":
            fp,

        "true_negative":
            tn,

        "false_negative":
            fn,

        "sensitivity":
            float(sensitivity),

        "specificity":
            float(specificity),

        "precision":
            float(precision),

        "negative_predictive_value":
            float(negative_predictive_value),

        "f1_score":
            float(f1),

        "false_negative_rate":
            float(false_negative_rate),

        "false_positive_rate":
            float(false_positive_rate),

        "predicted_positive_count":
            predicted_positive_count,

        "predicted_negative_count":
            predicted_negative_count,

        "predicted_positive_rate":
            float(predicted_positive_rate),

        "alerts_per_100_patients":
            float(alerts_per_100_patients),

        "number_needed_to_evaluate":
            float(number_needed_to_evaluate),

        "evaluation_partition":
            "validation",

        "threshold_selected":
            False,

        "locked_test_accessed":
            False,

        "deployment_authorized":
            False,
    }


# ============================================================
# D9.13 — CANDIDATE THRESHOLD GRID
# ============================================================

D9_THRESHOLD_GRID_MIN = 0.01

D9_THRESHOLD_GRID_MAX = 0.50

D9_THRESHOLD_GRID_STEP = 0.01


def build_d9_candidate_threshold_grid() -> np.ndarray:
    """
    Build the governed threshold-analysis grid.

    The grid is intentionally an evaluation grid, not a set of
    pre-approved clinical thresholds.
    """

    thresholds = np.round(
        np.arange(
            D9_THRESHOLD_GRID_MIN,
            D9_THRESHOLD_GRID_MAX
            + D9_THRESHOLD_GRID_STEP,
            D9_THRESHOLD_GRID_STEP,
        ),
        2,
    )

    if len(thresholds) == 0:
        raise RuntimeError(
            "D9 threshold grid is empty."
        )

    if (
        thresholds.min() < 0.0
        or thresholds.max() > 1.0
    ):
        raise RuntimeError(
            "D9 threshold grid contains invalid probabilities."
        )

    return thresholds


# ============================================================
# D9.14 — THRESHOLD PERFORMANCE TABLE
# ============================================================

def build_d9_threshold_performance_table(
    prediction_bundle: dict[str, Any] | None = None,
) -> pd.DataFrame:
    """
    Evaluate all governed candidate thresholds on VALIDATION.

    No threshold is selected by this function.
    """

    if prediction_bundle is None:
        prediction_bundle = (
            build_d9_validation_prediction_bundle()
        )

    if prediction_bundle[
        "locked_test_accessed"
    ] is not False:
        raise RuntimeError(
            "D9 threshold analysis cannot proceed after "
            "locked TEST access."
        )

    y_true = prediction_bundle[
        "y_validation"
    ]

    y_probability = prediction_bundle[
        "validation_probability"
    ]

    thresholds = (
        build_d9_candidate_threshold_grid()
    )

    records = [
        evaluate_d9_threshold(
            y_true=y_true,
            y_probability=y_probability,
            threshold=threshold,
        )
        for threshold in thresholds
    ]

    table = pd.DataFrame(
        records
    )

    if len(table) != len(thresholds):
        raise RuntimeError(
            "D9 threshold-performance table is incomplete."
        )

    if table[
        "threshold"
    ].duplicated().any():
        raise RuntimeError(
            "D9 threshold-performance table contains "
            "duplicate thresholds."
        )

    if table[
        "threshold_selected"
    ].any():
        raise RuntimeError(
            "D9 threshold evaluation unexpectedly selected "
            "a clinical threshold."
        )

    if table[
        "locked_test_accessed"
    ].any():
        raise RuntimeError(
            "D9 threshold evaluation indicates locked TEST "
            "access."
        )

    return table


# ============================================================
# D9.15 — VALIDATE THRESHOLD PERFORMANCE ENGINE
# ============================================================

def validate_d9_threshold_performance_engine(
    performance_table: pd.DataFrame | None = None,
) -> dict[str, Any]:
    """
    Validate the D9 threshold evaluation engine and its
    governance boundaries.
    """

    if performance_table is None:
        performance_table = (
            build_d9_threshold_performance_table()
        )

    required_columns = {
        "threshold",
        "true_positive",
        "false_positive",
        "true_negative",
        "false_negative",
        "sensitivity",
        "specificity",
        "precision",
        "negative_predictive_value",
        "f1_score",
        "predicted_positive_count",
        "predicted_positive_rate",
        "alerts_per_100_patients",
        "number_needed_to_evaluate",
        "evaluation_partition",
        "threshold_selected",
        "locked_test_accessed",
        "deployment_authorized",
    }

    missing_columns = (
        required_columns
        - set(performance_table.columns)
    )

    if missing_columns:
        raise RuntimeError(
            "D9 threshold-performance evidence is missing "
            f"required columns: {sorted(missing_columns)}"
        )

    confusion_totals = (
        performance_table[
            [
                "true_positive",
                "false_positive",
                "true_negative",
                "false_negative",
            ]
        ]
        .sum(axis=1)
    )

    checks = {
        "threshold_count_correct":
            len(performance_table)
            == 50,

        "thresholds_unique":
            performance_table[
                "threshold"
            ].is_unique,

        "minimum_threshold_correct":
            np.isclose(
                performance_table[
                    "threshold"
                ].min(),
                D9_THRESHOLD_GRID_MIN,
            ),

        "maximum_threshold_correct":
            np.isclose(
                performance_table[
                    "threshold"
                ].max(),
                D9_THRESHOLD_GRID_MAX,
            ),

        "all_confusion_matrices_complete":
            bool(
                (
                    confusion_totals
                    == D9_EXPECTED_VALIDATION_ENCOUNTERS
                ).all()
            ),

        "sensitivity_valid":
            bool(
                performance_table[
                    "sensitivity"
                ].between(
                    0.0,
                    1.0,
                ).all()
            ),

        "specificity_valid":
            bool(
                performance_table[
                    "specificity"
                ].between(
                    0.0,
                    1.0,
                ).all()
            ),

        "precision_valid":
            bool(
                performance_table[
                    "precision"
                ].dropna().between(
                    0.0,
                    1.0,
                ).all()
            ),

        "npv_valid":
            bool(
                performance_table[
                    "negative_predictive_value"
                ].dropna().between(
                    0.0,
                    1.0,
                ).all()
            ),

        "evaluation_partition_validation":
            bool(
                (
                    performance_table[
                        "evaluation_partition"
                    ]
                    == "validation"
                ).all()
            ),

        "no_threshold_selected":
            not bool(
                performance_table[
                    "threshold_selected"
                ].any()
            ),

        "locked_test_not_accessed":
            not bool(
                performance_table[
                    "locked_test_accessed"
                ].any()
            ),

        "deployment_not_authorized":
            not bool(
                performance_table[
                    "deployment_authorized"
                ].any()
            ),
    }

    failed_checks = [
        name
        for name, passed
        in checks.items()
        if not bool(passed)
    ]

    status = (
        "PASS"
        if not failed_checks
        else "FAIL"
    )

    result = {
        "threshold_count":
            int(
                len(performance_table)
            ),

        "minimum_threshold":
            float(
                performance_table[
                    "threshold"
                ].min()
            ),

        "maximum_threshold":
            float(
                performance_table[
                    "threshold"
                ].max()
            ),

        "validation_encounter_count":
            D9_EXPECTED_VALIDATION_ENCOUNTERS,

        "threshold_selected":
            False,

        "locked_test_accessed":
            False,

        "deployment_authorized":
            False,

        "failed_checks":
            failed_checks,

        "validation_status":
            status,
    }

    if status != "PASS":
        raise RuntimeError(
            "D9 threshold-performance engine failed: "
            f"{failed_checks}"
        )

    return result

# ============================================================
# D9.16 — CLINICALLY RELEVANT THRESHOLD TRADE-OFF TABLE
# ============================================================

D9_REFERENCE_THRESHOLDS = (
    0.05,
    0.075,
    0.10,
    0.125,
    0.15,
    0.175,
    0.20,
    0.25,
    0.30,
    0.40,
    0.50,
)


def build_d9_reference_threshold_table(
    prediction_bundle: dict[str, Any] | None = None,
) -> pd.DataFrame:
    """
    Evaluate clinically interpretable reference thresholds.

    Reference thresholds are descriptive operating points only.
    They are not approved clinical thresholds and are not used
    by this function to select a threshold.
    """

    if prediction_bundle is None:
        prediction_bundle = (
            build_d9_validation_prediction_bundle()
        )

    y_true = prediction_bundle[
        "y_validation"
    ]

    y_probability = prediction_bundle[
        "validation_probability"
    ]

    records = [
        evaluate_d9_threshold(
            y_true=y_true,
            y_probability=y_probability,
            threshold=threshold,
        )
        for threshold in D9_REFERENCE_THRESHOLDS
    ]

    table = pd.DataFrame(
        records
    )

    if table[
        "threshold_selected"
    ].any():
        raise RuntimeError(
            "D9 reference-threshold analysis must not "
            "select a threshold."
        )

    if table[
        "locked_test_accessed"
    ].any():
        raise RuntimeError(
            "D9 reference-threshold analysis indicates "
            "locked TEST access."
        )

    return table


# ============================================================
# D9.17 — THRESHOLD TRADE-OFF SUMMARY
# ============================================================

def build_d9_threshold_tradeoff_summary(
    performance_table: pd.DataFrame | None = None,
) -> dict[str, Any]:
    """
    Summarize the range of clinical and operational trade-offs
    observed across the governed D9 threshold grid.

    This is descriptive evidence only.
    """

    if performance_table is None:
        performance_table = (
            build_d9_threshold_performance_table()
        )

    highest_sensitivity_row = (
        performance_table
        .sort_values(
            by=[
                "sensitivity",
                "threshold",
            ],
            ascending=[
                False,
                True,
            ],
            kind="mergesort",
        )
        .iloc[0]
    )

    highest_precision_row = (
        performance_table
        .replace(
            [np.inf, -np.inf],
            np.nan,
        )
        .dropna(
            subset=["precision"]
        )
        .sort_values(
            by=[
                "precision",
                "threshold",
            ],
            ascending=[
                False,
                True,
            ],
            kind="mergesort",
        )
        .iloc[0]
    )

    highest_f1_row = (
        performance_table
        .sort_values(
            by=[
                "f1_score",
                "threshold",
            ],
            ascending=[
                False,
                True,
            ],
            kind="mergesort",
        )
        .iloc[0]
    )

    return {
        "lowest_evaluated_threshold":
            float(
                performance_table[
                    "threshold"
                ].min()
            ),

        "highest_evaluated_threshold":
            float(
                performance_table[
                    "threshold"
                ].max()
            ),

        "highest_observed_sensitivity":
            float(
                highest_sensitivity_row[
                    "sensitivity"
                ]
            ),

        "highest_sensitivity_threshold":
            float(
                highest_sensitivity_row[
                    "threshold"
                ]
            ),

        "highest_sensitivity_alerts_per_100":
            float(
                highest_sensitivity_row[
                    "alerts_per_100_patients"
                ]
            ),

        "highest_observed_precision":
            float(
                highest_precision_row[
                    "precision"
                ]
            ),

        "highest_precision_threshold":
            float(
                highest_precision_row[
                    "threshold"
                ]
            ),

        "highest_precision_sensitivity":
            float(
                highest_precision_row[
                    "sensitivity"
                ]
            ),

        "highest_observed_f1":
            float(
                highest_f1_row[
                    "f1_score"
                ]
            ),

        "highest_f1_threshold":
            float(
                highest_f1_row[
                    "threshold"
                ]
            ),

        "highest_f1_sensitivity":
            float(
                highest_f1_row[
                    "sensitivity"
                ]
            ),

        "highest_f1_precision":
            float(
                highest_f1_row[
                    "precision"
                ]
            ),

        "highest_f1_alerts_per_100":
            float(
                highest_f1_row[
                    "alerts_per_100_patients"
                ]
            ),

        "threshold_selected":
            False,

        "locked_test_accessed":
            False,

        "deployment_authorized":
            False,
    }


# ============================================================
# D9.18 — VALIDATE TRADE-OFF ANALYSIS
# ============================================================

def validate_d9_threshold_tradeoff_analysis() -> dict[str, Any]:
    """
    Validate descriptive D9 threshold trade-off evidence.
    """

    prediction_bundle = (
        build_d9_validation_prediction_bundle()
    )

    performance_table = (
        build_d9_threshold_performance_table(
            prediction_bundle
        )
    )

    reference_table = (
        build_d9_reference_threshold_table(
            prediction_bundle
        )
    )

    tradeoff_summary = (
        build_d9_threshold_tradeoff_summary(
            performance_table
        )
    )

    checks = {
        "performance_grid_complete":
            len(performance_table) == 50,

        "reference_thresholds_complete":
            len(reference_table)
            == len(D9_REFERENCE_THRESHOLDS),

        "reference_thresholds_unique":
            reference_table[
                "threshold"
            ].is_unique,

        "no_reference_threshold_selected":
            not bool(
                reference_table[
                    "threshold_selected"
                ].any()
            ),

        "locked_test_not_accessed":
            (
                tradeoff_summary[
                    "locked_test_accessed"
                ]
                is False
            ),

        "no_threshold_selected":
            (
                tradeoff_summary[
                    "threshold_selected"
                ]
                is False
            ),

        "deployment_not_authorized":
            (
                tradeoff_summary[
                    "deployment_authorized"
                ]
                is False
            ),
    }

    failed_checks = [
        name
        for name, passed
        in checks.items()
        if not bool(passed)
    ]

    status = (
        "PASS"
        if not failed_checks
        else "FAIL"
    )

    return {
        "reference_threshold_count":
            int(
                len(reference_table)
            ),

        "tradeoff_summary":
            tradeoff_summary,

        "threshold_selected":
            False,

        "locked_test_accessed":
            False,

        "deployment_authorized":
            False,

        "failed_checks":
            failed_checks,

        "validation_status":
            status,
    }

# ============================================================
# D9.19 — CLINICAL OPERATING SCENARIO DEFINITIONS
# ============================================================
#
# These scenarios are decision-analysis constraints.
#
# They are NOT claims that any particular workload capacity or
# sensitivity requirement has been approved by a hospital.
#
# Their purpose is to demonstrate how the model behaves under
# different plausible clinical-operational priorities.
# ============================================================

D9_OPERATING_SCENARIOS = {
    "HIGH_SENSITIVITY": {
        "description":
            (
                "Prioritize capture of patients who experience "
                "30-day readmission, accepting a high review "
                "burden."
            ),

        "minimum_sensitivity":
            0.80,

        "maximum_alerts_per_100":
            None,
    },

    "MODERATE_CAPACITY": {
        "description":
            (
                "Evaluate operating points under a hypothetical "
                "maximum review capacity of 30 alerts per "
                "100 eligible patients."
            ),

        "minimum_sensitivity":
            None,

        "maximum_alerts_per_100":
            30.0,
    },

    "RESTRICTED_CAPACITY": {
        "description":
            (
                "Evaluate operating points under a hypothetical "
                "maximum review capacity of 20 alerts per "
                "100 eligible patients."
            ),

        "minimum_sensitivity":
            None,

        "maximum_alerts_per_100":
            20.0,
    },

    "BALANCED_EXPLORATORY": {
        "description":
            (
                "Explore thresholds requiring at least 40% "
                "sensitivity while limiting review burden to "
                "35 alerts per 100 eligible patients."
            ),

        "minimum_sensitivity":
            0.40,

        "maximum_alerts_per_100":
            35.0,
    },
}


# ============================================================
# D9.20 — OPERATING-SCENARIO FEASIBILITY ENGINE
# ============================================================

def evaluate_d9_operating_scenarios(
    performance_table: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """
    Evaluate which candidate thresholds satisfy each governed
    decision-analysis scenario.

    This function identifies feasible operating points only.

    It does NOT select or authorize a clinical threshold.
    """

    if performance_table is None:
        performance_table = (
            build_d9_threshold_performance_table()
        )

    records = []

    for (
        scenario_name,
        scenario_definition,
    ) in D9_OPERATING_SCENARIOS.items():

        minimum_sensitivity = (
            scenario_definition[
                "minimum_sensitivity"
            ]
        )

        maximum_alerts = (
            scenario_definition[
                "maximum_alerts_per_100"
            ]
        )

        feasible = pd.Series(
            True,
            index=performance_table.index,
            dtype=bool,
        )

        if minimum_sensitivity is not None:
            feasible &= (
                performance_table[
                    "sensitivity"
                ]
                >= minimum_sensitivity
            )

        if maximum_alerts is not None:
            feasible &= (
                performance_table[
                    "alerts_per_100_patients"
                ]
                <= maximum_alerts
            )

        scenario_table = (
            performance_table
            .loc[feasible]
            .copy()
        )

        if scenario_table.empty:

            records.append(
                {
                    "scenario":
                        scenario_name,

                    "description":
                        scenario_definition[
                            "description"
                        ],

                    "minimum_sensitivity":
                        minimum_sensitivity,

                    "maximum_alerts_per_100":
                        maximum_alerts,

                    "feasible_threshold_count":
                        0,

                    "minimum_feasible_threshold":
                        np.nan,

                    "maximum_feasible_threshold":
                        np.nan,

                    "highest_feasible_sensitivity":
                        np.nan,

                    "lowest_feasible_alerts_per_100":
                        np.nan,

                    "highest_feasible_precision":
                        np.nan,

                    "scenario_feasible":
                        False,

                    "threshold_selected":
                        False,

                    "locked_test_accessed":
                        False,

                    "deployment_authorized":
                        False,
                }
            )

            continue

        records.append(
            {
                "scenario":
                    scenario_name,

                "description":
                    scenario_definition[
                        "description"
                    ],

                "minimum_sensitivity":
                    minimum_sensitivity,

                "maximum_alerts_per_100":
                    maximum_alerts,

                "feasible_threshold_count":
                    int(
                        len(scenario_table)
                    ),

                "minimum_feasible_threshold":
                    float(
                        scenario_table[
                            "threshold"
                        ].min()
                    ),

                "maximum_feasible_threshold":
                    float(
                        scenario_table[
                            "threshold"
                        ].max()
                    ),

                "highest_feasible_sensitivity":
                    float(
                        scenario_table[
                            "sensitivity"
                        ].max()
                    ),

                "lowest_feasible_alerts_per_100":
                    float(
                        scenario_table[
                            "alerts_per_100_patients"
                        ].min()
                    ),

                "highest_feasible_precision":
                    float(
                        scenario_table[
                            "precision"
                        ]
                        .dropna()
                        .max()
                    ),

                "scenario_feasible":
                    True,

                "threshold_selected":
                    False,

                "locked_test_accessed":
                    False,

                "deployment_authorized":
                    False,
            }
        )

    return pd.DataFrame(
        records
    )


# ============================================================
# D9.21 — CAPACITY FRONTIER
# ============================================================

D9_CAPACITY_LIMITS_PER_100 = (
    10.0,
    15.0,
    20.0,
    25.0,
    30.0,
    35.0,
    40.0,
    50.0,
)


def build_d9_capacity_frontier(
    performance_table: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """
    Determine the highest observed sensitivity achievable within
    each hypothetical alert-capacity limit.

    Capacity limits are analytical scenarios only and do not
    represent approved institutional staffing constraints.
    """

    if performance_table is None:
        performance_table = (
            build_d9_threshold_performance_table()
        )

    records = []

    for capacity_limit in D9_CAPACITY_LIMITS_PER_100:

        feasible = performance_table.loc[
            performance_table[
                "alerts_per_100_patients"
            ]
            <= capacity_limit
        ].copy()

        if feasible.empty:

            records.append(
                {
                    "capacity_limit_per_100":
                        capacity_limit,

                    "feasible":
                        False,

                    "threshold":
                        np.nan,

                    "sensitivity":
                        np.nan,

                    "specificity":
                        np.nan,

                    "precision":
                        np.nan,

                    "alerts_per_100_patients":
                        np.nan,

                    "true_positive":
                        np.nan,

                    "false_positive":
                        np.nan,

                    "false_negative":
                        np.nan,

                    "number_needed_to_evaluate":
                        np.nan,

                    "threshold_selected":
                        False,
                }
            )

            continue

        # Within the stated capacity, identify the threshold with
        # the highest observed sensitivity.
        #
        # Tie-breaking:
        #   1. higher sensitivity;
        #   2. higher precision;
        #   3. lower alert burden;
        #   4. higher threshold.
        #
        # This is a descriptive frontier rule, not clinical
        # threshold authorization.

        frontier_row = (
            feasible
            .sort_values(
                by=[
                    "sensitivity",
                    "precision",
                    "alerts_per_100_patients",
                    "threshold",
                ],
                ascending=[
                    False,
                    False,
                    True,
                    False,
                ],
                kind="mergesort",
            )
            .iloc[0]
        )

        records.append(
            {
                "capacity_limit_per_100":
                    capacity_limit,

                "feasible":
                    True,

                "threshold":
                    float(
                        frontier_row[
                            "threshold"
                        ]
                    ),

                "sensitivity":
                    float(
                        frontier_row[
                            "sensitivity"
                        ]
                    ),

                "specificity":
                    float(
                        frontier_row[
                            "specificity"
                        ]
                    ),

                "precision":
                    float(
                        frontier_row[
                            "precision"
                        ]
                    ),

                "alerts_per_100_patients":
                    float(
                        frontier_row[
                            "alerts_per_100_patients"
                        ]
                    ),

                "true_positive":
                    int(
                        frontier_row[
                            "true_positive"
                        ]
                    ),

                "false_positive":
                    int(
                        frontier_row[
                            "false_positive"
                        ]
                    ),

                "false_negative":
                    int(
                        frontier_row[
                            "false_negative"
                        ]
                    ),

                "number_needed_to_evaluate":
                    float(
                        frontier_row[
                            "number_needed_to_evaluate"
                        ]
                    ),

                "threshold_selected":
                    False,
            }
        )

    return pd.DataFrame(
        records
    )


# ============================================================
# D9.22 — VALIDATE OPERATING-SCENARIO ANALYSIS
# ============================================================

def validate_d9_operating_scenario_analysis() -> dict[str, Any]:
    """
    Validate scenario and capacity-frontier evidence without
    selecting a clinical operating threshold.
    """

    performance_table = (
        build_d9_threshold_performance_table()
    )

    scenario_table = (
        evaluate_d9_operating_scenarios(
            performance_table
        )
    )

    capacity_frontier = (
        build_d9_capacity_frontier(
            performance_table
        )
    )

    checks = {
        "all_scenarios_evaluated":
            len(scenario_table)
            == len(D9_OPERATING_SCENARIOS),

        "all_capacity_limits_evaluated":
            len(capacity_frontier)
            == len(D9_CAPACITY_LIMITS_PER_100),

        "scenario_names_unique":
            scenario_table[
                "scenario"
            ].is_unique,

        "capacity_limits_unique":
            capacity_frontier[
                "capacity_limit_per_100"
            ].is_unique,

        "no_scenario_selected_threshold":
            not bool(
                scenario_table[
                    "threshold_selected"
                ].any()
            ),

        "no_frontier_selected_threshold":
            not bool(
                capacity_frontier[
                    "threshold_selected"
                ].any()
            ),

        "locked_test_not_accessed":
            not bool(
                scenario_table[
                    "locked_test_accessed"
                ].any()
            ),

        "deployment_not_authorized":
            not bool(
                scenario_table[
                    "deployment_authorized"
                ].any()
            ),
    }

    failed_checks = [
        name
        for name, passed
        in checks.items()
        if not bool(passed)
    ]

    status = (
        "PASS"
        if not failed_checks
        else "FAIL"
    )

    return {
        "scenario_count":
            int(
                len(scenario_table)
            ),

        "capacity_limit_count":
            int(
                len(capacity_frontier)
            ),

        "threshold_selected":
            False,

        "locked_test_accessed":
            False,

        "deployment_authorized":
            False,

        "failed_checks":
            failed_checks,

        "validation_status":
            status,
    }

# ============================================================
# D9.23 — DEVELOPMENT THRESHOLD DECISION CONTRACT
# ============================================================
#
# IMPORTANT:
#
# The constraints below are development-stage analytical
# assumptions. They are NOT claimed to represent approved
# institutional staffing capacity, clinical policy, or an
# externally validated minimum-sensitivity requirement.
#
# The selected threshold remains a development operating point
# and must undergo later validation and governance.
# ============================================================

D9_DEVELOPMENT_MINIMUM_SENSITIVITY = 0.40

D9_DEVELOPMENT_MAXIMUM_ALERTS_PER_100 = 35.0

D9_THRESHOLD_SELECTION_PARTITION = "validation"

D9_THRESHOLD_SELECTION_RULE = (
    "Among VALIDATION thresholds satisfying sensitivity >= 0.40 "
    "and alerts_per_100_patients <= 35.0, select the threshold "
    "with highest sensitivity; break ties by higher precision, "
    "then lower alert burden, then higher threshold."
)

D9_THRESHOLD_DECISION_CLASSIFICATION = (
    "DEVELOPMENT_STAGE_OPERATING_THRESHOLD"
)

D9_THRESHOLD_EXTERNALLY_VALIDATED = False

D9_THRESHOLD_INSTITUTIONALLY_APPROVED = False

D9_THRESHOLD_DEPLOYMENT_APPROVED = False


# ============================================================
# D9.24 — SELECT DEVELOPMENT OPERATING THRESHOLD
# ============================================================

def select_d9_development_threshold(
    performance_table: pd.DataFrame | None = None,
) -> dict[str, Any]:
    """
    Select the governed D9 development-stage operating threshold.

    Selection is performed only on held-out VALIDATION using the
    pre-specified D9 development constraints.

    This is not a deployment threshold and is not evidence of
    institutional clinical approval.
    """

    if performance_table is None:
        performance_table = (
            build_d9_threshold_performance_table()
        )

    feasible = performance_table.loc[
        (
            performance_table[
                "sensitivity"
            ]
            >= D9_DEVELOPMENT_MINIMUM_SENSITIVITY
        )
        &
        (
            performance_table[
                "alerts_per_100_patients"
            ]
            <= D9_DEVELOPMENT_MAXIMUM_ALERTS_PER_100
        )
    ].copy()

    if feasible.empty:
        raise RuntimeError(
            "No D9 candidate threshold satisfies the "
            "pre-specified development-stage constraints."
        )

    ranked = (
        feasible
        .sort_values(
            by=[
                "sensitivity",
                "precision",
                "alerts_per_100_patients",
                "threshold",
            ],
            ascending=[
                False,
                False,
                True,
                False,
            ],
            kind="mergesort",
        )
        .reset_index(drop=True)
    )

    selected = ranked.iloc[0]

    return {
        "selected_threshold":
            float(
                selected[
                    "threshold"
                ]
            ),

        "selection_partition":
            D9_THRESHOLD_SELECTION_PARTITION,

        "selection_rule":
            D9_THRESHOLD_SELECTION_RULE,

        "decision_classification":
            D9_THRESHOLD_DECISION_CLASSIFICATION,

        "minimum_sensitivity_constraint":
            D9_DEVELOPMENT_MINIMUM_SENSITIVITY,

        "maximum_alerts_per_100_constraint":
            D9_DEVELOPMENT_MAXIMUM_ALERTS_PER_100,

        "feasible_threshold_count":
            int(
                len(feasible)
            ),

        "true_positive":
            int(
                selected[
                    "true_positive"
                ]
            ),

        "false_positive":
            int(
                selected[
                    "false_positive"
                ]
            ),

        "true_negative":
            int(
                selected[
                    "true_negative"
                ]
            ),

        "false_negative":
            int(
                selected[
                    "false_negative"
                ]
            ),

        "sensitivity":
            float(
                selected[
                    "sensitivity"
                ]
            ),

        "specificity":
            float(
                selected[
                    "specificity"
                ]
            ),

        "precision":
            float(
                selected[
                    "precision"
                ]
            ),

        "negative_predictive_value":
            float(
                selected[
                    "negative_predictive_value"
                ]
            ),

        "f1_score":
            float(
                selected[
                    "f1_score"
                ]
            ),

        "predicted_positive_count":
            int(
                selected[
                    "predicted_positive_count"
                ]
            ),

        "predicted_positive_rate":
            float(
                selected[
                    "predicted_positive_rate"
                ]
            ),

        "alerts_per_100_patients":
            float(
                selected[
                    "alerts_per_100_patients"
                ]
            ),

        "number_needed_to_evaluate":
            float(
                selected[
                    "number_needed_to_evaluate"
                ]
            ),

        "external_validation_completed":
            D9_THRESHOLD_EXTERNALLY_VALIDATED,

        "institutional_approval_obtained":
            D9_THRESHOLD_INSTITUTIONALLY_APPROVED,

        "locked_test_accessed":
            False,

        "deployment_authorized":
            D9_THRESHOLD_DEPLOYMENT_APPROVED,

        "development_threshold_selected":
            True,
    }


# ============================================================
# D9.25 — VALIDATE DEVELOPMENT THRESHOLD DECISION
# ============================================================

def validate_d9_development_threshold_selection(
    selection_bundle: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Validate the D9 development-stage threshold decision and
    preserve its lifecycle limitations.
    """

    if selection_bundle is None:
        selection_bundle = (
            select_d9_development_threshold()
        )

    checks = {
        "threshold_selected":
            selection_bundle[
                "development_threshold_selected"
            ]
            is True,

        "selection_partition_is_validation":
            selection_bundle[
                "selection_partition"
            ]
            == "validation",

        "minimum_sensitivity_satisfied":
            selection_bundle[
                "sensitivity"
            ]
            >= D9_DEVELOPMENT_MINIMUM_SENSITIVITY,

        "maximum_alert_burden_satisfied":
            selection_bundle[
                "alerts_per_100_patients"
            ]
            <= D9_DEVELOPMENT_MAXIMUM_ALERTS_PER_100,

        "classification_correct":
            selection_bundle[
                "decision_classification"
            ]
            == D9_THRESHOLD_DECISION_CLASSIFICATION,

        "external_validation_not_claimed":
            selection_bundle[
                "external_validation_completed"
            ]
            is False,

        "institutional_approval_not_claimed":
            selection_bundle[
                "institutional_approval_obtained"
            ]
            is False,

        "locked_test_not_accessed":
            selection_bundle[
                "locked_test_accessed"
            ]
            is False,

        "deployment_not_authorized":
            selection_bundle[
                "deployment_authorized"
            ]
            is False,
    }

    failed_checks = [
        name
        for name, passed
        in checks.items()
        if not bool(passed)
    ]

    status = (
        "PASS"
        if not failed_checks
        else "FAIL"
    )

    result = {
        **selection_bundle,

        "failed_checks":
            failed_checks,

        "validation_status":
            status,
    }

    if status != "PASS":
        raise RuntimeError(
            "D9 development-threshold selection failed: "
            f"{failed_checks}"
        )

    return result

# ============================================================
# D9.26 — DECISION-CURVE NET BENEFIT
# ============================================================

def calculate_d9_net_benefit(
    y_true: np.ndarray,
    y_probability: np.ndarray,
    threshold: float,
) -> dict[str, Any]:
    """
    Calculate model, treat-all, and treat-none net benefit at
    one threshold probability.

    IMPORTANT:
    D9 has not established probability calibration.
    Therefore this is exploratory development-stage decision
    analysis and not clinical deployment evidence.
    """

    y_true = np.asarray(
        y_true,
        dtype=np.int64,
    )

    y_probability = np.asarray(
        y_probability,
        dtype=np.float64,
    )

    threshold = float(threshold)

    if not 0.0 < threshold < 1.0:
        raise ValueError(
            "Decision-curve threshold must lie strictly "
            "between 0 and 1."
        )

    if len(y_true) != len(y_probability):
        raise ValueError(
            "Target and probability vectors must have "
            "identical lengths."
        )

    if len(y_true) == 0:
        raise ValueError(
            "Decision-curve analysis received no observations."
        )

    threshold_result = evaluate_d9_threshold(
        y_true=y_true,
        y_probability=y_probability,
        threshold=threshold,
    )

    n = len(y_true)

    tp = threshold_result[
        "true_positive"
    ]

    fp = threshold_result[
        "false_positive"
    ]

    prevalence = float(
        y_true.mean()
    )

    odds_weight = (
        threshold
        / (1.0 - threshold)
    )

    model_net_benefit = (
        (tp / n)
        -
        (fp / n) * odds_weight
    )

    treat_all_net_benefit = (
        prevalence
        -
        (1.0 - prevalence)
        * odds_weight
    )

    treat_none_net_benefit = 0.0

    best_default_strategy = max(
        treat_all_net_benefit,
        treat_none_net_benefit,
    )

    incremental_net_benefit_vs_best_default = (
        model_net_benefit
        - best_default_strategy
    )

    return {
        "threshold":
            threshold,

        "model_net_benefit":
            float(
                model_net_benefit
            ),

        "treat_all_net_benefit":
            float(
                treat_all_net_benefit
            ),

        "treat_none_net_benefit":
            float(
                treat_none_net_benefit
            ),

        "incremental_net_benefit_vs_best_default":
            float(
                incremental_net_benefit_vs_best_default
            ),

        "model_better_than_treat_all":
            bool(
                model_net_benefit
                > treat_all_net_benefit
            ),

        "model_better_than_treat_none":
            bool(
                model_net_benefit
                > treat_none_net_benefit
            ),

        "model_better_than_both_defaults":
            bool(
                model_net_benefit
                > max(
                    treat_all_net_benefit,
                    treat_none_net_benefit,
                )
            ),

        "probability_calibration_established":
            False,

        "analysis_classification":
            "EXPLORATORY_DEVELOPMENT_EVIDENCE",

        "locked_test_accessed":
            False,

        "deployment_authorized":
            False,
    }


# ============================================================
# D9.27 — DECISION-CURVE TABLE
# ============================================================

def build_d9_decision_curve_table(
    prediction_bundle: dict[str, Any] | None = None,
) -> pd.DataFrame:
    """
    Build exploratory decision-curve evidence across the
    governed D9 threshold grid.
    """

    if prediction_bundle is None:
        prediction_bundle = (
            build_d9_validation_prediction_bundle()
        )

    y_true = prediction_bundle[
        "y_validation"
    ]

    y_probability = prediction_bundle[
        "validation_probability"
    ]

    thresholds = (
        build_d9_candidate_threshold_grid()
    )

    records = [
        calculate_d9_net_benefit(
            y_true=y_true,
            y_probability=y_probability,
            threshold=threshold,
        )
        for threshold in thresholds
        if 0.0 < threshold < 1.0
    ]

    return pd.DataFrame(
        records
    )


# ============================================================
# D9.28 — SELECTED-THRESHOLD DECISION EVIDENCE
# ============================================================

def build_d9_selected_threshold_decision_evidence(
) -> dict[str, Any]:
    """
    Evaluate net benefit specifically at the governed D9
    development operating threshold.
    """

    prediction_bundle = (
        build_d9_validation_prediction_bundle()
    )

    threshold_selection = (
        select_d9_development_threshold()
    )

    selected_threshold = (
        threshold_selection[
            "selected_threshold"
        ]
    )

    decision_evidence = (
        calculate_d9_net_benefit(
            y_true=prediction_bundle[
                "y_validation"
            ],
            y_probability=prediction_bundle[
                "validation_probability"
            ],
            threshold=selected_threshold,
        )
    )

    return {
        **decision_evidence,

        "selected_development_threshold":
            selected_threshold,

        "development_threshold_selected":
            True,

        "external_validation_completed":
            False,

        "institutional_approval_obtained":
            False,

        "locked_test_accessed":
            False,

        "deployment_authorized":
            False,
    }


# ============================================================
# D9.29 — VALIDATE DECISION-CURVE ANALYSIS
# ============================================================

def validate_d9_decision_curve_analysis() -> dict[str, Any]:
    """
    Validate D9 exploratory decision-curve evidence while
    preserving lifecycle and calibration limitations.
    """

    curve_table = (
        build_d9_decision_curve_table()
    )

    selected_evidence = (
        build_d9_selected_threshold_decision_evidence()
    )

    required_curve_columns = {
        "threshold",
        "model_net_benefit",
        "treat_all_net_benefit",
        "treat_none_net_benefit",
        "incremental_net_benefit_vs_best_default",
        "model_better_than_treat_all",
        "model_better_than_treat_none",
        "model_better_than_both_defaults",
    }

    missing_columns = (
        required_curve_columns
        - set(curve_table.columns)
    )

    checks = {
        "curve_complete":
            len(curve_table) == 50,

        "required_columns_present":
            not missing_columns,

        "selected_threshold_matches_d9":
            np.isclose(
                selected_evidence[
                    "selected_development_threshold"
                ],
                select_d9_development_threshold()[
                    "selected_threshold"
                ],
            ),

        "calibration_not_claimed":
            selected_evidence[
                "probability_calibration_established"
            ]
            is False,

        "analysis_is_exploratory":
            selected_evidence[
                "analysis_classification"
            ]
            == "EXPLORATORY_DEVELOPMENT_EVIDENCE",

        "external_validation_not_claimed":
            selected_evidence[
                "external_validation_completed"
            ]
            is False,

        "institutional_approval_not_claimed":
            selected_evidence[
                "institutional_approval_obtained"
            ]
            is False,

        "locked_test_not_accessed":
            selected_evidence[
                "locked_test_accessed"
            ]
            is False,

        "deployment_not_authorized":
            selected_evidence[
                "deployment_authorized"
            ]
            is False,
    }

    failed_checks = [
        name
        for name, passed
        in checks.items()
        if not bool(passed)
    ]

    status = (
        "PASS"
        if not failed_checks
        else "FAIL"
    )

    result = {
        "decision_curve_threshold_count":
            int(
                len(curve_table)
            ),

        "selected_threshold":
            float(
                selected_evidence[
                    "selected_development_threshold"
                ]
            ),

        "model_net_benefit":
            float(
                selected_evidence[
                    "model_net_benefit"
                ]
            ),

        "treat_all_net_benefit":
            float(
                selected_evidence[
                    "treat_all_net_benefit"
                ]
            ),

        "treat_none_net_benefit":
            float(
                selected_evidence[
                    "treat_none_net_benefit"
                ]
            ),

        "incremental_net_benefit_vs_best_default":
            float(
                selected_evidence[
                    "incremental_net_benefit_vs_best_default"
                ]
            ),

        "model_better_than_treat_all":
            bool(
                selected_evidence[
                    "model_better_than_treat_all"
                ]
            ),

        "model_better_than_treat_none":
            bool(
                selected_evidence[
                    "model_better_than_treat_none"
                ]
            ),

        "model_better_than_both_defaults":
            bool(
                selected_evidence[
                    "model_better_than_both_defaults"
                ]
            ),

        "probability_calibration_established":
            False,

        "locked_test_accessed":
            False,

        "deployment_authorized":
            False,

        "failed_checks":
            failed_checks,

        "validation_status":
            status,
    }

    if status != "PASS":
        raise RuntimeError(
            "D9 decision-curve validation failed: "
            f"{failed_checks}"
        )

    return result

# ============================================================
# D9.30 — VALIDATION PROBABILITY CALIBRATION ASSESSMENT
# ============================================================

D9_CALIBRATION_BIN_COUNT = 10
D9_CALIBRATION_METHOD = "equal_frequency_quantile_bins"


def build_d9_calibration_table(
    prediction_bundle: dict[str, Any] | None = None,
    n_bins: int = D9_CALIBRATION_BIN_COUNT,
) -> pd.DataFrame:
    """
    Build descriptive calibration evidence on VALIDATION only.

    This function evaluates the frozen D8 probabilities.
    It does NOT recalibrate or refit the model.
    """

    if prediction_bundle is None:
        prediction_bundle = (
            build_d9_validation_prediction_bundle()
        )

    y_true = np.asarray(
        prediction_bundle["y_validation"],
        dtype=np.int64,
    )

    y_probability = np.asarray(
        prediction_bundle["validation_probability"],
        dtype=np.float64,
    )

    if n_bins < 2:
        raise ValueError(
            "D9 calibration assessment requires at least "
            "two bins."
        )

    calibration_frame = pd.DataFrame(
        {
            "y_true": y_true,
            "predicted_probability": y_probability,
        }
    )

    # Equal-frequency bins provide adequate observations
    # across the risk-score distribution.
    calibration_frame["calibration_bin"] = pd.qcut(
        calibration_frame["predicted_probability"],
        q=n_bins,
        duplicates="drop",
    )

    table = (
        calibration_frame
        .groupby(
            "calibration_bin",
            observed=True,
        )
        .agg(
            encounter_count=(
                "y_true",
                "size",
            ),
            observed_readmission_rate=(
                "y_true",
                "mean",
            ),
            mean_predicted_probability=(
                "predicted_probability",
                "mean",
            ),
            minimum_predicted_probability=(
                "predicted_probability",
                "min",
            ),
            maximum_predicted_probability=(
                "predicted_probability",
                "max",
            ),
        )
        .reset_index(drop=True)
    )

    table.insert(
        0,
        "bin_number",
        np.arange(
            1,
            len(table) + 1,
        ),
    )

    table[
        "absolute_calibration_error"
    ] = (
        table[
            "observed_readmission_rate"
        ]
        -
        table[
            "mean_predicted_probability"
        ]
    ).abs()

    return table


# ============================================================
# D9.31 — CALIBRATION INTERCEPT AND SLOPE
# ============================================================

def calculate_d9_calibration_intercept_slope(
    prediction_bundle: dict[str, Any] | None = None,
) -> dict[str, float]:
    """
    Estimate calibration intercept and slope on VALIDATION.

    Ideal values:
        intercept = 0
        slope     = 1

    The calculation is diagnostic only and does not recalibrate
    the frozen D8 model.
    """

    if prediction_bundle is None:
        prediction_bundle = (
            build_d9_validation_prediction_bundle()
        )

    y_true = np.asarray(
        prediction_bundle["y_validation"],
        dtype=np.int64,
    )

    probability = np.asarray(
        prediction_bundle["validation_probability"],
        dtype=np.float64,
    )

    epsilon = np.finfo(float).eps

    clipped_probability = np.clip(
        probability,
        epsilon,
        1.0 - epsilon,
    )

    logit_probability = np.log(
        clipped_probability
        / (1.0 - clipped_probability)
    ).reshape(-1, 1)

    calibration_model = LogisticRegression(
        C=np.inf,
        solver="lbfgs",
        max_iter=1000,
   )
    calibration_model.fit(
        logit_probability,
        y_true,
    )

    intercept = float(
        calibration_model.intercept_[0]
    )

    slope = float(
        calibration_model.coef_[0][0]
    )

    return {
        "calibration_intercept":
            intercept,

        "calibration_slope":
            slope,

        "ideal_intercept":
            0.0,

        "ideal_slope":
            1.0,
    }


# ============================================================
# D9.32 — CALIBRATION ERROR SUMMARY
# ============================================================

def build_d9_calibration_summary(
    prediction_bundle: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Summarize discrimination-independent probability
    calibration evidence on VALIDATION.
    """

    if prediction_bundle is None:
        prediction_bundle = (
            build_d9_validation_prediction_bundle()
        )

    y_true = np.asarray(
        prediction_bundle["y_validation"],
        dtype=np.int64,
    )

    probability = np.asarray(
        prediction_bundle["validation_probability"],
        dtype=np.float64,
    )

    calibration_table = (
        build_d9_calibration_table(
            prediction_bundle
        )
    )

    calibration_parameters = (
        calculate_d9_calibration_intercept_slope(
            prediction_bundle
        )
    )

    brier = float(
        brier_score_loss(
            y_true,
            probability,
        )
    )

    logarithmic_loss = float(
        log_loss(
            y_true,
            probability,
            labels=[0, 1],
        )
    )

    weighted_absolute_error = float(
        np.average(
            calibration_table[
                "absolute_calibration_error"
            ],
            weights=calibration_table[
                "encounter_count"
            ],
        )
    )

    maximum_bin_error = float(
        calibration_table[
            "absolute_calibration_error"
        ].max()
    )

    mean_predicted_probability = float(
        probability.mean()
    )

    observed_prevalence = float(
        y_true.mean()
    )

    return {
        "validation_encounter_count":
            int(len(y_true)),

        "observed_prevalence":
            observed_prevalence,

        "mean_predicted_probability":
            mean_predicted_probability,

        "mean_prediction_minus_prevalence":
            float(
                mean_predicted_probability
                - observed_prevalence
            ),

        "brier_score":
            brier,

        "log_loss":
            logarithmic_loss,

        "weighted_absolute_calibration_error":
            weighted_absolute_error,

        "maximum_bin_calibration_error":
            maximum_bin_error,

        **calibration_parameters,

        "calibration_bin_count":
            int(
                len(calibration_table)
            ),

        "calibration_method":
            D9_CALIBRATION_METHOD,

        "probability_calibration_established":
            False,

        "model_recalibrated":
            False,

        "locked_test_accessed":
            False,

        "deployment_authorized":
            False,
    }


# ============================================================
# D9.33 — VALIDATE CALIBRATION ASSESSMENT
# ============================================================

def validate_d9_calibration_assessment() -> dict[str, Any]:
    """
    Validate D9 calibration diagnostics.

    PASS means the calibration assessment executed correctly.
    PASS does NOT mean the model is clinically well calibrated.
    """

    prediction_bundle = (
        build_d9_validation_prediction_bundle()
    )

    calibration_table = (
        build_d9_calibration_table(
            prediction_bundle
        )
    )

    summary = (
        build_d9_calibration_summary(
            prediction_bundle
        )
    )

    checks = {
        "validation_count_correct":
            summary[
                "validation_encounter_count"
            ]
            == D9_EXPECTED_VALIDATION_ENCOUNTERS,

        "calibration_bins_present":
            len(calibration_table) >= 2,

        "all_encounters_accounted_for":
            int(
                calibration_table[
                    "encounter_count"
                ].sum()
            )
            == D9_EXPECTED_VALIDATION_ENCOUNTERS,

        "brier_score_valid":
            (
                np.isfinite(
                    summary[
                        "brier_score"
                    ]
                )
                and
                0.0
                <= summary[
                    "brier_score"
                ]
                <= 1.0
            ),

        "log_loss_finite":
            np.isfinite(
                summary[
                    "log_loss"
                ]
            ),

        "calibration_intercept_finite":
            np.isfinite(
                summary[
                    "calibration_intercept"
                ]
            ),

        "calibration_slope_finite":
            np.isfinite(
                summary[
                    "calibration_slope"
                ]
            ),

        "no_recalibration_performed":
            summary[
                "model_recalibrated"
            ]
            is False,

        "calibration_not_yet_claimed":
            summary[
                "probability_calibration_established"
            ]
            is False,

        "locked_test_not_accessed":
            summary[
                "locked_test_accessed"
            ]
            is False,

        "deployment_not_authorized":
            summary[
                "deployment_authorized"
            ]
            is False,
    }

    failed_checks = [
        name
        for name, passed
        in checks.items()
        if not bool(passed)
    ]

    status = (
        "PASS"
        if not failed_checks
        else "FAIL"
    )

    return {
        **summary,

        "failed_checks":
            failed_checks,

        "validation_status":
            status,
    }