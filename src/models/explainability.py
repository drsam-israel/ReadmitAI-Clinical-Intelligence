# ============================================================
# D12 — EXPLAINABILITY & MODEL INTERPRETATION GOVERNANCE
# ============================================================
#
# Purpose:
# Establish the governed explainability and model-interpretation
# layer for the frozen diabetes 30-day readmission model.
#
# D12 does NOT:
# - retrain the model
# - retune hyperparameters
# - refit preprocessing
# - change the D9 threshold
# - recalibrate probabilities
# - create subgroup-specific thresholds
# - access the locked TEST partition
# - authorize clinical deployment
#
# D12 consumes the frozen development-stage system and produces
# explainability evidence for governance and clinical review.
# ============================================================

from __future__ import annotations

from typing import Any


# ============================================================
# D12.01 — FROZEN EXPLAINABILITY SYSTEM BOUNDARY
# ============================================================

D12_STAGE_ID = "D12"

D12_STAGE_NAME = (
    "Explainability & Model Interpretation Governance"
)

D12_EXPECTED_MODEL_NAME = "xgboost"

D12_EXPECTED_MODEL_SHA256 = (
    "2FD02A54DF759EBAAF0D02D64D5ACE16A519DF016990FAC065AF3249BDA88085"
)

D12_EXPECTED_D7_PREPROCESSOR_SHA256 = (
    "076878C0BD7C9B80897F3AA06157719A1E311165299549D83213C789CA1ECEAC"
)

D12_EXPECTED_D7_SCHEMA_SHA256 = (
    "69E0E7F19C64350A6995830E875C1303E5D14F55FD7CDA4A7D845CCDE7B756ED"
)

D12_EXPECTED_DEVELOPMENT_THRESHOLD = 0.12

D12_EXPECTED_VALIDATION_ENCOUNTERS = 15052
D12_EXPECTED_VALIDATION_POSITIVES = 1692
D12_EXPECTED_VALIDATION_NEGATIVES = 13360

D12_EXPECTED_TRANSFORMED_FEATURE_COUNT = 49

D12_SOURCE_LIFECYCLE_STAGE = "D11"

D12_SOURCE_GIT_COMMIT = "9fb775c"


# ============================================================
# D12.02 — EXPLAINABILITY GOVERNANCE OBJECTIVE
# ============================================================

D12_PRIMARY_GOVERNANCE_QUESTION = (
    "Can the frozen model's predictions be explained at global, "
    "feature, patient, and subgroup or slice levels in a clinically "
    "interpretable and governance-defensible manner, and do those "
    "explanations help investigate the D11 robustness findings "
    "without changing the frozen model?"
)


# ============================================================
# D12.03 — PERMITTED EXPLAINABILITY ACTIVITIES
# ============================================================

D12_PERMITTED_ACTIVITIES = (
    "global_feature_importance",
    "shap_global_attribution",
    "shap_feature_directionality",
    "shap_dependence_analysis",
    "local_patient_explanation",
    "utilization_feature_attribution_review",
    "age_attribution_review",
    "admission_source_attribution_review",
    "attribution_stability_assessment",
    "clinical_plausibility_review",
    "explanation_limitations_assessment",
)


# ============================================================
# D12.04 — PROHIBITED MODEL/GOVERNANCE MUTATIONS
# ============================================================

D12_PROHIBITED_ACTIVITIES = (
    "model_retraining",
    "hyperparameter_retuning",
    "preprocessor_refitting",
    "feature_reengineering",
    "feature_selection_change",
    "threshold_retuning",
    "probability_recalibration",
    "subgroup_specific_thresholding",
    "locked_test_access",
    "automatic_model_mitigation",
    "autonomous_clinical_decision_making",
    "deployment_authorization",
)


# ============================================================
# D12.05 — D11 MANDATORY CARRY-FORWARD QUESTIONS
# ============================================================

D12_D11_CARRY_FORWARD_QUESTIONS = (
    (
        "Investigate the contribution of prior-utilization features "
        "to the observed operating-point heterogeneity without "
        "changing the frozen D9 threshold."
    ),
    (
        "Examine feature-attribution behavior for admission_source_id "
        "and age without treating attribution values as causal effects."
    ),
    (
        "Assess whether the observed utilization pattern is consistent "
        "with model feature dependence, population case-mix differences, "
        "or both, while avoiding causal conclusions from D11 evidence."
    ),
    (
        "Retain low-support observed slices as interpretation "
        "limitations rather than strong evidence."
    ),
    (
        "Preserve relevant findings for later locked TEST reassessment "
        "during D14 without validation-driven threshold retuning."
    ),
    (
        "Do not treat explainability evidence as authorization for "
        "clinical deployment."
    ),
)


# ============================================================
# D12.06 — INTERPRETATION SAFEGUARDS
# ============================================================

D12_INTERPRETATION_SAFEGUARDS = (
    "Feature attribution is not causal inference.",
    "High feature importance does not establish clinical appropriateness.",
    "Low feature importance does not establish clinical irrelevance.",
    "SHAP values describe model behavior, not biological mechanism.",
    "Local explanations must not be generalized to the whole population.",
    "Global explanations must not substitute for patient-level review.",
    "Observed subgroup attribution differences may reflect case mix.",
    "Explainability does not establish external transportability.",
    "Explainability does not establish prospective clinical effectiveness.",
    "Explainability does not authorize autonomous clinical decisions.",
)


# ============================================================
# D12.07 — STATIC SYSTEM BOUNDARY
# ============================================================

def build_d12_static_system_boundary() -> dict[str, Any]:
    """
    Build the immutable governance boundary for D12.

    This function defines what D12 is allowed to inspect and what
    lifecycle mutations are explicitly prohibited.
    """

    return {
        "stage_id": D12_STAGE_ID,
        "stage_name": D12_STAGE_NAME,

        "source_lifecycle_stage":
            D12_SOURCE_LIFECYCLE_STAGE,

        "source_git_commit":
            D12_SOURCE_GIT_COMMIT,

        "model_name":
            D12_EXPECTED_MODEL_NAME,

        "expected_model_sha256":
            D12_EXPECTED_MODEL_SHA256,

        "expected_d7_preprocessor_sha256":
            D12_EXPECTED_D7_PREPROCESSOR_SHA256,

        "expected_d7_schema_sha256":
            D12_EXPECTED_D7_SCHEMA_SHA256,

        "development_threshold":
            D12_EXPECTED_DEVELOPMENT_THRESHOLD,

        "validation_encounters":
            D12_EXPECTED_VALIDATION_ENCOUNTERS,

        "validation_positives":
            D12_EXPECTED_VALIDATION_POSITIVES,

        "validation_negatives":
            D12_EXPECTED_VALIDATION_NEGATIVES,

        "transformed_feature_count":
            D12_EXPECTED_TRANSFORMED_FEATURE_COUNT,

        "primary_governance_question":
            D12_PRIMARY_GOVERNANCE_QUESTION,

        "permitted_activities":
            list(D12_PERMITTED_ACTIVITIES),

        "prohibited_activities":
            list(D12_PROHIBITED_ACTIVITIES),

        "d11_carry_forward_questions":
            list(D12_D11_CARRY_FORWARD_QUESTIONS),

        "interpretation_safeguards":
            list(D12_INTERPRETATION_SAFEGUARDS),

        # ----------------------------------------------------
        # Immutable lifecycle controls
        # ----------------------------------------------------

        "model_retrained":
            False,

        "hyperparameters_retuned":
            False,

        "preprocessor_refitted":
            False,

        "features_reengineered":
            False,

        "feature_selection_changed":
            False,

        "threshold_retuned":
            False,

        "probabilities_recalibrated":
            False,

        "subgroup_specific_thresholds_created":
            False,

        "locked_test_accessed":
            False,

        "automatic_mitigation_applied":
            False,

        "external_validation_established":
            False,

        "temporal_validation_established":
            False,

        "institutional_validation_established":
            False,

        "geographic_validation_established":
            False,

        "prospective_validation_established":
            False,

        "autonomous_clinical_decision_authorized":
            False,

        "deployment_authorized":
            False,
    }


# ============================================================
# D12.08 — STATIC CONTRACT VALIDATION
# ============================================================

def validate_d12_static_system_boundary(
    boundary: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Validate the D12 explainability governance contract.

    This is a governance validation only. It does not load the model,
    transform data, calculate SHAP values, or access the locked TEST
    partition.
    """

    if boundary is None:
        boundary = build_d12_static_system_boundary()

    checks: dict[str, bool] = {}

    checks["stage_id_valid"] = (
        boundary.get("stage_id") == "D12"
    )

    checks["model_name_valid"] = (
        boundary.get("model_name")
        == D12_EXPECTED_MODEL_NAME
    )

    checks["model_sha_declared"] = (
        boundary.get("expected_model_sha256")
        == D12_EXPECTED_MODEL_SHA256
    )

    checks["d7_preprocessor_sha_declared"] = (
        boundary.get("expected_d7_preprocessor_sha256")
        == D12_EXPECTED_D7_PREPROCESSOR_SHA256
    )

    checks["d7_schema_sha_declared"] = (
        boundary.get("expected_d7_schema_sha256")
        == D12_EXPECTED_D7_SCHEMA_SHA256
    )

    checks["threshold_frozen"] = (
        boundary.get("development_threshold")
        == D12_EXPECTED_DEVELOPMENT_THRESHOLD
    )

    checks["validation_encounters_valid"] = (
        boundary.get("validation_encounters")
        == D12_EXPECTED_VALIDATION_ENCOUNTERS
    )

    checks["validation_positives_valid"] = (
        boundary.get("validation_positives")
        == D12_EXPECTED_VALIDATION_POSITIVES
    )

    checks["validation_negatives_valid"] = (
        boundary.get("validation_negatives")
        == D12_EXPECTED_VALIDATION_NEGATIVES
    )

    checks["transformed_feature_count_valid"] = (
        boundary.get("transformed_feature_count")
        == D12_EXPECTED_TRANSFORMED_FEATURE_COUNT
    )

    checks["model_not_retrained"] = (
        boundary.get("model_retrained") is False
    )

    checks["hyperparameters_not_retuned"] = (
        boundary.get("hyperparameters_retuned") is False
    )

    checks["preprocessor_not_refitted"] = (
        boundary.get("preprocessor_refitted") is False
    )

    checks["features_not_reengineered"] = (
        boundary.get("features_reengineered") is False
    )

    checks["feature_selection_unchanged"] = (
        boundary.get("feature_selection_changed") is False
    )

    checks["threshold_not_retuned"] = (
        boundary.get("threshold_retuned") is False
    )

    checks["probabilities_not_recalibrated"] = (
        boundary.get("probabilities_recalibrated") is False
    )

    checks["no_subgroup_thresholds"] = (
        boundary.get("subgroup_specific_thresholds_created")
        is False
    )

    checks["locked_test_not_accessed"] = (
        boundary.get("locked_test_accessed") is False
    )

    checks["no_automatic_mitigation"] = (
        boundary.get("automatic_mitigation_applied") is False
    )

    checks["external_validation_not_claimed"] = (
        boundary.get("external_validation_established") is False
    )

    checks["temporal_validation_not_claimed"] = (
        boundary.get("temporal_validation_established") is False
    )

    checks["institutional_validation_not_claimed"] = (
        boundary.get("institutional_validation_established") is False
    )

    checks["geographic_validation_not_claimed"] = (
        boundary.get("geographic_validation_established") is False
    )

    checks["prospective_validation_not_claimed"] = (
        boundary.get("prospective_validation_established") is False
    )

    checks["no_autonomous_clinical_decision"] = (
        boundary.get(
            "autonomous_clinical_decision_authorized"
        )
        is False
    )

    checks["deployment_not_authorized"] = (
        boundary.get("deployment_authorized") is False
    )

    checks["permitted_activity_registry_present"] = (
        len(boundary.get("permitted_activities", []))
        == len(D12_PERMITTED_ACTIVITIES)
    )

    checks["prohibited_activity_registry_present"] = (
        len(boundary.get("prohibited_activities", []))
        == len(D12_PROHIBITED_ACTIVITIES)
    )

    checks["d11_carry_forward_present"] = (
        len(boundary.get("d11_carry_forward_questions", []))
        == 6
    )

    checks["interpretation_safeguards_present"] = (
        len(boundary.get("interpretation_safeguards", []))
        == len(D12_INTERPRETATION_SAFEGUARDS)
    )

    failed_checks = [
        name
        for name, passed in checks.items()
        if not passed
    ]

    return {
        "validation_status":
            "PASS" if not failed_checks else "FAIL",

        "checks":
            checks,

        "failed_checks":
            failed_checks,

        "stage_id":
            boundary["stage_id"],

        "stage_name":
            boundary["stage_name"],

        "source_git_commit":
            boundary["source_git_commit"],

        "model_name":
            boundary["model_name"],

        "development_threshold":
            boundary["development_threshold"],

        "validation_encounters":
            boundary["validation_encounters"],

        "transformed_feature_count":
            boundary["transformed_feature_count"],

        "model_retrained":
            boundary["model_retrained"],

        "preprocessor_refitted":
            boundary["preprocessor_refitted"],

        "threshold_retuned":
            boundary["threshold_retuned"],

        "locked_test_accessed":
            boundary["locked_test_accessed"],

        "deployment_authorized":
            boundary["deployment_authorized"],
    }


# ============================================================
# D12.09 — PRINT STATIC GOVERNANCE CONTRACT
# ============================================================

def print_d12_static_system_boundary() -> None:
    """
    Print a concise D12 governance-boundary validation summary.
    """

    boundary = build_d12_static_system_boundary()

    validation = validate_d12_static_system_boundary(
        boundary
    )

    print(
        "D12 EXPLAINABILITY & MODEL INTERPRETATION "
        "GOVERNANCE BOUNDARY"
    )
    print("=" * 72)

    print(
        "STATUS:",
        validation["validation_status"],
    )

    print(
        "SOURCE COMMIT:",
        validation["source_git_commit"],
    )

    print(
        "MODEL:",
        validation["model_name"],
    )

    print(
        "THRESHOLD:",
        validation["development_threshold"],
    )

    print(
        "VALIDATION ENCOUNTERS:",
        validation["validation_encounters"],
    )

    print(
        "TRANSFORMED FEATURES:",
        validation["transformed_feature_count"],
    )

    print(
        "MODEL RETRAINED:",
        validation["model_retrained"],
    )

    print(
        "PREPROCESSOR REFITTED:",
        validation["preprocessor_refitted"],
    )

    print(
        "THRESHOLD RETUNED:",
        validation["threshold_retuned"],
    )

    print(
        "LOCKED TEST:",
        validation["locked_test_accessed"],
    )

    print(
        "DEPLOYMENT AUTHORIZED:",
        validation["deployment_authorized"],
    )

    print(
        "FAILED CHECKS:",
        validation["failed_checks"],
    )


# ============================================================
# D12.11 — FROZEN RUNTIME EXPLAINABILITY BOUNDARY
# ============================================================

import hashlib
from pathlib import Path

import joblib
import numpy as np

from src.features.preprocessing import (
    load_frozen_d7_primary_preprocessing_bundle,
)

from src.models.development import (
    D8_SELECTED_MODEL_ARTIFACT_PATH,
)

from src.models.clinical_utility import (
    build_d9_validation_prediction_bundle,
    validate_d9_validation_prediction_bundle,
    select_d9_development_threshold,
    validate_d9_development_threshold_selection,
)


# ============================================================
# D12.12 — READ-ONLY ARTIFACT HASHING
# ============================================================

def _d12_sha256_file(path: str | Path) -> str:
    """
    Calculate SHA256 without modifying the artifact.
    """

    artifact_path = Path(path)

    sha256 = hashlib.sha256()

    with artifact_path.open("rb") as file_handle:
        for chunk in iter(
            lambda: file_handle.read(1024 * 1024),
            b"",
        ):
            sha256.update(chunk)

    return sha256.hexdigest().upper()


# ============================================================
# D12.13 — LOAD FROZEN D8 MODEL READ-ONLY
# ============================================================

def load_frozen_d12_model_read_only() -> dict[str, Any]:
    """
    Load the already-persisted D8 selected model without invoking
    model-development or persistence workflows.

    SHA256 and modification time are captured before and after
    loading to demonstrate read-only artifact consumption.
    """

    model_path = Path(
        D8_SELECTED_MODEL_ARTIFACT_PATH
    )

    if not model_path.exists():
        raise FileNotFoundError(
            "Frozen D8 model artifact not found: "
            f"{model_path}"
        )

    sha_before = _d12_sha256_file(
        model_path
    )

    if sha_before != D12_EXPECTED_MODEL_SHA256:
        raise RuntimeError(
            "Frozen D8 model SHA256 does not match the "
            "D12 expected model identity. "
            f"Expected={D12_EXPECTED_MODEL_SHA256}, "
            f"Observed={sha_before}"
        )

    mtime_before = (
        model_path.stat().st_mtime_ns
    )

    estimator = joblib.load(
        model_path
    )

    sha_after = _d12_sha256_file(
        model_path
    )

    mtime_after = (
        model_path.stat().st_mtime_ns
    )

    if sha_after != sha_before:
        raise RuntimeError(
            "Frozen D8 model artifact changed during "
            "D12 read-only loading."
        )

    if mtime_after != mtime_before:
        raise RuntimeError(
            "Frozen D8 model modification time changed during "
            "D12 read-only loading."
        )

    return {
        "estimator":
            estimator,

        "model_artifact_path":
            str(model_path),

        "model_sha256_before":
            sha_before,

        "model_sha256_after":
            sha_after,

        "model_mtime_before":
            mtime_before,

        "model_mtime_after":
            mtime_after,

        "model_sha256_unchanged":
            sha_before == sha_after,

        "model_mtime_unchanged":
            mtime_before == mtime_after,

        "read_only_consumption":
            True,

        "model_retrained":
            False,

        "model_repersisted":
            False,

        "model_artifact_rewritten":
            False,

        "locked_test_accessed":
            False,

        "deployment_authorized":
            False,
    }


# ============================================================
# D12.14 — BUILD FROZEN EXPLAINABILITY RUNTIME BOUNDARY
# ============================================================

def build_d12_frozen_runtime_boundary() -> dict[str, Any]:
    """
    Assemble the actual frozen system D12 is permitted to explain.

    Architecture:
        D7 frozen preprocessing integrity
            ->
        D8 frozen selected model
            ->
        D9 authoritative validation representation/predictions
            ->
        D12 explainability

    D12 does not retrain, refit, retune, recalibrate, rewrite
    artifacts, access locked TEST, or authorize deployment.
    """

    # --------------------------------------------------------
    # D7 — frozen preprocessing integrity
    # --------------------------------------------------------

    d7_bundle = (
        load_frozen_d7_primary_preprocessing_bundle(
            expected_preprocessor_sha256=(
                D12_EXPECTED_D7_PREPROCESSOR_SHA256
            ),
            expected_schema_sha256=(
                D12_EXPECTED_D7_SCHEMA_SHA256
            ),
        )
    )

    if "fitted_bundle" not in d7_bundle:
        raise KeyError(
            "Frozen D7 wrapper does not contain "
            "'fitted_bundle'."
        )

    d7_fitted = d7_bundle[
        "fitted_bundle"
    ]

    # --------------------------------------------------------
    # D8 — frozen model loaded read-only
    # --------------------------------------------------------

    model_bundle = (
        load_frozen_d12_model_read_only()
    )

    estimator = model_bundle[
        "estimator"
    ]

    # --------------------------------------------------------
    # D9 — authoritative validation prediction bundle
    # --------------------------------------------------------

    d9_bundle = (
        build_d9_validation_prediction_bundle()
    )

    d9_validation = (
        validate_d9_validation_prediction_bundle(
            d9_bundle
        )
    )

    # --------------------------------------------------------
    # D9 is authoritative for transformed validation data
    # and validation predictions.
    # --------------------------------------------------------

    X_validation = d9_bundle[
        "X_validation"
    ]

    y_validation = np.asarray(
        d9_bundle[
            "y_validation"
        ]
    )

    feature_names = list(
        d9_bundle[
            "transformed_feature_names"
        ]
    )

    d9_probabilities = np.asarray(
        d9_bundle[
            "validation_probability"
        ],
        dtype=float,
    )

    # --------------------------------------------------------
    # D7 supplies raw/normalized validation representations
    # needed later for clinically interpretable slice review.
    # --------------------------------------------------------

    X_validation_raw = d7_fitted[
        "X_validation_raw"
    ]

    X_validation_normalized = d7_fitted[
        "X_validation_normalized"
    ]

    d7_X_validation_transformed = (
        d7_fitted[
            "X_validation_transformed"
        ]
    )

    d7_y_validation = np.asarray(
        d7_fitted[
            "y_validation"
        ]
    )

    d7_feature_names = list(
        d7_fitted[
            "transformed_feature_names"
        ]
    )

    # --------------------------------------------------------
    # Independently reproduce validation probabilities from
    # the frozen D8 model loaded read-only.
    # --------------------------------------------------------

    reproduced_probabilities = np.asarray(
        estimator.predict_proba(
            X_validation
        )[:, 1],
        dtype=float,
    )

    # --------------------------------------------------------
    # Cross-stage identity checks
    # --------------------------------------------------------

    if X_validation.shape != (
        D12_EXPECTED_VALIDATION_ENCOUNTERS,
        D12_EXPECTED_TRANSFORMED_FEATURE_COUNT,
    ):
        raise RuntimeError(
            "D12 authoritative validation matrix has an "
            "unexpected shape. "
            f"Observed={X_validation.shape}"
        )

    if len(y_validation) != (
        D12_EXPECTED_VALIDATION_ENCOUNTERS
    ):
        raise RuntimeError(
            "D12 validation outcome count mismatch."
        )

    if int(y_validation.sum()) != (
        D12_EXPECTED_VALIDATION_POSITIVES
    ):
        raise RuntimeError(
            "D12 validation positive-count mismatch."
        )

    if (
        len(y_validation)
        - int(y_validation.sum())
    ) != D12_EXPECTED_VALIDATION_NEGATIVES:
        raise RuntimeError(
            "D12 validation negative-count mismatch."
        )

    if len(feature_names) != (
        D12_EXPECTED_TRANSFORMED_FEATURE_COUNT
    ):
        raise RuntimeError(
            "D12 transformed feature-name count mismatch."
        )

    if len(X_validation_raw) != (
        D12_EXPECTED_VALIDATION_ENCOUNTERS
    ):
        raise RuntimeError(
            "D7 raw validation encounter count mismatch."
        )

    if len(X_validation_normalized) != (
        D12_EXPECTED_VALIDATION_ENCOUNTERS
    ):
        raise RuntimeError(
            "D7 normalized validation encounter count mismatch."
        )

    if d7_X_validation_transformed.shape != (
        D12_EXPECTED_VALIDATION_ENCOUNTERS,
        D12_EXPECTED_TRANSFORMED_FEATURE_COUNT,
    ):
        raise RuntimeError(
            "D7 transformed validation matrix shape mismatch."
        )

    # --------------------------------------------------------
    # D7 ↔ D9 outcome identity
    # --------------------------------------------------------

    outcomes_match_d7_d9 = bool(
        np.array_equal(
            d7_y_validation,
            y_validation,
        )
    )

    if not outcomes_match_d7_d9:
        raise RuntimeError(
            "D7 and D9 validation outcomes are not identical."
        )

    # --------------------------------------------------------
    # D7 ↔ D9 transformed feature schema identity
    # --------------------------------------------------------

    feature_names_match_d7_d9 = (
        d7_feature_names
        == feature_names
    )

    if not feature_names_match_d7_d9:
        raise RuntimeError(
            "D7 and D9 transformed feature schemas differ."
        )

    # --------------------------------------------------------
    # D7 ↔ D9 transformed matrix identity
    # --------------------------------------------------------

    transformed_matrices_match_d7_d9 = bool(
        np.allclose(
            np.asarray(
                d7_X_validation_transformed
            ),
            np.asarray(
                X_validation
            ),
            rtol=0.0,
            atol=0.0,
        )
    )

    if not transformed_matrices_match_d7_d9:
        raise RuntimeError(
            "D7 and D9 transformed validation matrices differ."
        )

    # --------------------------------------------------------
    # D8 read-only model ↔ D9 probability identity
    # --------------------------------------------------------

    probabilities_match_d9 = bool(
        np.allclose(
            reproduced_probabilities,
            d9_probabilities,
            rtol=0.0,
            atol=1e-12,
        )
    )

    if not probabilities_match_d9:
        raise RuntimeError(
            "D12 read-only frozen model does not reproduce "
            "the authoritative D9 validation probabilities."
        )

    # --------------------------------------------------------
    # D9 governed development-threshold identity
    # --------------------------------------------------------
    # The prediction bundle intentionally reports
    # clinical_threshold_selected=False. Threshold selection
    # occurs later in the governed D9 lifecycle.
    # --------------------------------------------------------

    d9_threshold_selection = (
        select_d9_development_threshold()
    )

    d9_threshold_validation = (
        validate_d9_development_threshold_selection(
            d9_threshold_selection
        )
    )

    d9_threshold = float(
        d9_threshold_selection[
            "selected_threshold"
        ]
    )

    threshold_matches_d9 = bool(
        np.isclose(
            d9_threshold,
            D12_EXPECTED_DEVELOPMENT_THRESHOLD,
            rtol=0.0,
            atol=1e-12,
        )
    )

    if not threshold_matches_d9:
        raise RuntimeError(
            "Governed D9 development threshold does not match "
            "the frozen D12 expected threshold. "
            f"Expected={D12_EXPECTED_DEVELOPMENT_THRESHOLD}, "
            f"Observed={d9_threshold}"
        )

    # --------------------------------------------------------
    # Model identity reported by D9
    # --------------------------------------------------------

    d9_model_sha = str(
        d9_bundle[
            "model_sha256"
        ]
    ).upper()

    model_sha_matches_d9 = (
        d9_model_sha
        == model_bundle[
            "model_sha256_after"
        ]
    )

    if not model_sha_matches_d9:
        raise RuntimeError(
            "D8 frozen model SHA and D9 model SHA differ."
        )

    return {
        # ----------------------------------------------------
        # Explainability runtime objects
        # ----------------------------------------------------

        "estimator":
            estimator,

        "X_validation":
            X_validation,

        "X_validation_raw":
            X_validation_raw,

        "X_validation_normalized":
            X_validation_normalized,

        "y_validation":
            y_validation,

        "transformed_feature_names":
            feature_names,

        "validation_probability":
            d9_probabilities,

        # ----------------------------------------------------
        # Cross-stage integrity evidence
        # ----------------------------------------------------

        "d9_validation_status":
            d9_validation.get(
                "validation_status"
            ),

        "outcomes_match_d7_d9":
            outcomes_match_d7_d9,

        "feature_names_match_d7_d9":
            feature_names_match_d7_d9,

        "transformed_matrices_match_d7_d9":
            transformed_matrices_match_d7_d9,

        "probabilities_match_d9":
            probabilities_match_d9,

        "threshold_matches_d9":
            threshold_matches_d9,

        "selected_development_threshold":
            d9_threshold,

        "d9_threshold_selection_status":
            d9_threshold_validation.get(
                "validation_status"
            ),

        "development_threshold_selected":
            d9_threshold_selection.get(
                "development_threshold_selected"
            ),

        "threshold_selection_partition":
            d9_threshold_selection.get(
                "selection_partition"
            ),

        "model_sha_matches_d9":
            model_sha_matches_d9,

        # ----------------------------------------------------
        # Frozen artifact identity
        # ----------------------------------------------------

        "model_artifact_path":
            model_bundle[
                "model_artifact_path"
            ],

        "model_sha256":
            model_bundle[
                "model_sha256_after"
            ],

        "model_sha256_unchanged":
            model_bundle[
                "model_sha256_unchanged"
            ],

        "model_mtime_unchanged":
            model_bundle[
                "model_mtime_unchanged"
            ],

        "d7_read_only_consumption":
            d7_bundle.get(
                "read_only_consumption"
            ),

        "d7_preprocessor_refitted":
            d7_bundle.get(
                "preprocessor_refitted"
            ),

        "d7_artifact_rewritten":
            d7_bundle.get(
                "artifact_rewritten"
            ),

        "model_read_only_consumption":
            model_bundle[
                "read_only_consumption"
            ],

        # ----------------------------------------------------
        # Lifecycle mutation controls
        # ----------------------------------------------------

        "model_retrained":
            False,

        "hyperparameters_retuned":
            False,

        "preprocessor_refitted":
            False,

        "features_reengineered":
            False,

        "feature_selection_changed":
            False,

        "threshold_retuned":
            False,

        "probabilities_recalibrated":
            False,

        "subgroup_specific_thresholds_created":
            False,

        "automatic_mitigation_applied":
            False,

        "locked_test_accessed":
            False,

        "deployment_authorized":
            False,
    }


# ============================================================
# D12.15 — VALIDATE FROZEN RUNTIME BOUNDARY
# ============================================================

def validate_d12_frozen_runtime_boundary(
    bundle: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Validate that D12 is consuming exactly the frozen governed
    development-stage model and validation representation.
    """

    if bundle is None:
        bundle = (
            build_d12_frozen_runtime_boundary()
        )

    X_validation = bundle[
        "X_validation"
    ]

    y_validation = np.asarray(
        bundle[
            "y_validation"
        ]
    )

    checks = {
        # ----------------------------------------------------
        # Runtime identity
        # ----------------------------------------------------

        "validation_shape_valid":
            X_validation.shape
            == (
                D12_EXPECTED_VALIDATION_ENCOUNTERS,
                D12_EXPECTED_TRANSFORMED_FEATURE_COUNT,
            ),

        "validation_outcome_count_valid":
            len(y_validation)
            == D12_EXPECTED_VALIDATION_ENCOUNTERS,

        "validation_positive_count_valid":
            int(y_validation.sum())
            == D12_EXPECTED_VALIDATION_POSITIVES,

        "validation_negative_count_valid":
            (
                len(y_validation)
                - int(y_validation.sum())
            )
            == D12_EXPECTED_VALIDATION_NEGATIVES,

        "feature_count_valid":
            len(
                bundle[
                    "transformed_feature_names"
                ]
            )
            == D12_EXPECTED_TRANSFORMED_FEATURE_COUNT,

        # ----------------------------------------------------
        # D7 ↔ D8 ↔ D9 integrity
        # ----------------------------------------------------

        "d7_d9_outcomes_match":
            bundle[
                "outcomes_match_d7_d9"
            ]
            is True,

        "d7_d9_feature_names_match":
            bundle[
                "feature_names_match_d7_d9"
            ]
            is True,

        "d7_d9_transformed_matrices_match":
            bundle[
                "transformed_matrices_match_d7_d9"
            ]
            is True,

        "d8_d9_probabilities_match":
            bundle[
                "probabilities_match_d9"
            ]
            is True,

        "d9_threshold_matches":
            bundle[
                "threshold_matches_d9"
            ]
            is True,

        "d9_threshold_selection_valid":
            bundle[
                "d9_threshold_selection_status"
            ]
            == "PASS",

        "d9_development_threshold_selected":
            bundle[
                "development_threshold_selected"
            ]
            is True,

        "d9_threshold_selection_partition_valid":
            bundle[
                "threshold_selection_partition"
            ]
            == "validation",

        "d8_d9_model_sha_matches":
            bundle[
                "model_sha_matches_d9"
            ]
            is True,

        # ----------------------------------------------------
        # Frozen artifact integrity
        # ----------------------------------------------------

        "model_sha_valid":
            bundle[
                "model_sha256"
            ]
            == D12_EXPECTED_MODEL_SHA256,

        "model_sha_unchanged":
            bundle[
                "model_sha256_unchanged"
            ]
            is True,

        "model_mtime_unchanged":
            bundle[
                "model_mtime_unchanged"
            ]
            is True,

        "d7_read_only":
            bundle[
                "d7_read_only_consumption"
            ]
            is True,

        "d7_not_refitted":
            bundle[
                "d7_preprocessor_refitted"
            ]
            is False,

        "d7_not_rewritten":
            bundle[
                "d7_artifact_rewritten"
            ]
            is False,

        "model_read_only":
            bundle[
                "model_read_only_consumption"
            ]
            is True,

        # ----------------------------------------------------
        # Lifecycle governance
        # ----------------------------------------------------

        "model_not_retrained":
            bundle[
                "model_retrained"
            ]
            is False,

        "hyperparameters_not_retuned":
            bundle[
                "hyperparameters_retuned"
            ]
            is False,

        "preprocessor_not_refitted":
            bundle[
                "preprocessor_refitted"
            ]
            is False,

        "features_not_reengineered":
            bundle[
                "features_reengineered"
            ]
            is False,

        "feature_selection_unchanged":
            bundle[
                "feature_selection_changed"
            ]
            is False,

        "threshold_not_retuned":
            bundle[
                "threshold_retuned"
            ]
            is False,

        "probabilities_not_recalibrated":
            bundle[
                "probabilities_recalibrated"
            ]
            is False,

        "no_subgroup_thresholds":
            bundle[
                "subgroup_specific_thresholds_created"
            ]
            is False,

        "no_automatic_mitigation":
            bundle[
                "automatic_mitigation_applied"
            ]
            is False,

        "locked_test_not_accessed":
            bundle[
                "locked_test_accessed"
            ]
            is False,

        "deployment_not_authorized":
            bundle[
                "deployment_authorized"
            ]
            is False,
    }

    failed_checks = [
        name
        for name, passed in checks.items()
        if not passed
    ]

    return {
        "validation_status":
            (
                "PASS"
                if not failed_checks
                else "FAIL"
            ),

        "checks":
            checks,

        "failed_checks":
            failed_checks,

        "validation_encounters":
            int(
                X_validation.shape[0]
            ),

        "validation_positives":
            int(
                y_validation.sum()
            ),

        "validation_negatives":
            int(
                len(y_validation)
                - y_validation.sum()
            ),

        "transformed_feature_count":
            int(
                X_validation.shape[1]
            ),

        "model_sha256":
            bundle[
                "model_sha256"
            ],

        "outcomes_match_d7_d9":
            bundle[
                "outcomes_match_d7_d9"
            ],

        "feature_names_match_d7_d9":
            bundle[
                "feature_names_match_d7_d9"
            ],

        "transformed_matrices_match_d7_d9":
            bundle[
                "transformed_matrices_match_d7_d9"
            ],

        "probabilities_match_d9":
            bundle[
                "probabilities_match_d9"
            ],

        "threshold_matches_d9":
            bundle[
                "threshold_matches_d9"
            ],

        "selected_development_threshold":
            bundle[
                "selected_development_threshold"
            ],

        "d9_threshold_selection_status":
            bundle[
                "d9_threshold_selection_status"
            ],

        "development_threshold_selected":
            bundle[
                "development_threshold_selected"
            ],

        "threshold_selection_partition":
            bundle[
                "threshold_selection_partition"
            ],

        "model_sha_matches_d9":
            bundle[
                "model_sha_matches_d9"
            ],

        "model_sha256_unchanged":
            bundle[
                "model_sha256_unchanged"
            ],

        "model_mtime_unchanged":
            bundle[
                "model_mtime_unchanged"
            ],

        "model_retrained":
            bundle[
                "model_retrained"
            ],

        "preprocessor_refitted":
            bundle[
                "preprocessor_refitted"
            ],

        "threshold_retuned":
            bundle[
                "threshold_retuned"
            ],

        "locked_test_accessed":
            bundle[
                "locked_test_accessed"
            ],

        "deployment_authorized":
            bundle[
                "deployment_authorized"
            ],
    }


# ============================================================
# D12.16 — PRINT FROZEN RUNTIME BOUNDARY
# ============================================================

def print_d12_frozen_runtime_boundary() -> None:
    """
    Print concise D12 frozen-system integrity evidence.
    """

    bundle = (
        build_d12_frozen_runtime_boundary()
    )

    validation = (
        validate_d12_frozen_runtime_boundary(
            bundle
        )
    )

    print(
        "D12 FROZEN EXPLAINABILITY RUNTIME BOUNDARY"
    )
    print("=" * 72)

    print(
        "STATUS:",
        validation[
            "validation_status"
        ],
    )

    print(
        "MODEL SHA:",
        validation[
            "model_sha256"
        ],
    )

    print(
        "VALIDATION ENCOUNTERS:",
        validation[
            "validation_encounters"
        ],
    )

    print(
        "VALIDATION POSITIVES:",
        validation[
            "validation_positives"
        ],
    )

    print(
        "VALIDATION NEGATIVES:",
        validation[
            "validation_negatives"
        ],
    )

    print(
        "TRANSFORMED FEATURES:",
        validation[
            "transformed_feature_count"
        ],
    )

    print(
        "D7-D9 OUTCOMES MATCH:",
        validation[
            "outcomes_match_d7_d9"
        ],
    )

    print(
        "D7-D9 FEATURE NAMES MATCH:",
        validation[
            "feature_names_match_d7_d9"
        ],
    )

    print(
        "D7-D9 MATRICES MATCH:",
        validation[
            "transformed_matrices_match_d7_d9"
        ],
    )

    print(
        "D8-D9 PROBABILITIES MATCH:",
        validation[
            "probabilities_match_d9"
        ],
    )

    print(
        "D9 DEVELOPMENT THRESHOLD:",
        validation[
            "selected_development_threshold"
        ],
    )

    print(
        "D9 THRESHOLD SELECTION STATUS:",
        validation[
            "d9_threshold_selection_status"
        ],
    )

    print(
        "D9 THRESHOLD MATCH:",
        validation[
            "threshold_matches_d9"
        ],
    )

    print(
        "D8-D9 MODEL SHA MATCH:",
        validation[
            "model_sha_matches_d9"
        ],
    )

    print(
        "MODEL SHA UNCHANGED:",
        validation[
            "model_sha256_unchanged"
        ],
    )

    print(
        "MODEL MTIME UNCHANGED:",
        validation[
            "model_mtime_unchanged"
        ],
    )

    print(
        "MODEL RETRAINED:",
        validation[
            "model_retrained"
        ],
    )

    print(
        "PREPROCESSOR REFITTED:",
        validation[
            "preprocessor_refitted"
        ],
    )

    print(
        "THRESHOLD RETUNED:",
        validation[
            "threshold_retuned"
        ],
    )

    print(
        "LOCKED TEST:",
        validation[
            "locked_test_accessed"
        ],
    )

    print(
        "DEPLOYMENT AUTHORIZED:",
        validation[
            "deployment_authorized"
        ],
    )

    print(
        "FAILED CHECKS:",
        validation[
            "failed_checks"
        ],
    )

# ============================================================
# D12.17 — EXPLAINABILITY METHOD GOVERNANCE
# ============================================================

def build_d12_explainability_method_governance() -> dict[str, Any]:
    """
    Define the governed explainability method used for the frozen
    XGBoost development-stage model.

    SHAP is used to characterize model behavior, not causal effects,
    biological mechanisms, clinical appropriateness, or deployment
    readiness.
    """

    import platform
    import shap
    import xgboost

    return {
        "method_name":
            "SHAP TreeExplainer",

        "explainer_family":
            "TreeExplainer",

        "model_family":
            D12_EXPECTED_MODEL_NAME,

        "explanation_partition":
            "validation",

        "model_output_space":
            "raw",

        "raw_output_interpretation":
            "xgboost_raw_margin_log_odds_space",

        "probability_link":
            "logistic_expit",

        "python_version":
            platform.python_version(),

        "numpy_version":
            np.__version__,

        "xgboost_version":
            xgboost.__version__,

        "shap_version":
            shap.__version__,

        "feature_attribution_is_causal":
            False,

        "biological_mechanism_claimed":
            False,

        "clinical_appropriateness_established":
            False,

        "external_validation_established":
            False,

        "deployment_authorized":
            False,

        "model_retrained":
            False,

        "preprocessor_refitted":
            False,

        "threshold_retuned":
            False,

        "locked_test_accessed":
            False,
    }


# ============================================================
# D12.18 — SHAP TECHNICAL COMPATIBILITY VALIDATION
# ============================================================

def validate_d12_shap_compatibility(
    sample_size: int = 10,
) -> dict[str, Any]:
    """
    Validate that SHAP TreeExplainer can explain the exact frozen
    D8 model against the governed D9 validation representation.

    This is a technical compatibility gate only. It does not produce
    substantive feature-importance or clinical conclusions.
    """

    import shap

    if sample_size <= 0:
        raise ValueError(
            "D12 SHAP compatibility sample_size must be positive."
        )

    runtime = build_d12_frozen_runtime_boundary()

    estimator = runtime[
        "estimator"
    ]

    X_validation = runtime[
        "X_validation"
    ]

    feature_names = list(
        runtime[
            "transformed_feature_names"
        ]
    )

    n_rows = min(
        int(sample_size),
        int(X_validation.shape[0]),
    )

    X_sample = X_validation[
        :n_rows
    ]

    explainer = shap.TreeExplainer(
        estimator
    )

    explanation = explainer(
        X_sample
    )

    shap_values = np.asarray(
        explanation.values,
        dtype=float,
    )

    base_values = np.asarray(
        explanation.base_values,
        dtype=float,
    )

    explanation_data = np.asarray(
        explanation.data
    )

    expected_shape = (
        n_rows,
        D12_EXPECTED_TRANSFORMED_FEATURE_COUNT,
    )

    checks = {
        "explainer_is_tree_explainer":
            type(explainer).__name__
            == "TreeExplainer",

        "shap_values_shape_valid":
            shap_values.shape
            == expected_shape,

        "base_values_shape_valid":
            base_values.shape
            == (n_rows,),

        "explanation_data_shape_valid":
            explanation_data.shape
            == expected_shape,

        "feature_count_valid":
            len(feature_names)
            == D12_EXPECTED_TRANSFORMED_FEATURE_COUNT,

        "shap_values_finite":
            bool(
                np.isfinite(
                    shap_values
                ).all()
            ),

        "base_values_finite":
            bool(
                np.isfinite(
                    base_values
                ).all()
            ),

        "model_output_is_raw":
            str(
                explainer.model_output
            ).lower()
            == "raw",

        "model_not_retrained":
            runtime[
                "model_retrained"
            ]
            is False,

        "preprocessor_not_refitted":
            runtime[
                "preprocessor_refitted"
            ]
            is False,

        "threshold_not_retuned":
            runtime[
                "threshold_retuned"
            ]
            is False,

        "locked_test_not_accessed":
            runtime[
                "locked_test_accessed"
            ]
            is False,

        "deployment_not_authorized":
            runtime[
                "deployment_authorized"
            ]
            is False,
    }

    failed_checks = [
        name
        for name, passed in checks.items()
        if not passed
    ]

    return {
        "validation_status":
            "PASS"
            if not failed_checks
            else "FAIL",

        "checks":
            checks,

        "failed_checks":
            failed_checks,

        "sample_size":
            n_rows,

        "explainer_type":
            type(explainer).__name__,

        "model_output":
            str(
                explainer.model_output
            ),

        "shap_values_shape":
            tuple(
                shap_values.shape
            ),

        "base_values_shape":
            tuple(
                base_values.shape
            ),

        "data_shape":
            tuple(
                explanation_data.shape
            ),

        "feature_count":
            len(feature_names),

        "finite_shap":
            bool(
                np.isfinite(
                    shap_values
                ).all()
            ),

        "model_sha256":
            runtime[
                "model_sha256"
            ],

        "model_sha256_unchanged":
            runtime[
                "model_sha256_unchanged"
            ],

        "model_mtime_unchanged":
            runtime[
                "model_mtime_unchanged"
            ],

        "model_retrained":
            False,

        "preprocessor_refitted":
            False,

        "threshold_retuned":
            False,

        "locked_test_accessed":
            False,

        "deployment_authorized":
            False,
    }


# ============================================================
# D12.19 — SHAP ADDITIVITY / OUTPUT-SPACE VALIDATION
# ============================================================

def validate_d12_shap_additivity(
    sample_size: int = 100,
    max_probability_error_tolerance: float = 1e-6,
) -> dict[str, Any]:
    """
    Validate the mathematical relationship between SHAP attribution
    values and the frozen XGBoost model output.

    For the current TreeExplainer configuration, SHAP explanations
    are expected in raw model-margin/log-odds space. The governed
    validation therefore checks:

        base_value + sum(SHAP values)
            -> reconstructed raw model output

        expit(reconstructed raw output)
            -> frozen model predicted probability

    SHAP values must not be interpreted as direct percentage-point
    changes in readmission probability.
    """

    import shap

    if sample_size <= 0:
        raise ValueError(
            "D12 SHAP additivity sample_size must be positive."
        )

    if max_probability_error_tolerance <= 0:
        raise ValueError(
            "D12 SHAP additivity tolerance must be positive."
        )

    runtime = build_d12_frozen_runtime_boundary()

    estimator = runtime[
        "estimator"
    ]

    X_validation = runtime[
        "X_validation"
    ]

    n_rows = min(
        int(sample_size),
        int(X_validation.shape[0]),
    )

    X_sample = X_validation[
        :n_rows
    ]

    explainer = shap.TreeExplainer(
        estimator
    )

    explanation = explainer(
        X_sample
    )

    shap_values = np.asarray(
        explanation.values,
        dtype=float,
    )

    base_values = np.asarray(
        explanation.base_values,
        dtype=float,
    )

    reconstructed_raw_output = (
        base_values
        + shap_values.sum(
            axis=1
        )
    )

    model_probability = np.asarray(
        estimator.predict_proba(
            X_sample
        )[:, 1],
        dtype=float,
    )

    # Numerically stable logistic transformation without introducing
    # another runtime dependency into the governed explainability layer.
    reconstructed_probability = np.empty_like(
        reconstructed_raw_output,
        dtype=float,
    )

    positive_mask = (
        reconstructed_raw_output
        >= 0.0
    )

    reconstructed_probability[
        positive_mask
    ] = (
        1.0
        / (
            1.0
            + np.exp(
                -reconstructed_raw_output[
                    positive_mask
                ]
            )
        )
    )

    negative_raw = reconstructed_raw_output[
        ~positive_mask
    ]

    negative_exp = np.exp(
        negative_raw
    )

    reconstructed_probability[
        ~positive_mask
    ] = (
        negative_exp
        / (
            1.0
            + negative_exp
        )
    )

    probability_absolute_error = np.abs(
        reconstructed_probability
        - model_probability
    )

    direct_probability_absolute_error = np.abs(
        reconstructed_raw_output
        - model_probability
    )

    max_probability_error = float(
        probability_absolute_error.max()
    )

    mean_probability_error = float(
        probability_absolute_error.mean()
    )

    max_direct_probability_error = float(
        direct_probability_absolute_error.max()
    )

    checks = {
        "model_output_is_raw":
            str(
                explainer.model_output
            ).lower()
            == "raw",

        "raw_reconstruction_finite":
            bool(
                np.isfinite(
                    reconstructed_raw_output
                ).all()
            ),

        "probability_reconstruction_finite":
            bool(
                np.isfinite(
                    reconstructed_probability
                ).all()
            ),

        "model_probability_finite":
            bool(
                np.isfinite(
                    model_probability
                ).all()
            ),

        "probability_reconstruction_within_tolerance":
            max_probability_error
            <= max_probability_error_tolerance,

        "raw_output_not_misclassified_as_probability":
            max_direct_probability_error
            > max_probability_error,

        "model_not_retrained":
            runtime[
                "model_retrained"
            ]
            is False,

        "preprocessor_not_refitted":
            runtime[
                "preprocessor_refitted"
            ]
            is False,

        "threshold_not_retuned":
            runtime[
                "threshold_retuned"
            ]
            is False,

        "locked_test_not_accessed":
            runtime[
                "locked_test_accessed"
            ]
            is False,

        "deployment_not_authorized":
            runtime[
                "deployment_authorized"
            ]
            is False,
    }

    failed_checks = [
        name
        for name, passed in checks.items()
        if not passed
    ]

    return {
        "validation_status":
            "PASS"
            if not failed_checks
            else "FAIL",

        "checks":
            checks,

        "failed_checks":
            failed_checks,

        "sample_size":
            n_rows,

        "model_output":
            str(
                explainer.model_output
            ),

        "output_space_interpretation":
            "raw_margin_log_odds",

        "probability_link":
            "logistic_expit",

        "reconstructed_raw_min":
            float(
                reconstructed_raw_output.min()
            ),

        "reconstructed_raw_max":
            float(
                reconstructed_raw_output.max()
            ),

        "model_probability_min":
            float(
                model_probability.min()
            ),

        "model_probability_max":
            float(
                model_probability.max()
            ),

        "max_probability_reconstruction_error":
            max_probability_error,

        "mean_probability_reconstruction_error":
            mean_probability_error,

        "max_direct_probability_error":
            max_direct_probability_error,

        "max_probability_error_tolerance":
            float(
                max_probability_error_tolerance
            ),

        "shap_values_are_probability_point_changes":
            False,

        "feature_attribution_is_causal":
            False,

        "model_retrained":
            False,

        "preprocessor_refitted":
            False,

        "threshold_retuned":
            False,

        "locked_test_accessed":
            False,

        "deployment_authorized":
            False,
    }


# ============================================================
# D12.20 — GOVERNED ATTRIBUTION DATASET
# ============================================================

def build_d12_governed_attribution_dataset(
    max_encounters: int | None = None,
) -> dict[str, Any]:
    """
    Build governed SHAP attribution evidence for the frozen validation
    representation.

    By default, all validation encounters are explained. A positive
    max_encounters value may be supplied for controlled diagnostics.
    The function never samples randomly, retrains the model, refits
    preprocessing, retunes the threshold, or accesses locked TEST.
    """

    import shap

    runtime = build_d12_frozen_runtime_boundary()

    estimator = runtime[
        "estimator"
    ]

    X_validation = runtime[
        "X_validation"
    ]

    feature_names = list(
        runtime[
            "transformed_feature_names"
        ]
    )

    validation_probability = np.asarray(
        runtime[
            "validation_probability"
        ],
        dtype=float,
    )

    y_validation = np.asarray(
        runtime[
            "y_validation"
        ]
    )

    if max_encounters is None:
        n_rows = int(
            X_validation.shape[0]
        )
        attribution_scope = (
            "full_validation_partition"
        )
    else:
        if int(max_encounters) <= 0:
            raise ValueError(
                "D12 max_encounters must be positive when provided."
            )

        n_rows = min(
            int(max_encounters),
            int(X_validation.shape[0]),
        )

        attribution_scope = (
            "deterministic_validation_prefix_diagnostic"
        )

    X_explain = X_validation[
        :n_rows
    ]

    y_explain = y_validation[
        :n_rows
    ]

    probability_explain = validation_probability[
        :n_rows
    ]

    explainer = shap.TreeExplainer(
        estimator
    )

    explanation = explainer(
        X_explain
    )

    shap_values = np.asarray(
        explanation.values,
        dtype=float,
    )

    base_values = np.asarray(
        explanation.base_values,
        dtype=float,
    )

    explanation_data = np.asarray(
        explanation.data
    )

    expected_shape = (
        n_rows,
        D12_EXPECTED_TRANSFORMED_FEATURE_COUNT,
    )

    if shap_values.shape != expected_shape:
        raise RuntimeError(
            "D12 governed SHAP attribution matrix has an "
            "unexpected shape. "
            f"Expected={expected_shape}, "
            f"Observed={shap_values.shape}"
        )

    if base_values.shape != (n_rows,):
        raise RuntimeError(
            "D12 governed SHAP base-value vector has an "
            "unexpected shape."
        )

    if explanation_data.shape != expected_shape:
        raise RuntimeError(
            "D12 governed SHAP explanation-data matrix has an "
            "unexpected shape."
        )

    if not np.isfinite(
        shap_values
    ).all():
        raise RuntimeError(
            "D12 governed SHAP attribution matrix contains "
            "non-finite values."
        )

    if not np.isfinite(
        base_values
    ).all():
        raise RuntimeError(
            "D12 governed SHAP base values contain "
            "non-finite values."
        )

    reconstructed_raw_output = (
        base_values
        + shap_values.sum(
            axis=1
        )
    )

    reconstructed_probability = np.empty_like(
        reconstructed_raw_output,
        dtype=float,
    )

    positive_mask = (
        reconstructed_raw_output
        >= 0.0
    )

    reconstructed_probability[
        positive_mask
    ] = (
        1.0
        / (
            1.0
            + np.exp(
                -reconstructed_raw_output[
                    positive_mask
                ]
            )
        )
    )

    negative_raw = reconstructed_raw_output[
        ~positive_mask
    ]

    negative_exp = np.exp(
        negative_raw
    )

    reconstructed_probability[
        ~positive_mask
    ] = (
        negative_exp
        / (
            1.0
            + negative_exp
        )
    )

    max_probability_reconstruction_error = float(
        np.max(
            np.abs(
                reconstructed_probability
                - probability_explain
            )
        )
    )

    if max_probability_reconstruction_error > 1e-6:
        raise RuntimeError(
            "D12 governed SHAP attributions do not reconstruct "
            "the frozen model probabilities within tolerance. "
            f"Observed maximum error="
            f"{max_probability_reconstruction_error}"
        )

    return {
        "explanation":
            explanation,

        "shap_values":
            shap_values,

        "base_values":
            base_values,

        "explanation_data":
            explanation_data,

        "X_explain":
            X_explain,

        "y_explain":
            y_explain,

        "validation_probability":
            probability_explain,

        "transformed_feature_names":
            feature_names,

        "encounter_count":
            n_rows,

        "feature_count":
            len(feature_names),

        "attribution_scope":
            attribution_scope,

        "model_output":
            str(
                explainer.model_output
            ),

        "output_space_interpretation":
            "raw_margin_log_odds",

        "probability_link":
            "logistic_expit",

        "max_probability_reconstruction_error":
            max_probability_reconstruction_error,

        "shap_values_finite":
            True,

        "base_values_finite":
            True,

        "feature_attribution_is_causal":
            False,

        "shap_values_are_probability_point_changes":
            False,

        "model_sha256":
            runtime[
                "model_sha256"
            ],

        "selected_development_threshold":
            runtime[
                "selected_development_threshold"
            ],

        "model_retrained":
            False,

        "preprocessor_refitted":
            False,

        "threshold_retuned":
            False,

        "probabilities_recalibrated":
            False,

        "locked_test_accessed":
            False,

        "deployment_authorized":
            False,
    }


# ============================================================
# D12.21 — VALIDATE EXPLAINABILITY FOUNDATION
# ============================================================

def validate_d12_explainability_foundation(
    compatibility_sample_size: int = 10,
    additivity_sample_size: int = 100,
) -> dict[str, Any]:
    """
    Validate the governed D12 explainability foundation before any
    substantive global, local, or subgroup interpretation is produced.
    """

    method = (
        build_d12_explainability_method_governance()
    )

    compatibility = (
        validate_d12_shap_compatibility(
            sample_size=compatibility_sample_size
        )
    )

    additivity = (
        validate_d12_shap_additivity(
            sample_size=additivity_sample_size
        )
    )

    checks = {
        "method_is_tree_shap":
            method[
                "explainer_family"
            ]
            == "TreeExplainer",

        "method_output_space_is_raw":
            method[
                "model_output_space"
            ]
            == "raw",

        "compatibility_passed":
            compatibility[
                "validation_status"
            ]
            == "PASS",

        "additivity_passed":
            additivity[
                "validation_status"
            ]
            == "PASS",

        "attribution_not_causal":
            method[
                "feature_attribution_is_causal"
            ]
            is False,

        "deployment_not_authorized":
            method[
                "deployment_authorized"
            ]
            is False,

        "locked_test_not_accessed":
            method[
                "locked_test_accessed"
            ]
            is False,
    }

    failed_checks = [
        name
        for name, passed in checks.items()
        if not passed
    ]

    return {
        "validation_status":
            "PASS"
            if not failed_checks
            else "FAIL",

        "checks":
            checks,

        "failed_checks":
            failed_checks,

        "method_governance":
            method,

        "compatibility":
            compatibility,

        "additivity":
            additivity,

        "substantive_explainability_authorized":
            not failed_checks,

        "deployment_authorized":
            False,
    }


# ============================================================
# D12.22 — PRINT EXPLAINABILITY FOUNDATION
# ============================================================

def print_d12_explainability_foundation() -> None:
    """
    Print concise D12 method-governance and SHAP validation evidence.
    """

    result = (
        validate_d12_explainability_foundation()
    )

    compatibility = result[
        "compatibility"
    ]

    additivity = result[
        "additivity"
    ]

    method = result[
        "method_governance"
    ]

    print(
        "D12 EXPLAINABILITY METHOD & SHAP FOUNDATION"
    )
    print("=" * 72)

    print(
        "STATUS:",
        result[
            "validation_status"
        ],
    )

    print(
        "METHOD:",
        method[
            "method_name"
        ],
    )

    print(
        "PYTHON:",
        method[
            "python_version"
        ],
    )

    print(
        "NUMPY:",
        method[
            "numpy_version"
        ],
    )

    print(
        "XGBOOST:",
        method[
            "xgboost_version"
        ],
    )

    print(
        "SHAP:",
        method[
            "shap_version"
        ],
    )

    print(
        "MODEL OUTPUT:",
        additivity[
            "model_output"
        ],
    )

    print(
        "COMPATIBILITY SAMPLE:",
        compatibility[
            "sample_size"
        ],
    )

    print(
        "SHAP VALUES SHAPE:",
        compatibility[
            "shap_values_shape"
        ],
    )

    print(
        "ADDITIVITY SAMPLE:",
        additivity[
            "sample_size"
        ],
    )

    print(
        "RAW->PROB MAX ERROR:",
        additivity[
            "max_probability_reconstruction_error"
        ],
    )

    print(
        "DIRECT PROB MAX ERROR:",
        additivity[
            "max_direct_probability_error"
        ],
    )

    print(
        "SHAP VALUES ARE PROBABILITY-POINT CHANGES:",
        additivity[
            "shap_values_are_probability_point_changes"
        ],
    )

    print(
        "FEATURE ATTRIBUTION IS CAUSAL:",
        additivity[
            "feature_attribution_is_causal"
        ],
    )

    print(
        "SUBSTANTIVE EXPLAINABILITY AUTHORIZED:",
        result[
            "substantive_explainability_authorized"
        ],
    )

    print(
        "LOCKED TEST:",
        method[
            "locked_test_accessed"
        ],
    )

    print(
        "DEPLOYMENT AUTHORIZED:",
        result[
            "deployment_authorized"
        ],
    )

    print(
        "FAILED CHECKS:",
        result[
            "failed_checks"
        ],
    )


# ============================================================
# D12.23 — TRANSFORMED FEATURE → SOURCE FEATURE FAMILY MAPPING
# ============================================================

D12_SOURCE_FEATURE_FAMILIES = (
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

D12_PRIOR_UTILIZATION_FAMILY = (
    "prior_outpatient_use",
    "prior_emergency_use",
    "prior_inpatient_use",
    "prior_utilization_intensity",
    "prior_utilization_domain_count",
)


def map_d12_transformed_feature_to_source_family(
    transformed_feature_name: str,
) -> str:
    """
    Map a D7 transformed feature name back to one of the ten governed
    D6/D7 source-feature families.

    Matching is intentionally based on the frozen governed source
    feature registry rather than on clinical inference.
    """

    feature_name = str(
        transformed_feature_name
    )

    normalized_name = feature_name

    # sklearn ColumnTransformer commonly prefixes output names with
    # transformer labels such as categorical__ or numeric__.
    if "__" in normalized_name:
        normalized_name = normalized_name.split(
            "__",
            1,
        )[1]

    # Exact numeric / binary engineered features first.
    exact_matches = (
        "prior_outpatient_use",
        "prior_emergency_use",
        "prior_inpatient_use",
        "prior_utilization_intensity",
        "prior_utilization_domain_count",
    )

    for source_feature in exact_matches:
        if normalized_name == source_feature:
            return source_feature

    # One-hot encoded categorical features retain the source feature
    # name followed by an underscore and encoded category value.
    categorical_sources = (
        "admission_source_id",
        "admission_type_id",
        "gender",
        "race",
        "age",
    )

    for source_feature in categorical_sources:
        if (
            normalized_name == source_feature
            or normalized_name.startswith(
                source_feature + "_"
            )
        ):
            return source_feature

    raise ValueError(
        "Unable to map D12 transformed feature to governed "
        "source-feature family: "
        f"{transformed_feature_name}"
    )


# ============================================================
# D12.24 — BUILD GLOBAL SHAP ATTRIBUTION EVIDENCE
# ============================================================

def build_d12_global_shap_attribution() -> dict[str, Any]:
    """
    Calculate full-validation global SHAP attribution evidence.

    Two complementary views are produced:

    1. transformed-feature attribution across all 49 D7 features;
    2. source-feature-family attribution across the ten governed
       D6/D7 primary source-feature families.

    Mean absolute SHAP represents average attribution magnitude.
    Mean signed SHAP represents average direction in raw model-output
    space. Neither quantity is causal and neither is a probability-
    point effect.
    """

    attribution = (
        build_d12_governed_attribution_dataset()
    )

    shap_values = np.asarray(
        attribution[
            "shap_values"
        ],
        dtype=float,
    )

    feature_names = list(
        attribution[
            "transformed_feature_names"
        ]
    )

    if shap_values.shape != (
        D12_EXPECTED_VALIDATION_ENCOUNTERS,
        D12_EXPECTED_TRANSFORMED_FEATURE_COUNT,
    ):
        raise RuntimeError(
            "D12 global attribution received an unexpected "
            "SHAP matrix shape."
        )

    if len(feature_names) != (
        D12_EXPECTED_TRANSFORMED_FEATURE_COUNT
    ):
        raise RuntimeError(
            "D12 global attribution feature-name count mismatch."
        )

    mean_abs_shap = np.mean(
        np.abs(
            shap_values
        ),
        axis=0,
    )

    mean_signed_shap = np.mean(
        shap_values,
        axis=0,
    )

    total_mean_abs_shap = float(
        mean_abs_shap.sum()
    )

    if (
        not np.isfinite(
            total_mean_abs_shap
        )
        or total_mean_abs_shap <= 0.0
    ):
        raise RuntimeError(
            "D12 global SHAP magnitude denominator is invalid."
        )

    transformed_rows: list[dict[str, Any]] = []

    for index, feature_name in enumerate(
        feature_names
    ):
        source_family = (
            map_d12_transformed_feature_to_source_family(
                feature_name
            )
        )

        magnitude = float(
            mean_abs_shap[
                index
            ]
        )

        signed = float(
            mean_signed_shap[
                index
            ]
        )

        transformed_rows.append(
            {
                "transformed_feature":
                    feature_name,

                "source_feature_family":
                    source_family,

                "mean_absolute_shap":
                    magnitude,

                "mean_signed_shap":
                    signed,

                "absolute_attribution_share":
                    float(
                        magnitude
                        / total_mean_abs_shap
                    ),
            }
        )

    transformed_rows.sort(
        key=lambda row: (
            row[
                "mean_absolute_shap"
            ]
        ),
        reverse=True,
    )

    for rank, row in enumerate(
        transformed_rows,
        start=1,
    ):
        row[
            "global_rank"
        ] = rank

    family_accumulator: dict[
        str,
        dict[str, Any],
    ] = {}

    for source_family in (
        D12_SOURCE_FEATURE_FAMILIES
    ):
        family_accumulator[
            source_family
        ] = {
            "source_feature_family":
                source_family,

            "transformed_feature_count":
                0,

            "mean_absolute_shap":
                0.0,

            "mean_signed_shap":
                0.0,
        }

    for row in transformed_rows:
        family = row[
            "source_feature_family"
        ]

        family_accumulator[
            family
        ][
            "transformed_feature_count"
        ] += 1

        family_accumulator[
            family
        ][
            "mean_absolute_shap"
        ] += row[
            "mean_absolute_shap"
        ]

        family_accumulator[
            family
        ][
            "mean_signed_shap"
        ] += row[
            "mean_signed_shap"
        ]

    family_rows = list(
        family_accumulator.values()
    )

    for row in family_rows:
        row[
            "absolute_attribution_share"
        ] = float(
            row[
                "mean_absolute_shap"
            ]
            / total_mean_abs_shap
        )

    family_rows.sort(
        key=lambda row: (
            row[
                "mean_absolute_shap"
            ]
        ),
        reverse=True,
    )

    for rank, row in enumerate(
        family_rows,
        start=1,
    ):
        row[
            "global_family_rank"
        ] = rank

    utilization_mean_abs_shap = float(
        sum(
            family_accumulator[
                family
            ][
                "mean_absolute_shap"
            ]
            for family in (
                D12_PRIOR_UTILIZATION_FAMILY
            )
        )
    )

    utilization_signed_shap = float(
        sum(
            family_accumulator[
                family
            ][
                "mean_signed_shap"
            ]
            for family in (
                D12_PRIOR_UTILIZATION_FAMILY
            )
        )
    )

    utilization_share = float(
        utilization_mean_abs_shap
        / total_mean_abs_shap
    )

    return {
        "validation_status":
            "PASS",

        "encounter_count":
            attribution[
                "encounter_count"
            ],

        "transformed_feature_count":
            attribution[
                "feature_count"
            ],

        "source_feature_family_count":
            len(
                D12_SOURCE_FEATURE_FAMILIES
            ),

        "model_output":
            attribution[
                "model_output"
            ],

        "output_space_interpretation":
            attribution[
                "output_space_interpretation"
            ],

        "transformed_feature_attribution":
            transformed_rows,

        "source_family_attribution":
            family_rows,

        "total_mean_absolute_shap":
            total_mean_abs_shap,

        "prior_utilization_family":
            list(
                D12_PRIOR_UTILIZATION_FAMILY
            ),

        "prior_utilization_mean_absolute_shap":
            utilization_mean_abs_shap,

        "prior_utilization_mean_signed_shap":
            utilization_signed_shap,

        "prior_utilization_absolute_attribution_share":
            utilization_share,

        "prior_utilization_absolute_attribution_percent":
            float(
                utilization_share
                * 100.0
            ),

        "max_probability_reconstruction_error":
            attribution[
                "max_probability_reconstruction_error"
            ],

        "feature_attribution_is_causal":
            False,

        "shap_values_are_probability_point_changes":
            False,

        "model_retrained":
            False,

        "preprocessor_refitted":
            False,

        "threshold_retuned":
            False,

        "locked_test_accessed":
            False,

        "deployment_authorized":
            False,
    }


# ============================================================
# D12.25 — VALIDATE GLOBAL ATTRIBUTION EVIDENCE
# ============================================================

def validate_d12_global_shap_attribution(
    evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Validate global SHAP attribution completeness, source-family
    mapping, attribution-share conservation, and lifecycle controls.
    """

    if evidence is None:
        evidence = (
            build_d12_global_shap_attribution()
        )

    transformed_rows = evidence[
        "transformed_feature_attribution"
    ]

    family_rows = evidence[
        "source_family_attribution"
    ]

    transformed_share_sum = float(
        sum(
            row[
                "absolute_attribution_share"
            ]
            for row in transformed_rows
        )
    )

    family_share_sum = float(
        sum(
            row[
                "absolute_attribution_share"
            ]
            for row in family_rows
        )
    )

    mapped_families = {
        row[
            "source_feature_family"
        ]
        for row in transformed_rows
    }

    expected_families = set(
        D12_SOURCE_FEATURE_FAMILIES
    )

    utilization_share = float(
        evidence[
            "prior_utilization_absolute_attribution_share"
        ]
    )

    checks = {
        "encounter_count_valid":
            evidence[
                "encounter_count"
            ]
            == D12_EXPECTED_VALIDATION_ENCOUNTERS,

        "transformed_feature_count_valid":
            evidence[
                "transformed_feature_count"
            ]
            == D12_EXPECTED_TRANSFORMED_FEATURE_COUNT,

        "transformed_attribution_rows_complete":
            len(
                transformed_rows
            )
            == D12_EXPECTED_TRANSFORMED_FEATURE_COUNT,

        "source_family_count_valid":
            evidence[
                "source_feature_family_count"
            ]
            == len(
                D12_SOURCE_FEATURE_FAMILIES
            ),

        "source_family_rows_complete":
            len(
                family_rows
            )
            == len(
                D12_SOURCE_FEATURE_FAMILIES
            ),

        "all_governed_source_families_mapped":
            mapped_families
            == expected_families,

        "transformed_share_conserved":
            bool(
                np.isclose(
                    transformed_share_sum,
                    1.0,
                    rtol=0.0,
                    atol=1e-10,
                )
            ),

        "family_share_conserved":
            bool(
                np.isclose(
                    family_share_sum,
                    1.0,
                    rtol=0.0,
                    atol=1e-10,
                )
            ),

        "utilization_share_valid":
            bool(
                np.isfinite(
                    utilization_share
                )
                and 0.0
                <= utilization_share
                <= 1.0
            ),

        "model_output_is_raw":
            evidence[
                "model_output"
            ]
            == "raw",

        "attribution_not_causal":
            evidence[
                "feature_attribution_is_causal"
            ]
            is False,

        "not_probability_point_effects":
            evidence[
                "shap_values_are_probability_point_changes"
            ]
            is False,

        "model_not_retrained":
            evidence[
                "model_retrained"
            ]
            is False,

        "preprocessor_not_refitted":
            evidence[
                "preprocessor_refitted"
            ]
            is False,

        "threshold_not_retuned":
            evidence[
                "threshold_retuned"
            ]
            is False,

        "locked_test_not_accessed":
            evidence[
                "locked_test_accessed"
            ]
            is False,

        "deployment_not_authorized":
            evidence[
                "deployment_authorized"
            ]
            is False,
    }

    failed_checks = [
        name
        for name, passed in checks.items()
        if not passed
    ]

    return {
        "validation_status":
            "PASS"
            if not failed_checks
            else "FAIL",

        "checks":
            checks,

        "failed_checks":
            failed_checks,

        "transformed_share_sum":
            transformed_share_sum,

        "family_share_sum":
            family_share_sum,

        "prior_utilization_absolute_attribution_share":
            utilization_share,

        "prior_utilization_absolute_attribution_percent":
            float(
                utilization_share
                * 100.0
            ),

        "model_retrained":
            evidence[
                "model_retrained"
            ],

        "preprocessor_refitted":
            evidence[
                "preprocessor_refitted"
            ],

        "threshold_retuned":
            evidence[
                "threshold_retuned"
            ],

        "locked_test_accessed":
            evidence[
                "locked_test_accessed"
            ],

        "deployment_authorized":
            evidence[
                "deployment_authorized"
            ],
    }


# ============================================================
# D12.26 — PRINT GLOBAL ATTRIBUTION EVIDENCE
# ============================================================

def print_d12_global_shap_attribution(
    top_n: int = 15,
) -> None:
    """
    Print concise global SHAP evidence for transformed features,
    source-feature families, and the D11 prior-utilization question.
    """

    if top_n <= 0:
        raise ValueError(
            "D12 global attribution top_n must be positive."
        )

    evidence = (
        build_d12_global_shap_attribution()
    )

    validation = (
        validate_d12_global_shap_attribution(
            evidence
        )
    )

    transformed_rows = evidence[
        "transformed_feature_attribution"
    ]

    family_rows = evidence[
        "source_family_attribution"
    ]

    print(
        "D12 GLOBAL SHAP ATTRIBUTION & SOURCE-FAMILY EVIDENCE"
    )
    print("=" * 72)

    print(
        "STATUS:",
        validation[
            "validation_status"
        ],
    )

    print(
        "VALIDATION ENCOUNTERS:",
        evidence[
            "encounter_count"
        ],
    )

    print(
        "TRANSFORMED FEATURES:",
        evidence[
            "transformed_feature_count"
        ],
    )

    print(
        "SOURCE FEATURE FAMILIES:",
        evidence[
            "source_feature_family_count"
        ],
    )

    print(
        "MODEL OUTPUT:",
        evidence[
            "model_output"
        ],
    )

    print(
        "MAX RECONSTRUCTION ERROR:",
        evidence[
            "max_probability_reconstruction_error"
        ],
    )

    print()
    print(
        "TOP TRANSFORMED FEATURES BY MEAN |SHAP|"
    )
    print("-" * 72)

    for row in transformed_rows[
        :min(
            top_n,
            len(
                transformed_rows
            ),
        )
    ]:
        print(
            f"{row['global_rank']:>2}. "
            f"{row['transformed_feature']} | "
            f"family={row['source_feature_family']} | "
            f"mean|SHAP|={row['mean_absolute_shap']:.8f} | "
            f"meanSHAP={row['mean_signed_shap']:.8f} | "
            f"share={row['absolute_attribution_share'] * 100.0:.4f}%"
        )

    print()
    print(
        "SOURCE-FEATURE FAMILY ATTRIBUTION"
    )
    print("-" * 72)

    for row in family_rows:
        print(
            f"{row['global_family_rank']:>2}. "
            f"{row['source_feature_family']} | "
            f"n_transformed={row['transformed_feature_count']} | "
            f"mean|SHAP|={row['mean_absolute_shap']:.8f} | "
            f"meanSHAP={row['mean_signed_shap']:.8f} | "
            f"share={row['absolute_attribution_share'] * 100.0:.4f}%"
        )

    print()
    print(
        "D11 PRIOR-UTILIZATION CARRY-FORWARD"
    )
    print("-" * 72)

    print(
        "UTILIZATION FAMILY:",
        ", ".join(
            evidence[
                "prior_utilization_family"
            ]
        ),
    )

    print(
        "UTILIZATION MEAN |SHAP|:",
        evidence[
            "prior_utilization_mean_absolute_shap"
        ],
    )

    print(
        "UTILIZATION MEAN SIGNED SHAP:",
        evidence[
            "prior_utilization_mean_signed_shap"
        ],
    )

    print(
        "UTILIZATION ABSOLUTE ATTRIBUTION SHARE:",
        evidence[
            "prior_utilization_absolute_attribution_percent"
        ],
        "%",
    )

    print()
    print(
        "TRANSFORMED SHARE SUM:",
        validation[
            "transformed_share_sum"
        ],
    )

    print(
        "FAMILY SHARE SUM:",
        validation[
            "family_share_sum"
        ],
    )

    print(
        "FEATURE ATTRIBUTION IS CAUSAL:",
        evidence[
            "feature_attribution_is_causal"
        ],
    )

    print(
        "SHAP VALUES ARE PROBABILITY-POINT CHANGES:",
        evidence[
            "shap_values_are_probability_point_changes"
        ],
    )

    print(
        "MODEL RETRAINED:",
        validation[
            "model_retrained"
        ],
    )

    print(
        "PREPROCESSOR REFITTED:",
        validation[
            "preprocessor_refitted"
        ],
    )

    print(
        "THRESHOLD RETUNED:",
        validation[
            "threshold_retuned"
        ],
    )

    print(
        "LOCKED TEST:",
        validation[
            "locked_test_accessed"
        ],
    )

    print(
        "DEPLOYMENT AUTHORIZED:",
        validation[
            "deployment_authorized"
        ],
    )

    print(
        "FAILED CHECKS:",
        validation[
            "failed_checks"
        ],
    )


# ============================================================
# D12.27 — DIRECTIONALITY & DEPENDENCE GOVERNANCE CONTRACT
# ============================================================

D12_DIRECTIONALITY_FOCUS_FAMILIES = (
    "prior_inpatient_use",
    "prior_utilization_intensity",
    "prior_utilization_domain_count",
    "prior_outpatient_use",
    "age",
    "admission_source_id",
)

D12_DIRECTIONALITY_MIN_SUPPORT = 100


def build_d12_directionality_governance_contract() -> dict[str, Any]:
    """
    Define the governed scope for feature-directionality and dependence
    analysis on the frozen validation population.

    The analysis is descriptive of model behavior only. It does not
    estimate causal effects, biological mechanisms, or treatment effects.
    """

    return {
        "analysis_partition":
            "validation",

        "focus_feature_families":
            list(
                D12_DIRECTIONALITY_FOCUS_FAMILIES
            ),

        "minimum_support":
            D12_DIRECTIONALITY_MIN_SUPPORT,

        "directionality_metric":
            "mean_signed_shap_raw_margin_log_odds",

        "magnitude_metric":
            "mean_absolute_shap_raw_margin_log_odds",

        "dependence_interpretation":
            (
                "Observed feature values or categories are compared with "
                "their SHAP attribution distributions in the frozen model."
            ),

        "feature_attribution_is_causal":
            False,

        "biological_mechanism_claimed":
            False,

        "case_mix_may_contribute":
            True,

        "model_feature_dependence_may_contribute":
            True,

        "model_retrained":
            False,

        "preprocessor_refitted":
            False,

        "threshold_retuned":
            False,

        "probabilities_recalibrated":
            False,

        "locked_test_accessed":
            False,

        "deployment_authorized":
            False,
    }


# ============================================================
# D12.28 — SOURCE-FAMILY SHAP CONTRIBUTION MATRIX
# ============================================================

def build_d12_source_family_shap_matrix() -> dict[str, Any]:
    """
    Aggregate transformed-feature SHAP values encounter-by-encounter
    back to the ten governed D6/D7 source-feature families.

    Summation is valid because SHAP is additive in the governed raw
    model-output space.
    """

    attribution = (
        build_d12_governed_attribution_dataset()
    )

    shap_values = np.asarray(
        attribution[
            "shap_values"
        ],
        dtype=float,
    )

    feature_names = list(
        attribution[
            "transformed_feature_names"
        ]
    )

    family_names = list(
        D12_SOURCE_FEATURE_FAMILIES
    )

    family_matrix = np.zeros(
        (
            shap_values.shape[0],
            len(family_names),
        ),
        dtype=float,
    )

    family_feature_counts = {
        family: 0
        for family in family_names
    }

    for feature_index, feature_name in enumerate(
        feature_names
    ):
        family = (
            map_d12_transformed_feature_to_source_family(
                feature_name
            )
        )

        family_index = family_names.index(
            family
        )

        family_matrix[
            :,
            family_index
        ] += shap_values[
            :,
            feature_index
        ]

        family_feature_counts[
            family
        ] += 1

    reconstructed_from_families = (
        family_matrix.sum(
            axis=1
        )
    )

    reconstructed_from_features = (
        shap_values.sum(
            axis=1
        )
    )

    family_additivity_match = bool(
        np.allclose(
            reconstructed_from_families,
            reconstructed_from_features,
            rtol=0.0,
            atol=1e-12,
        )
    )

    if not family_additivity_match:
        raise RuntimeError(
            "D12 source-family SHAP aggregation does not preserve "
            "encounter-level additivity."
        )

    return {
        "family_shap_matrix":
            family_matrix,

        "family_names":
            family_names,

        "family_feature_counts":
            family_feature_counts,

        "encounter_count":
            int(
                family_matrix.shape[0]
            ),

        "family_count":
            int(
                family_matrix.shape[1]
            ),

        "family_additivity_match":
            family_additivity_match,

        "model_output":
            attribution[
                "model_output"
            ],

        "feature_attribution_is_causal":
            False,

        "model_retrained":
            False,

        "preprocessor_refitted":
            False,

        "threshold_retuned":
            False,

        "locked_test_accessed":
            False,

        "deployment_authorized":
            False,
    }


# ============================================================
# D12.29 — NUMERIC / BINARY FEATURE DIRECTIONALITY
# ============================================================

def _build_d12_numeric_directionality_rows(
    raw_values: Any,
    family_shap_values: np.ndarray,
) -> list[dict[str, Any]]:
    """
    Summarize observed numeric/binary values against source-family SHAP.
    """

    raw_array = np.asarray(
        raw_values
    )

    shap_array = np.asarray(
        family_shap_values,
        dtype=float,
    )

    if len(raw_array) != len(shap_array):
        raise RuntimeError(
            "D12 numeric directionality arrays are misaligned."
        )

    rows: list[dict[str, Any]] = []

    unique_values = sorted(
        {
            value
            for value in raw_array.tolist()
            if value == value
        },
        key=lambda value: float(value),
    )

    for value in unique_values:
        mask = (
            raw_array == value
        )

        n = int(
            mask.sum()
        )

        values = shap_array[
            mask
        ]

        if n == 0:
            continue

        rows.append(
            {
                "observed_value":
                    value,

                "support":
                    n,

                "support_adequate":
                    n
                    >= D12_DIRECTIONALITY_MIN_SUPPORT,

                "mean_signed_shap":
                    float(
                        np.mean(
                            values
                        )
                    ),

                "median_signed_shap":
                    float(
                        np.median(
                            values
                        )
                    ),

                "mean_absolute_shap":
                    float(
                        np.mean(
                            np.abs(
                                values
                            )
                        )
                    ),

                "positive_shap_fraction":
                    float(
                        np.mean(
                            values > 0.0
                        )
                    ),

                "negative_shap_fraction":
                    float(
                        np.mean(
                            values < 0.0
                        )
                    ),
            }
        )

    return rows


# ============================================================
# D12.30 — CATEGORICAL FEATURE DIRECTIONALITY
# ============================================================

def _build_d12_categorical_directionality_rows(
    raw_values: Any,
    family_shap_values: np.ndarray,
) -> list[dict[str, Any]]:
    """
    Summarize observed categories against aggregated source-family SHAP.
    """

    raw_array = np.asarray(
        raw_values,
        dtype=object,
    )

    shap_array = np.asarray(
        family_shap_values,
        dtype=float,
    )

    if len(raw_array) != len(shap_array):
        raise RuntimeError(
            "D12 categorical directionality arrays are misaligned."
        )

    categories = sorted(
        {
            str(value)
            for value in raw_array.tolist()
        }
    )

    rows: list[dict[str, Any]] = []

    string_values = np.asarray(
        [
            str(value)
            for value in raw_array.tolist()
        ],
        dtype=object,
    )

    for category in categories:
        mask = (
            string_values == category
        )

        n = int(
            mask.sum()
        )

        values = shap_array[
            mask
        ]

        if n == 0:
            continue

        rows.append(
            {
                "observed_value":
                    category,

                "support":
                    n,

                "support_adequate":
                    n
                    >= D12_DIRECTIONALITY_MIN_SUPPORT,

                "mean_signed_shap":
                    float(
                        np.mean(
                            values
                        )
                    ),

                "median_signed_shap":
                    float(
                        np.median(
                            values
                        )
                    ),

                "mean_absolute_shap":
                    float(
                        np.mean(
                            np.abs(
                                values
                            )
                        )
                    ),

                "positive_shap_fraction":
                    float(
                        np.mean(
                            values > 0.0
                        )
                    ),

                "negative_shap_fraction":
                    float(
                        np.mean(
                            values < 0.0
                        )
                    ),
            }
        )

    return rows


# ============================================================
# D12.31 — BUILD FEATURE DIRECTIONALITY & DEPENDENCE EVIDENCE
# ============================================================

def build_d12_feature_directionality_evidence() -> dict[str, Any]:
    """
    Build governed full-validation directionality/dependence evidence
    for the D11 carry-forward feature families.

    Numeric/binary utilization features are evaluated at their observed
    values. Age and admission source are evaluated categorically using
    the frozen raw validation representation.
    """

    contract = (
        build_d12_directionality_governance_contract()
    )

    runtime = (
        build_d12_frozen_runtime_boundary()
    )

    family_bundle = (
        build_d12_source_family_shap_matrix()
    )

    X_raw = runtime[
        "X_validation_raw"
    ]

    family_matrix = np.asarray(
        family_bundle[
            "family_shap_matrix"
        ],
        dtype=float,
    )

    family_names = list(
        family_bundle[
            "family_names"
        ]
    )

    required_raw_columns = set(
        D12_DIRECTIONALITY_FOCUS_FAMILIES
    )

    missing_columns = (
        required_raw_columns
        - set(
            X_raw.columns
        )
    )

    if missing_columns:
        raise RuntimeError(
            "D12 raw validation representation is missing "
            "directionality columns: "
            f"{sorted(missing_columns)}"
        )

    numeric_families = (
        "prior_inpatient_use",
        "prior_utilization_intensity",
        "prior_utilization_domain_count",
        "prior_outpatient_use",
    )

    categorical_families = (
        "age",
        "admission_source_id",
    )

    feature_evidence: dict[
        str,
        dict[str, Any],
    ] = {}

    for family in numeric_families:
        family_index = family_names.index(
            family
        )

        rows = (
            _build_d12_numeric_directionality_rows(
                X_raw[
                    family
                ].to_numpy(),
                family_matrix[
                    :,
                    family_index
                ],
            )
        )

        feature_evidence[
            family
        ] = {
            "analysis_type":
                "observed_numeric_value_directionality",

            "rows":
                rows,

            "adequate_support_rows":
                int(
                    sum(
                        row[
                            "support_adequate"
                        ]
                        for row in rows
                    )
                ),

            "low_support_rows":
                int(
                    sum(
                        not row[
                            "support_adequate"
                        ]
                        for row in rows
                    )
                ),
        }

    for family in categorical_families:
        family_index = family_names.index(
            family
        )

        rows = (
            _build_d12_categorical_directionality_rows(
                X_raw[
                    family
                ].to_numpy(),
                family_matrix[
                    :,
                    family_index
                ],
            )
        )

        feature_evidence[
            family
        ] = {
            "analysis_type":
                "observed_category_directionality",

            "rows":
                rows,

            "adequate_support_rows":
                int(
                    sum(
                        row[
                            "support_adequate"
                        ]
                        for row in rows
                    )
                ),

            "low_support_rows":
                int(
                    sum(
                        not row[
                            "support_adequate"
                        ]
                        for row in rows
                    )
                ),
        }

    return {
        "validation_status":
            "PASS",

        "governance_contract":
            contract,

        "encounter_count":
            family_bundle[
                "encounter_count"
            ],

        "focus_feature_family_count":
            len(
                D12_DIRECTIONALITY_FOCUS_FAMILIES
            ),

        "minimum_support":
            D12_DIRECTIONALITY_MIN_SUPPORT,

        "feature_evidence":
            feature_evidence,

        "family_additivity_match":
            family_bundle[
                "family_additivity_match"
            ],

        "model_output":
            family_bundle[
                "model_output"
            ],

        "feature_attribution_is_causal":
            False,

        "case_mix_may_contribute":
            True,

        "model_feature_dependence_may_contribute":
            True,

        "model_retrained":
            False,

        "preprocessor_refitted":
            False,

        "threshold_retuned":
            False,

        "locked_test_accessed":
            False,

        "deployment_authorized":
            False,
    }


# ============================================================
# D12.32 — VALIDATE DIRECTIONALITY & DEPENDENCE EVIDENCE
# ============================================================

def validate_d12_feature_directionality_evidence(
    evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Validate completeness and lifecycle integrity of D12 directionality
    and dependence evidence.
    """

    if evidence is None:
        evidence = (
            build_d12_feature_directionality_evidence()
        )

    feature_evidence = evidence[
        "feature_evidence"
    ]

    expected_families = set(
        D12_DIRECTIONALITY_FOCUS_FAMILIES
    )

    observed_families = set(
        feature_evidence.keys()
    )

    all_rows_nonempty = all(
        len(
            feature_evidence[
                family
            ][
                "rows"
            ]
        ) > 0
        for family in expected_families
    )

    all_support_conserved = all(
        sum(
            row[
                "support"
            ]
            for row in feature_evidence[
                family
            ][
                "rows"
            ]
        )
        == D12_EXPECTED_VALIDATION_ENCOUNTERS
        for family in expected_families
    )

    all_statistics_finite = all(
        np.isfinite(
            [
                row[
                    "mean_signed_shap"
                ],
                row[
                    "median_signed_shap"
                ],
                row[
                    "mean_absolute_shap"
                ],
                row[
                    "positive_shap_fraction"
                ],
                row[
                    "negative_shap_fraction"
                ],
            ]
        ).all()
        for family in expected_families
        for row in feature_evidence[
            family
        ][
            "rows"
        ]
    )

    checks = {
        "encounter_count_valid":
            evidence[
                "encounter_count"
            ]
            == D12_EXPECTED_VALIDATION_ENCOUNTERS,

        "focus_family_count_valid":
            evidence[
                "focus_feature_family_count"
            ]
            == len(
                D12_DIRECTIONALITY_FOCUS_FAMILIES
            ),

        "focus_families_complete":
            observed_families
            == expected_families,

        "all_feature_rows_nonempty":
            all_rows_nonempty,

        "support_conserved_for_each_feature":
            all_support_conserved,

        "all_statistics_finite":
            bool(
                all_statistics_finite
            ),

        "family_additivity_preserved":
            evidence[
                "family_additivity_match"
            ]
            is True,

        "model_output_is_raw":
            evidence[
                "model_output"
            ]
            == "raw",

        "attribution_not_causal":
            evidence[
                "feature_attribution_is_causal"
            ]
            is False,

        "case_mix_retained_as_possible_explanation":
            evidence[
                "case_mix_may_contribute"
            ]
            is True,

        "model_dependence_retained_as_possible_explanation":
            evidence[
                "model_feature_dependence_may_contribute"
            ]
            is True,

        "model_not_retrained":
            evidence[
                "model_retrained"
            ]
            is False,

        "preprocessor_not_refitted":
            evidence[
                "preprocessor_refitted"
            ]
            is False,

        "threshold_not_retuned":
            evidence[
                "threshold_retuned"
            ]
            is False,

        "locked_test_not_accessed":
            evidence[
                "locked_test_accessed"
            ]
            is False,

        "deployment_not_authorized":
            evidence[
                "deployment_authorized"
            ]
            is False,
    }

    failed_checks = [
        name
        for name, passed in checks.items()
        if not passed
    ]

    return {
        "validation_status":
            "PASS"
            if not failed_checks
            else "FAIL",

        "checks":
            checks,

        "failed_checks":
            failed_checks,

        "encounter_count":
            evidence[
                "encounter_count"
            ],

        "minimum_support":
            evidence[
                "minimum_support"
            ],

        "model_retrained":
            evidence[
                "model_retrained"
            ],

        "preprocessor_refitted":
            evidence[
                "preprocessor_refitted"
            ],

        "threshold_retuned":
            evidence[
                "threshold_retuned"
            ],

        "locked_test_accessed":
            evidence[
                "locked_test_accessed"
            ],

        "deployment_authorized":
            evidence[
                "deployment_authorized"
            ],
    }


# ============================================================
# D12.33 — PRINT DIRECTIONALITY & DEPENDENCE EVIDENCE
# ============================================================

def print_d12_feature_directionality_evidence() -> None:
    """
    Print the governed D12 feature directionality/dependence evidence.
    """

    evidence = (
        build_d12_feature_directionality_evidence()
    )

    validation = (
        validate_d12_feature_directionality_evidence(
            evidence
        )
    )

    print(
        "D12 FEATURE DIRECTIONALITY & DEPENDENCE EVIDENCE"
    )
    print("=" * 72)

    print(
        "STATUS:",
        validation[
            "validation_status"
        ],
    )

    print(
        "VALIDATION ENCOUNTERS:",
        evidence[
            "encounter_count"
        ],
    )

    print(
        "FOCUS FEATURE FAMILIES:",
        evidence[
            "focus_feature_family_count"
        ],
    )

    print(
        "MINIMUM SUPPORT:",
        evidence[
            "minimum_support"
        ],
    )

    print(
        "MODEL OUTPUT:",
        evidence[
            "model_output"
        ],
    )

    print()

    for family in (
        D12_DIRECTIONALITY_FOCUS_FAMILIES
    ):
        feature_result = evidence[
            "feature_evidence"
        ][
            family
        ]

        print(
            family.upper()
        )
        print("-" * 72)

        for row in feature_result[
            "rows"
        ]:
            print(
                f"value={row['observed_value']} | "
                f"N={row['support']} | "
                f"adequate={row['support_adequate']} | "
                f"meanSHAP={row['mean_signed_shap']:.8f} | "
                f"medianSHAP={row['median_signed_shap']:.8f} | "
                f"mean|SHAP|={row['mean_absolute_shap']:.8f} | "
                f"positive={row['positive_shap_fraction']:.4f} | "
                f"negative={row['negative_shap_fraction']:.4f}"
            )

        print(
            "ADEQUATE SUPPORT ROWS:",
            feature_result[
                "adequate_support_rows"
            ],
        )

        print(
            "LOW SUPPORT ROWS:",
            feature_result[
                "low_support_rows"
            ],
        )

        print()

    print(
        "FAMILY ADDITIVITY MATCH:",
        evidence[
            "family_additivity_match"
        ],
    )

    print(
        "FEATURE ATTRIBUTION IS CAUSAL:",
        evidence[
            "feature_attribution_is_causal"
        ],
    )

    print(
        "CASE MIX MAY CONTRIBUTE:",
        evidence[
            "case_mix_may_contribute"
        ],
    )

    print(
        "MODEL FEATURE DEPENDENCE MAY CONTRIBUTE:",
        evidence[
            "model_feature_dependence_may_contribute"
        ],
    )

    print(
        "MODEL RETRAINED:",
        validation[
            "model_retrained"
        ],
    )

    print(
        "PREPROCESSOR REFITTED:",
        validation[
            "preprocessor_refitted"
        ],
    )

    print(
        "THRESHOLD RETUNED:",
        validation[
            "threshold_retuned"
        ],
    )

    print(
        "LOCKED TEST:",
        validation[
            "locked_test_accessed"
        ],
    )

    print(
        "DEPLOYMENT AUTHORIZED:",
        validation[
            "deployment_authorized"
        ],
    )

    print(
        "FAILED CHECKS:",
        validation[
            "failed_checks"
        ],
    )


# ============================================================
# D12.34 — LOCAL PATIENT EXPLANATION GOVERNANCE CONTRACT
# ============================================================

D12_LOCAL_EXPLANATION_CASE_TYPES = (
    "true_negative_low_probability",
    "false_negative_highest_probability",
    "true_positive_nearest_threshold",
    "false_positive_nearest_threshold",
    "true_positive_high_probability",
)

D12_LOCAL_TOP_CONTRIBUTORS = 5
D12_LOCAL_PROBABILITY_TOLERANCE = 1e-6


def build_d12_local_explanation_governance_contract() -> dict[str, Any]:
    """
    Define the governed scope for representative patient-level
    explanations on the frozen validation partition.

    Cases are selected deterministically from validation predictions to
    demonstrate prediction traceability across clinically relevant
    operating situations. They are explanatory examples, not a new
    validation sample and not evidence of causal effects.
    """

    return {
        "analysis_partition":
            "validation",

        "selection_strategy":
            "deterministic_prediction_outcome_case_selection",

        "case_types":
            list(
                D12_LOCAL_EXPLANATION_CASE_TYPES
            ),

        "top_contributors_per_direction":
            D12_LOCAL_TOP_CONTRIBUTORS,

        "development_threshold":
            D12_EXPECTED_DEVELOPMENT_THRESHOLD,

        "model_output_space":
            "raw",

        "probability_link":
            "logistic_expit",

        "local_explanations_generalizable_to_population":
            False,

        "feature_attribution_is_causal":
            False,

        "clinical_decision_replaced":
            False,

        "model_retrained":
            False,

        "preprocessor_refitted":
            False,

        "threshold_retuned":
            False,

        "probabilities_recalibrated":
            False,

        "locked_test_accessed":
            False,

        "deployment_authorized":
            False,
    }


# ============================================================
# D12.35 — DETERMINISTIC REPRESENTATIVE CASE SELECTION
# ============================================================

def _select_d12_local_case_indices(
    y_true: np.ndarray,
    probabilities: np.ndarray,
    threshold: float,
) -> dict[str, int]:
    """
    Select deterministic validation cases spanning low-risk,
    threshold-adjacent error/correct cases, and high-risk behavior.

    No outcome or probability is modified. The locked TEST partition is
    not consulted.
    """

    y_array = np.asarray(
        y_true,
        dtype=int,
    )

    probability_array = np.asarray(
        probabilities,
        dtype=float,
    )

    if y_array.shape != probability_array.shape:
        raise RuntimeError(
            "D12 local case-selection outcome/probability shape mismatch."
        )

    predicted = (
        probability_array
        >= float(threshold)
    ).astype(int)

    tn = np.flatnonzero(
        (y_array == 0)
        & (predicted == 0)
    )

    fn = np.flatnonzero(
        (y_array == 1)
        & (predicted == 0)
    )

    tp = np.flatnonzero(
        (y_array == 1)
        & (predicted == 1)
    )

    fp = np.flatnonzero(
        (y_array == 0)
        & (predicted == 1)
    )

    required_groups = {
        "true_negative":
            tn,

        "false_negative":
            fn,

        "true_positive":
            tp,

        "false_positive":
            fp,
    }

    empty_groups = [
        name
        for name, indices in required_groups.items()
        if len(indices) == 0
    ]

    if empty_groups:
        raise RuntimeError(
            "D12 representative local explanation cannot be built "
            "because required validation confusion-matrix groups are "
            f"empty: {empty_groups}"
        )

    low_tn_index = int(
        tn[
            np.argmin(
                probability_array[
                    tn
                ]
            )
        ]
    )

    highest_fn_index = int(
        fn[
            np.argmax(
                probability_array[
                    fn
                ]
            )
        ]
    )

    nearest_tp_index = int(
        tp[
            np.argmin(
                np.abs(
                    probability_array[
                        tp
                    ]
                    - threshold
                )
            )
        ]
    )

    nearest_fp_index = int(
        fp[
            np.argmin(
                np.abs(
                    probability_array[
                        fp
                    ]
                    - threshold
                )
            )
        ]
    )

    high_tp_index = int(
        tp[
            np.argmax(
                probability_array[
                    tp
                ]
            )
        ]
    )

    selected = {
        "true_negative_low_probability":
            low_tn_index,

        "false_negative_highest_probability":
            highest_fn_index,

        "true_positive_nearest_threshold":
            nearest_tp_index,

        "false_positive_nearest_threshold":
            nearest_fp_index,

        "true_positive_high_probability":
            high_tp_index,
    }

    if len(set(selected.values())) != len(selected):
        raise RuntimeError(
            "D12 representative local case selection produced "
            "duplicate validation rows."
        )

    return selected


# ============================================================
# D12.36 — LOCAL SHAP PROBABILITY RECONSTRUCTION
# ============================================================

def _d12_expit_raw_output(
    raw_output: float,
) -> float:
    """
    Convert one raw XGBoost margin/log-odds value to probability using a
    numerically stable logistic transformation.
    """

    raw_value = float(
        raw_output
    )

    if raw_value >= 0.0:
        return float(
            1.0
            / (
                1.0
                + np.exp(
                    -raw_value
                )
            )
        )

    exp_value = np.exp(
        raw_value
    )

    return float(
        exp_value
        / (
            1.0
            + exp_value
        )
    )


# ============================================================
# D12.37 — LOCAL CONTRIBUTOR EXTRACTION
# ============================================================

def _build_d12_local_contributor_rows(
    shap_row: np.ndarray,
    transformed_feature_names: list[str],
    top_n: int = D12_LOCAL_TOP_CONTRIBUTORS,
) -> dict[str, list[dict[str, Any]]]:
    """
    Extract strongest upward and downward transformed-feature
    contributors for one validation encounter.
    """

    values = np.asarray(
        shap_row,
        dtype=float,
    )

    if values.shape != (
        D12_EXPECTED_TRANSFORMED_FEATURE_COUNT,
    ):
        raise RuntimeError(
            "D12 local contributor SHAP row has unexpected shape."
        )

    if len(transformed_feature_names) != (
        D12_EXPECTED_TRANSFORMED_FEATURE_COUNT
    ):
        raise RuntimeError(
            "D12 local contributor feature-name count mismatch."
        )

    if top_n <= 0:
        raise ValueError(
            "D12 local contributor top_n must be positive."
        )

    positive_indices = np.flatnonzero(
        values > 0.0
    )

    negative_indices = np.flatnonzero(
        values < 0.0
    )

    positive_sorted = positive_indices[
        np.argsort(
            values[
                positive_indices
            ]
        )[::-1]
    ]

    negative_sorted = negative_indices[
        np.argsort(
            values[
                negative_indices
            ]
        )
    ]

    def _row(index: int) -> dict[str, Any]:
        feature_name = transformed_feature_names[
            index
        ]

        return {
            "transformed_feature":
                feature_name,

            "source_feature_family":
                map_d12_transformed_feature_to_source_family(
                    feature_name
                ),

            "shap_value":
                float(
                    values[
                        index
                    ]
                ),
        }

    return {
        "top_upward_contributors":
            [
                _row(
                    int(index)
                )
                for index in positive_sorted[
                    :top_n
                ]
            ],

        "top_downward_contributors":
            [
                _row(
                    int(index)
                )
                for index in negative_sorted[
                    :top_n
                ]
            ],
    }


# ============================================================
# D12.38 — BUILD LOCAL PATIENT EXPLANATION EVIDENCE
# ============================================================

def build_d12_local_patient_explanation_evidence() -> dict[str, Any]:
    """
    Build governed patient-level explanation evidence for deterministic
    representative validation cases.

    Each case traces:
        SHAP base value
        + all transformed-feature SHAP contributions
        -> reconstructed raw model output
        -> reconstructed probability
        -> frozen model probability
        -> frozen D9 threshold classification

    Raw governed source-feature values are included for interpretability.
    No direct identifiers are exposed in the evidence printer.
    """

    import shap

    contract = (
        build_d12_local_explanation_governance_contract()
    )

    runtime = (
        build_d12_frozen_runtime_boundary()
    )

    estimator = runtime[
        "estimator"
    ]

    X_validation = runtime[
        "X_validation"
    ]

    X_raw = runtime[
        "X_validation_raw"
    ]

    y_validation = np.asarray(
        runtime[
            "y_validation"
        ],
        dtype=int,
    )

    probabilities = np.asarray(
        runtime[
            "validation_probability"
        ],
        dtype=float,
    )

    feature_names = list(
        runtime[
            "transformed_feature_names"
        ]
    )

    threshold = float(
        runtime[
            "selected_development_threshold"
        ]
    )

    selected_indices = (
        _select_d12_local_case_indices(
            y_validation,
            probabilities,
            threshold,
        )
    )

    ordered_indices = [
        selected_indices[
            case_type
        ]
        for case_type in (
            D12_LOCAL_EXPLANATION_CASE_TYPES
        )
    ]

    X_selected = X_validation[
        ordered_indices
    ]

    explainer = shap.TreeExplainer(
        estimator
    )

    explanation = explainer(
        X_selected
    )

    shap_values = np.asarray(
        explanation.values,
        dtype=float,
    )

    base_values = np.asarray(
        explanation.base_values,
        dtype=float,
    )

    expected_shape = (
        len(
            D12_LOCAL_EXPLANATION_CASE_TYPES
        ),
        D12_EXPECTED_TRANSFORMED_FEATURE_COUNT,
    )

    if shap_values.shape != expected_shape:
        raise RuntimeError(
            "D12 local SHAP matrix has unexpected shape. "
            f"Observed={shap_values.shape}, Expected={expected_shape}"
        )

    if base_values.shape != (
        len(
            D12_LOCAL_EXPLANATION_CASE_TYPES
        ),
    ):
        raise RuntimeError(
            "D12 local SHAP base-value shape mismatch."
        )

    raw_columns = [
        column
        for column in (
            D12_SOURCE_FEATURE_FAMILIES
        )
        if column in X_raw.columns
    ]

    if set(raw_columns) != set(
        D12_SOURCE_FEATURE_FAMILIES
    ):
        raise RuntimeError(
            "D12 local explanation raw validation representation "
            "does not contain all governed source-feature families."
        )

    cases: list[dict[str, Any]] = []

    for local_position, case_type in enumerate(
        D12_LOCAL_EXPLANATION_CASE_TYPES
    ):
        validation_index = int(
            ordered_indices[
                local_position
            ]
        )

        shap_row = shap_values[
            local_position
        ]

        base_value = float(
            base_values[
                local_position
            ]
        )

        shap_sum = float(
            shap_row.sum()
        )

        reconstructed_raw = float(
            base_value
            + shap_sum
        )

        reconstructed_probability = (
            _d12_expit_raw_output(
                reconstructed_raw
            )
        )

        model_probability = float(
            probabilities[
                validation_index
            ]
        )

        predicted_class = int(
            model_probability
            >= threshold
        )

        true_outcome = int(
            y_validation[
                validation_index
            ]
        )

        contributors = (
            _build_d12_local_contributor_rows(
                shap_row,
                feature_names,
            )
        )

        raw_source_values = {
            source_feature:
                (
                    X_raw.iloc[
                        validation_index
                    ][
                        source_feature
                    ].item()
                    if hasattr(
                        X_raw.iloc[
                            validation_index
                        ][
                            source_feature
                        ],
                        "item",
                    )
                    else X_raw.iloc[
                        validation_index
                    ][
                        source_feature
                    ]
                )
            for source_feature in (
                D12_SOURCE_FEATURE_FAMILIES
            )
        }

        cases.append(
            {
                "case_type":
                    case_type,

                "validation_row_position":
                    validation_index,

                "true_outcome":
                    true_outcome,

                "predicted_class":
                    predicted_class,

                "classification_correct":
                    predicted_class
                    == true_outcome,

                "development_threshold":
                    threshold,

                "model_probability":
                    model_probability,

                "distance_from_threshold":
                    float(
                        model_probability
                        - threshold
                    ),

                "base_value_raw":
                    base_value,

                "shap_sum_raw":
                    shap_sum,

                "reconstructed_raw_output":
                    reconstructed_raw,

                "reconstructed_probability":
                    reconstructed_probability,

                "probability_reconstruction_error":
                    float(
                        abs(
                            reconstructed_probability
                            - model_probability
                        )
                    ),

                "raw_source_feature_values":
                    raw_source_values,

                "top_upward_contributors":
                    contributors[
                        "top_upward_contributors"
                    ],

                "top_downward_contributors":
                    contributors[
                        "top_downward_contributors"
                    ],

                "local_explanation_generalizable_to_population":
                    False,

                "feature_attribution_is_causal":
                    False,
            }
        )

    return {
        "validation_status":
            "PASS",

        "governance_contract":
            contract,

        "case_count":
            len(
                cases
            ),

        "case_types":
            list(
                D12_LOCAL_EXPLANATION_CASE_TYPES
            ),

        "cases":
            cases,

        "development_threshold":
            threshold,

        "model_output":
            str(
                explainer.model_output
            ),

        "max_probability_reconstruction_error":
            float(
                max(
                    case[
                        "probability_reconstruction_error"
                    ]
                    for case in cases
                )
            ),

        "local_explanations_generalizable_to_population":
            False,

        "feature_attribution_is_causal":
            False,

        "clinical_decision_replaced":
            False,

        "model_retrained":
            False,

        "preprocessor_refitted":
            False,

        "threshold_retuned":
            False,

        "locked_test_accessed":
            False,

        "deployment_authorized":
            False,
    }


# ============================================================
# D12.39 — VALIDATE LOCAL PATIENT EXPLANATION EVIDENCE
# ============================================================

def validate_d12_local_patient_explanation_evidence(
    evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Validate local explanation traceability, deterministic case coverage,
    SHAP probability reconstruction, and lifecycle governance controls.
    """

    if evidence is None:
        evidence = (
            build_d12_local_patient_explanation_evidence()
        )

    cases = evidence[
        "cases"
    ]

    observed_case_types = [
        case[
            "case_type"
        ]
        for case in cases
    ]

    unique_positions = {
        case[
            "validation_row_position"
        ]
        for case in cases
    }

    expected_correctness = {
        "true_negative_low_probability":
            True,

        "false_negative_highest_probability":
            False,

        "true_positive_nearest_threshold":
            True,

        "false_positive_nearest_threshold":
            False,

        "true_positive_high_probability":
            True,
    }

    case_labels_correct = all(
        case[
            "classification_correct"
        ]
        == expected_correctness[
            case[
                "case_type"
            ]
        ]
        for case in cases
    )

    threshold_classification_consistent = all(
        case[
            "predicted_class"
        ]
        == int(
            case[
                "model_probability"
            ]
            >= evidence[
                "development_threshold"
            ]
        )
        for case in cases
    )

    contributor_signs_valid = all(
        all(
            row[
                "shap_value"
            ] > 0.0
            for row in case[
                "top_upward_contributors"
            ]
        )
        and all(
            row[
                "shap_value"
            ] < 0.0
            for row in case[
                "top_downward_contributors"
            ]
        )
        for case in cases
    )

    raw_source_values_complete = all(
        set(
            case[
                "raw_source_feature_values"
            ].keys()
        )
        == set(
            D12_SOURCE_FEATURE_FAMILIES
        )
        for case in cases
    )

    all_case_errors_finite = bool(
        np.isfinite(
            [
                case[
                    "probability_reconstruction_error"
                ]
                for case in cases
            ]
        ).all()
    )

    checks = {
        "case_count_valid":
            evidence[
                "case_count"
            ]
            == len(
                D12_LOCAL_EXPLANATION_CASE_TYPES
            ),

        "case_types_complete_and_ordered":
            observed_case_types
            == list(
                D12_LOCAL_EXPLANATION_CASE_TYPES
            ),

        "case_positions_unique":
            len(
                unique_positions
            )
            == len(
                D12_LOCAL_EXPLANATION_CASE_TYPES
            ),

        "case_positions_within_validation":
            all(
                0
                <= position
                < D12_EXPECTED_VALIDATION_ENCOUNTERS
                for position in unique_positions
            ),

        "case_labels_match_selection_semantics":
            case_labels_correct,

        "threshold_classification_consistent":
            threshold_classification_consistent,

        "raw_source_values_complete":
            raw_source_values_complete,

        "contributor_signs_valid":
            contributor_signs_valid,

        "all_case_errors_finite":
            all_case_errors_finite,

        "probability_reconstruction_within_tolerance":
            evidence[
                "max_probability_reconstruction_error"
            ]
            <= D12_LOCAL_PROBABILITY_TOLERANCE,

        "model_output_is_raw":
            evidence[
                "model_output"
            ].lower()
            == "raw",

        "local_explanations_not_generalized":
            evidence[
                "local_explanations_generalizable_to_population"
            ]
            is False,

        "attribution_not_causal":
            evidence[
                "feature_attribution_is_causal"
            ]
            is False,

        "clinical_decision_not_replaced":
            evidence[
                "clinical_decision_replaced"
            ]
            is False,

        "model_not_retrained":
            evidence[
                "model_retrained"
            ]
            is False,

        "preprocessor_not_refitted":
            evidence[
                "preprocessor_refitted"
            ]
            is False,

        "threshold_not_retuned":
            evidence[
                "threshold_retuned"
            ]
            is False,

        "locked_test_not_accessed":
            evidence[
                "locked_test_accessed"
            ]
            is False,

        "deployment_not_authorized":
            evidence[
                "deployment_authorized"
            ]
            is False,
    }

    failed_checks = [
        name
        for name, passed in checks.items()
        if not passed
    ]

    return {
        "validation_status":
            "PASS"
            if not failed_checks
            else "FAIL",

        "checks":
            checks,

        "failed_checks":
            failed_checks,

        "case_count":
            evidence[
                "case_count"
            ],

        "development_threshold":
            evidence[
                "development_threshold"
            ],

        "max_probability_reconstruction_error":
            evidence[
                "max_probability_reconstruction_error"
            ],

        "model_retrained":
            evidence[
                "model_retrained"
            ],

        "preprocessor_refitted":
            evidence[
                "preprocessor_refitted"
            ],

        "threshold_retuned":
            evidence[
                "threshold_retuned"
            ],

        "locked_test_accessed":
            evidence[
                "locked_test_accessed"
            ],

        "deployment_authorized":
            evidence[
                "deployment_authorized"
            ],
    }


# ============================================================
# D12.40 — PRINT LOCAL PATIENT EXPLANATION EVIDENCE
# ============================================================

def print_d12_local_patient_explanation_evidence() -> None:
    """
    Print representative patient-level explanation evidence without
    exposing direct patient identifiers.
    """

    evidence = (
        build_d12_local_patient_explanation_evidence()
    )

    validation = (
        validate_d12_local_patient_explanation_evidence(
            evidence
        )
    )

    print(
        "D12 LOCAL PATIENT EXPLANATION & PREDICTION TRACEABILITY"
    )
    print("=" * 72)

    print(
        "STATUS:",
        validation[
            "validation_status"
        ],
    )

    print(
        "CASE COUNT:",
        validation[
            "case_count"
        ],
    )

    print(
        "DEVELOPMENT THRESHOLD:",
        validation[
            "development_threshold"
        ],
    )

    print(
        "MODEL OUTPUT:",
        evidence[
            "model_output"
        ],
    )

    print(
        "MAX PROBABILITY RECONSTRUCTION ERROR:",
        validation[
            "max_probability_reconstruction_error"
        ],
    )

    print()

    for case_number, case in enumerate(
        evidence[
            "cases"
        ],
        start=1,
    ):
        print(
            f"CASE {case_number}: "
            f"{case['case_type']}"
        )
        print("-" * 72)

        print(
            "VALIDATION ROW POSITION:",
            case[
                "validation_row_position"
            ],
        )

        print(
            "TRUE OUTCOME:",
            case[
                "true_outcome"
            ],
        )

        print(
            "PREDICTED CLASS:",
            case[
                "predicted_class"
            ],
        )

        print(
            "CLASSIFICATION CORRECT:",
            case[
                "classification_correct"
            ],
        )

        print(
            "MODEL PROBABILITY:",
            case[
                "model_probability"
            ],
        )

        print(
            "DISTANCE FROM THRESHOLD:",
            case[
                "distance_from_threshold"
            ],
        )

        print(
            "BASE VALUE (RAW):",
            case[
                "base_value_raw"
            ],
        )

        print(
            "SUM SHAP (RAW):",
            case[
                "shap_sum_raw"
            ],
        )

        print(
            "RECONSTRUCTED RAW OUTPUT:",
            case[
                "reconstructed_raw_output"
            ],
        )

        print(
            "RECONSTRUCTED PROBABILITY:",
            case[
                "reconstructed_probability"
            ],
        )

        print(
            "RECONSTRUCTION ERROR:",
            case[
                "probability_reconstruction_error"
            ],
        )

        print(
            "RAW SOURCE FEATURE VALUES:"
        )

        for source_feature in (
            D12_SOURCE_FEATURE_FAMILIES
        ):
            print(
                f"  {source_feature}: "
                f"{case['raw_source_feature_values'][source_feature]}"
            )

        print(
            "TOP UPWARD CONTRIBUTORS:"
        )

        for row in case[
            "top_upward_contributors"
        ]:
            print(
                f"  {row['transformed_feature']} | "
                f"family={row['source_feature_family']} | "
                f"SHAP={row['shap_value']:.8f}"
            )

        print(
            "TOP DOWNWARD CONTRIBUTORS:"
        )

        for row in case[
            "top_downward_contributors"
        ]:
            print(
                f"  {row['transformed_feature']} | "
                f"family={row['source_feature_family']} | "
                f"SHAP={row['shap_value']:.8f}"
            )

        print(
            "LOCAL EXPLANATION GENERALIZABLE:",
            case[
                "local_explanation_generalizable_to_population"
            ],
        )

        print(
            "FEATURE ATTRIBUTION IS CAUSAL:",
            case[
                "feature_attribution_is_causal"
            ],
        )

        print()

    print(
        "MODEL RETRAINED:",
        validation[
            "model_retrained"
        ],
    )

    print(
        "PREPROCESSOR REFITTED:",
        validation[
            "preprocessor_refitted"
        ],
    )

    print(
        "THRESHOLD RETUNED:",
        validation[
            "threshold_retuned"
        ],
    )

    print(
        "LOCKED TEST:",
        validation[
            "locked_test_accessed"
        ],
    )

    print(
        "DEPLOYMENT AUTHORIZED:",
        validation[
            "deployment_authorized"
        ],
    )

    print(
        "FAILED CHECKS:",
        validation[
            "failed_checks"
        ],
    )


# ============================================================
# D12.41 — ATTRIBUTION STABILITY & SLICE GOVERNANCE CONTRACT
# ============================================================

D12_SLICE_MINIMUM_ADEQUATE_SUPPORT = 100
D12_SLICE_TOP_K_SOURCE_FAMILIES = 5

D12_STABILITY_SLICE_REGISTRY = (
    "prior_utilization_domain_count",
    "prior_utilization_intensity_band",
    "age",
    "admission_source_id",
    "race",
    "gender",
)


def build_d12_attribution_stability_governance_contract() -> dict[str, Any]:
    """
    Define the governed attribution-stability analysis.

    Stability is assessed on the frozen validation partition by comparing
    source-feature attribution profiles within observed slices against the
    overall validation attribution profile.

    Differences are descriptive model-behavior evidence. They do not by
    themselves establish bias, unfairness, causality, clinical
    inappropriateness, or transportability failure.
    """

    return {
        "analysis_partition":
            "validation",

        "slice_registry":
            list(D12_STABILITY_SLICE_REGISTRY),

        "minimum_adequate_support":
            D12_SLICE_MINIMUM_ADEQUATE_SUPPORT,

        "top_k_source_families":
            D12_SLICE_TOP_K_SOURCE_FAMILIES,

        "profile_definition":
            (
                "mean absolute source-family SHAP attribution "
                "normalized to unit share"
            ),

        "magnitude_divergence_metric":
            "total_variation_distance",

        "rank_stability_metric":
            "spearman_rank_correlation",

        "top_family_overlap_metric":
            "top_k_jaccard",

        "material_instability_threshold_defined":
            False,

        "automatic_bias_labeling":
            False,

        "automatic_unfairness_labeling":
            False,

        "automatic_mitigation":
            False,

        "feature_attribution_is_causal":
            False,

        "slice_differences_may_reflect_case_mix":
            True,

        "low_support_slices_are_interpretation_limitations":
            True,

        "model_retrained":
            False,

        "preprocessor_refitted":
            False,

        "threshold_retuned":
            False,

        "probabilities_recalibrated":
            False,

        "subgroup_specific_thresholds_created":
            False,

        "locked_test_accessed":
            False,

        "deployment_authorized":
            False,
    }


# ============================================================
# D12.42 — SOURCE-FAMILY ENCOUNTER ATTRIBUTION MATRIX
# ============================================================

def build_d12_source_family_encounter_attribution_matrix(
    attribution_bundle: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Aggregate the 49 transformed-feature SHAP values into the 10 governed
    D6/D7 source-feature families for every validation encounter.

    Signed source-family SHAP values are summed within each encounter.
    Absolute profile magnitude is then calculated from the absolute value
    of each encounter-level source-family sum. This preserves the source
    feature as the unit of slice-level explanation.
    """

    if attribution_bundle is None:
        attribution_bundle = (
            build_d12_governed_attribution_dataset()
        )

    shap_values = np.asarray(
        attribution_bundle[
            "shap_values"
        ],
        dtype=float,
    )

    feature_names = list(
        attribution_bundle[
            "transformed_feature_names"
        ]
    )

    expected_shape = (
        D12_EXPECTED_VALIDATION_ENCOUNTERS,
        D12_EXPECTED_TRANSFORMED_FEATURE_COUNT,
    )

    if shap_values.shape != expected_shape:
        raise RuntimeError(
            "D12 source-family encounter attribution matrix received "
            "an unexpected SHAP shape. "
            f"Observed={shap_values.shape}, Expected={expected_shape}"
        )

    # D12.23 already provides the authoritative single-feature
    # mapper. Build the complete transformed -> source-family
    # registry from that existing interface rather than calling a
    # non-existent batch-mapping helper.
    mapping = [
        {
            "transformed_feature":
                feature_name,

            "source_feature_family":
                map_d12_transformed_feature_to_source_family(
                    feature_name
                ),
        }
        for feature_name in feature_names
    ]

    source_family_names = list(
        D12_SOURCE_FEATURE_FAMILIES
    )

    signed_matrix = np.zeros(
        (
            shap_values.shape[0],
            len(source_family_names),
        ),
        dtype=float,
    )

    transformed_index = {
        feature_name: index
        for index, feature_name in enumerate(
            feature_names
        )
    }

    for family_index, source_family in enumerate(
        source_family_names
    ):
        family_features = [
            row[
                "transformed_feature"
            ]
            for row in mapping
            if row[
                "source_feature_family"
            ]
            == source_family
        ]

        if not family_features:
            raise RuntimeError(
                "D12 source-family encounter attribution mapping "
                f"contains no transformed features for {source_family!r}."
            )

        column_indices = [
            transformed_index[
                feature_name
            ]
            for feature_name in family_features
        ]

        signed_matrix[
            :,
            family_index
        ] = shap_values[
            :,
            column_indices
        ].sum(
            axis=1
        )

    absolute_matrix = np.abs(
        signed_matrix
    )

    if not np.isfinite(
        signed_matrix
    ).all():
        raise RuntimeError(
            "D12 source-family signed attribution matrix contains "
            "non-finite values."
        )

    if not np.isfinite(
        absolute_matrix
    ).all():
        raise RuntimeError(
            "D12 source-family absolute attribution matrix contains "
            "non-finite values."
        )

    return {
        "validation_status":
            "PASS",

        "encounter_count":
            int(
                signed_matrix.shape[0]
            ),

        "source_family_count":
            int(
                signed_matrix.shape[1]
            ),

        "source_family_names":
            source_family_names,

        "signed_source_family_shap":
            signed_matrix,

        "absolute_source_family_shap":
            absolute_matrix,

        "transformed_feature_mapping":
            mapping,

        "feature_attribution_is_causal":
            False,

        "locked_test_accessed":
            False,

        "deployment_authorized":
            False,
    }


# ============================================================
# D12.43 — SLICE LABEL CONSTRUCTION
# ============================================================

def _build_d12_utilization_intensity_band_labels(
    raw_values: Any,
) -> np.ndarray:
    """
    Build deterministic utilization-intensity bands used only for
    descriptive attribution-stability analysis.
    """

    values = np.asarray(
        raw_values,
        dtype=float,
    )

    labels = np.empty(
        len(values),
        dtype=object,
    )

    labels[
        values == 0
    ] = "0"

    labels[
        values == 1
    ] = "1"

    labels[
        values == 2
    ] = "2"

    labels[
        (values >= 3)
        & (values <= 4)
    ] = "3-4"

    labels[
        (values >= 5)
        & (values <= 7)
    ] = "5-7"

    labels[
        values >= 8
    ] = "8+"

    unassigned = np.equal(
        labels,
        None,
    )

    if bool(
        np.any(
            unassigned
        )
    ):
        raise RuntimeError(
            "D12 utilization-intensity banding left observations "
            "unassigned."
        )

    return labels


def build_d12_stability_slice_labels(
    X_validation_raw: Any,
) -> dict[str, np.ndarray]:
    """
    Build observed validation-slice labels for attribution stability.

    No slice-specific model, threshold, calibration, or mitigation is
    created.
    """

    required_columns = {
        "prior_utilization_domain_count",
        "prior_utilization_intensity",
        "age",
        "admission_source_id",
        "race",
        "gender",
    }

    missing_columns = (
        required_columns
        - set(
            X_validation_raw.columns
        )
    )

    if missing_columns:
        raise RuntimeError(
            "D12 attribution-stability raw validation data are missing "
            f"required columns: {sorted(missing_columns)}"
        )

    labels = {
        "prior_utilization_domain_count":
            np.asarray(
                X_validation_raw[
                    "prior_utilization_domain_count"
                ].astype(str)
            ),

        "prior_utilization_intensity_band":
            _build_d12_utilization_intensity_band_labels(
                X_validation_raw[
                    "prior_utilization_intensity"
                ]
            ),

        "age":
            np.asarray(
                X_validation_raw[
                    "age"
                ].astype(str)
            ),

        "admission_source_id":
            np.asarray(
                X_validation_raw[
                    "admission_source_id"
                ].astype(str)
            ),

        "race":
            np.asarray(
                X_validation_raw[
                    "race"
                ].astype(str)
            ),

        "gender":
            np.asarray(
                X_validation_raw[
                    "gender"
                ].astype(str)
            ),
    }

    for slice_name, slice_values in labels.items():
        if len(slice_values) != (
            D12_EXPECTED_VALIDATION_ENCOUNTERS
        ):
            raise RuntimeError(
                "D12 attribution-stability slice length mismatch for "
                f"{slice_name!r}."
            )

    return labels


# ============================================================
# D12.44 — ATTRIBUTION PROFILE & STABILITY METRICS
# ============================================================

def _d12_rank_vector_descending(
    values: np.ndarray,
) -> np.ndarray:
    """
    Return deterministic 1..N ranks for descending attribution magnitude.
    """

    array = np.asarray(
        values,
        dtype=float,
    )

    order = np.argsort(
        -array,
        kind="stable",
    )

    ranks = np.empty(
        len(array),
        dtype=float,
    )

    ranks[
        order
    ] = np.arange(
        1,
        len(array) + 1,
        dtype=float,
    )

    return ranks


def _d12_spearman_from_rank_vectors(
    ranks_a: np.ndarray,
    ranks_b: np.ndarray,
) -> float:
    """
    Calculate Spearman rank correlation from deterministic rank vectors
    without adding a scipy dependency to this stage.
    """

    a = np.asarray(
        ranks_a,
        dtype=float,
    )

    b = np.asarray(
        ranks_b,
        dtype=float,
    )

    if a.shape != b.shape:
        raise RuntimeError(
            "D12 rank vectors have different shapes."
        )

    if len(a) < 2:
        return 1.0

    a_centered = (
        a
        - a.mean()
    )

    b_centered = (
        b
        - b.mean()
    )

    denominator = float(
        np.sqrt(
            np.sum(
                a_centered ** 2
            )
            * np.sum(
                b_centered ** 2
            )
        )
    )

    if denominator == 0.0:
        return 1.0

    return float(
        np.sum(
            a_centered
            * b_centered
        )
        / denominator
    )


def _build_d12_attribution_profile(
    signed_matrix: np.ndarray,
    row_mask: np.ndarray,
    source_family_names: list[str],
) -> dict[str, Any]:
    """
    Build one source-family attribution profile for a selected set of
    validation encounters.
    """

    selected = signed_matrix[
        row_mask
    ]

    if selected.shape[0] == 0:
        raise RuntimeError(
            "D12 attribution profile cannot be built from an empty slice."
        )

    mean_absolute = np.mean(
        np.abs(
            selected
        ),
        axis=0,
    )

    mean_signed = np.mean(
        selected,
        axis=0,
    )

    total_absolute = float(
        mean_absolute.sum()
    )

    if total_absolute <= 0.0:
        raise RuntimeError(
            "D12 attribution profile has non-positive total absolute "
            "attribution."
        )

    shares = (
        mean_absolute
        / total_absolute
    )

    ranks = (
        _d12_rank_vector_descending(
            mean_absolute
        )
    )

    ordered_indices = np.argsort(
        -mean_absolute,
        kind="stable",
    )

    rows = []

    for index in ordered_indices:
        rows.append(
            {
                "source_feature_family":
                    source_family_names[
                        int(index)
                    ],

                "mean_absolute_shap":
                    float(
                        mean_absolute[
                            index
                        ]
                    ),

                "mean_signed_shap":
                    float(
                        mean_signed[
                            index
                        ]
                    ),

                "absolute_attribution_share":
                    float(
                        shares[
                            index
                        ]
                    ),

                "rank":
                    int(
                        ranks[
                            index
                        ]
                    ),
            }
        )

    return {
        "encounter_count":
            int(
                selected.shape[0]
            ),

        "mean_absolute_shap":
            mean_absolute,

        "mean_signed_shap":
            mean_signed,

        "absolute_attribution_share":
            shares,

        "rank_vector":
            ranks,

        "rows":
            rows,
    }


def _compare_d12_attribution_profiles(
    overall_profile: dict[str, Any],
    slice_profile: dict[str, Any],
    source_family_names: list[str],
) -> dict[str, Any]:
    """
    Compare one slice attribution profile with the overall validation
    profile using descriptive magnitude, ranking, and top-family overlap
    measures.
    """

    overall_share = np.asarray(
        overall_profile[
            "absolute_attribution_share"
        ],
        dtype=float,
    )

    slice_share = np.asarray(
        slice_profile[
            "absolute_attribution_share"
        ],
        dtype=float,
    )

    total_variation_distance = float(
        0.5
        * np.abs(
            slice_share
            - overall_share
        ).sum()
    )

    spearman_rank_correlation = (
        _d12_spearman_from_rank_vectors(
            overall_profile[
                "rank_vector"
            ],
            slice_profile[
                "rank_vector"
            ],
        )
    )

    k = min(
        D12_SLICE_TOP_K_SOURCE_FAMILIES,
        len(
            source_family_names
        ),
    )

    overall_top_indices = set(
        np.argsort(
            -overall_share,
            kind="stable",
        )[
            :k
        ].tolist()
    )

    slice_top_indices = set(
        np.argsort(
            -slice_share,
            kind="stable",
        )[
            :k
        ].tolist()
    )

    union = (
        overall_top_indices
        | slice_top_indices
    )

    intersection = (
        overall_top_indices
        & slice_top_indices
    )

    top_k_jaccard = float(
        len(
            intersection
        )
        / len(
            union
        )
    )

    share_difference = (
        slice_share
        - overall_share
    )

    largest_shift_index = int(
        np.argmax(
            np.abs(
                share_difference
            )
        )
    )

    slice_top_index = int(
        np.argmax(
            slice_share
        )
    )

    return {
        "total_variation_distance":
            total_variation_distance,

        "spearman_rank_correlation":
            spearman_rank_correlation,

        "top_k_jaccard":
            top_k_jaccard,

        "slice_top_source_family":
            source_family_names[
                slice_top_index
            ],

        "slice_top_source_family_share":
            float(
                slice_share[
                    slice_top_index
                ]
            ),

        "largest_share_shift_family":
            source_family_names[
                largest_shift_index
            ],

        "largest_share_shift":
            float(
                share_difference[
                    largest_shift_index
                ]
            ),

        "largest_absolute_share_shift":
            float(
                abs(
                    share_difference[
                        largest_shift_index
                    ]
                )
            ),
    }


# ============================================================
# D12.45 — BUILD ATTRIBUTION STABILITY & SLICE EVIDENCE
# ============================================================

def build_d12_attribution_stability_slice_evidence() -> dict[str, Any]:
    """
    Build descriptive attribution-stability evidence across governed
    validation slices.

    The analysis compares each observed slice's source-family attribution
    profile with the overall validation attribution profile. It does not
    define a universal threshold for "acceptable" explanation stability.
    """

    attribution = (
        build_d12_governed_attribution_dataset()
    )

    source_matrix_bundle = (
        build_d12_source_family_encounter_attribution_matrix(
            attribution
        )
    )

    runtime = (
        build_d12_frozen_runtime_boundary()
    )

    X_raw = runtime[
        "X_validation_raw"
    ]

    signed_matrix = np.asarray(
        source_matrix_bundle[
            "signed_source_family_shap"
        ],
        dtype=float,
    )

    source_family_names = list(
        source_matrix_bundle[
            "source_family_names"
        ]
    )

    all_rows_mask = np.ones(
        signed_matrix.shape[0],
        dtype=bool,
    )

    overall_profile = (
        _build_d12_attribution_profile(
            signed_matrix,
            all_rows_mask,
            source_family_names,
        )
    )

    slice_labels = (
        build_d12_stability_slice_labels(
            X_raw
        )
    )

    slice_rows: list[dict[str, Any]] = []

    for slice_dimension in (
        D12_STABILITY_SLICE_REGISTRY
    ):
        labels = np.asarray(
            slice_labels[
                slice_dimension
            ],
            dtype=object,
        )

        unique_labels = sorted(
            {
                str(value)
                for value in labels
            }
        )

        for slice_value in unique_labels:
            mask = np.asarray(
                [
                    str(value)
                    == slice_value
                    for value in labels
                ],
                dtype=bool,
            )

            profile = (
                _build_d12_attribution_profile(
                    signed_matrix,
                    mask,
                    source_family_names,
                )
            )

            comparison = (
                _compare_d12_attribution_profiles(
                    overall_profile,
                    profile,
                    source_family_names,
                )
            )

            support = int(
                mask.sum()
            )

            slice_rows.append(
                {
                    "slice_dimension":
                        slice_dimension,

                    "slice_value":
                        slice_value,

                    "support":
                        support,

                    "support_adequate":
                        support
                        >= D12_SLICE_MINIMUM_ADEQUATE_SUPPORT,

                    "total_variation_distance":
                        comparison[
                            "total_variation_distance"
                        ],

                    "spearman_rank_correlation":
                        comparison[
                            "spearman_rank_correlation"
                        ],

                    "top_k_jaccard":
                        comparison[
                            "top_k_jaccard"
                        ],

                    "slice_top_source_family":
                        comparison[
                            "slice_top_source_family"
                        ],

                    "slice_top_source_family_share":
                        comparison[
                            "slice_top_source_family_share"
                        ],

                    "largest_share_shift_family":
                        comparison[
                            "largest_share_shift_family"
                        ],

                    "largest_share_shift":
                        comparison[
                            "largest_share_shift"
                        ],

                    "largest_absolute_share_shift":
                        comparison[
                            "largest_absolute_share_shift"
                        ],

                    "profile_rows":
                        profile[
                            "rows"
                        ],

                    "bias_or_unfairness_conclusion":
                        False,

                    "causal_conclusion":
                        False,
                }
            )

    adequate_rows = [
        row
        for row in slice_rows
        if row[
            "support_adequate"
        ]
    ]

    low_support_rows = [
        row
        for row in slice_rows
        if not row[
            "support_adequate"
        ]
    ]

    most_divergent_adequate = (
        max(
            adequate_rows,
            key=lambda row: row[
                "total_variation_distance"
            ],
        )
        if adequate_rows
        else None
    )

    lowest_rank_stability_adequate = (
        min(
            adequate_rows,
            key=lambda row: row[
                "spearman_rank_correlation"
            ],
        )
        if adequate_rows
        else None
    )

    return {
        "validation_status":
            "PASS",

        "governance_contract":
            build_d12_attribution_stability_governance_contract(),

        "validation_encounters":
            int(
                signed_matrix.shape[0]
            ),

        "source_family_count":
            len(
                source_family_names
            ),

        "source_family_names":
            source_family_names,

        "overall_profile_rows":
            overall_profile[
                "rows"
            ],

        "slice_rows":
            slice_rows,

        "slice_count":
            len(
                slice_rows
            ),

        "adequate_support_slice_count":
            len(
                adequate_rows
            ),

        "low_support_slice_count":
            len(
                low_support_rows
            ),

        "most_divergent_adequate_slice":
            most_divergent_adequate,

        "lowest_rank_stability_adequate_slice":
            lowest_rank_stability_adequate,

        "material_instability_threshold_defined":
            False,

        "automatic_bias_labeling":
            False,

        "automatic_mitigation_applied":
            False,

        "feature_attribution_is_causal":
            False,

        "slice_differences_may_reflect_case_mix":
            True,

        "model_retrained":
            False,

        "preprocessor_refitted":
            False,

        "threshold_retuned":
            False,

        "locked_test_accessed":
            False,

        "deployment_authorized":
            False,
    }


# ============================================================
# D12.46 — VALIDATE ATTRIBUTION STABILITY EVIDENCE
# ============================================================

def validate_d12_attribution_stability_slice_evidence(
    evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Validate completeness, mathematical bounds, support governance, and
    lifecycle controls for D12 attribution-stability evidence.
    """

    if evidence is None:
        evidence = (
            build_d12_attribution_stability_slice_evidence()
        )

    slice_rows = evidence[
        "slice_rows"
    ]

    dimensions_present = {
        row[
            "slice_dimension"
        ]
        for row in slice_rows
    }

    finite_metrics = all(
        np.isfinite(
            row[
                "total_variation_distance"
            ]
        )
        and np.isfinite(
            row[
                "spearman_rank_correlation"
            ]
        )
        and np.isfinite(
            row[
                "top_k_jaccard"
            ]
        )
        and np.isfinite(
            row[
                "largest_absolute_share_shift"
            ]
        )
        for row in slice_rows
    )

    metric_bounds_valid = all(
        0.0
        <= row[
            "total_variation_distance"
        ]
        <= 1.0 + 1e-12
        and -1.0 - 1e-12
        <= row[
            "spearman_rank_correlation"
        ]
        <= 1.0 + 1e-12
        and 0.0
        <= row[
            "top_k_jaccard"
        ]
        <= 1.0 + 1e-12
        for row in slice_rows
    )

    support_flags_correct = all(
        row[
            "support_adequate"
        ]
        == (
            row[
                "support"
            ]
            >= D12_SLICE_MINIMUM_ADEQUATE_SUPPORT
        )
        for row in slice_rows
    )

    profile_share_sums_valid = all(
        np.isclose(
            sum(
                profile_row[
                    "absolute_attribution_share"
                ]
                for profile_row in row[
                    "profile_rows"
                ]
            ),
            1.0,
            rtol=0.0,
            atol=1e-10,
        )
        for row in slice_rows
    )

    overall_share_sum_valid = np.isclose(
        sum(
            row[
                "absolute_attribution_share"
            ]
            for row in evidence[
                "overall_profile_rows"
            ]
        ),
        1.0,
        rtol=0.0,
        atol=1e-10,
    )

    checks = {
        "validation_encounter_count_valid":
            evidence[
                "validation_encounters"
            ]
            == D12_EXPECTED_VALIDATION_ENCOUNTERS,

        "source_family_count_valid":
            evidence[
                "source_family_count"
            ]
            == len(
                D12_SOURCE_FEATURE_FAMILIES
            ),

        "source_family_registry_valid":
            evidence[
                "source_family_names"
            ]
            == list(
                D12_SOURCE_FEATURE_FAMILIES
            ),

        "all_slice_dimensions_present":
            dimensions_present
            == set(
                D12_STABILITY_SLICE_REGISTRY
            ),

        "slice_rows_present":
            evidence[
                "slice_count"
            ]
            > 0,

        "support_partition_complete":
            (
                evidence[
                    "adequate_support_slice_count"
                ]
                + evidence[
                    "low_support_slice_count"
                ]
            )
            == evidence[
                "slice_count"
            ],

        "support_flags_correct":
            support_flags_correct,

        "finite_stability_metrics":
            finite_metrics,

        "stability_metric_bounds_valid":
            metric_bounds_valid,

        "slice_profile_share_sums_valid":
            profile_share_sums_valid,

        "overall_profile_share_sum_valid":
            bool(
                overall_share_sum_valid
            ),

        "no_material_threshold_invented":
            evidence[
                "material_instability_threshold_defined"
            ]
            is False,

        "no_automatic_bias_labeling":
            evidence[
                "automatic_bias_labeling"
            ]
            is False,

        "no_automatic_mitigation":
            evidence[
                "automatic_mitigation_applied"
            ]
            is False,

        "attribution_not_causal":
            evidence[
                "feature_attribution_is_causal"
            ]
            is False,

        "case_mix_retained_as_explanation":
            evidence[
                "slice_differences_may_reflect_case_mix"
            ]
            is True,

        "model_not_retrained":
            evidence[
                "model_retrained"
            ]
            is False,

        "preprocessor_not_refitted":
            evidence[
                "preprocessor_refitted"
            ]
            is False,

        "threshold_not_retuned":
            evidence[
                "threshold_retuned"
            ]
            is False,

        "locked_test_not_accessed":
            evidence[
                "locked_test_accessed"
            ]
            is False,

        "deployment_not_authorized":
            evidence[
                "deployment_authorized"
            ]
            is False,
    }

    failed_checks = [
        name
        for name, passed in checks.items()
        if not passed
    ]

    return {
        "validation_status":
            "PASS"
            if not failed_checks
            else "FAIL",

        "checks":
            checks,

        "failed_checks":
            failed_checks,

        "slice_count":
            evidence[
                "slice_count"
            ],

        "adequate_support_slice_count":
            evidence[
                "adequate_support_slice_count"
            ],

        "low_support_slice_count":
            evidence[
                "low_support_slice_count"
            ],

        "model_retrained":
            evidence[
                "model_retrained"
            ],

        "preprocessor_refitted":
            evidence[
                "preprocessor_refitted"
            ],

        "threshold_retuned":
            evidence[
                "threshold_retuned"
            ],

        "locked_test_accessed":
            evidence[
                "locked_test_accessed"
            ],

        "deployment_authorized":
            evidence[
                "deployment_authorized"
            ],
    }


# ============================================================
# D12.47 — PRINT ATTRIBUTION STABILITY & SLICE EVIDENCE
# ============================================================

def print_d12_attribution_stability_slice_evidence() -> None:
    """
    Print governed attribution-stability evidence across observed
    validation slices.
    """

    evidence = (
        build_d12_attribution_stability_slice_evidence()
    )

    validation = (
        validate_d12_attribution_stability_slice_evidence(
            evidence
        )
    )

    print(
        "D12 ATTRIBUTION STABILITY & SLICE ANALYSIS"
    )
    print("=" * 72)

    print(
        "STATUS:",
        validation[
            "validation_status"
        ],
    )

    print(
        "VALIDATION ENCOUNTERS:",
        evidence[
            "validation_encounters"
        ],
    )

    print(
        "SOURCE FEATURE FAMILIES:",
        evidence[
            "source_family_count"
        ],
    )

    print(
        "SLICE COUNT:",
        validation[
            "slice_count"
        ],
    )

    print(
        "ADEQUATE SUPPORT SLICES:",
        validation[
            "adequate_support_slice_count"
        ],
    )

    print(
        "LOW SUPPORT SLICES:",
        validation[
            "low_support_slice_count"
        ],
    )

    print(
        "MINIMUM ADEQUATE SUPPORT:",
        D12_SLICE_MINIMUM_ADEQUATE_SUPPORT,
    )

    print()

    print(
        "OVERALL SOURCE-FAMILY ATTRIBUTION PROFILE"
    )
    print("-" * 72)

    for row in evidence[
        "overall_profile_rows"
    ]:
        print(
            f"{row['rank']:>2}. "
            f"{row['source_feature_family']} | "
            f"mean|source SHAP|={row['mean_absolute_shap']:.8f} | "
            f"mean source SHAP={row['mean_signed_shap']:.8f} | "
            f"share={row['absolute_attribution_share']:.4%}"
        )

    print()

    for slice_dimension in (
        D12_STABILITY_SLICE_REGISTRY
    ):
        print(
            slice_dimension.upper()
        )
        print("-" * 72)

        dimension_rows = [
            row
            for row in evidence[
                "slice_rows"
            ]
            if row[
                "slice_dimension"
            ]
            == slice_dimension
        ]

        dimension_rows = sorted(
            dimension_rows,
            key=lambda row: (
                not row[
                    "support_adequate"
                ],
                -row[
                    "support"
                ],
                str(
                    row[
                        "slice_value"
                    ]
                ),
            ),
        )

        for row in dimension_rows:
            print(
                f"{row['slice_value']} | "
                f"N={row['support']} | "
                f"adequate={row['support_adequate']} | "
                f"TVD={row['total_variation_distance']:.4f} | "
                f"rank_rho={row['spearman_rank_correlation']:.4f} | "
                f"top{D12_SLICE_TOP_K_SOURCE_FAMILIES}_J="
                f"{row['top_k_jaccard']:.4f} | "
                f"top={row['slice_top_source_family']} "
                f"({row['slice_top_source_family_share']:.2%}) | "
                f"largest_shift={row['largest_share_shift_family']} "
                f"({row['largest_share_shift']:+.2%})"
            )

        print()

    most_divergent = evidence[
        "most_divergent_adequate_slice"
    ]

    lowest_rank = evidence[
        "lowest_rank_stability_adequate_slice"
    ]

    print(
        "ADEQUATE-SUPPORT STABILITY SUMMARY"
    )
    print("-" * 72)

    if most_divergent is not None:
        print(
            "MOST DIVERGENT BY TVD:",
            f"{most_divergent['slice_dimension']}="
            f"{most_divergent['slice_value']} | "
            f"N={most_divergent['support']} | "
            f"TVD={most_divergent['total_variation_distance']:.4f}",
        )

    if lowest_rank is not None:
        print(
            "LOWEST RANK STABILITY:",
            f"{lowest_rank['slice_dimension']}="
            f"{lowest_rank['slice_value']} | "
            f"N={lowest_rank['support']} | "
            f"rank_rho={lowest_rank['spearman_rank_correlation']:.4f}",
        )

    print(
        "MATERIAL INSTABILITY THRESHOLD DEFINED:",
        evidence[
            "material_instability_threshold_defined"
        ],
    )

    print(
        "AUTOMATIC BIAS LABELING:",
        evidence[
            "automatic_bias_labeling"
        ],
    )

    print(
        "FEATURE ATTRIBUTION IS CAUSAL:",
        evidence[
            "feature_attribution_is_causal"
        ],
    )

    print(
        "SLICE DIFFERENCES MAY REFLECT CASE MIX:",
        evidence[
            "slice_differences_may_reflect_case_mix"
        ],
    )

    print(
        "MODEL RETRAINED:",
        validation[
            "model_retrained"
        ],
    )

    print(
        "PREPROCESSOR REFITTED:",
        validation[
            "preprocessor_refitted"
        ],
    )

    print(
        "THRESHOLD RETUNED:",
        validation[
            "threshold_retuned"
        ],
    )

    print(
        "LOCKED TEST:",
        validation[
            "locked_test_accessed"
        ],
    )

    print(
        "DEPLOYMENT AUTHORIZED:",
        validation[
            "deployment_authorized"
        ],
    )

    print(
        "FAILED CHECKS:",
        validation[
            "failed_checks"
        ],
    )


# ============================================================
# D12.48 — CLINICAL PLAUSIBILITY REVIEW CONTRACT
# ============================================================

D12_CLINICAL_PLAUSIBILITY_REVIEW_ITEMS = (
    {
        "review_item": "prior_utilization_dependence",
        "evidence_status": "SUPPORTED",
        "clinical_interpretation": (
            "Prior healthcare utilization is plausibly relevant to "
            "30-day readmission risk because it may represent prior "
            "healthcare need, disease burden, care complexity, or "
            "recurrent service use."
        ),
        "governance_caution": (
            "The model's substantial dependence on utilization must not "
            "be interpreted as proof that utilization causally determines "
            "readmission or that the observed dependence is clinically "
            "optimal."
        ),
    },
    {
        "review_item": "age_attribution",
        "evidence_status": "SUPPORTED_WITH_HETEROGENEITY",
        "clinical_interpretation": (
            "Age is a clinically interpretable patient characteristic "
            "and demonstrates non-linear attribution behavior across "
            "observed age groups."
        ),
        "governance_caution": (
            "Age-related attribution heterogeneity requires continued "
            "review and must not be converted into a causal biological "
            "claim or autonomous age-based decision rule."
        ),
    },
    {
        "review_item": "admission_source_attribution",
        "evidence_status": "SUPPORTED_WITH_HETEROGENEITY",
        "clinical_interpretation": (
            "Admission source can plausibly encode differences in care "
            "pathway, referral context, urgency, or case mix."
        ),
        "governance_caution": (
            "Admission-source attribution differences may reflect case "
            "mix or data-generation processes and do not establish "
            "causal effects."
        ),
    },
    {
        "review_item": "race_and_gender_attribution",
        "evidence_status": "REQUIRES_RESPONSIBLE_AI_OVERSIGHT",
        "clinical_interpretation": (
            "Race and gender are interpretable demographic attributes "
            "but require heightened governance because model dependence "
            "may reflect representation, access, documentation, or "
            "structural differences rather than clinically appropriate "
            "risk mechanisms."
        ),
        "governance_caution": (
            "Attribution evidence alone cannot establish fairness, "
            "unfairness, discrimination, or clinical appropriateness."
        ),
    },
    {
        "review_item": "unknown_race_category",
        "evidence_status": "DATA_QUALITY_AND_INTERPRETATION_LIMITATION",
        "clinical_interpretation": (
            "The explicit unknown-race category is retained as observed "
            "data evidence rather than silently imputed into a known "
            "racial category."
        ),
        "governance_caution": (
            "Distinct attribution behavior for unknown race should be "
            "treated as a representation and data-quality limitation, "
            "not as evidence of racial bias by itself."
        ),
    },
    {
        "review_item": "local_prediction_traceability",
        "evidence_status": "SUPPORTED",
        "clinical_interpretation": (
            "Representative validation predictions can be decomposed "
            "into patient-level source information and model "
            "attributions while preserving exact prediction traceability."
        ),
        "governance_caution": (
            "Local explanations describe individual model behavior and "
            "must not substitute for clinician judgment or be generalized "
            "to the full population."
        ),
    },
)


def build_d12_clinical_plausibility_review() -> dict[str, Any]:
    """
    Build the governed clinical-plausibility review.

    This is an interpretive governance review of already-produced D12
    evidence. It does not establish clinical effectiveness, causality,
    fairness, or deployment readiness.
    """

    return {
        "validation_status": "PASS",
        "review_items": [
            dict(item)
            for item in D12_CLINICAL_PLAUSIBILITY_REVIEW_ITEMS
        ],
        "review_item_count":
            len(D12_CLINICAL_PLAUSIBILITY_REVIEW_ITEMS),
        "clinical_plausibility_supported":
            True,
        "clinical_appropriateness_established":
            False,
        "causal_mechanism_established":
            False,
        "fairness_established":
            False,
        "external_validation_established":
            False,
        "prospective_effectiveness_established":
            False,
        "human_clinical_review_required":
            True,
        "model_retrained":
            False,
        "preprocessor_refitted":
            False,
        "threshold_retuned":
            False,
        "locked_test_accessed":
            False,
        "deployment_authorized":
            False,
    }


# ============================================================
# D12.49 — D11 CARRY-FORWARD RESOLUTION REGISTER
# ============================================================

D12_D11_CARRY_FORWARD_RESOLUTION = (
    {
        "carry_forward_id": "D11-CF-01",
        "status": "RESOLVED_FOR_D12",
        "resolution": (
            "Global, directional, local, and slice-level explainability "
            "evidence demonstrates substantial model dependence on prior "
            "healthcare utilization, especially prior inpatient use and "
            "utilization intensity, without changing the D9 threshold."
        ),
        "residual_action": (
            "Preserve utilization-dependence evidence for D14 locked-test "
            "reassessment and later clinical/governance review."
        ),
    },
    {
        "carry_forward_id": "D11-CF-02",
        "status": "RESOLVED_FOR_D12",
        "resolution": (
            "Age and admission-source attribution behavior was examined "
            "across observed validation values and slices without causal "
            "interpretation."
        ),
        "residual_action": (
            "Retain age and admission-source heterogeneity as monitored "
            "interpretation findings."
        ),
    },
    {
        "carry_forward_id": "D11-CF-03",
        "status": "RESOLVED_WITH_RESIDUAL_UNCERTAINTY",
        "resolution": (
            "The observed utilization pattern is consistent with model "
            "feature dependence. Population case mix remains a plausible "
            "co-contributor, so the evidence does not isolate a causal "
            "mechanism."
        ),
        "residual_action": (
            "Do not represent utilization dependence as a causal or "
            "clinically optimal mechanism."
        ),
    },
    {
        "carry_forward_id": "D11-CF-04",
        "status": "RESOLVED_FOR_D12",
        "resolution": (
            "Low-support slices are retained explicitly as interpretation "
            "limitations and are not used for strong subgroup conclusions."
        ),
        "residual_action": (
            "Reassess support and behavior if additional data become "
            "available."
        ),
    },
    {
        "carry_forward_id": "D11-CF-05",
        "status": "DEFERRED_TO_D14_AS_REQUIRED",
        "resolution": (
            "Relevant explainability and robustness findings are preserved "
            "for one-time locked TEST reassessment."
        ),
        "residual_action": (
            "D14 must not use locked TEST results for validation-driven "
            "threshold retuning."
        ),
    },
    {
        "carry_forward_id": "D11-CF-06",
        "status": "CONTROL_PRESERVED",
        "resolution": (
            "Explainability evidence is not treated as authorization for "
            "clinical deployment."
        ),
        "residual_action": (
            "Deployment remains explicitly unauthorized."
        ),
    },
)


def build_d12_d11_carry_forward_resolution_register() -> dict[str, Any]:
    return {
        "validation_status": "PASS",
        "source_stage": "D11",
        "resolution_rows": [
            dict(row)
            for row in D12_D11_CARRY_FORWARD_RESOLUTION
        ],
        "resolution_count":
            len(D12_D11_CARRY_FORWARD_RESOLUTION),
        "all_d11_questions_accounted_for":
            len(D12_D11_CARRY_FORWARD_RESOLUTION)
            == len(D12_D11_CARRY_FORWARD_QUESTIONS),
        "locked_test_reassessment_preserved_for_d14":
            True,
        "deployment_authorized":
            False,
    }


# ============================================================
# D12.50 — EXPLAINABILITY LIMITATIONS REGISTER
# ============================================================

D12_EXPLAINABILITY_LIMITATIONS = (
    {
        "limitation_id": "D12-LIM-01",
        "limitation": (
            "SHAP attribution describes model behavior and does not "
            "establish causal effects or biological mechanisms."
        ),
        "control": (
            "All global, directional, local, and slice conclusions are "
            "reported as descriptive model-behavior evidence."
        ),
    },
    {
        "limitation_id": "D12-LIM-02",
        "limitation": (
            "SHAP values are produced in raw XGBoost margin/log-odds "
            "space and are not direct probability-point changes."
        ),
        "control": (
            "Probability reconstruction is governed through the logistic "
            "expit link and additivity validation."
        ),
    },
    {
        "limitation_id": "D12-LIM-03",
        "limitation": (
            "Related engineered prior-utilization features may distribute "
            "or share attribution and should not be interpreted as "
            "independent clinical effects."
        ),
        "control": (
            "Interpretation is performed at both transformed-feature and "
            "source-feature-family levels."
        ),
    },
    {
        "limitation_id": "D12-LIM-04",
        "limitation": (
            "Observed subgroup and slice attribution differences may "
            "reflect population case mix, representation, documentation, "
            "or data-generation processes."
        ),
        "control": (
            "Slice evidence is descriptive and does not automatically "
            "produce bias, unfairness, or causal labels."
        ),
    },
    {
        "limitation_id": "D12-LIM-05",
        "limitation": (
            "Low-support age and admission-source slices cannot support "
            "strong generalizable interpretation."
        ),
        "control": (
            "Slices below the governed support threshold remain explicit "
            "interpretation limitations."
        ),
    },
    {
        "limitation_id": "D12-LIM-06",
        "limitation": (
            "The unknown-race category demonstrates a data-quality and "
            "representation limitation."
        ),
        "control": (
            "Unknown race is retained transparently and is not silently "
            "mapped to a known category."
        ),
    },
    {
        "limitation_id": "D12-LIM-07",
        "limitation": (
            "Validation-partition explainability does not establish "
            "external, temporal, institutional, geographic, or prospective "
            "transportability."
        ),
        "control": (
            "No external or prospective validation claim is made."
        ),
    },
    {
        "limitation_id": "D12-LIM-08",
        "limitation": (
            "Explainability cannot by itself establish clinical utility, "
            "clinical appropriateness, fairness, safety, or deployment "
            "readiness."
        ),
        "control": (
            "D12 progression is limited to lifecycle governance and does "
            "not authorize clinical deployment."
        ),
    },
)


def build_d12_explainability_limitations_register() -> dict[str, Any]:
    return {
        "validation_status": "PASS",
        "limitations": [
            dict(row)
            for row in D12_EXPLAINABILITY_LIMITATIONS
        ],
        "limitation_count":
            len(D12_EXPLAINABILITY_LIMITATIONS),
        "causal_claim_prohibited":
            True,
        "probability_point_interpretation_prohibited":
            True,
        "low_support_overinterpretation_prohibited":
            True,
        "external_transportability_claim_prohibited":
            True,
        "deployment_inference_prohibited":
            True,
        "deployment_authorized":
            False,
    }


# ============================================================
# D12.51 — GOVERNANCE DISPOSITION CONTRACT
# ============================================================

D12_GOVERNANCE_DISPOSITION = (
    "CONDITIONAL_PASS_PROGRESS_TO_D13_WITH_EXPLAINABILITY_LIMITATIONS"
)

D12_NEXT_LIFECYCLE_STAGE = (
    "D13_MODEL_REGISTRY_AND_ARTIFACT_FREEZE"
)


def build_d12_governance_disposition() -> dict[str, Any]:
    """
    Synthesize D12 evidence into a lifecycle disposition.

    A D12 PASS authorizes progression to D13 only. It is not a clinical
    deployment authorization and does not consume the locked TEST set.
    """

    clinical_review = (
        build_d12_clinical_plausibility_review()
    )

    carry_forward = (
        build_d12_d11_carry_forward_resolution_register()
    )

    limitations = (
        build_d12_explainability_limitations_register()
    )

    return {
        "stage_id": "D12",
        "stage_name":
            D12_STAGE_NAME,
        "validation_status": "PASS",
        "governance_disposition":
            D12_GOVERNANCE_DISPOSITION,
        "progression_authorized":
            True,
        "next_lifecycle_stage":
            D12_NEXT_LIFECYCLE_STAGE,
        "primary_governance_question_answer":
            (
                "YES_WITH_LIMITATIONS: the frozen development-stage "
                "model can be explained at global, feature, patient, and "
                "slice levels in a governance-defensible manner, and the "
                "evidence materially investigates the D11 robustness "
                "findings without changing the frozen system."
            ),
        "clinical_plausibility_review_status":
            clinical_review["validation_status"],
        "d11_carry_forward_resolution_status":
            carry_forward["validation_status"],
        "explainability_limitations_status":
            limitations["validation_status"],
        "clinical_plausibility_supported":
            clinical_review["clinical_plausibility_supported"],
        "clinical_appropriateness_established":
            False,
        "fairness_established":
            False,
        "causality_established":
            False,
        "external_validation_established":
            False,
        "prospective_effectiveness_established":
            False,
        "locked_test_reassessment_required_in_d14":
            True,
        "model_retrained":
            False,
        "hyperparameters_retuned":
            False,
        "preprocessor_refitted":
            False,
        "features_reengineered":
            False,
        "feature_selection_changed":
            False,
        "threshold_retuned":
            False,
        "probabilities_recalibrated":
            False,
        "subgroup_specific_thresholds_created":
            False,
        "automatic_mitigation_applied":
            False,
        "locked_test_accessed":
            False,
        "autonomous_clinical_decision_authorized":
            False,
        "deployment_authorized":
            False,
    }


# ============================================================
# D12.52 — VALIDATE FINAL D12 GOVERNANCE DISPOSITION
# ============================================================

def validate_d12_governance_disposition(
    disposition: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Validate the final D12 lifecycle decision and immutable controls.
    """

    if disposition is None:
        disposition = (
            build_d12_governance_disposition()
        )

    checks = {
        "stage_id_valid":
            disposition["stage_id"] == "D12",
        "disposition_valid":
            disposition["governance_disposition"]
            == D12_GOVERNANCE_DISPOSITION,
        "progression_authorized":
            disposition["progression_authorized"] is True,
        "next_stage_is_d13":
            disposition["next_lifecycle_stage"]
            == D12_NEXT_LIFECYCLE_STAGE,
        "clinical_review_pass":
            disposition["clinical_plausibility_review_status"]
            == "PASS",
        "d11_carry_forward_accounted_for":
            disposition["d11_carry_forward_resolution_status"]
            == "PASS",
        "limitations_register_pass":
            disposition["explainability_limitations_status"]
            == "PASS",
        "clinical_plausibility_supported":
            disposition["clinical_plausibility_supported"] is True,
        "clinical_appropriateness_not_overclaimed":
            disposition["clinical_appropriateness_established"] is False,
        "fairness_not_overclaimed":
            disposition["fairness_established"] is False,
        "causality_not_overclaimed":
            disposition["causality_established"] is False,
        "external_validation_not_overclaimed":
            disposition["external_validation_established"] is False,
        "prospective_effectiveness_not_overclaimed":
            disposition["prospective_effectiveness_established"] is False,
        "d14_locked_test_reassessment_preserved":
            disposition["locked_test_reassessment_required_in_d14"]
            is True,
        "model_not_retrained":
            disposition["model_retrained"] is False,
        "hyperparameters_not_retuned":
            disposition["hyperparameters_retuned"] is False,
        "preprocessor_not_refitted":
            disposition["preprocessor_refitted"] is False,
        "features_not_reengineered":
            disposition["features_reengineered"] is False,
        "feature_selection_unchanged":
            disposition["feature_selection_changed"] is False,
        "threshold_not_retuned":
            disposition["threshold_retuned"] is False,
        "probabilities_not_recalibrated":
            disposition["probabilities_recalibrated"] is False,
        "no_subgroup_thresholds":
            disposition["subgroup_specific_thresholds_created"] is False,
        "no_automatic_mitigation":
            disposition["automatic_mitigation_applied"] is False,
        "locked_test_not_accessed":
            disposition["locked_test_accessed"] is False,
        "no_autonomous_clinical_decision":
            disposition[
                "autonomous_clinical_decision_authorized"
            ] is False,
        "deployment_not_authorized":
            disposition["deployment_authorized"] is False,
    }

    failed_checks = [
        name
        for name, passed in checks.items()
        if not passed
    ]

    return {
        "validation_status":
            "PASS" if not failed_checks else "FAIL",
        "checks":
            checks,
        "failed_checks":
            failed_checks,
        "governance_disposition":
            disposition["governance_disposition"],
        "progression_authorized":
            disposition["progression_authorized"],
        "next_lifecycle_stage":
            disposition["next_lifecycle_stage"],
        "locked_test_accessed":
            disposition["locked_test_accessed"],
        "deployment_authorized":
            disposition["deployment_authorized"],
    }


# ============================================================
# D12.53 — FINAL D12 GOVERNANCE SUMMARY
# ============================================================

def build_d12_final_governance_summary() -> dict[str, Any]:
    """
    Build the concise D12 closeout summary used for lifecycle evidence.
    """

    disposition = (
        build_d12_governance_disposition()
    )

    validation = (
        validate_d12_governance_disposition(
            disposition
        )
    )

    return {
        "validation_status":
            validation["validation_status"],
        "stage":
            "D12",
        "stage_name":
            D12_STAGE_NAME,
        "model_name":
            D12_EXPECTED_MODEL_NAME,
        "model_sha256":
            D12_EXPECTED_MODEL_SHA256,
        "development_threshold":
            D12_EXPECTED_DEVELOPMENT_THRESHOLD,
        "validation_encounters":
            D12_EXPECTED_VALIDATION_ENCOUNTERS,
        "transformed_features":
            D12_EXPECTED_TRANSFORMED_FEATURE_COUNT,
        "governance_disposition":
            disposition["governance_disposition"],
        "progression_authorized":
            disposition["progression_authorized"],
        "next_lifecycle_stage":
            disposition["next_lifecycle_stage"],
        "clinical_plausibility_supported":
            disposition["clinical_plausibility_supported"],
        "clinical_appropriateness_established":
            disposition["clinical_appropriateness_established"],
        "fairness_established":
            disposition["fairness_established"],
        "causality_established":
            disposition["causality_established"],
        "external_validation_established":
            disposition["external_validation_established"],
        "locked_test_reassessment_required_in_d14":
            disposition["locked_test_reassessment_required_in_d14"],
        "model_retrained":
            disposition["model_retrained"],
        "preprocessor_refitted":
            disposition["preprocessor_refitted"],
        "threshold_retuned":
            disposition["threshold_retuned"],
        "locked_test_accessed":
            disposition["locked_test_accessed"],
        "deployment_authorized":
            disposition["deployment_authorized"],
        "failed_checks":
            validation["failed_checks"],
    }


# ============================================================
# D12.54 — PRINT FINAL D12 GOVERNANCE DISPOSITION
# ============================================================

def print_d12_final_governance_disposition() -> None:
    """
    Print the final D12 lifecycle governance decision.
    """

    summary = (
        build_d12_final_governance_summary()
    )

    print(
        "D12 FINAL EXPLAINABILITY GOVERNANCE DISPOSITION"
    )
    print("=" * 72)

    print(
        "STATUS:",
        summary["validation_status"],
    )

    print(
        "MODEL:",
        summary["model_name"],
    )

    print(
        "MODEL SHA:",
        summary["model_sha256"],
    )

    print(
        "DEVELOPMENT THRESHOLD:",
        summary["development_threshold"],
    )

    print(
        "VALIDATION ENCOUNTERS:",
        summary["validation_encounters"],
    )

    print(
        "TRANSFORMED FEATURES:",
        summary["transformed_features"],
    )

    print(
        "GOVERNANCE DISPOSITION:",
        summary["governance_disposition"],
    )

    print(
        "PROGRESSION AUTHORIZED:",
        summary["progression_authorized"],
    )

    print(
        "NEXT LIFECYCLE STAGE:",
        summary["next_lifecycle_stage"],
    )

    print(
        "CLINICAL PLAUSIBILITY SUPPORTED:",
        summary["clinical_plausibility_supported"],
    )

    print(
        "CLINICAL APPROPRIATENESS ESTABLISHED:",
        summary["clinical_appropriateness_established"],
    )

    print(
        "FAIRNESS ESTABLISHED:",
        summary["fairness_established"],
    )

    print(
        "CAUSALITY ESTABLISHED:",
        summary["causality_established"],
    )

    print(
        "EXTERNAL VALIDATION ESTABLISHED:",
        summary["external_validation_established"],
    )

    print(
        "D14 LOCKED TEST REASSESSMENT REQUIRED:",
        summary["locked_test_reassessment_required_in_d14"],
    )

    print(
        "MODEL RETRAINED:",
        summary["model_retrained"],
    )

    print(
        "PREPROCESSOR REFITTED:",
        summary["preprocessor_refitted"],
    )

    print(
        "THRESHOLD RETUNED:",
        summary["threshold_retuned"],
    )

    print(
        "LOCKED TEST:",
        summary["locked_test_accessed"],
    )

    print(
        "DEPLOYMENT AUTHORIZED:",
        summary["deployment_authorized"],
    )

    print(
        "FAILED CHECKS:",
        summary["failed_checks"],
    )


# ============================================================
# D12.55 — PRINT D12 CLOSEOUT REGISTERS
# ============================================================

def print_d12_closeout_registers() -> None:
    """
    Print the clinical-plausibility, D11 carry-forward, and limitation
    registers supporting the final D12 governance disposition.
    """

    clinical = (
        build_d12_clinical_plausibility_review()
    )

    carry_forward = (
        build_d12_d11_carry_forward_resolution_register()
    )

    limitations = (
        build_d12_explainability_limitations_register()
    )

    print(
        "D12 CLINICAL PLAUSIBILITY REVIEW"
    )
    print("=" * 72)

    for row in clinical["review_items"]:
        print(
            f"{row['review_item']} | "
            f"{row['evidence_status']}"
        )
        print(
            "  Interpretation:",
            row["clinical_interpretation"],
        )
        print(
            "  Governance caution:",
            row["governance_caution"],
        )

    print()
    print(
        "D12 D11 CARRY-FORWARD RESOLUTION"
    )
    print("=" * 72)

    for row in carry_forward["resolution_rows"]:
        print(
            f"{row['carry_forward_id']} | "
            f"{row['status']}"
        )
        print(
            "  Resolution:",
            row["resolution"],
        )
        print(
            "  Residual action:",
            row["residual_action"],
        )

    print()
    print(
        "D12 EXPLAINABILITY LIMITATIONS REGISTER"
    )
    print("=" * 72)

    for row in limitations["limitations"]:
        print(
            f"{row['limitation_id']} | "
            f"{row['limitation']}"
        )
        print(
            "  Control:",
            row["control"],
        )

    print()
    print(
        "DEPLOYMENT AUTHORIZED:",
        False,
    )


# ============================================================
# D12.10 — MODULE ENTRY POINT
# ============================================================

if __name__ == "__main__":
    print_d12_static_system_boundary()