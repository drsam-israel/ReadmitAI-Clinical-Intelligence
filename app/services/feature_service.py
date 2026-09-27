# ============================================================
# READMITAI — GOVERNED FEATURE ENGINEERING SERVICE
# ============================================================
#
# Purpose:
# Bridge clinician-facing ReadmitAI inputs to the frozen
# 10-feature source contract used by the D7 preprocessor.
#
# IMPORTANT:
# Prior-utilization transformations are NOT reimplemented here.
# This service calls the authoritative D6 implementation in:
#     src.features.engineering.engineer_prior_utilization_features
#
# ============================================================

from typing import Any

import pandas as pd

from src.features.engineering import engineer_prior_utilization_features


# ============================================================
# FROZEN SOURCE FEATURE CONTRACT
# ============================================================

PRIMARY_CANDIDATE_FEATURES = [
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
]


# ============================================================
# BUILD GOVERNED MODEL INPUT
# ============================================================

def build_model_input(
    *,
    race: str,
    gender: str,
    age: str,
    admission_type_id: int,
    admission_source_id: int,
    number_outpatient: int,
    number_emergency: int,
    number_inpatient: int,
) -> pd.DataFrame:
    """
    Convert one clinician-entered assessment into the exact
    10-feature source contract expected by the frozen D7
    preprocessing pipeline.

    The three raw utilization counts are used only as source
    variables for the authoritative D6 governed transformation.
    """

    # --------------------------------------------------------
    # BASIC INPUT VALIDATION
    # --------------------------------------------------------

    required_categorical_inputs = {
        "race": race,
        "gender": gender,
        "age": age,
    }

    missing_inputs = [
        name
        for name, value in required_categorical_inputs.items()
        if value is None or str(value).strip() == ""
    ]

    if missing_inputs:
        raise ValueError(
            "Missing required categorical inputs: "
            f"{missing_inputs}"
        )

    utilization_values = {
        "number_outpatient": number_outpatient,
        "number_emergency": number_emergency,
        "number_inpatient": number_inpatient,
    }

    for name, value in utilization_values.items():

        if value is None:
            raise ValueError(
                f"{name} cannot be missing."
            )

        if int(value) < 0:
            raise ValueError(
                f"{name} cannot be negative."
            )

    # --------------------------------------------------------
    # CREATE SINGLE-ASSESSMENT SOURCE RECORD
    # --------------------------------------------------------

    source_df = pd.DataFrame(
        [
            {
                "race": race,
                "gender": gender,
                "age": age,
                "admission_type_id": int(admission_type_id),
                "admission_source_id": int(admission_source_id),
                "number_outpatient": int(number_outpatient),
                "number_emergency": int(number_emergency),
                "number_inpatient": int(number_inpatient),
            }
        ]
    )

    # --------------------------------------------------------
    # CALL AUTHORITATIVE D6 FEATURE ENGINEERING
    # --------------------------------------------------------

    engineered_df = engineer_prior_utilization_features(
        source_df
    )

    # --------------------------------------------------------
    # EXTRACT EXACT FROZEN SOURCE FEATURE CONTRACT
    # --------------------------------------------------------

    missing_model_features = [
        feature
        for feature in PRIMARY_CANDIDATE_FEATURES
        if feature not in engineered_df.columns
    ]

    if missing_model_features:
        raise RuntimeError(
            "Governed feature engineering failed to produce "
            "the complete frozen source feature contract: "
            f"{missing_model_features}"
        )

    model_input = engineered_df[
        PRIMARY_CANDIDATE_FEATURES
    ].copy()

    # --------------------------------------------------------
    # STRUCTURAL CONTRACT VALIDATION
    # --------------------------------------------------------

    if model_input.shape != (1, 10):
        raise RuntimeError(
            "ReadmitAI model-input contract violation. "
            f"Expected shape (1, 10), received "
            f"{model_input.shape}."
        )

    if list(model_input.columns) != PRIMARY_CANDIDATE_FEATURES:
        raise RuntimeError(
            "ReadmitAI model-input column order does not match "
            "the frozen source feature contract."
        )

    return model_input


# ============================================================
# GOVERNANCE / UI SUMMARY
# ============================================================

def summarize_engineered_utilization(
    model_input: pd.DataFrame,
) -> dict[str, Any]:
    """
    Return the governed prior-utilization transformations for
    runtime verification, audit logging, and UI interpretation.
    """

    if len(model_input) != 1:
        raise ValueError(
            "Utilization summary requires exactly one assessment."
        )

    row = model_input.iloc[0]

    return {
        "prior_outpatient_use":
            int(row["prior_outpatient_use"]),

        "prior_emergency_use":
            int(row["prior_emergency_use"]),

        "prior_inpatient_use":
            int(row["prior_inpatient_use"]),

        "prior_utilization_intensity":
            int(row["prior_utilization_intensity"]),

        "prior_utilization_domain_count":
            int(row["prior_utilization_domain_count"]),
    }