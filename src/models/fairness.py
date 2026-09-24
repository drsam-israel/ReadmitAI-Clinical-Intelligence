# ============================================================
# D10 — FAIRNESS & SUBGROUP EVALUATION
# ============================================================
#
# Purpose:
#   Evaluate whether the frozen D8 development model, operating
#   at the frozen D9 development threshold, demonstrates
#   materially different performance across clinically and
#   demographically relevant patient subgroups.
#
# Governance principles:
#   - D8 model remains frozen.
#   - D7 preprocessing remains frozen.
#   - D9 development threshold remains frozen.
#   - VALIDATION is the D10 evaluation partition.
#   - Locked TEST remains inaccessible until D14.
#   - No model retraining.
#   - No hyperparameter retuning.
#   - No preprocessing refitting.
#   - No subgroup-specific threshold optimization.
#   - No automatic mitigation.
#   - No deployment authorization.
#
# D10 evaluates disparity; it does not silently "repair" it.
# ============================================================

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


# ============================================================
# D10.01 — LIFECYCLE CONTRACT
# ============================================================

D10_STAGE = "D10"

D10_STAGE_NAME = "Fairness & Subgroup Evaluation"

D10_TARGET = "readmitted_30d"

D10_SOURCE_MODEL_STAGE = "D8"

D10_SOURCE_THRESHOLD_STAGE = "D9"

D10_EVALUATION_PARTITION = "validation"

D10_LOCKED_TEST_EVALUATION_STAGE = "D14"


# ============================================================
# D10.02 — FROZEN UPSTREAM GOVERNANCE
# ============================================================

D10_EXPECTED_SELECTED_MODEL = "xgboost"

D10_EXPECTED_MODEL_SHA256 = (
    "2FD02A54DF759EBAAF0D02D64D5ACE16A519DF016990FAC065AF3249BDA88085"
)

D10_EXPECTED_DEVELOPMENT_THRESHOLD = 0.12

D10_EXPECTED_VALIDATION_ENCOUNTERS = 15052

D10_EXPECTED_VALIDATION_POSITIVES = 1692

D10_EXPECTED_TRANSFORMED_FEATURE_COUNT = 49

D10_EXPECTED_D7_PREPROCESSOR_SHA256 = (
    "076878C0BD7C9B80897F3AA06157719A1E311165299549D83213C789CA1ECEAC"
)

D10_EXPECTED_D7_SCHEMA_SHA256 = (
    "69E0E7F19C64350A6995830E875C1303E5D14F55FD7CDA4A7D845CCDE7B756ED"
)


# ============================================================
# D10.03 — GOVERNANCE PROHIBITIONS
# ============================================================

D10_MODEL_RETRAINING_PERMITTED = False

D10_HYPERPARAMETER_RETUNING_PERMITTED = False

D10_PREPROCESSOR_REFITTING_PERMITTED = False

D10_THRESHOLD_RETUNING_PERMITTED = False

D10_SUBGROUP_SPECIFIC_THRESHOLDS_PERMITTED = False

D10_LOCKED_TEST_ACCESS_PERMITTED = False

D10_AUTOMATIC_FAIRNESS_MITIGATION_PERMITTED = False

D10_AUTONOMOUS_CLINICAL_DECISION_PERMITTED = False

D10_DEPLOYMENT_AUTHORIZED = False


# ============================================================
# D10.04 — FAIRNESS EVALUATION SCOPE
# ============================================================

D10_PRIMARY_SUBGROUP_VARIABLES = (
    "race",
    "gender",
    "age",
)

D10_PRIMARY_FAIRNESS_PERSPECTIVES = (
    "representation",
    "outcome_prevalence",
    "discrimination",
    "calibration",
    "sensitivity",
    "specificity",
    "precision",
    "negative_predictive_value",
    "false_negative_rate",
    "false_positive_rate",
    "alert_burden",
)


# ============================================================
# D10.05 — FAIRNESS INTERPRETATION CONTRACT
# ============================================================

D10_FAIRNESS_INTERPRETATION = {
    "representation": (
        "Assess whether subgroup sample sizes are sufficient "
        "for meaningful interpretation."
    ),

    "outcome_prevalence": (
        "Assess differences in observed 30-day readmission "
        "prevalence across subgroups."
    ),

    "discrimination": (
        "Assess subgroup ROC-AUC and PR-AUC where estimable."
    ),

    "calibration": (
        "Assess agreement between subgroup mean predicted "
        "risk and observed outcome prevalence, together with "
        "subgroup Brier score."
    ),

    "error_burden": (
        "Assess subgroup false-negative and false-positive "
        "burden at the frozen D9 development threshold."
    ),

    "operational_burden": (
        "Assess subgroup alert rates generated at the frozen "
        "D9 development threshold."
    ),
}


# ============================================================
# D10.06 — EXPLICIT FAIRNESS LIMITATIONS
# ============================================================

D10_FAIRNESS_LIMITATIONS = (
    "Subgroup performance differences do not by themselves "
    "establish unlawful discrimination, causal bias, or "
    "clinical inequity.",

    "Observed disparities may reflect differences in sample "
    "size, outcome prevalence, data quality, measurement, "
    "clinical pathways, or model behavior.",

    "Small subgroup estimates may be statistically unstable.",

    "D10 evaluates the held-out development VALIDATION cohort "
    "and does not establish fairness on external populations.",

    "No subgroup-specific threshold is authorized in D10.",

    "No mitigation intervention is automatically justified "
    "solely by an observed numerical disparity.",
)


# ============================================================
# D10.07 — REQUIRED SUBGROUP METRICS
# ============================================================

D10_REQUIRED_SUBGROUP_METRICS = (
    "subgroup",
    "subgroup_value",
    "encounter_count",
    "positive_count",
    "negative_count",
    "outcome_prevalence",
    "mean_predicted_probability",
    "roc_auc",
    "pr_auc",
    "brier_score",
    "true_positive",
    "false_positive",
    "true_negative",
    "false_negative",
    "sensitivity",
    "specificity",
    "precision",
    "negative_predictive_value",
    "false_negative_rate",
    "false_positive_rate",
    "predicted_positive_count",
    "predicted_positive_rate",
    "alerts_per_100_patients",
)


# ============================================================
# D10.08 — SAFE NUMERICAL HELPERS
# ============================================================

def _d10_safe_divide(
    numerator: float | int,
    denominator: float | int,
) -> float:
    """
    Safely divide two numeric values.

    Returns NaN when the denominator is zero because the metric
    is not estimable for that subgroup.
    """

    if denominator == 0:
        return float("nan")

    return float(numerator / denominator)


# ============================================================
# D10.09 — STATIC GOVERNANCE CONTRACT VALIDATION
# ============================================================

def validate_d10_static_contract() -> dict[str, Any]:
    """
    Validate the static D10 lifecycle and governance contract.

    No clinical data are accessed by this function.
    """

    checks = {
        "stage_is_d10":
            D10_STAGE == "D10",

        "target_is_readmitted_30d":
            D10_TARGET == "readmitted_30d",

        "source_model_stage_is_d8":
            D10_SOURCE_MODEL_STAGE == "D8",

        "source_threshold_stage_is_d9":
            D10_SOURCE_THRESHOLD_STAGE == "D9",

        "evaluation_partition_is_validation":
            D10_EVALUATION_PARTITION == "validation",

        "development_threshold_is_frozen":
            np.isclose(
                D10_EXPECTED_DEVELOPMENT_THRESHOLD,
                0.12,
            ),

        "model_retraining_prohibited":
            D10_MODEL_RETRAINING_PERMITTED is False,

        "hyperparameter_retuning_prohibited":
            D10_HYPERPARAMETER_RETUNING_PERMITTED is False,

        "preprocessor_refitting_prohibited":
            D10_PREPROCESSOR_REFITTING_PERMITTED is False,

        "threshold_retuning_prohibited":
            D10_THRESHOLD_RETUNING_PERMITTED is False,

        "subgroup_specific_thresholds_prohibited":
            D10_SUBGROUP_SPECIFIC_THRESHOLDS_PERMITTED
            is False,

        "locked_test_access_prohibited":
            D10_LOCKED_TEST_ACCESS_PERMITTED is False,

        "automatic_mitigation_prohibited":
            D10_AUTOMATIC_FAIRNESS_MITIGATION_PERMITTED
            is False,

        "autonomous_clinical_decision_prohibited":
            D10_AUTONOMOUS_CLINICAL_DECISION_PERMITTED
            is False,

        "deployment_prohibited":
            D10_DEPLOYMENT_AUTHORIZED is False,

        "primary_subgroups_defined":
            D10_PRIMARY_SUBGROUP_VARIABLES
            == (
                "race",
                "gender",
                "age",
            ),

        "required_metrics_defined":
            len(
                D10_REQUIRED_SUBGROUP_METRICS
            )
            == 23,
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
        "stage":
            D10_STAGE,

        "stage_name":
            D10_STAGE_NAME,

        "target":
            D10_TARGET,

        "source_model_stage":
            D10_SOURCE_MODEL_STAGE,

        "source_threshold_stage":
            D10_SOURCE_THRESHOLD_STAGE,

        "evaluation_partition":
            D10_EVALUATION_PARTITION,

        "frozen_development_threshold":
            D10_EXPECTED_DEVELOPMENT_THRESHOLD,

        "primary_subgroup_variables":
            list(
                D10_PRIMARY_SUBGROUP_VARIABLES
            ),

        "required_subgroup_metric_count":
            len(
                D10_REQUIRED_SUBGROUP_METRICS
            ),

        "model_retraining_permitted":
            D10_MODEL_RETRAINING_PERMITTED,

        "hyperparameter_retuning_permitted":
            D10_HYPERPARAMETER_RETUNING_PERMITTED,

        "preprocessor_refitting_permitted":
            D10_PREPROCESSOR_REFITTING_PERMITTED,

        "threshold_retuning_permitted":
            D10_THRESHOLD_RETUNING_PERMITTED,

        "subgroup_specific_thresholds_permitted":
            D10_SUBGROUP_SPECIFIC_THRESHOLDS_PERMITTED,

        "locked_test_access_permitted":
            D10_LOCKED_TEST_ACCESS_PERMITTED,

        "automatic_fairness_mitigation_permitted":
            D10_AUTOMATIC_FAIRNESS_MITIGATION_PERMITTED,

        "deployment_authorized":
            D10_DEPLOYMENT_AUTHORIZED,

        "failed_checks":
            failed_checks,

        "validation_status":
            status,
    }

    if status != "PASS":
        raise RuntimeError(
            "D10 static governance contract failed: "
            f"{failed_checks}"
        )

    return result


# ============================================================
# D10.10 — GOVERNED VALIDATION SUBGROUP SOURCE
# ============================================================

def build_d10_validation_subgroup_source() -> dict[str, Any]:
    """
    Load the authoritative raw VALIDATION feature frame through
    the frozen D7 READ-ONLY downstream-consumption boundary.

    D10 uses the raw D7 validation frame only for subgroup labels
    and governed encounter alignment. Model predictions continue
    to come from the frozen D8/D9 prediction pathway.

    D10 must not refit or rewrite the frozen D7 preprocessing
    artifacts and must not access the locked TEST partition.
    """

    from src.features.preprocessing import (
        load_frozen_d7_primary_preprocessing_bundle,
    )

    d7_bundle = (
        load_frozen_d7_primary_preprocessing_bundle(
            expected_preprocessor_sha256=(
                D10_EXPECTED_D7_PREPROCESSOR_SHA256
            ),
            expected_schema_sha256=(
                D10_EXPECTED_D7_SCHEMA_SHA256
            ),
        )
    )

    required_top_level_keys = {
        "fitted_bundle",
        "persistence_validation",
        "persistence_result",
        "read_only_consumption",
        "preprocessor_refitted",
        "artifact_rewritten",
        "locked_test_accessed",
    }

    missing_top_level_keys = sorted(
        required_top_level_keys.difference(
            d7_bundle.keys()
        )
    )

    if missing_top_level_keys:
        raise RuntimeError(
            "D10 received an incomplete frozen D7 preprocessing "
            "bundle. "
            f"Missing={missing_top_level_keys}"
        )

    if d7_bundle.get(
        "read_only_consumption"
    ) is not True:
        raise RuntimeError(
            "D10 requires read-only consumption of the frozen "
            "D7 preprocessing state."
        )

    if d7_bundle.get(
        "preprocessor_refitted"
    ) is not False:
        raise RuntimeError(
            "D10 detected unauthorized D7 preprocessor refitting."
        )

    if d7_bundle.get(
        "artifact_rewritten"
    ) is not False:
        raise RuntimeError(
            "D10 detected unauthorized mutation of a frozen "
            "D7 preprocessing artifact."
        )

    if d7_bundle.get(
        "locked_test_accessed"
    ) is not False:
        raise RuntimeError(
            "D10 detected unauthorized locked TEST access "
            "through the D7 boundary."
        )

    persistence_validation = d7_bundle[
        "persistence_validation"
    ]

    if persistence_validation.get(
        "validation_status"
    ) != "PASS":
        raise RuntimeError(
            "D10 cannot proceed because frozen D7 persisted "
            "preprocessing validation is not PASS."
        )

    persistence_result = d7_bundle[
        "persistence_result"
    ]

    d7_preprocessor_sha256 = persistence_result.get(
        "preprocessor_sha256"
    )

    d7_schema_sha256 = persistence_result.get(
        "schema_sha256"
    )

    if (
        d7_preprocessor_sha256
        != D10_EXPECTED_D7_PREPROCESSOR_SHA256
    ):
        raise RuntimeError(
            "D10 frozen D7 preprocessor checksum mismatch. "
            f"Expected={D10_EXPECTED_D7_PREPROCESSOR_SHA256}, "
            f"Observed={d7_preprocessor_sha256}"
        )

    if (
        d7_schema_sha256
        != D10_EXPECTED_D7_SCHEMA_SHA256
    ):
        raise RuntimeError(
            "D10 frozen D7 transformed-schema checksum mismatch. "
            f"Expected={D10_EXPECTED_D7_SCHEMA_SHA256}, "
            f"Observed={d7_schema_sha256}"
        )

    fitted_bundle = d7_bundle[
        "fitted_bundle"
    ]

    required_fitted_keys = {
        "X_validation_raw",
        "y_validation",
    }

    missing_fitted_keys = sorted(
        required_fitted_keys.difference(
            fitted_bundle.keys()
        )
    )

    if missing_fitted_keys:
        raise RuntimeError(
            "D10 received an incomplete frozen D7 fitted bundle. "
            f"Missing={missing_fitted_keys}"
        )

    X_validation_raw = fitted_bundle[
        "X_validation_raw"
    ].copy()

    y_validation_d7 = fitted_bundle[
        "y_validation"
    ].copy()

    if not isinstance(
        X_validation_raw,
        pd.DataFrame,
    ):
        raise TypeError(
            "D10 requires D7 X_validation_raw to be "
            "a pandas DataFrame."
        )

    if not isinstance(
        y_validation_d7,
        pd.Series,
    ):
        raise TypeError(
            "D10 requires D7 y_validation to be "
            "a pandas Series."
        )

    missing_subgroup_columns = [
        column
        for column in D10_PRIMARY_SUBGROUP_VARIABLES
        if column not in X_validation_raw.columns
    ]

    if missing_subgroup_columns:
        raise RuntimeError(
            "D10 subgroup columns missing from governed D7 "
            f"validation frame: {missing_subgroup_columns}"
        )

    if not X_validation_raw.index.is_unique:
        raise RuntimeError(
            "D10 requires a unique governed validation index."
        )

    if not X_validation_raw.index.equals(
        y_validation_d7.index
    ):
        raise RuntimeError(
            "D7 raw validation features and outcomes are not "
            "index-aligned."
        )

    if len(
        X_validation_raw
    ) != D10_EXPECTED_VALIDATION_ENCOUNTERS:
        raise RuntimeError(
            "Unexpected D10 raw VALIDATION encounter count. "
            f"Expected={D10_EXPECTED_VALIDATION_ENCOUNTERS}, "
            f"Observed={len(X_validation_raw)}"
        )

    if int(
        y_validation_d7.sum()
    ) != D10_EXPECTED_VALIDATION_POSITIVES:
        raise RuntimeError(
            "Unexpected D10 raw VALIDATION positive count. "
            f"Expected={D10_EXPECTED_VALIDATION_POSITIVES}, "
            f"Observed={int(y_validation_d7.sum())}"
        )

    return {
        "X_validation_raw":
            X_validation_raw,

        "y_validation_d7":
            y_validation_d7,

        "validation_index":
            X_validation_raw.index.copy(),

        "d7_preprocessor_sha256":
            d7_preprocessor_sha256,

        "d7_schema_sha256":
            d7_schema_sha256,

        "d7_read_only_consumption":
            True,

        "d7_preprocessor_refitted":
            False,

        "d7_artifact_rewritten":
            False,

        "locked_test_accessed":
            False,

        "validation_status":
            "PASS",
    }


# ============================================================
# D10.11 — FROZEN D9 PREDICTION SOURCE
# ============================================================

def build_d10_frozen_prediction_source() -> dict[str, Any]:
    """
    Obtain the frozen D9 validation prediction bundle.

    No model retraining, hyperparameter retuning, preprocessing
    refitting, threshold retuning, or locked-test access occurs.
    """

    from src.models.clinical_utility import (
        build_d9_validation_prediction_bundle,
    )

    d9_bundle = (
        build_d9_validation_prediction_bundle()
    )

    required_keys = {
        "selected_model",
        "model_sha256",
        "X_validation",
        "y_validation",
        "validation_probability",
        "validation_encounter_count",
        "validation_positive_count",
        "transformed_feature_count",
        "prediction_partition",
        "model_retrained",
        "hyperparameters_retuned",
        "preprocessor_refitted_in_d9",
        "locked_test_accessed",
        "deployment_authorized",
        "validation_status",
    }

    missing_keys = sorted(
        required_keys.difference(
            d9_bundle.keys()
        )
    )

    if missing_keys:
        raise RuntimeError(
            "D9 prediction bundle is missing required D10 "
            f"governance fields: {missing_keys}"
        )

    return d9_bundle


# ============================================================
# D10.12 — CROSS-STAGE ALIGNMENT VALIDATION
# ============================================================

def validate_d10_cross_stage_alignment() -> dict[str, Any]:
    """
    Prove that D10 subgroup labels, D7 validation outcomes, and
    frozen D9 validation probabilities refer to the same governed
    validation population and ordering.
    """

    subgroup_source = (
        build_d10_validation_subgroup_source()
    )

    d9_bundle = (
        build_d10_frozen_prediction_source()
    )

    X_raw = subgroup_source[
        "X_validation_raw"
    ]

    y_d7 = subgroup_source[
        "y_validation_d7"
    ]

    y_d9 = np.asarray(
        d9_bundle["y_validation"]
    ).reshape(-1)

    probability = np.asarray(
        d9_bundle["validation_probability"],
        dtype=float,
    ).reshape(-1)

    y_d7_array = np.asarray(
        y_d7,
        dtype=int,
    ).reshape(-1)

    checks = {
        "d7_validation_encounter_count_matches_expected":
            len(X_raw)
            == D10_EXPECTED_VALIDATION_ENCOUNTERS,

        "d9_validation_encounter_count_matches_expected":
            int(
                d9_bundle[
                    "validation_encounter_count"
                ]
            )
            == D10_EXPECTED_VALIDATION_ENCOUNTERS,

        "d7_outcome_count_matches_expected":
            len(y_d7_array)
            == D10_EXPECTED_VALIDATION_ENCOUNTERS,

        "d9_outcome_count_matches_expected":
            len(y_d9)
            == D10_EXPECTED_VALIDATION_ENCOUNTERS,

        "probability_count_matches_expected":
            len(probability)
            == D10_EXPECTED_VALIDATION_ENCOUNTERS,

        "d7_positive_count_matches_expected":
            int(y_d7_array.sum())
            == D10_EXPECTED_VALIDATION_POSITIVES,

        "d9_positive_count_matches_expected":
            int(y_d9.sum())
            == D10_EXPECTED_VALIDATION_POSITIVES,

        "d7_and_d9_outcomes_match_elementwise":
            np.array_equal(
                y_d7_array,
                y_d9.astype(int),
            ),

        "selected_model_matches_frozen_d8":
            d9_bundle["selected_model"]
            == D10_EXPECTED_SELECTED_MODEL,

        "model_sha256_matches_frozen_d8":
            d9_bundle["model_sha256"]
            == D10_EXPECTED_MODEL_SHA256,

        "transformed_feature_count_matches_expected":
            int(
                d9_bundle[
                    "transformed_feature_count"
                ]
            )
            == D10_EXPECTED_TRANSFORMED_FEATURE_COUNT,

        "prediction_partition_is_validation":
            d9_bundle["prediction_partition"]
            == D10_EVALUATION_PARTITION,

        "model_not_retrained":
            d9_bundle["model_retrained"]
            is False,

        "hyperparameters_not_retuned":
            d9_bundle["hyperparameters_retuned"]
            is False,

        "preprocessor_not_refitted":
            d9_bundle[
                "preprocessor_refitted_in_d9"
            ]
            is False,

        "locked_test_not_accessed":
            d9_bundle["locked_test_accessed"]
            is False,

        "deployment_not_authorized":
            d9_bundle["deployment_authorized"]
            is False,

        "d9_validation_status_pass":
            d9_bundle["validation_status"]
            == "PASS",

        "probabilities_are_finite":
            bool(
                np.isfinite(
                    probability
                ).all()
            ),

        "probabilities_within_unit_interval":
            bool(
                (
                    (probability >= 0.0)
                    &
                    (probability <= 1.0)
                ).all()
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
        "validation_encounter_count":
            len(X_raw),

        "validation_positive_count":
            int(
                y_d7_array.sum()
            ),

        "validation_negative_count":
            int(
                len(y_d7_array)
                - y_d7_array.sum()
            ),

        "d7_d9_outcomes_match_elementwise":
            bool(
                np.array_equal(
                    y_d7_array,
                    y_d9.astype(int),
                )
            ),

        "probability_count":
            len(probability),

        "selected_model":
            d9_bundle["selected_model"],

        "model_sha256":
            d9_bundle["model_sha256"],

        "prediction_partition":
            d9_bundle["prediction_partition"],

        "locked_test_accessed":
            d9_bundle["locked_test_accessed"],

        "failed_checks":
            failed_checks,

        "validation_status":
            status,
    }

    if status != "PASS":
        raise RuntimeError(
            "D10 cross-stage alignment validation failed: "
            f"{failed_checks}"
        )

    return result


# ============================================================
# D10.13 — GOVERNED FAIRNESS EVALUATION FRAME
# ============================================================

def build_d10_fairness_evaluation_frame() -> pd.DataFrame:
    """
    Construct the governed D10 row-level fairness evaluation frame.

    Demographic subgroup values come from the authoritative D7 raw
    validation frame.

    Outcomes and probabilities are cross-stage validated against
    the frozen D9 validation prediction pathway before attachment.
    """

    validate_d10_cross_stage_alignment()

    subgroup_source = (
        build_d10_validation_subgroup_source()
    )

    d9_bundle = (
        build_d10_frozen_prediction_source()
    )

    X_raw = subgroup_source[
        "X_validation_raw"
    ]

    y_validation = subgroup_source[
        "y_validation_d7"
    ]

    probability = np.asarray(
        d9_bundle["validation_probability"],
        dtype=float,
    ).reshape(-1)

    fairness_frame = pd.DataFrame(
        index=X_raw.index.copy()
    )

    fairness_frame.index.name = (
        "governed_validation_index"
    )

    for subgroup in D10_PRIMARY_SUBGROUP_VARIABLES:
        fairness_frame[subgroup] = (
            X_raw[subgroup].copy()
        )

    fairness_frame[D10_TARGET] = (
        y_validation.astype(int)
    )

    fairness_frame[
        "predicted_probability"
    ] = probability

    fairness_frame[
        "predicted_positive"
    ] = (
        fairness_frame[
            "predicted_probability"
        ]
        >= D10_EXPECTED_DEVELOPMENT_THRESHOLD
    ).astype(int)

    return fairness_frame


# ============================================================
# D10.14 — FAIRNESS FRAME GOVERNANCE VALIDATION
# ============================================================

def validate_d10_fairness_evaluation_frame() -> dict[str, Any]:
    """
    Validate the governed D10 fairness evaluation frame before any
    subgroup metric or disparity calculation is permitted.
    """

    frame = (
        build_d10_fairness_evaluation_frame()
    )

    required_columns = {
        "race",
        "gender",
        "age",
        D10_TARGET,
        "predicted_probability",
        "predicted_positive",
    }

    missing_columns = sorted(
        required_columns.difference(
            frame.columns
        )
    )

    race_values = sorted(
        frame["race"]
        .astype(str)
        .unique()
        .tolist()
    )

    gender_values = sorted(
        frame["gender"]
        .astype(str)
        .unique()
        .tolist()
    )

    age_values = sorted(
        frame["age"]
        .astype(str)
        .unique()
        .tolist()
    )

    checks = {
        "required_columns_present":
            len(missing_columns) == 0,

        "encounter_count_matches_expected":
            len(frame)
            == D10_EXPECTED_VALIDATION_ENCOUNTERS,

        "index_is_unique":
            frame.index.is_unique,

        "positive_count_matches_expected":
            int(
                frame[D10_TARGET].sum()
            )
            == D10_EXPECTED_VALIDATION_POSITIVES,

        "target_is_binary":
            set(
                frame[D10_TARGET]
                .dropna()
                .unique()
                .tolist()
            ).issubset(
                {0, 1}
            ),

        "prediction_is_binary":
            set(
                frame["predicted_positive"]
                .dropna()
                .unique()
                .tolist()
            ).issubset(
                {0, 1}
            ),

        "probabilities_are_finite":
            bool(
                np.isfinite(
                    frame[
                        "predicted_probability"
                    ].to_numpy(
                        dtype=float
                    )
                ).all()
            ),

        "probabilities_within_unit_interval":
            bool(
                (
                    (
                        frame[
                            "predicted_probability"
                        ]
                        >= 0.0
                    )
                    &
                    (
                        frame[
                            "predicted_probability"
                        ]
                        <= 1.0
                    )
                ).all()
            ),

        "race_preserved":
            frame["race"]
            .notna()
            .all(),

        "gender_preserved":
            frame["gender"]
            .notna()
            .all(),

        "age_preserved":
            frame["age"]
            .notna()
            .all(),

        "locked_test_not_accessed":
            D10_LOCKED_TEST_ACCESS_PERMITTED
            is False,

        "threshold_remains_frozen":
            np.isclose(
                D10_EXPECTED_DEVELOPMENT_THRESHOLD,
                0.12,
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
        "validation_encounter_count":
            len(frame),

        "validation_positive_count":
            int(
                frame[D10_TARGET].sum()
            ),

        "validation_negative_count":
            int(
                len(frame)
                - frame[D10_TARGET].sum()
            ),

        "frozen_development_threshold":
            D10_EXPECTED_DEVELOPMENT_THRESHOLD,

        "predicted_positive_count":
            int(
                frame[
                    "predicted_positive"
                ].sum()
            ),

        "predicted_positive_rate":
            float(
                frame[
                    "predicted_positive"
                ].mean()
            ),

        "race_categories":
            race_values,

        "gender_categories":
            gender_values,

        "age_categories":
            age_values,

        "missing_required_columns":
            missing_columns,

        "locked_test_accessed":
            False,

        "failed_checks":
            failed_checks,

        "validation_status":
            status,
    }

    if status != "PASS":
        raise RuntimeError(
            "D10 fairness evaluation frame validation failed: "
            f"{failed_checks}"
        )

    return result


# ============================================================
# D10.15 — SUBGROUP ANALYTICAL STABILITY POLICY
# ============================================================

D10_MIN_SUBGROUP_ENCOUNTERS = 100

D10_MIN_POSITIVE_OUTCOMES = 20

D10_MIN_NEGATIVE_OUTCOMES = 20


D10_STABILITY_POLICY = {
    "minimum_encounters":
        D10_MIN_SUBGROUP_ENCOUNTERS,

    "minimum_positive_outcomes":
        D10_MIN_POSITIVE_OUTCOMES,

    "minimum_negative_outcomes":
        D10_MIN_NEGATIVE_OUTCOMES,

    "interpretation": (
        "Subgroups failing one or more minimum-support "
        "requirements remain visible in D10 evidence but are "
        "flagged LOW_SUPPORT. Their estimates must not be used "
        "as the sole basis for governance conclusions or "
        "max-min disparity summaries."
    ),

    "fairness_standard":
        False,

    "clinical_threshold":
        False,

    "regulatory_threshold":
        False,
}


def classify_d10_subgroup_support(
    encounter_count: int,
    positive_count: int,
    negative_count: int,
) -> str:
    """
    Classify subgroup analytical support.

    This is an evidence-stability rule, not a definition of
    fairness, clinical acceptability, or regulatory compliance.
    """

    if (
        encounter_count
        < D10_MIN_SUBGROUP_ENCOUNTERS
        or positive_count
        < D10_MIN_POSITIVE_OUTCOMES
        or negative_count
        < D10_MIN_NEGATIVE_OUTCOMES
    ):
        return "LOW_SUPPORT"

    return "ADEQUATE_SUPPORT"


def validate_d10_stability_policy() -> dict[str, Any]:
    """
    Validate the D10 analytical stability policy.
    """

    checks = {
        "minimum_encounters_positive":
            D10_MIN_SUBGROUP_ENCOUNTERS > 0,

        "minimum_positive_outcomes_positive":
            D10_MIN_POSITIVE_OUTCOMES > 0,

        "minimum_negative_outcomes_positive":
            D10_MIN_NEGATIVE_OUTCOMES > 0,

        "not_defined_as_fairness_standard":
            D10_STABILITY_POLICY[
                "fairness_standard"
            ] is False,

        "not_defined_as_clinical_threshold":
            D10_STABILITY_POLICY[
                "clinical_threshold"
            ] is False,

        "not_defined_as_regulatory_threshold":
            D10_STABILITY_POLICY[
                "regulatory_threshold"
            ] is False,

        "adequate_support_logic_operational":
            classify_d10_subgroup_support(
                100,
                20,
                20,
            )
            == "ADEQUATE_SUPPORT",

        "low_encounter_support_detected":
            classify_d10_subgroup_support(
                99,
                20,
                20,
            )
            == "LOW_SUPPORT",

        "low_positive_support_detected":
            classify_d10_subgroup_support(
                100,
                19,
                81,
            )
            == "LOW_SUPPORT",

        "low_negative_support_detected":
            classify_d10_subgroup_support(
                100,
                80,
                19,
            )
            == "LOW_SUPPORT",
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
        "minimum_subgroup_encounters":
            D10_MIN_SUBGROUP_ENCOUNTERS,

        "minimum_positive_outcomes":
            D10_MIN_POSITIVE_OUTCOMES,

        "minimum_negative_outcomes":
            D10_MIN_NEGATIVE_OUTCOMES,

        "low_support_groups_retained":
            True,

        "low_support_excluded_from_primary_disparity_summary":
            True,

        "fairness_standard":
            False,

        "clinical_threshold":
            False,

        "regulatory_threshold":
            False,

        "failed_checks":
            failed_checks,

        "validation_status":
            status,
    }

    if status != "PASS":
        raise RuntimeError(
            "D10 subgroup stability policy failed: "
            f"{failed_checks}"
        )

    return result

# ============================================================
# D10.17 — SUBGROUP PERFORMANCE ENGINE
# ============================================================

def _d10_safe_roc_auc(
    y_true: np.ndarray,
    probability: np.ndarray,
) -> float:
    """
    Calculate ROC-AUC only when both outcome classes are present.
    """

    from sklearn.metrics import roc_auc_score

    if np.unique(y_true).size < 2:
        return float("nan")

    return float(
        roc_auc_score(
            y_true,
            probability,
        )
    )


def _d10_safe_pr_auc(
    y_true: np.ndarray,
    probability: np.ndarray,
) -> float:
    """
    Calculate PR-AUC only when at least one positive outcome is
    present.
    """

    from sklearn.metrics import average_precision_score

    if np.sum(y_true == 1) == 0:
        return float("nan")

    return float(
        average_precision_score(
            y_true,
            probability,
        )
    )


def calculate_d10_subgroup_metrics(
    subgroup_frame: pd.DataFrame,
    subgroup: str,
    subgroup_value: str,
) -> dict[str, Any]:
    """
    Calculate the complete governed D10 metric profile for one
    subgroup at the frozen D9 development threshold.

    No threshold optimization or subgroup-specific thresholding
    occurs here.
    """

    from sklearn.metrics import brier_score_loss

    y_true = (
        subgroup_frame[D10_TARGET]
        .to_numpy(dtype=int)
    )

    probability = (
        subgroup_frame["predicted_probability"]
        .to_numpy(dtype=float)
    )

    predicted_positive = (
        subgroup_frame["predicted_positive"]
        .to_numpy(dtype=int)
    )

    encounter_count = int(
        len(subgroup_frame)
    )

    positive_count = int(
        np.sum(y_true == 1)
    )

    negative_count = int(
        np.sum(y_true == 0)
    )

    true_positive = int(
        np.sum(
            (y_true == 1)
            & (predicted_positive == 1)
        )
    )

    false_positive = int(
        np.sum(
            (y_true == 0)
            & (predicted_positive == 1)
        )
    )

    true_negative = int(
        np.sum(
            (y_true == 0)
            & (predicted_positive == 0)
        )
    )

    false_negative = int(
        np.sum(
            (y_true == 1)
            & (predicted_positive == 0)
        )
    )

    predicted_positive_count = int(
        predicted_positive.sum()
    )

    outcome_prevalence = _d10_safe_divide(
        positive_count,
        encounter_count,
    )

    mean_predicted_probability = float(
        np.mean(probability)
    )

    roc_auc = _d10_safe_roc_auc(
        y_true,
        probability,
    )

    pr_auc = _d10_safe_pr_auc(
        y_true,
        probability,
    )

    brier_score = float(
        brier_score_loss(
            y_true,
            probability,
        )
    )

    sensitivity = _d10_safe_divide(
        true_positive,
        positive_count,
    )

    specificity = _d10_safe_divide(
        true_negative,
        negative_count,
    )

    precision = _d10_safe_divide(
        true_positive,
        true_positive + false_positive,
    )

    negative_predictive_value = _d10_safe_divide(
        true_negative,
        true_negative + false_negative,
    )

    false_negative_rate = _d10_safe_divide(
        false_negative,
        positive_count,
    )

    false_positive_rate = _d10_safe_divide(
        false_positive,
        negative_count,
    )

    predicted_positive_rate = _d10_safe_divide(
        predicted_positive_count,
        encounter_count,
    )

    alerts_per_100_patients = (
        predicted_positive_rate * 100.0
        if np.isfinite(predicted_positive_rate)
        else float("nan")
    )

    support_classification = (
        classify_d10_subgroup_support(
            encounter_count=encounter_count,
            positive_count=positive_count,
            negative_count=negative_count,
        )
    )

    return {
        "subgroup":
            subgroup,

        "subgroup_value":
            str(subgroup_value),

        "encounter_count":
            encounter_count,

        "positive_count":
            positive_count,

        "negative_count":
            negative_count,

        "outcome_prevalence":
            outcome_prevalence,

        "mean_predicted_probability":
            mean_predicted_probability,

        "roc_auc":
            roc_auc,

        "pr_auc":
            pr_auc,

        "brier_score":
            brier_score,

        "true_positive":
            true_positive,

        "false_positive":
            false_positive,

        "true_negative":
            true_negative,

        "false_negative":
            false_negative,

        "sensitivity":
            sensitivity,

        "specificity":
            specificity,

        "precision":
            precision,

        "negative_predictive_value":
            negative_predictive_value,

        "false_negative_rate":
            false_negative_rate,

        "false_positive_rate":
            false_positive_rate,

        "predicted_positive_count":
            predicted_positive_count,

        "predicted_positive_rate":
            predicted_positive_rate,

        "alerts_per_100_patients":
            alerts_per_100_patients,

        "support_classification":
            support_classification,
    }


def build_d10_subgroup_performance_table() -> pd.DataFrame:
    """
    Build the complete D10 subgroup performance table for race,
    gender, and age.

    Every observed subgroup is retained, including low-support
    groups and explicit unknown source categories.
    """

    validate_d10_fairness_evaluation_frame()
    validate_d10_stability_policy()

    frame = (
        build_d10_fairness_evaluation_frame()
    )

    records: list[dict[str, Any]] = []

    for subgroup in D10_PRIMARY_SUBGROUP_VARIABLES:

        subgroup_values = (
            frame[subgroup]
            .astype(str)
            .unique()
            .tolist()
        )

        subgroup_values = sorted(
            subgroup_values
        )

        for subgroup_value in subgroup_values:

            mask = (
                frame[subgroup]
                .astype(str)
                == subgroup_value
            )

            subgroup_frame = (
                frame.loc[mask]
                .copy()
            )

            records.append(
                calculate_d10_subgroup_metrics(
                    subgroup_frame=
                        subgroup_frame,

                    subgroup=
                        subgroup,

                    subgroup_value=
                        subgroup_value,
                )
            )

    result = pd.DataFrame(
        records
    )

    return result


# ============================================================
# D10.18 — SUBGROUP PERFORMANCE VALIDATION
# ============================================================

def validate_d10_subgroup_performance_table() -> dict[str, Any]:
    """
    Validate completeness and internal consistency of the D10
    subgroup performance table.
    """

    table = (
        build_d10_subgroup_performance_table()
    )

    required_columns = set(
        D10_REQUIRED_SUBGROUP_METRICS
    ).union(
        {
            "support_classification",
        }
    )

    missing_columns = sorted(
        required_columns.difference(
            table.columns
        )
    )

    expected_subgroup_values = {
        subgroup:
            set(
                build_d10_fairness_evaluation_frame()[
                    subgroup
                ]
                .astype(str)
                .unique()
                .tolist()
            )
        for subgroup
        in D10_PRIMARY_SUBGROUP_VARIABLES
    }

    observed_subgroup_values = {
        subgroup:
            set(
                table.loc[
                    table["subgroup"] == subgroup,
                    "subgroup_value",
                ]
                .astype(str)
                .tolist()
            )
        for subgroup
        in D10_PRIMARY_SUBGROUP_VARIABLES
    }

    subgroup_value_sets_match = all(
        observed_subgroup_values[subgroup]
        == expected_subgroup_values[subgroup]
        for subgroup
        in D10_PRIMARY_SUBGROUP_VARIABLES
    )

    expected_row_count = sum(
        len(values)
        for values
        in expected_subgroup_values.values()
    )

    encounter_totals = (
        table.groupby(
            "subgroup"
        )["encounter_count"]
        .sum()
        .to_dict()
    )

    positive_totals = (
        table.groupby(
            "subgroup"
        )["positive_count"]
        .sum()
        .to_dict()
    )

    predicted_positive_totals = (
        table.groupby(
            "subgroup"
        )["predicted_positive_count"]
        .sum()
        .to_dict()
    )

    expected_encounter_total = (
        D10_EXPECTED_VALIDATION_ENCOUNTERS
    )

    expected_positive_total = (
        D10_EXPECTED_VALIDATION_POSITIVES
    )

    expected_predicted_positive_total = (
        int(
            build_d10_fairness_evaluation_frame()[
                "predicted_positive"
            ].sum()
        )
    )

    support_values = set(
        table[
            "support_classification"
        ]
        .unique()
        .tolist()
    )

    checks = {
        "required_columns_present":
            len(missing_columns) == 0,

        "row_count_matches_observed_subgroups":
            len(table)
            == expected_row_count,

        "subgroup_value_sets_match":
            subgroup_value_sets_match,

        "all_subgroup_dimensions_present":
            set(
                table["subgroup"]
                .unique()
                .tolist()
            )
            == set(
                D10_PRIMARY_SUBGROUP_VARIABLES
            ),

        "encounter_totals_reconcile":
            all(
                int(
                    encounter_totals[subgroup]
                )
                == expected_encounter_total
                for subgroup
                in D10_PRIMARY_SUBGROUP_VARIABLES
            ),

        "positive_totals_reconcile":
            all(
                int(
                    positive_totals[subgroup]
                )
                == expected_positive_total
                for subgroup
                in D10_PRIMARY_SUBGROUP_VARIABLES
            ),

        "predicted_positive_totals_reconcile":
            all(
                int(
                    predicted_positive_totals[
                        subgroup
                    ]
                )
                == expected_predicted_positive_total
                for subgroup
                in D10_PRIMARY_SUBGROUP_VARIABLES
            ),

        "support_classification_valid":
            support_values.issubset(
                {
                    "ADEQUATE_SUPPORT",
                    "LOW_SUPPORT",
                }
            ),

        "threshold_remains_frozen":
            np.isclose(
                D10_EXPECTED_DEVELOPMENT_THRESHOLD,
                0.12,
            ),

        "locked_test_remains_inaccessible":
            D10_LOCKED_TEST_ACCESS_PERMITTED
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

    support_counts = (
        table[
            "support_classification"
        ]
        .value_counts()
        .to_dict()
    )

    result = {
        "subgroup_table_rows":
            len(table),

        "race_subgroups":
            len(
                expected_subgroup_values[
                    "race"
                ]
            ),

        "gender_subgroups":
            len(
                expected_subgroup_values[
                    "gender"
                ]
            ),

        "age_subgroups":
            len(
                expected_subgroup_values[
                    "age"
                ]
            ),

        "expected_total_rows":
            expected_row_count,

        "encounter_total_per_subgroup_dimension":
            encounter_totals,

        "positive_total_per_subgroup_dimension":
            positive_totals,

        "predicted_positive_total_per_subgroup_dimension":
            predicted_positive_totals,

        "adequate_support_rows":
            int(
                support_counts.get(
                    "ADEQUATE_SUPPORT",
                    0,
                )
            ),

        "low_support_rows":
            int(
                support_counts.get(
                    "LOW_SUPPORT",
                    0,
                )
            ),

        "frozen_development_threshold":
            D10_EXPECTED_DEVELOPMENT_THRESHOLD,

        "locked_test_accessed":
            False,

        "missing_required_columns":
            missing_columns,

        "failed_checks":
            failed_checks,

        "validation_status":
            status,
    }

    if status != "PASS":
        raise RuntimeError(
            "D10 subgroup performance validation failed: "
            f"{failed_checks}"
        )

    return result

# ============================================================
# D10.19 — GOVERNED DISPARITY ANALYSIS
# ============================================================

D10_PRIMARY_DISPARITY_METRICS = (
    "outcome_prevalence",
    "mean_predicted_probability",
    "roc_auc",
    "pr_auc",
    "brier_score",
    "sensitivity",
    "specificity",
    "precision",
    "negative_predictive_value",
    "false_negative_rate",
    "false_positive_rate",
    "predicted_positive_rate",
    "alerts_per_100_patients",
)

D10_NONINTERPRETABLE_SUBGROUP_VALUES = {
    "race": {"?"},
    "gender": set(),
    "age": set(),
}


def build_d10_primary_disparity_population() -> pd.DataFrame:
    """
    Construct the subgroup-level population eligible for primary
    descriptive disparity analysis.

    LOW_SUPPORT groups remain in the complete evidence table but
    are excluded from primary disparity ranges.

    Explicit unknown/not-recorded demographic categories are also
    retained in evidence but excluded from demographic comparisons.

    This filtering does not define fairness or unfairness.
    """

    table = build_d10_subgroup_performance_table().copy()

    table["primary_disparity_eligible"] = (
        table["support_classification"]
        == "ADEQUATE_SUPPORT"
    )

    table["exclusion_reason"] = ""

    low_support_mask = (
        table["support_classification"]
        == "LOW_SUPPORT"
    )

    table.loc[
        low_support_mask,
        "exclusion_reason",
    ] = "LOW_SUPPORT"

    for subgroup, excluded_values in (
        D10_NONINTERPRETABLE_SUBGROUP_VALUES.items()
    ):

        if not excluded_values:
            continue

        unknown_mask = (
            (table["subgroup"] == subgroup)
            &
            (
                table["subgroup_value"]
                .isin(excluded_values)
            )
        )

        table.loc[
            unknown_mask,
            "primary_disparity_eligible",
        ] = False

        table.loc[
            unknown_mask,
            "exclusion_reason",
        ] = "UNKNOWN_OR_NOT_RECORDED"

    return table


def build_d10_disparity_summary() -> pd.DataFrame:
    """
    Calculate descriptive max-min disparity ranges across eligible
    subgroup values within each demographic dimension.

    These are descriptive development-validation statistics only.
    They are not fairness thresholds, regulatory cutoffs, or
    evidence of unlawful discrimination.
    """

    table = build_d10_primary_disparity_population()

    records: list[dict[str, Any]] = []

    for subgroup in D10_PRIMARY_SUBGROUP_VARIABLES:

        eligible = table.loc[
            (table["subgroup"] == subgroup)
            &
            (
                table["primary_disparity_eligible"]
            )
        ].copy()

        for metric in D10_PRIMARY_DISPARITY_METRICS:

            metric_frame = eligible.loc[
                eligible[metric].notna()
            ].copy()

            if metric_frame.empty:
                records.append(
                    {
                        "subgroup":
                            subgroup,

                        "metric":
                            metric,

                        "eligible_group_count":
                            0,

                        "minimum_value":
                            float("nan"),

                        "minimum_group":
                            None,

                        "maximum_value":
                            float("nan"),

                        "maximum_group":
                            None,

                        "absolute_range":
                            float("nan"),
                    }
                )

                continue

            minimum_index = (
                metric_frame[metric].idxmin()
            )

            maximum_index = (
                metric_frame[metric].idxmax()
            )

            minimum_value = float(
                metric_frame.loc[
                    minimum_index,
                    metric,
                ]
            )

            maximum_value = float(
                metric_frame.loc[
                    maximum_index,
                    metric,
                ]
            )

            records.append(
                {
                    "subgroup":
                        subgroup,

                    "metric":
                        metric,

                    "eligible_group_count":
                        int(len(metric_frame)),

                    "minimum_value":
                        minimum_value,

                    "minimum_group":
                        str(
                            metric_frame.loc[
                                minimum_index,
                                "subgroup_value",
                            ]
                        ),

                    "maximum_value":
                        maximum_value,

                    "maximum_group":
                        str(
                            metric_frame.loc[
                                maximum_index,
                                "subgroup_value",
                            ]
                        ),

                    "absolute_range":
                        float(
                            maximum_value
                            - minimum_value
                        ),
                }
            )

    return pd.DataFrame(records)


# ============================================================
# D10.20 — DISPARITY ANALYSIS VALIDATION
# ============================================================

def validate_d10_disparity_analysis() -> dict[str, Any]:
    """
    Validate governance and completeness of descriptive disparity
    analysis.
    """

    population = (
        build_d10_primary_disparity_population()
    )

    summary = (
        build_d10_disparity_summary()
    )

    expected_summary_rows = (
        len(D10_PRIMARY_SUBGROUP_VARIABLES)
        *
        len(D10_PRIMARY_DISPARITY_METRICS)
    )

    low_support_in_primary = population.loc[
        (
            population[
                "support_classification"
            ]
            == "LOW_SUPPORT"
        )
        &
        (
            population[
                "primary_disparity_eligible"
            ]
        )
    ]

    unknown_race_in_primary = population.loc[
        (
            population["subgroup"]
            == "race"
        )
        &
        (
            population["subgroup_value"]
            == "?"
        )
        &
        (
            population[
                "primary_disparity_eligible"
            ]
        )
    ]

    eligible_counts = (
        population.loc[
            population[
                "primary_disparity_eligible"
            ]
        ]
        .groupby("subgroup")
        .size()
        .to_dict()
    )

    excluded_counts = (
        population.loc[
            ~population[
                "primary_disparity_eligible"
            ]
        ]
        .groupby("subgroup")
        .size()
        .to_dict()
    )

    checks = {
        "summary_row_count_correct":
            len(summary)
            == expected_summary_rows,

        "all_primary_metrics_present":
            set(summary["metric"])
            == set(
                D10_PRIMARY_DISPARITY_METRICS
            ),

        "all_subgroup_dimensions_present":
            set(summary["subgroup"])
            == set(
                D10_PRIMARY_SUBGROUP_VARIABLES
            ),

        "low_support_excluded":
            low_support_in_primary.empty,

        "unknown_race_excluded":
            unknown_race_in_primary.empty,

        "absolute_ranges_nonnegative":
            bool(
                (
                    summary[
                        "absolute_range"
                    ]
                    .dropna()
                    >= 0.0
                ).all()
            ),

        "threshold_remains_frozen":
            np.isclose(
                D10_EXPECTED_DEVELOPMENT_THRESHOLD,
                0.12,
            ),

        "subgroup_thresholds_not_created":
            D10_SUBGROUP_SPECIFIC_THRESHOLDS_PERMITTED
            is False,

        "automatic_mitigation_not_permitted":
            D10_AUTOMATIC_FAIRNESS_MITIGATION_PERMITTED
            is False,

        "locked_test_not_accessed":
            D10_LOCKED_TEST_ACCESS_PERMITTED
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
        "disparity_summary_rows":
            len(summary),

        "primary_disparity_metric_count":
            len(
                D10_PRIMARY_DISPARITY_METRICS
            ),

        "eligible_group_counts":
            eligible_counts,

        "excluded_group_counts":
            excluded_counts,

        "unknown_race_excluded":
            True,

        "low_support_groups_excluded":
            True,

        "fairness_threshold_applied":
            False,

        "subgroup_specific_thresholds_created":
            False,

        "automatic_mitigation_applied":
            False,

        "locked_test_accessed":
            False,

        "failed_checks":
            failed_checks,

        "validation_status":
            status,
    }

    if status != "PASS":
        raise RuntimeError(
            "D10 disparity analysis validation failed: "
            f"{failed_checks}"
        )

    return result

# ============================================================
# D10.22 — SUBGROUP PROPORTION UNCERTAINTY
# ============================================================

D10_CONFIDENCE_LEVEL = 0.95
D10_WILSON_Z = 1.959963984540054


def calculate_d10_wilson_interval(
    successes: int,
    trials: int,
    z: float = D10_WILSON_Z,
) -> tuple[float, float]:
    """
    Calculate a two-sided Wilson score interval for a binomial
    proportion.

    Returns NaN bounds when trials == 0.
    """

    if trials == 0:
        return (
            float("nan"),
            float("nan"),
        )

    p_hat = successes / trials

    denominator = (
        1.0
        + (z ** 2 / trials)
    )

    centre = (
        p_hat
        + (z ** 2 / (2.0 * trials))
    ) / denominator

    margin = (
        z
        * np.sqrt(
            (
                p_hat * (1.0 - p_hat) / trials
            )
            + (
                z ** 2
                / (4.0 * trials ** 2)
            )
        )
        / denominator
    )

    lower = max(
        0.0,
        centre - margin,
    )

    upper = min(
        1.0,
        centre + margin,
    )

    return (
        float(lower),
        float(upper),
    )


def build_d10_subgroup_uncertainty_table() -> pd.DataFrame:
    """
    Add 95% Wilson intervals to key subgroup proportions.

    All subgroup rows are retained. LOW_SUPPORT status remains
    explicit and is not overridden by confidence intervals.
    """

    table = (
        build_d10_primary_disparity_population()
        .copy()
    )

    records: list[dict[str, Any]] = []

    for _, row in table.iterrows():

        interval_specs = {
            "outcome_prevalence": (
                int(row["positive_count"]),
                int(row["encounter_count"]),
            ),

            "sensitivity": (
                int(row["true_positive"]),
                int(row["positive_count"]),
            ),

            "specificity": (
                int(row["true_negative"]),
                int(row["negative_count"]),
            ),

            "precision": (
                int(row["true_positive"]),
                int(
                    row["true_positive"]
                    + row["false_positive"]
                ),
            ),

            "negative_predictive_value": (
                int(row["true_negative"]),
                int(
                    row["true_negative"]
                    + row["false_negative"]
                ),
            ),

            "false_negative_rate": (
                int(row["false_negative"]),
                int(row["positive_count"]),
            ),

            "false_positive_rate": (
                int(row["false_positive"]),
                int(row["negative_count"]),
            ),

            "predicted_positive_rate": (
                int(row["predicted_positive_count"]),
                int(row["encounter_count"]),
            ),
        }

        record = {
            "subgroup":
                row["subgroup"],

            "subgroup_value":
                row["subgroup_value"],

            "encounter_count":
                int(row["encounter_count"]),

            "positive_count":
                int(row["positive_count"]),

            "negative_count":
                int(row["negative_count"]),

            "support_classification":
                row["support_classification"],

            "primary_disparity_eligible":
                bool(
                    row[
                        "primary_disparity_eligible"
                    ]
                ),

            "exclusion_reason":
                row["exclusion_reason"],
        }

        for metric, (
            successes,
            trials,
        ) in interval_specs.items():

            lower, upper = (
                calculate_d10_wilson_interval(
                    successes=successes,
                    trials=trials,
                )
            )

            record[metric] = float(
                row[metric]
            )

            record[
                f"{metric}_ci_lower"
            ] = lower

            record[
                f"{metric}_ci_upper"
            ] = upper

            record[
                f"{metric}_ci_width"
            ] = (
                float(upper - lower)
                if (
                    np.isfinite(lower)
                    and np.isfinite(upper)
                )
                else float("nan")
            )

        records.append(record)

    return pd.DataFrame(records)


# ============================================================
# D10.23 — UNCERTAINTY ANALYSIS VALIDATION
# ============================================================

def validate_d10_subgroup_uncertainty() -> dict[str, Any]:
    """
    Validate D10 Wilson confidence interval evidence.
    """

    table = (
        build_d10_subgroup_uncertainty_table()
    )

    interval_metrics = (
        "outcome_prevalence",
        "sensitivity",
        "specificity",
        "precision",
        "negative_predictive_value",
        "false_negative_rate",
        "false_positive_rate",
        "predicted_positive_rate",
    )

    required_interval_columns = set()

    for metric in interval_metrics:
        required_interval_columns.update(
            {
                metric,
                f"{metric}_ci_lower",
                f"{metric}_ci_upper",
                f"{metric}_ci_width",
            }
        )

    missing_columns = sorted(
        required_interval_columns.difference(
            table.columns
        )
    )

    bounded_checks = []

    ordered_checks = []

    point_inside_checks = []

    numerical_tolerance = 1e-12

    for metric in interval_metrics:

        lower = table[
            f"{metric}_ci_lower"
        ]

        upper = table[
            f"{metric}_ci_upper"
        ]

        point = table[metric]

        estimable = (
            lower.notna()
            & upper.notna()
            & point.notna()
        )

        bounded_checks.append(
            bool(
                (
                    (lower[estimable] >= 0.0)
                    &
                    (upper[estimable] <= 1.0)
                ).all()
            )
        )

        ordered_checks.append(
            bool(
                (
                    lower[estimable]
                    <= upper[estimable]
                ).all()
            )
        )

        point_inside_checks.append(
            bool(
                (
                    (
                        point[estimable]
                        >= (
                            lower[estimable]
                            - numerical_tolerance
                        )
                    )
                    &
                    (
                        point[estimable]
                        <= (
                            upper[estimable]
                            + numerical_tolerance
                        )
                    )
                ).all()
            )
        )

    checks = {
        "row_count_matches_subgroup_table":
            len(table) == 18,

        "required_interval_columns_present":
            len(missing_columns) == 0,

        "all_estimable_intervals_bounded":
            all(bounded_checks),

        "all_estimable_intervals_ordered":
            all(ordered_checks),

        "all_point_estimates_inside_intervals":
            all(point_inside_checks),

        "confidence_level_is_95_percent":
            np.isclose(
                D10_CONFIDENCE_LEVEL,
                0.95,
            ),

        "low_support_rows_retained":
            int(
                (
                    table[
                        "support_classification"
                    ]
                    == "LOW_SUPPORT"
                ).sum()
            )
            == 4,

        "threshold_remains_frozen":
            np.isclose(
                D10_EXPECTED_DEVELOPMENT_THRESHOLD,
                0.12,
            ),

        "locked_test_not_accessed":
            D10_LOCKED_TEST_ACCESS_PERMITTED
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
        "subgroup_rows":
            len(table),

        "interval_metric_count":
            len(interval_metrics),

        "confidence_level":
            D10_CONFIDENCE_LEVEL,

        "interval_method":
            "Wilson score interval",

        "low_support_rows_retained":
            int(
                (
                    table[
                        "support_classification"
                    ]
                    == "LOW_SUPPORT"
                ).sum()
            ),

        "missing_required_columns":
            missing_columns,

        "fairness_threshold_applied":
            False,

        "threshold_retuned":
            False,

        "locked_test_accessed":
            False,

        "failed_checks":
            failed_checks,

        "validation_status":
            status,
    }

    if status != "PASS":
        raise RuntimeError(
            "D10 subgroup uncertainty validation failed: "
            f"{failed_checks}"
        )

    return result

# ============================================================
# D10.25 — SUBGROUP CALIBRATION ANALYSIS
# ============================================================

D10_CALIBRATION_BIN_COUNT = 5
D10_CALIBRATION_METHOD = "within_subgroup_equal_frequency_quantile_bins"


def _d10_assign_quantile_bins(
    probability: pd.Series,
    requested_bins: int = D10_CALIBRATION_BIN_COUNT,
) -> pd.Series:
    """
    Assign deterministic equal-frequency calibration bins.

    Ranking is used before qcut so repeated probability values do not
    collapse bin edges unpredictably. This is evaluation-only and does
    not alter model probabilities.
    """
    if len(probability) == 0:
        return pd.Series(dtype="Int64", index=probability.index)

    effective_bins = min(int(requested_bins), int(len(probability)))
    ranks = probability.rank(method="first")

    bins = pd.qcut(
        ranks,
        q=effective_bins,
        labels=False,
        duplicates="drop",
    )

    return bins.astype("Int64") + 1


def build_d10_subgroup_calibration_table() -> pd.DataFrame:
    """
    Build within-subgroup calibration-bin evidence for race, gender,
    and age using frozen D9 validation probabilities.

    All observed subgroup values are retained, including LOW_SUPPORT
    and unknown/not-recorded categories. No recalibration is performed.
    """
    frame = build_d10_fairness_evaluation_frame().copy()
    support = build_d10_primary_disparity_population()[
        [
            "subgroup",
            "subgroup_value",
            "support_classification",
            "primary_disparity_eligible",
            "exclusion_reason",
        ]
    ].copy()

    records: list[dict[str, Any]] = []

    for subgroup in D10_PRIMARY_SUBGROUP_VARIABLES:
        subgroup_values = sorted(
            frame[subgroup].astype(str).unique().tolist()
        )

        for subgroup_value in subgroup_values:
            subgroup_frame = frame.loc[
                frame[subgroup].astype(str) == subgroup_value
            ].copy()

            subgroup_frame["calibration_bin"] = _d10_assign_quantile_bins(
                subgroup_frame["predicted_probability"],
                requested_bins=D10_CALIBRATION_BIN_COUNT,
            )

            support_row = support.loc[
                (support["subgroup"] == subgroup)
                & (support["subgroup_value"].astype(str) == subgroup_value)
            ].iloc[0]

            for calibration_bin, bin_frame in subgroup_frame.groupby(
                "calibration_bin",
                sort=True,
                observed=True,
            ):
                encounter_count = int(len(bin_frame))
                positive_count = int(bin_frame[D10_TARGET].sum())
                observed_rate = _d10_safe_divide(
                    positive_count,
                    encounter_count,
                )
                mean_predicted_probability = float(
                    bin_frame["predicted_probability"].mean()
                )
                calibration_gap = float(
                    mean_predicted_probability - observed_rate
                )

                records.append(
                    {
                        "subgroup": subgroup,
                        "subgroup_value": subgroup_value,
                        "calibration_bin": int(calibration_bin),
                        "encounter_count": encounter_count,
                        "positive_count": positive_count,
                        "observed_outcome_rate": observed_rate,
                        "mean_predicted_probability": mean_predicted_probability,
                        "calibration_gap": calibration_gap,
                        "absolute_calibration_gap": abs(calibration_gap),
                        "support_classification": support_row[
                            "support_classification"
                        ],
                        "primary_disparity_eligible": bool(
                            support_row["primary_disparity_eligible"]
                        ),
                        "exclusion_reason": support_row["exclusion_reason"],
                    }
                )

    return pd.DataFrame(records)


def build_d10_subgroup_calibration_summary() -> pd.DataFrame:
    """
    Summarize aggregate and binned calibration for each subgroup.

    Weighted absolute calibration error is descriptive validation
    evidence only. It is not a fairness threshold or deployment gate.
    """
    performance = build_d10_primary_disparity_population().copy()
    bins = build_d10_subgroup_calibration_table().copy()

    records: list[dict[str, Any]] = []

    for _, row in performance.iterrows():
        subgroup = str(row["subgroup"])
        subgroup_value = str(row["subgroup_value"])

        subgroup_bins = bins.loc[
            (bins["subgroup"] == subgroup)
            & (bins["subgroup_value"].astype(str) == subgroup_value)
        ].copy()

        total = int(subgroup_bins["encounter_count"].sum())

        if total > 0:
            weighted_absolute_calibration_error = float(
                (
                    subgroup_bins["absolute_calibration_gap"]
                    * subgroup_bins["encounter_count"]
                ).sum()
                / total
            )
            maximum_absolute_bin_gap = float(
                subgroup_bins["absolute_calibration_gap"].max()
            )
        else:
            weighted_absolute_calibration_error = float("nan")
            maximum_absolute_bin_gap = float("nan")

        aggregate_calibration_gap = float(
            row["mean_predicted_probability"]
            - row["outcome_prevalence"]
        )

        records.append(
            {
                "subgroup": subgroup,
                "subgroup_value": subgroup_value,
                "encounter_count": int(row["encounter_count"]),
                "positive_count": int(row["positive_count"]),
                "outcome_prevalence": float(row["outcome_prevalence"]),
                "mean_predicted_probability": float(
                    row["mean_predicted_probability"]
                ),
                "aggregate_calibration_gap": aggregate_calibration_gap,
                "absolute_aggregate_calibration_gap": abs(
                    aggregate_calibration_gap
                ),
                "brier_score": float(row["brier_score"]),
                "calibration_bin_count": int(len(subgroup_bins)),
                "weighted_absolute_calibration_error": (
                    weighted_absolute_calibration_error
                ),
                "maximum_absolute_bin_gap": maximum_absolute_bin_gap,
                "support_classification": row["support_classification"],
                "primary_disparity_eligible": bool(
                    row["primary_disparity_eligible"]
                ),
                "exclusion_reason": row["exclusion_reason"],
                "model_recalibrated": False,
                "probability_calibration_established": False,
            }
        )

    return pd.DataFrame(records)


# ============================================================
# D10.26 — SUBGROUP CALIBRATION VALIDATION
# ============================================================

def validate_d10_subgroup_calibration() -> dict[str, Any]:
    """Validate completeness and governance of D10 calibration evidence."""
    calibration = build_d10_subgroup_calibration_table()
    summary = build_d10_subgroup_calibration_summary()

    expected_performance = build_d10_subgroup_performance_table()
    expected_keys = set(
        zip(
            expected_performance["subgroup"].astype(str),
            expected_performance["subgroup_value"].astype(str),
        )
    )
    observed_keys = set(
        zip(
            summary["subgroup"].astype(str),
            summary["subgroup_value"].astype(str),
        )
    )

    calibration_encounter_totals = (
        calibration.groupby("subgroup")["encounter_count"].sum().to_dict()
    )

    summary_encounter_totals = (
        summary.groupby("subgroup")["encounter_count"].sum().to_dict()
    )

    finite_probability_bounds = bool(
        (
            calibration["mean_predicted_probability"].between(0.0, 1.0)
        ).all()
    )
    finite_outcome_bounds = bool(
        calibration["observed_outcome_rate"].between(0.0, 1.0).all()
    )

    checks = {
        "summary_has_18_subgroups": len(summary) == 18,
        "subgroup_keys_match_performance_table": observed_keys == expected_keys,
        "calibration_rows_present": len(calibration) > 0,
        "calibration_encounters_reconcile": all(
            int(calibration_encounter_totals[subgroup])
            == D10_EXPECTED_VALIDATION_ENCOUNTERS
            for subgroup in D10_PRIMARY_SUBGROUP_VARIABLES
        ),
        "summary_encounters_reconcile": all(
            int(summary_encounter_totals[subgroup])
            == D10_EXPECTED_VALIDATION_ENCOUNTERS
            for subgroup in D10_PRIMARY_SUBGROUP_VARIABLES
        ),
        "predicted_probabilities_bounded": finite_probability_bounds,
        "observed_rates_bounded": finite_outcome_bounds,
        "requested_bin_count_is_five": D10_CALIBRATION_BIN_COUNT == 5,
        "no_subgroup_exceeds_requested_bins": bool(
            (summary["calibration_bin_count"] <= D10_CALIBRATION_BIN_COUNT).all()
        ),
        "low_support_rows_retained": int(
            (summary["support_classification"] == "LOW_SUPPORT").sum()
        ) == 4,
        "no_recalibration_performed": bool(
            (summary["model_recalibrated"] == False).all()  # noqa: E712
        ),
        "calibration_not_declared_established": bool(
            (summary["probability_calibration_established"] == False).all()  # noqa: E712
        ),
        "threshold_remains_frozen": np.isclose(
            D10_EXPECTED_DEVELOPMENT_THRESHOLD,
            0.12,
        ),
        "locked_test_not_accessed": D10_LOCKED_TEST_ACCESS_PERMITTED is False,
    }

    failed_checks = [
        name for name, passed in checks.items() if not bool(passed)
    ]
    status = "PASS" if not failed_checks else "FAIL"

    result = {
        "subgroup_summary_rows": int(len(summary)),
        "calibration_bin_rows": int(len(calibration)),
        "requested_bins_per_subgroup": D10_CALIBRATION_BIN_COUNT,
        "calibration_method": D10_CALIBRATION_METHOD,
        "low_support_rows_retained": int(
            (summary["support_classification"] == "LOW_SUPPORT").sum()
        ),
        "model_recalibrated": False,
        "probability_calibration_established": False,
        "fairness_threshold_applied": False,
        "threshold_retuned": False,
        "locked_test_accessed": False,
        "failed_checks": failed_checks,
        "validation_status": status,
    }

    if status != "PASS":
        raise RuntimeError(
            "D10 subgroup calibration validation failed: "
            f"{failed_checks}"
        )

    return result

# ============================================================
# D10.27 — GOVERNANCE FINDINGS & REVIEW TRIGGERS
# ============================================================

D10_GOVERNANCE_FINDING_IDS = (
    "D10-F01",
    "D10-F02",
    "D10-F03",
    "D10-F04",
    "D10-F05",
    "D10-F06",
    "D10-F07",
)

D10_GOVERNANCE_DISPOSITIONS = {
    "CLINICAL_REVIEW_REQUIRED",
    "REVIEW_REQUIRED",
    "MONITOR",
    "MONITOR_AND_REVIEW",
    "INSUFFICIENT_EVIDENCE",
    "DATA_GOVERNANCE_REVIEW",
}

D10_FINDINGS_INTERPRETATION_PRINCIPLE = (
    "Observed subgroup differences are governance review triggers, not automatic "
    "findings of unfairness, unlawful discrimination, causal bias, or clinical inequity."
)


def _d10_disparity_value(
    subgroup: str,
    metric: str,
    field: str,
) -> Any:
    """Retrieve one value from the governed primary disparity summary."""
    summary = build_d10_disparity_summary()
    row = summary.loc[
        (summary["subgroup"] == subgroup)
        & (summary["metric"] == metric)
    ]
    if len(row) != 1:
        raise RuntimeError(
            f"Expected exactly one D10 disparity row for {subgroup}/{metric}; "
            f"found {len(row)}."
        )
    return row.iloc[0][field]


def _d10_calibration_row(
    subgroup: str,
    subgroup_value: str,
) -> pd.Series:
    """Retrieve one governed subgroup calibration summary row."""
    table = build_d10_subgroup_calibration_summary()
    row = table.loc[
        (table["subgroup"] == subgroup)
        & (table["subgroup_value"] == subgroup_value)
    ]
    if len(row) != 1:
        raise RuntimeError(
            f"Expected exactly one D10 calibration row for "
            f"{subgroup}/{subgroup_value}; found {len(row)}."
        )
    return row.iloc[0]


def build_d10_governance_findings_registry() -> pd.DataFrame:
    """
    Convert validated D10 evidence into an enterprise governance findings registry.

    Findings are evidence-backed review/monitoring dispositions. They do not create
    fairness standards, subgroup-specific thresholds, automatic mitigation, model
    retraining, recalibration, deployment authorization, or locked-test access.
    """
    validate_d10_subgroup_performance_table()
    validate_d10_disparity_analysis()
    validate_d10_subgroup_uncertainty()
    validate_d10_subgroup_calibration()

    performance = build_d10_subgroup_performance_table()
    population = build_d10_primary_disparity_population()
    calibration = build_d10_subgroup_calibration_summary()

    total_fn = int(performance.loc[performance["subgroup"] == "gender", "false_negative"].sum())
    total_positive = int(performance.loc[performance["subgroup"] == "gender", "positive_count"].sum())
    overall_fnr = _d10_safe_divide(total_fn, total_positive)
    overall_sensitivity = 1.0 - overall_fnr

    age_sensitivity_range = float(_d10_disparity_value("age", "sensitivity", "absolute_range"))
    age_roc_range = float(_d10_disparity_value("age", "roc_auc", "absolute_range"))
    age_alert_range = float(_d10_disparity_value("age", "alerts_per_100_patients", "absolute_range"))
    age_sensitivity_min_group = str(_d10_disparity_value("age", "sensitivity", "minimum_group"))
    age_sensitivity_max_group = str(_d10_disparity_value("age", "sensitivity", "maximum_group"))

    age_20_30 = _d10_calibration_row("age", "[20-30)")
    gender_sensitivity_range = float(_d10_disparity_value("gender", "sensitivity", "absolute_range"))
    gender_alert_range = float(_d10_disparity_value("gender", "alerts_per_100_patients", "absolute_range"))
    race_sensitivity_range = float(_d10_disparity_value("race", "sensitivity", "absolute_range"))
    race_alert_range = float(_d10_disparity_value("race", "alerts_per_100_patients", "absolute_range"))

    low_support = population.loc[
        population["support_classification"] == "LOW_SUPPORT"
    ].copy()
    low_support_labels = ", ".join(
        f"{r.subgroup}={r.subgroup_value}"
        for r in low_support.itertuples(index=False)
    )

    unknown_race = population.loc[
        (population["subgroup"] == "race")
        & (population["subgroup_value"] == "?")
    ].iloc[0]

    records = [
        {
            "finding_id": "D10-F01",
            "domain": "clinical_utility_and_safety",
            "finding": "Overall false-negative burden remains material at the frozen D9 threshold.",
            "affected_population": "validation cohort",
            "evidence": (
                f"At threshold {D10_EXPECTED_DEVELOPMENT_THRESHOLD:.2f}, overall sensitivity is "
                f"{overall_sensitivity:.6f} and false-negative rate is {overall_fnr:.6f} "
                f"({total_fn} false negatives among {total_positive} positive outcomes)."
            ),
            "evidence_strength": "HIGH",
            "disposition": "CLINICAL_REVIEW_REQUIRED",
            "required_action": (
                "Carry the false-negative burden into clinical governance, robustness, "
                "locked-test evaluation, and deployment-readiness review; do not represent "
                "the model as a high-sensitivity screening system."
            ),
            "owner": "Clinical AI Governance / Clinical Safety",
            "deployment_implication": "UNRESOLVED_BEFORE_DEPLOYMENT",
        },
        {
            "finding_id": "D10-F02",
            "domain": "age_subgroup_performance",
            "finding": "Age-related model performance and operational burden are heterogeneous.",
            "affected_population": "adequately supported age subgroups",
            "evidence": (
                f"Eligible age-group sensitivity range={age_sensitivity_range:.6f} "
                f"({age_sensitivity_min_group} to {age_sensitivity_max_group}); "
                f"ROC-AUC range={age_roc_range:.6f}; alert-burden range="
                f"{age_alert_range:.6f} alerts per 100 patients."
            ),
            "evidence_strength": "MODERATE_TO_HIGH",
            "disposition": "REVIEW_REQUIRED",
            "required_action": (
                "Carry age heterogeneity into robustness/transportability review and "
                "locked-test subgroup evaluation. Investigate data representation, pathway, "
                "measurement, and model-behavior explanations before deployment decisions."
            ),
            "owner": "Responsible AI / Clinical Model Governance",
            "deployment_implication": "REVIEW_REQUIRED_BEFORE_DEPLOYMENT",
        },
        {
            "finding_id": "D10-F03",
            "domain": "age_subgroup_calibration",
            "finding": "The age 20-30 subgroup shows a development-validation calibration signal.",
            "affected_population": "age=[20-30)",
            "evidence": (
                f"Observed prevalence={float(age_20_30['outcome_prevalence']):.6f}; mean predicted "
                f"probability={float(age_20_30['mean_predicted_probability']):.6f}; aggregate "
                f"calibration gap={float(age_20_30['aggregate_calibration_gap']):.6f}; weighted "
                f"absolute calibration error={float(age_20_30['weighted_absolute_calibration_error']):.6f}; "
                f"positive outcomes={int(age_20_30['positive_count'])}."
            ),
            "evidence_strength": "MODERATE_UNCERTAINTY_SENSITIVE",
            "disposition": "REVIEW_REQUIRED",
            "required_action": (
                "Reassess calibration stability in robustness analyses and the locked TEST set. "
                "Do not recalibrate from this subgroup signal alone."
            ),
            "owner": "Model Validation / Responsible AI",
            "deployment_implication": "REVIEW_REQUIRED_BEFORE_DEPLOYMENT",
        },
        {
            "finding_id": "D10-F04",
            "domain": "gender_subgroup_performance",
            "finding": "Gender subgroup differences are comparatively limited in development validation.",
            "affected_population": "Female and Male validation subgroups",
            "evidence": (
                f"Sensitivity range={gender_sensitivity_range:.6f}; alert-burden range="
                f"{gender_alert_range:.6f} alerts per 100 patients. Uncertainty intervals are "
                "retained in the D10 evidence package."
            ),
            "evidence_strength": "HIGH_FOR_DEVELOPMENT_VALIDATION",
            "disposition": "MONITOR",
            "required_action": (
                "Retain gender subgroup monitoring through locked-test evaluation and future "
                "post-deployment monitoring; no subgroup-specific intervention is authorized by D10."
            ),
            "owner": "Responsible AI / Model Monitoring",
            "deployment_implication": "MONITORING_REQUIREMENT",
        },
        {
            "finding_id": "D10-F05",
            "domain": "race_subgroup_performance",
            "finding": "Race subgroup performance differences warrant continued review with support-aware interpretation.",
            "affected_population": "eligible recorded-race subgroups",
            "evidence": (
                f"Among primary disparity-eligible race groups, sensitivity range="
                f"{race_sensitivity_range:.6f} and alert-burden range={race_alert_range:.6f} "
                "alerts per 100 patients. Low-support race groups and unknown race are excluded "
                "from primary disparity extrema but retained in evidence."
            ),
            "evidence_strength": "MODERATE_SUPPORT_DEPENDENT",
            "disposition": "MONITOR_AND_REVIEW",
            "required_action": (
                "Continue race subgroup evaluation in robustness and locked-test stages, retain "
                "uncertainty/support context, and avoid causal or legal conclusions from numerical "
                "differences alone."
            ),
            "owner": "Responsible AI / Data Governance / Clinical Governance",
            "deployment_implication": "REVIEW_AND_MONITORING_REQUIREMENT",
        },
        {
            "finding_id": "D10-F06",
            "domain": "subgroup_evidence_sufficiency",
            "finding": "Four subgroup rows have insufficient analytical support for primary disparity conclusions.",
            "affected_population": low_support_labels,
            "evidence": (
                f"{len(low_support)} subgroup rows fail one or more D10 minimum-support requirements "
                f"of {D10_MIN_SUBGROUP_ENCOUNTERS} encounters, {D10_MIN_POSITIVE_OUTCOMES} positives, "
                f"and {D10_MIN_NEGATIVE_OUTCOMES} negatives."
            ),
            "evidence_strength": "INSUFFICIENT_FOR_PRIMARY_DISPARITY_CONCLUSION",
            "disposition": "INSUFFICIENT_EVIDENCE",
            "required_action": (
                "Retain these groups in all evidence, avoid primary disparity conclusions from their "
                "point estimates, and seek additional evidence in later validation/monitoring."
            ),
            "owner": "Model Validation / Responsible AI",
            "deployment_implication": "EVIDENCE_LIMITATION_TO_CARRY_FORWARD",
        },
        {
            "finding_id": "D10-F07",
            "domain": "demographic_data_quality",
            "finding": "Unknown/not-recorded race remains a material demographic data-quality category.",
            "affected_population": "race=?",
            "evidence": (
                f"Unknown/not-recorded race contains {int(unknown_race['encounter_count'])} encounters "
                f"and {int(unknown_race['positive_count'])} positive outcomes. It is retained in evidence "
                "but excluded from primary demographic disparity comparisons."
            ),
            "evidence_strength": "HIGH_FOR_DATA_QUALITY_OBSERVATION",
            "disposition": "DATA_GOVERNANCE_REVIEW",
            "required_action": (
                "Investigate demographic data capture, missingness provenance, and monitoring requirements. "
                "Do not merge unknown race into an observed race category."
            ),
            "owner": "Data Governance / Data Quality",
            "deployment_implication": "DATA_QUALITY_ACTION_REQUIRED",
        },
    ]

    registry = pd.DataFrame(records)
    registry["fairness_violation_determined"] = False
    registry["causal_bias_determined"] = False
    registry["subgroup_threshold_change_authorized"] = False
    registry["automatic_mitigation_authorized"] = False
    registry["model_recalibration_authorized"] = False
    registry["deployment_authorized"] = False
    registry["locked_test_accessed"] = False
    return registry


# ============================================================
# D10.28 — GOVERNANCE FINDINGS VALIDATION
# ============================================================

def validate_d10_governance_findings_registry() -> dict[str, Any]:
    """Validate completeness and guardrails of the D10 governance findings registry."""
    registry = build_d10_governance_findings_registry()

    required_columns = {
        "finding_id",
        "domain",
        "finding",
        "affected_population",
        "evidence",
        "evidence_strength",
        "disposition",
        "required_action",
        "owner",
        "deployment_implication",
        "fairness_violation_determined",
        "causal_bias_determined",
        "subgroup_threshold_change_authorized",
        "automatic_mitigation_authorized",
        "model_recalibration_authorized",
        "deployment_authorized",
        "locked_test_accessed",
    }

    missing_columns = sorted(required_columns.difference(registry.columns))
    observed_ids = tuple(registry["finding_id"].tolist())
    dispositions = set(registry["disposition"].tolist())

    checks = {
        "required_columns_present": len(missing_columns) == 0,
        "exact_finding_ids_present": observed_ids == D10_GOVERNANCE_FINDING_IDS,
        "finding_ids_unique": bool(registry["finding_id"].is_unique),
        "seven_findings_present": len(registry) == 7,
        "dispositions_governed": dispositions.issubset(D10_GOVERNANCE_DISPOSITIONS),
        "no_fairness_violation_declared": bool((~registry["fairness_violation_determined"]).all()),
        "no_causal_bias_declared": bool((~registry["causal_bias_determined"]).all()),
        "no_subgroup_threshold_change_authorized": bool((~registry["subgroup_threshold_change_authorized"]).all()),
        "no_automatic_mitigation_authorized": bool((~registry["automatic_mitigation_authorized"]).all()),
        "no_recalibration_authorized": bool((~registry["model_recalibration_authorized"]).all()),
        "deployment_not_authorized": bool((~registry["deployment_authorized"]).all()),
        "locked_test_not_accessed": bool((~registry["locked_test_accessed"]).all()),
        "global_threshold_remains_frozen": np.isclose(D10_EXPECTED_DEVELOPMENT_THRESHOLD, 0.12),
        "source_policy_prohibits_subgroup_thresholds": D10_SUBGROUP_SPECIFIC_THRESHOLDS_PERMITTED is False,
        "source_policy_prohibits_automatic_mitigation": D10_AUTOMATIC_FAIRNESS_MITIGATION_PERMITTED is False,
        "source_policy_prohibits_deployment": D10_DEPLOYMENT_AUTHORIZED is False,
    }

    failed_checks = [name for name, passed in checks.items() if not bool(passed)]
    status = "PASS" if not failed_checks else "FAIL"

    disposition_counts = registry["disposition"].value_counts().to_dict()
    result = {
        "governance_finding_count": int(len(registry)),
        "finding_ids": list(observed_ids),
        "disposition_counts": {str(k): int(v) for k, v in disposition_counts.items()},
        "fairness_violation_determined": False,
        "causal_bias_determined": False,
        "subgroup_specific_thresholds_created": False,
        "automatic_mitigation_applied": False,
        "model_recalibrated": False,
        "deployment_authorized": False,
        "locked_test_accessed": False,
        "missing_required_columns": missing_columns,
        "failed_checks": failed_checks,
        "validation_status": status,
    }

    if status != "PASS":
        raise RuntimeError(
            "D10 governance findings validation failed: "
            f"{failed_checks}"
        )
    return result


# ============================================================
# D10.29 — COMMAND-LINE GOVERNANCE VALIDATION
# ============================================================

if __name__ == "__main__":

    import pprint

    print(
        "\nD10 STATIC GOVERNANCE CONTRACT"
    )
    print("=" * 60)

    pprint.pp(
        validate_d10_static_contract()
    )

    print(
        "\nD10 CROSS-STAGE ALIGNMENT"
    )
    print("=" * 60)

    pprint.pp(
        validate_d10_cross_stage_alignment()
    )

    print(
        "\nD10 FAIRNESS EVALUATION FRAME"
    )
    print("=" * 60)

    pprint.pp(
        validate_d10_fairness_evaluation_frame()
    )

    print(
        "\nD10 SUBGROUP ANALYTICAL STABILITY POLICY"
    )
    print("=" * 60)

    pprint.pp(
        validate_d10_stability_policy()
    )
    print(
        "\nD10 SUBGROUP PERFORMANCE VALIDATION"
    )
    print("=" * 60)

    pprint.pp(
        validate_d10_subgroup_performance_table()
    )

    print(
        "\nD10 SUBGROUP PERFORMANCE TABLE"
    )
    print("=" * 60)

    subgroup_table = (
        build_d10_subgroup_performance_table()
    )

    display_columns = [
        "subgroup",
        "subgroup_value",
        "encounter_count",
        "positive_count",
        "outcome_prevalence",
        "roc_auc",
        "pr_auc",
        "brier_score",
        "sensitivity",
        "specificity",
        "precision",
        "false_negative_rate",
        "false_positive_rate",
        "alerts_per_100_patients",
        "support_classification",
    ]

    print(
        subgroup_table[
            display_columns
        ].to_string(
            index=False
        )
    )
    print(
        "\nD10 DISPARITY ANALYSIS VALIDATION"
    )
    print("=" * 60)

    pprint.pp(
        validate_d10_disparity_analysis()
    )

    print(
        "\nD10 PRIMARY DISPARITY SUMMARY"
    )
    print("=" * 60)

    disparity_summary = (
        build_d10_disparity_summary()
    )

    print(
        disparity_summary.to_string(
            index=False
        )
    )

    print(
        "\nD10 SUBGROUP UNCERTAINTY VALIDATION"
    )
    print("=" * 60)

    pprint.pp(
        validate_d10_subgroup_uncertainty()
    )

    print(
        "\nD10 SENSITIVITY UNCERTAINTY TABLE"
    )
    print("=" * 60)

    uncertainty_table = (
        build_d10_subgroup_uncertainty_table()
    )

    uncertainty_display = [
        "subgroup",
        "subgroup_value",
        "positive_count",
        "sensitivity",
        "sensitivity_ci_lower",
        "sensitivity_ci_upper",
        "false_negative_rate",
        "false_negative_rate_ci_lower",
        "false_negative_rate_ci_upper",
        "support_classification",
        "primary_disparity_eligible",
    ]

    print(
        uncertainty_table[
            uncertainty_display
        ].to_string(
            index=False
        )
    )

    print(
        "\nD10 SUBGROUP CALIBRATION VALIDATION"
    )
    print("=" * 60)

    pprint.pp(
        validate_d10_subgroup_calibration()
    )

    print(
        "\nD10 SUBGROUP CALIBRATION SUMMARY"
    )
    print("=" * 60)

    calibration_summary = (
        build_d10_subgroup_calibration_summary()
    )

    calibration_display = [
        "subgroup",
        "subgroup_value",
        "encounter_count",
        "positive_count",
        "outcome_prevalence",
        "mean_predicted_probability",
        "aggregate_calibration_gap",
        "brier_score",
        "weighted_absolute_calibration_error",
        "maximum_absolute_bin_gap",
        "support_classification",
        "primary_disparity_eligible",
    ]

    print(
        calibration_summary[
            calibration_display
        ].to_string(
            index=False
        )
    )

    print(
        "\nD10 GOVERNANCE FINDINGS VALIDATION"
    )
    print("=" * 60)

    pprint.pp(
        validate_d10_governance_findings_registry()
    )

    print(
        "\nD10 GOVERNANCE FINDINGS REGISTRY"
    )
    print("=" * 60)

    findings_registry = (
        build_d10_governance_findings_registry()
    )

    findings_display = [
        "finding_id",
        "domain",
        "affected_population",
        "evidence_strength",
        "disposition",
        "deployment_implication",
    ]

    print(
        findings_registry[
            findings_display
        ].to_string(
            index=False
        )
    )