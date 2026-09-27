# ============================================================
# READMITAI — GOVERNED INFERENCE SERVICE
# ============================================================
#
# Runtime pathway:
#
# Clinical inputs
#       ↓
# Governed D6 feature engineering
#       ↓
# Frozen 10-feature source contract
#       ↓
# Frozen D7 preprocessor
#       ↓
# 49 transformed features
#       ↓
# Frozen D8 XGBoost model
#       ↓
# Predicted probability
#       ↓
# Frozen operating threshold = 0.12
#       ↓
# Model advisory
#
# ============================================================

from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from app.services.feature_service import (
    build_model_input,
    summarize_engineered_utilization,
)


# ============================================================
# FROZEN DEPLOYMENT CONTRACT
# ============================================================

MODEL_REGISTRY_ID = "DIABETES_READMISSION_XGB_D13_V1"
MODEL_VERSION = "1.0.0"
OPERATING_THRESHOLD = 0.12

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


# ============================================================
# LOAD FROZEN ARTIFACTS
# ============================================================

def load_frozen_artifacts():
    """
    Load the registered frozen preprocessing and model artifacts.

    This function does not fit, retrain, recalibrate, or mutate
    either artifact.
    """

    if not PREPROCESSOR_PATH.exists():
        raise FileNotFoundError(
            f"Frozen preprocessor not found: {PREPROCESSOR_PATH}"
        )

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Frozen model not found: {MODEL_PATH}"
        )

    preprocessor = joblib.load(PREPROCESSOR_PATH)
    model = joblib.load(MODEL_PATH)

    return preprocessor, model


# ============================================================
# RUN GOVERNED INFERENCE
# ============================================================

def run_readmission_inference(
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
    Run one ReadmitAI assessment through the frozen inference
    pathway and return the governed model result.
    """

    # --------------------------------------------------------
    # D6 — GOVERNED SOURCE FEATURE ENGINEERING
    # --------------------------------------------------------

    model_input = build_model_input(
        race=race,
        gender=gender,
        age=age,
        admission_type_id=admission_type_id,
        admission_source_id=admission_source_id,
        number_outpatient=number_outpatient,
        number_emergency=number_emergency,
        number_inpatient=number_inpatient,
    )

    utilization_summary = summarize_engineered_utilization(
        model_input
    )

    # --------------------------------------------------------
    # LOAD FROZEN D7 + D8 ARTIFACTS
    # --------------------------------------------------------

    preprocessor, model = load_frozen_artifacts()

    # --------------------------------------------------------
    # D7 — FROZEN PREPROCESSING
    # --------------------------------------------------------

    transformed_input = preprocessor.transform(model_input)

    if transformed_input.shape != (1, 49):
        raise RuntimeError(
            "Frozen preprocessing contract violation. "
            "Expected transformed shape (1, 49), received "
            f"{transformed_input.shape}."
        )

    # --------------------------------------------------------
    # D8 — FROZEN MODEL INFERENCE
    # --------------------------------------------------------

    probability = float(
        model.predict_proba(transformed_input)[0, 1]
    )

    if not 0.0 <= probability <= 1.0:
        raise RuntimeError(
            "Model returned an invalid probability outside [0, 1]."
        )

    # --------------------------------------------------------
    # D9 — FROZEN OPERATING-POINT LOGIC
    # --------------------------------------------------------

    priority_flag = probability >= OPERATING_THRESHOLD

    advisory = (
        "PRIORITIZE FOR HUMAN REVIEW"
        if priority_flag
        else "NO MODEL PRIORITY FLAG"
    )

    # --------------------------------------------------------
    # RUNTIME SAFETY CONTEXT
    # --------------------------------------------------------

    zero_prior_utilization = (
        utilization_summary["prior_utilization_intensity"] == 0
    )

    # --------------------------------------------------------
    # GOVERNED RESULT
    # --------------------------------------------------------

    return {
        "registry_id": MODEL_REGISTRY_ID,
        "model_version": MODEL_VERSION,

        "probability": probability,
        "operating_threshold": OPERATING_THRESHOLD,

        "priority_flag": bool(priority_flag),
        "advisory": advisory,

        "zero_prior_utilization": bool(
            zero_prior_utilization
        ),

        "utilization_summary": utilization_summary,

        "source_feature_count": int(
            model_input.shape[1]
        ),

        "transformed_feature_count": int(
            transformed_input.shape[1]
        ),

        "deployment_authorized": False,

        "clinical_decision_authority":
            "HUMAN CLINICAL DECISION REQUIRED",
    }