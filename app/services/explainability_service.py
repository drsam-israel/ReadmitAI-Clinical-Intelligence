"""
ReadmitAI Clinical Intelligence
Governed Patient-Level Explainability Service

Purpose
-------
Generate patient-level SHAP explanations for the frozen
30-day diabetes readmission model.

Governance controls
-------------------
- Uses the frozen D7 preprocessor.
- Uses the frozen D8 XGBoost model.
- Uses D12 TreeExplainer methodology.
- Reuses the authoritative D12 transformed-feature-to-source-family mapper.
- Does not retrain the model.
- Does not refit the preprocessor.
- Does not alter the operating threshold.
- Does not interpret SHAP values as probability-point changes.
- Does not interpret feature attribution as clinical causality.
"""

from pathlib import Path
from typing import Any

import joblib
import numpy as np
import shap

from app.services.feature_service import build_model_input
from src.models.explainability import (
    map_d12_transformed_feature_to_source_family,
)


# ============================================================
# FROZEN SYSTEM CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PREPROCESSOR_PATH = (
    PROJECT_ROOT
    / "artifacts"
    / "preprocessors"
    / "D7_primary_preprocessor.joblib"
)

MODEL_PATH = (
    PROJECT_ROOT
    / "artifacts"
    / "models"
    / "D8_selected_development_model.joblib"
)

TRANSFORMED_SCHEMA_PATH = (
    PROJECT_ROOT
    / "artifacts"
    / "preprocessors"
    / "D7_transformed_feature_schema.txt"
)

EXPECTED_SOURCE_FEATURE_COUNT = 10
EXPECTED_TRANSFORMED_FEATURE_COUNT = 49


# ============================================================
# LOAD FROZEN EXPLAINABILITY ARTIFACTS
# ============================================================

def load_explainability_artifacts():
    """
    Load the frozen D7 preprocessor and D8 model.

    No fitting, retraining, calibration, or mutation occurs.
    """

    if not PREPROCESSOR_PATH.exists():
        raise FileNotFoundError(
            f"Frozen D7 preprocessor not found: {PREPROCESSOR_PATH}"
        )

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Frozen D8 model not found: {MODEL_PATH}"
        )

    preprocessor = joblib.load(PREPROCESSOR_PATH)
    model = joblib.load(MODEL_PATH)

    return preprocessor, model


# ============================================================
# TRANSFORMED FEATURE NAMES
# ============================================================

def get_transformed_feature_names(
    preprocessor,
) -> list[str]:
    """
    Recover the governed D7 transformed feature names.

    The frozen preprocessor is treated as the primary runtime source.
    The persisted D7 schema is used as a fallback.
    """

    try:
        names = list(
            preprocessor.get_feature_names_out()
        )
    except Exception:
        if not TRANSFORMED_SCHEMA_PATH.exists():
            raise RuntimeError(
                "Unable to recover governed D7 transformed feature names."
            )

        names = [
            line.strip()
            for line in TRANSFORMED_SCHEMA_PATH.read_text(
                encoding="utf-8"
            ).splitlines()
            if line.strip()
        ]

    if len(names) != EXPECTED_TRANSFORMED_FEATURE_COUNT:
        raise RuntimeError(
            "Unexpected transformed feature count. "
            f"Expected={EXPECTED_TRANSFORMED_FEATURE_COUNT}, "
            f"Observed={len(names)}"
        )

    return names


# ============================================================
# NUMERICALLY STABLE LOGISTIC TRANSFORMATION
# ============================================================

def _expit(raw_value: float) -> float:
    """
    Convert raw XGBoost margin/log-odds to probability.
    """

    raw_value = float(raw_value)

    if raw_value >= 0.0:
        return float(
            1.0 / (1.0 + np.exp(-raw_value))
        )

    exp_value = np.exp(raw_value)

    return float(
        exp_value / (1.0 + exp_value)
    )


# ============================================================
# LIVE PATIENT EXPLANATION
# ============================================================

def explain_readmission_prediction(
    *,
    race: str,
    gender: str,
    age: str,
    admission_type_id: int,
    admission_source_id: int,
    number_outpatient: int,
    number_emergency: int,
    number_inpatient: int,
) -> dict[str, Any]:
    """
    Generate a governed patient-level TreeSHAP explanation.

    SHAP values are calculated in raw XGBoost model-output
    (margin/log-odds) space.

    They are NOT direct probability-point changes and must not
    be interpreted as causal clinical effects.
    """

    # --------------------------------------------------------
    # 1. Build governed D6/D7 source-feature record
    # --------------------------------------------------------

    source_df = build_model_input(
        race=race,
        gender=gender,
        age=age,
        admission_type_id=admission_type_id,
        admission_source_id=admission_source_id,
        number_outpatient=number_outpatient,
        number_emergency=number_emergency,
        number_inpatient=number_inpatient,
    )

    if source_df.shape != (
        1,
        EXPECTED_SOURCE_FEATURE_COUNT,
    ):
        raise RuntimeError(
            "Unexpected governed source-feature shape. "
            f"Observed={source_df.shape}"
        )

    # --------------------------------------------------------
    # 2. Load frozen D7/D8 artifacts
    # --------------------------------------------------------

    preprocessor, model = (
        load_explainability_artifacts()
    )

    # --------------------------------------------------------
    # 3. Apply frozen D7 preprocessing
    # --------------------------------------------------------

    transformed = preprocessor.transform(
        source_df
    )

    if hasattr(transformed, "toarray"):
        transformed = transformed.toarray()

    transformed = np.asarray(
        transformed,
        dtype=float,
    )

    expected_shape = (
        1,
        EXPECTED_TRANSFORMED_FEATURE_COUNT,
    )

    if transformed.shape != expected_shape:
        raise RuntimeError(
            "Unexpected D7 transformed feature shape. "
            f"Expected={expected_shape}, "
            f"Observed={transformed.shape}"
        )

    # --------------------------------------------------------
    # 4. Frozen model probability
    # --------------------------------------------------------

    probability = float(
        model.predict_proba(
            transformed
        )[0, 1]
    )

    # --------------------------------------------------------
    # 5. D12-governed TreeSHAP method
    # --------------------------------------------------------

    explainer = shap.TreeExplainer(
        model
    )

    explanation = explainer(
        transformed
    )

    shap_values = np.asarray(
        explanation.values,
        dtype=float,
    )

    base_values = np.asarray(
        explanation.base_values,
        dtype=float,
    )

    if shap_values.shape != expected_shape:
        raise RuntimeError(
            "Unexpected patient SHAP shape. "
            f"Expected={expected_shape}, "
            f"Observed={shap_values.shape}"
        )

    if base_values.size != 1:
        raise RuntimeError(
            "Unexpected patient SHAP base-value shape."
        )

    if not np.isfinite(shap_values).all():
        raise RuntimeError(
            "Patient SHAP values contain non-finite values."
        )

    base_value = float(
        base_values.reshape(-1)[0]
    )

    # --------------------------------------------------------
    # 6. Verify SHAP additivity against frozen prediction
    # --------------------------------------------------------

    shap_sum = float(
        shap_values[0].sum()
    )

    reconstructed_raw_output = float(
        base_value + shap_sum
    )

    reconstructed_probability = _expit(
        reconstructed_raw_output
    )

    probability_reconstruction_error = abs(
        reconstructed_probability
        - probability
    )

    if probability_reconstruction_error > 1e-6:
        raise RuntimeError(
            "Patient SHAP explanation failed governed "
            "probability reconstruction. "
            f"Error={probability_reconstruction_error}"
        )

    # --------------------------------------------------------
    # 7. Recover governed transformed feature names
    # --------------------------------------------------------

    feature_names = (
        get_transformed_feature_names(
            preprocessor
        )
    )

    # --------------------------------------------------------
    # 8. Aggregate 49 transformed features into the
    #    10 governed D12 source-feature families
    # --------------------------------------------------------

    source_family_attribution: dict[str, float] = {}

    transformed_rows = []

    for index, feature_name in enumerate(
        feature_names
    ):

        shap_value = float(
            shap_values[0, index]
        )

        source_family = (
            map_d12_transformed_feature_to_source_family(
                feature_name
            )
        )

        source_family_attribution[
            source_family
        ] = (
            source_family_attribution.get(
                source_family,
                0.0,
            )
            + shap_value
        )

        transformed_rows.append(
            {
                "transformed_feature": feature_name,
                "source_feature_family": source_family,
                "shap_value": shap_value,
                "absolute_shap_value": abs(
                    shap_value
                ),
            }
        )

    # --------------------------------------------------------
    # 9. Validate source-family aggregation
    # --------------------------------------------------------

    family_sum = float(
        sum(
            source_family_attribution.values()
        )
    )

    if not np.isclose(
        family_sum,
        shap_sum,
        rtol=0.0,
        atol=1e-12,
    ):
        raise RuntimeError(
            "Source-family SHAP aggregation failed "
            "encounter-level additivity."
        )

    # --------------------------------------------------------
    # 10. Prepare clinician-facing ranked contributions
    # --------------------------------------------------------

    source_family_rows = [
        {
            "source_feature_family":
                source_family,
            "shap_value":
                float(shap_value),
            "absolute_shap_value":
                abs(float(shap_value)),
            "direction":
                (
                    "higher_model_output"
                    if shap_value > 0
                    else
                    "lower_model_output"
                    if shap_value < 0
                    else
                    "neutral"
                ),
        }
        for source_family, shap_value
        in source_family_attribution.items()
    ]

    source_family_rows = sorted(
        source_family_rows,
        key=lambda row:
            row["absolute_shap_value"],
        reverse=True,
    )

    # --------------------------------------------------------
    # 11. Governed response
    # --------------------------------------------------------

    return {
        "probability":
            probability,

        "base_value":
            base_value,

        "shap_sum":
            shap_sum,

        "reconstructed_raw_output":
            reconstructed_raw_output,

        "reconstructed_probability":
            reconstructed_probability,

        "probability_reconstruction_error":
            probability_reconstruction_error,

        "source_family_contributions":
            source_family_rows,

        "transformed_feature_contributions":
            transformed_rows,

        "source_feature_count":
            EXPECTED_SOURCE_FEATURE_COUNT,

        "transformed_feature_count":
            EXPECTED_TRANSFORMED_FEATURE_COUNT,

        "model_output_space":
            "raw_margin_log_odds",

        "probability_link":
            "logistic_expit",

        "shap_values_are_probability_point_changes":
            False,

        "feature_attribution_is_causal":
            False,

        "clinical_decision_replaced":
            False,

        "deployment_authorized":
            False,
    }