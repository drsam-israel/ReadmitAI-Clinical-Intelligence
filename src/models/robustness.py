# ============================================================
# D11 — ROBUSTNESS & TRANSPORTABILITY
# ============================================================
#
# Purpose:
#   Evaluate the robustness, stability, and development-stage
#   transportability of the frozen clinical AI candidate under
#   plausible perturbations and population conditions.
#
# Governance principle:
#   D11 evaluates the existing frozen system. It does not
#   retrain, retune, recalibrate, refit preprocessing, modify
#   the D9 operating threshold, access the locked TEST set,
#   or authorize clinical deployment.
# ============================================================

from __future__ import annotations

from typing import Final


# ============================================================
# D11.01 — LIFECYCLE IDENTITY
# ============================================================

D11_STAGE: Final[str] = "D11"
D11_STAGE_NAME: Final[str] = "Robustness & Transportability"

D11_TARGET: Final[str] = "readmitted_30d"

D11_SOURCE_PREPROCESSING_STAGE: Final[str] = "D7"
D11_SOURCE_MODEL_STAGE: Final[str] = "D8"
D11_SOURCE_THRESHOLD_STAGE: Final[str] = "D9"
D11_SOURCE_FAIRNESS_STAGE: Final[str] = "D10"

D11_EVALUATION_PARTITION: Final[str] = "validation"
D11_LOCKED_TEST_EVALUATION_STAGE: Final[str] = "D14"


# ============================================================
# D11.02 — FROZEN UPSTREAM SYSTEM IDENTITY
# ============================================================

D11_EXPECTED_SELECTED_MODEL: Final[str] = "xgboost"

D11_EXPECTED_MODEL_SHA256: Final[str] = (
    "2FD02A54DF759EBAAF0D02D64D5ACE16A519DF016990FAC065AF3249BDA88085"
)

D11_EXPECTED_DEVELOPMENT_THRESHOLD: Final[float] = 0.12

D11_EXPECTED_VALIDATION_ENCOUNTERS: Final[int] = 15052
D11_EXPECTED_VALIDATION_POSITIVES: Final[int] = 1692
D11_EXPECTED_VALIDATION_NEGATIVES: Final[int] = 13360

D11_EXPECTED_TRANSFORMED_FEATURE_COUNT: Final[int] = 49


# ============================================================
# D11.03 — FROZEN SYSTEM PROHIBITIONS
# ============================================================

D11_MODEL_RETRAINING_PERMITTED: Final[bool] = False

D11_HYPERPARAMETER_RETUNING_PERMITTED: Final[bool] = False

D11_PREPROCESSOR_REFITTING_PERMITTED: Final[bool] = False

D11_THRESHOLD_RETUNING_PERMITTED: Final[bool] = False

D11_SUBGROUP_SPECIFIC_THRESHOLDS_PERMITTED: Final[bool] = False

D11_MODEL_RECALIBRATION_PERMITTED: Final[bool] = False

D11_AUTOMATIC_ROBUSTNESS_MITIGATION_PERMITTED: Final[bool] = False

D11_LOCKED_TEST_ACCESS_PERMITTED: Final[bool] = False

D11_AUTONOMOUS_CLINICAL_DECISION_PERMITTED: Final[bool] = False

D11_DEPLOYMENT_AUTHORIZED: Final[bool] = False


# ============================================================
# D11.04 — ROBUSTNESS EVALUATION DOMAINS
# ============================================================

D11_ROBUSTNESS_DOMAINS: Final[tuple[str, ...]] = (
    "baseline_reproducibility",
    "input_perturbation",
    "missingness_stress",
    "category_stability",
    "utilization_shift",
    "population_slice_stability",
    "performance_stability",
    "calibration_stability",
    "threshold_operating_stability",
)


# ============================================================
# D11.05 — TRANSPORTABILITY INTERPRETATION BOUNDARY
# ============================================================

D11_TRANSPORTABILITY_SCOPE: Final[str] = (
    "Development-stage internal transportability analysis using "
    "the frozen held-out validation population and governed stress "
    "conditions. This stage does not constitute external validation."
)

D11_EXTERNAL_VALIDATION_ESTABLISHED: Final[bool] = False

D11_TEMPORAL_VALIDATION_ESTABLISHED: Final[bool] = False

D11_GEOGRAPHIC_TRANSPORTABILITY_ESTABLISHED: Final[bool] = False

D11_INSTITUTIONAL_TRANSPORTABILITY_ESTABLISHED: Final[bool] = False

D11_PROSPECTIVE_VALIDATION_ESTABLISHED: Final[bool] = False


# ============================================================
# D11.06 — ROBUSTNESS INTERPRETATION PRINCIPLES
# ============================================================

D11_INTERPRETATION_PRINCIPLES: Final[tuple[str, ...]] = (
    "Robustness is evaluated against the frozen D7-D10 system.",
    "Stress-test degradation is evidence for governance review, not automatic model rejection.",
    "Absence of degradation under simulated stress does not establish external transportability.",
    "Validation-cohort robustness does not substitute for temporal, geographic, institutional, or prospective validation.",
    "Stress conditions must be clinically and operationally interpretable.",
    "The D9 development threshold remains frozen at 0.12 throughout D11.",
    "No subgroup-specific threshold optimization is permitted.",
    "No model retraining, hyperparameter retuning, preprocessing refit, or recalibration is permitted.",
    "The locked TEST partition remains inaccessible until D14.",
    "D11 cannot authorize clinical deployment.",
)


# ============================================================
# D11.07 — STATIC GOVERNANCE CONTRACT VALIDATION
# ============================================================

def validate_d11_static_contract() -> dict:
    """
    Validate the frozen D11 lifecycle and governance boundary.

    This validator deliberately performs no model fitting,
    prediction, stress testing, or locked TEST access.
    """

    checks = {
        "stage_identity": D11_STAGE == "D11",
        "stage_name": D11_STAGE_NAME == "Robustness & Transportability",
        "target_identity": D11_TARGET == "readmitted_30d",

        "source_preprocessing_stage": D11_SOURCE_PREPROCESSING_STAGE == "D7",
        "source_model_stage": D11_SOURCE_MODEL_STAGE == "D8",
        "source_threshold_stage": D11_SOURCE_THRESHOLD_STAGE == "D9",
        "source_fairness_stage": D11_SOURCE_FAIRNESS_STAGE == "D10",

        "evaluation_partition_is_validation":
            D11_EVALUATION_PARTITION == "validation",

        "locked_test_stage_is_d14":
            D11_LOCKED_TEST_EVALUATION_STAGE == "D14",

        "selected_model_is_xgboost":
            D11_EXPECTED_SELECTED_MODEL == "xgboost",

        "model_sha256_is_frozen":
            D11_EXPECTED_MODEL_SHA256
            == "2FD02A54DF759EBAAF0D02D64D5ACE16A519DF016990FAC065AF3249BDA88085",

        "development_threshold_is_frozen":
            D11_EXPECTED_DEVELOPMENT_THRESHOLD == 0.12,

        "validation_encounters_are_frozen":
            D11_EXPECTED_VALIDATION_ENCOUNTERS == 15052,

        "validation_positives_are_frozen":
            D11_EXPECTED_VALIDATION_POSITIVES == 1692,

        "validation_negatives_are_frozen":
            D11_EXPECTED_VALIDATION_NEGATIVES == 13360,

        "transformed_feature_count_is_frozen":
            D11_EXPECTED_TRANSFORMED_FEATURE_COUNT == 49,

        "model_retraining_prohibited":
            D11_MODEL_RETRAINING_PERMITTED is False,

        "hyperparameter_retuning_prohibited":
            D11_HYPERPARAMETER_RETUNING_PERMITTED is False,

        "preprocessor_refitting_prohibited":
            D11_PREPROCESSOR_REFITTING_PERMITTED is False,

        "threshold_retuning_prohibited":
            D11_THRESHOLD_RETUNING_PERMITTED is False,

        "subgroup_thresholds_prohibited":
            D11_SUBGROUP_SPECIFIC_THRESHOLDS_PERMITTED is False,

        "model_recalibration_prohibited":
            D11_MODEL_RECALIBRATION_PERMITTED is False,

        "automatic_mitigation_prohibited":
            D11_AUTOMATIC_ROBUSTNESS_MITIGATION_PERMITTED is False,

        "locked_test_access_prohibited":
            D11_LOCKED_TEST_ACCESS_PERMITTED is False,

        "autonomous_clinical_decision_prohibited":
            D11_AUTONOMOUS_CLINICAL_DECISION_PERMITTED is False,

        "deployment_not_authorized":
            D11_DEPLOYMENT_AUTHORIZED is False,

        "external_validation_not_established":
            D11_EXTERNAL_VALIDATION_ESTABLISHED is False,

        "temporal_validation_not_established":
            D11_TEMPORAL_VALIDATION_ESTABLISHED is False,

        "geographic_transportability_not_established":
            D11_GEOGRAPHIC_TRANSPORTABILITY_ESTABLISHED is False,

        "institutional_transportability_not_established":
            D11_INSTITUTIONAL_TRANSPORTABILITY_ESTABLISHED is False,

        "prospective_validation_not_established":
            D11_PROSPECTIVE_VALIDATION_ESTABLISHED is False,
    }

    failed_checks = [
        check_name
        for check_name, passed in checks.items()
        if not passed
    ]

    return {
        "stage": D11_STAGE,
        "stage_name": D11_STAGE_NAME,
        "target": D11_TARGET,

        "evaluation_partition": D11_EVALUATION_PARTITION,

        "selected_model": D11_EXPECTED_SELECTED_MODEL,
        "model_sha256": D11_EXPECTED_MODEL_SHA256,

        "development_threshold":
            D11_EXPECTED_DEVELOPMENT_THRESHOLD,

        "validation_encounter_count":
            D11_EXPECTED_VALIDATION_ENCOUNTERS,

        "validation_positive_count":
            D11_EXPECTED_VALIDATION_POSITIVES,

        "validation_negative_count":
            D11_EXPECTED_VALIDATION_NEGATIVES,

        "transformed_feature_count":
            D11_EXPECTED_TRANSFORMED_FEATURE_COUNT,

        "robustness_domain_count":
            len(D11_ROBUSTNESS_DOMAINS),

        "robustness_domains":
            list(D11_ROBUSTNESS_DOMAINS),

        "transportability_scope":
            D11_TRANSPORTABILITY_SCOPE,

        "external_validation_established":
            D11_EXTERNAL_VALIDATION_ESTABLISHED,

        "temporal_validation_established":
            D11_TEMPORAL_VALIDATION_ESTABLISHED,

        "geographic_transportability_established":
            D11_GEOGRAPHIC_TRANSPORTABILITY_ESTABLISHED,

        "institutional_transportability_established":
            D11_INSTITUTIONAL_TRANSPORTABILITY_ESTABLISHED,

        "prospective_validation_established":
            D11_PROSPECTIVE_VALIDATION_ESTABLISHED,

        "model_retraining_permitted":
            D11_MODEL_RETRAINING_PERMITTED,

        "hyperparameter_retuning_permitted":
            D11_HYPERPARAMETER_RETUNING_PERMITTED,

        "preprocessor_refitting_permitted":
            D11_PREPROCESSOR_REFITTING_PERMITTED,

        "threshold_retuning_permitted":
            D11_THRESHOLD_RETUNING_PERMITTED,

        "subgroup_specific_thresholds_permitted":
            D11_SUBGROUP_SPECIFIC_THRESHOLDS_PERMITTED,

        "model_recalibration_permitted":
            D11_MODEL_RECALIBRATION_PERMITTED,

        "automatic_robustness_mitigation_permitted":
            D11_AUTOMATIC_ROBUSTNESS_MITIGATION_PERMITTED,

        "locked_test_access_permitted":
            D11_LOCKED_TEST_ACCESS_PERMITTED,

        "deployment_authorized":
            D11_DEPLOYMENT_AUTHORIZED,

        "checks": checks,
        "failed_checks": failed_checks,

        "validation_status":
            "PASS" if not failed_checks else "FAIL",
    }


# ============================================================
# D11.08 — EXECUTABLE STATIC CONTRACT CHECK
# ============================================================

if __name__ == "__main__":
    result = validate_d11_static_contract()

    print("=" * 60)
    print("D11 STATIC GOVERNANCE CONTRACT")
    print("=" * 60)

    for key, value in result.items():
        if key != "checks":
            print(f"{key}: {value}")

# ============================================================
# D11.09 — AUTHORITATIVE FROZEN BASELINE BOUNDARY
# ============================================================
#
# D11 must not independently recreate the governed D9 baseline
# by refitting or reconstructing preprocessing state.
#
# The authoritative D11 baseline is inherited from the frozen
# upstream lifecycle:
#
#   D7 -> persisted preprocessing artifacts and schema integrity
#   D8 -> persisted selected development model integrity
#   D9 -> authoritative validation probabilities and threshold
#   D10 -> fairness/subgroup validation outcome identity
#
# D11 may subsequently create governed perturbations for stress
# testing, but those experiments must always be compared against
# this immutable baseline.
# ============================================================

from pathlib import Path
import hashlib
import numpy as np

from src.models import clinical_utility as d9
from src.models import fairness as d10


# ============================================================
# D11.09A — FROZEN ARTIFACT PATHS
# ============================================================

D11_FROZEN_PREPROCESSOR_PATH: Final[Path] = Path(
    "artifacts/preprocessors/D7_primary_preprocessor.joblib"
)

D11_FROZEN_SCHEMA_PATH: Final[Path] = Path(
    "artifacts/preprocessors/D7_transformed_feature_schema.txt"
)

D11_FROZEN_MODEL_PATH: Final[Path] = Path(
    "artifacts/models/D8_selected_development_model.joblib"
)

D11_FROZEN_MODEL_METADATA_PATH: Final[Path] = Path(
    "artifacts/models/D8_selected_development_model_metadata.json"
)


# ============================================================
# D11.09B — FROZEN D7 ARTIFACT IDENTITIES
# ============================================================

D11_EXPECTED_D7_PREPROCESSOR_SHA256: Final[str] = (
    "076878C0BD7C9B80897F3AA06157719A1E311165299549D83213C789CA1ECEAC"
)

D11_EXPECTED_D7_SCHEMA_SHA256: Final[str] = (
    "69E0E7F19C64350A6995830E875C1303E5D14F55FD7CDA4A7D845CCDE7B756ED"
)


# ============================================================
# D11.09C — AUTHORITATIVE D9 BASELINE EXPECTATIONS
# ============================================================

D11_EXPECTED_BASELINE_PREDICTED_POSITIVE_COUNT: Final[int] = 4709

D11_EXPECTED_BASELINE_PREDICTED_POSITIVE_RATE: Final[float] = (
    0.3128487908583577
)

D11_EXPECTED_BASELINE_MEAN_PROBABILITY: Final[float] = (
    0.11372116307581723
)

D11_EXPECTED_BASELINE_MIN_PROBABILITY: Final[float] = (
    0.02802971936762333
)

D11_EXPECTED_BASELINE_MAX_PROBABILITY: Final[float] = (
    0.5256381630897522
)


# ============================================================
# D11.09D — FILE INTEGRITY HELPER
# ============================================================

def _d11_sha256_file(path: Path) -> str:
    """
    Return the uppercase SHA-256 digest of a persisted artifact.
    """

    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest().upper()


# ============================================================
# D11.09E — BUILD AUTHORITATIVE FROZEN BASELINE
# ============================================================

def build_d11_frozen_system_boundary() -> dict:
    """
    Build the authoritative D11 baseline boundary.

    IMPORTANT
    ---------
    D11 does not independently refit D7 preprocessing to recreate
    the D9 operating baseline.

    Instead, this function:

    1. verifies persisted D7 preprocessing artifact integrity;
    2. verifies persisted D8 model integrity;
    3. consumes the authoritative governed D9 validation
       probability boundary;
    4. verifies the frozen D9 threshold operating point;
    5. confirms outcome identity against D10;
    6. explicitly preserves all lifecycle prohibitions.

    This prevents baseline reconstruction drift from being
    misinterpreted as model robustness evidence.
    """

    # --------------------------------------------------------
    # 1. Verify required persisted artifacts exist
    # --------------------------------------------------------

    required_paths = {
        "d7_preprocessor":
            D11_FROZEN_PREPROCESSOR_PATH,

        "d7_schema":
            D11_FROZEN_SCHEMA_PATH,

        "d8_model":
            D11_FROZEN_MODEL_PATH,

        "d8_model_metadata":
            D11_FROZEN_MODEL_METADATA_PATH,
    }

    missing_artifacts = [
        name
        for name, path in required_paths.items()
        if not path.exists()
    ]

    if missing_artifacts:
        raise FileNotFoundError(
            "Required frozen lifecycle artifacts are missing: "
            f"{missing_artifacts}"
        )

    # --------------------------------------------------------
    # 2. Verify persisted D7 artifact integrity
    # --------------------------------------------------------

    observed_d7_preprocessor_sha256 = _d11_sha256_file(
        D11_FROZEN_PREPROCESSOR_PATH
    )

    observed_d7_schema_sha256 = _d11_sha256_file(
        D11_FROZEN_SCHEMA_PATH
    )

    if (
        observed_d7_preprocessor_sha256
        != D11_EXPECTED_D7_PREPROCESSOR_SHA256
    ):
        raise RuntimeError(
            "Frozen D7 preprocessor SHA-256 mismatch. "
            f"Expected {D11_EXPECTED_D7_PREPROCESSOR_SHA256}, "
            f"observed {observed_d7_preprocessor_sha256}."
        )

    if (
        observed_d7_schema_sha256
        != D11_EXPECTED_D7_SCHEMA_SHA256
    ):
        raise RuntimeError(
            "Frozen D7 transformed-feature schema SHA-256 mismatch. "
            f"Expected {D11_EXPECTED_D7_SCHEMA_SHA256}, "
            f"observed {observed_d7_schema_sha256}."
        )

    # --------------------------------------------------------
    # 3. Verify persisted D8 model integrity
    # --------------------------------------------------------

    observed_model_sha256 = _d11_sha256_file(
        D11_FROZEN_MODEL_PATH
    )

    if observed_model_sha256 != D11_EXPECTED_MODEL_SHA256:
        raise RuntimeError(
            "Frozen D8 model SHA-256 mismatch. "
            f"Expected {D11_EXPECTED_MODEL_SHA256}, "
            f"observed {observed_model_sha256}."
        )

    # --------------------------------------------------------
    # 4. Recover authoritative governed D9 baseline
    # --------------------------------------------------------

    d9_bundle = d9.build_d9_validation_prediction_bundle()

    required_d9_keys = {
        "validation_probability",
        "y_validation",
        "selected_model",
        "model_sha256",
        "d7_preprocessor_sha256",
        "d7_schema_sha256",
        "validation_encounter_count",
        "validation_positive_count",
        "validation_prevalence",
        "transformed_feature_count",
        "model_retrained",
        "hyperparameters_retuned",
        "preprocessor_refitted_in_d9",
        "locked_test_accessed",
        "deployment_authorized",
    }

    missing_d9_keys = sorted(
        required_d9_keys.difference(d9_bundle.keys())
    )

    if missing_d9_keys:
        raise RuntimeError(
            "D9 validation prediction bundle is missing required "
            f"D11 baseline keys: {missing_d9_keys}"
        )

    probabilities = np.asarray(
        d9_bundle["validation_probability"],
        dtype=float,
    )

    y_validation = np.asarray(
        d9_bundle["y_validation"],
        dtype=int,
    )

    # --------------------------------------------------------
    # 5. Validate authoritative D9 population
    # --------------------------------------------------------

    if len(probabilities) != D11_EXPECTED_VALIDATION_ENCOUNTERS:
        raise RuntimeError(
            "Authoritative D9 probability count does not match "
            "the frozen D11 validation population."
        )

    if len(y_validation) != D11_EXPECTED_VALIDATION_ENCOUNTERS:
        raise RuntimeError(
            "Authoritative D9 outcome count does not match "
            "the frozen D11 validation population."
        )

    observed_positive_count = int(
        y_validation.sum()
    )

    observed_negative_count = int(
        len(y_validation) - observed_positive_count
    )

    if observed_positive_count != D11_EXPECTED_VALIDATION_POSITIVES:
        raise RuntimeError(
            "Authoritative D9 validation positive count does not "
            "match the frozen D11 lifecycle contract."
        )

    if observed_negative_count != D11_EXPECTED_VALIDATION_NEGATIVES:
        raise RuntimeError(
            "Authoritative D9 validation negative count does not "
            "match the frozen D11 lifecycle contract."
        )

    # --------------------------------------------------------
    # 6. Validate authoritative probability vector
    # --------------------------------------------------------

    if not np.isfinite(probabilities).all():
        raise RuntimeError(
            "Authoritative D9 validation probabilities contain "
            "non-finite values."
        )

    if not (
        (probabilities >= 0.0)
        & (probabilities <= 1.0)
    ).all():
        raise RuntimeError(
            "Authoritative D9 validation probabilities fall "
            "outside [0, 1]."
        )

    probability_mean = float(
        probabilities.mean()
    )

    probability_min = float(
        probabilities.min()
    )

    probability_max = float(
        probabilities.max()
    )

    # --------------------------------------------------------
    # 7. Apply immutable D9 development threshold
    # --------------------------------------------------------

    predictions = (
        probabilities
        >= D11_EXPECTED_DEVELOPMENT_THRESHOLD
    ).astype(int)

    predicted_positive_count = int(
        predictions.sum()
    )

    predicted_positive_rate = float(
        predictions.mean()
    )

    # --------------------------------------------------------
    # 8. Verify exact frozen D9 operating baseline
    # --------------------------------------------------------

    if (
        predicted_positive_count
        != D11_EXPECTED_BASELINE_PREDICTED_POSITIVE_COUNT
    ):
        raise RuntimeError(
            "D11 authoritative baseline alert count does not "
            "reproduce the frozen D9 operating point. "
            f"Expected "
            f"{D11_EXPECTED_BASELINE_PREDICTED_POSITIVE_COUNT}, "
            f"observed {predicted_positive_count}."
        )

    if not np.isclose(
        predicted_positive_rate,
        D11_EXPECTED_BASELINE_PREDICTED_POSITIVE_RATE,
        rtol=0.0,
        atol=1e-15,
    ):
        raise RuntimeError(
            "D11 authoritative baseline predicted-positive rate "
            "does not reproduce the frozen D9 operating point."
        )

    if not np.isclose(
        probability_mean,
        D11_EXPECTED_BASELINE_MEAN_PROBABILITY,
        rtol=0.0,
        atol=1e-15,
    ):
        raise RuntimeError(
            "D11 authoritative baseline mean probability does "
            "not reproduce the frozen D9 probability boundary."
        )

    if not np.isclose(
        probability_min,
        D11_EXPECTED_BASELINE_MIN_PROBABILITY,
        rtol=0.0,
        atol=1e-15,
    ):
        raise RuntimeError(
            "D11 authoritative baseline minimum probability does "
            "not reproduce the frozen D9 probability boundary."
        )

    if not np.isclose(
        probability_max,
        D11_EXPECTED_BASELINE_MAX_PROBABILITY,
        rtol=0.0,
        atol=1e-15,
    ):
        raise RuntimeError(
            "D11 authoritative baseline maximum probability does "
            "not reproduce the frozen D9 probability boundary."
        )

    # --------------------------------------------------------
    # 9. Verify D9 carried frozen upstream identities
    # --------------------------------------------------------

    d9_model_identity_matches = bool(
        d9_bundle["selected_model"]
        == D11_EXPECTED_SELECTED_MODEL
    )

    d9_model_sha_matches = bool(
        d9_bundle["model_sha256"]
        == D11_EXPECTED_MODEL_SHA256
    )

    d9_preprocessor_sha_matches = bool(
        d9_bundle["d7_preprocessor_sha256"]
        == D11_EXPECTED_D7_PREPROCESSOR_SHA256
    )

    d9_schema_sha_matches = bool(
        d9_bundle["d7_schema_sha256"]
        == D11_EXPECTED_D7_SCHEMA_SHA256
    )

    d9_feature_count_matches = bool(
        int(d9_bundle["transformed_feature_count"])
        == D11_EXPECTED_TRANSFORMED_FEATURE_COUNT
    )

    # --------------------------------------------------------
    # 10. Recover D10 governed outcome boundary
    # --------------------------------------------------------

    d10_frame = d10.build_d10_fairness_evaluation_frame()

    if D11_TARGET not in d10_frame.columns:
        raise RuntimeError(
            "D10 fairness evaluation frame does not contain "
            f"required target column: {D11_TARGET}"
        )

    d10_outcomes = np.asarray(
        d10_frame[D11_TARGET],
        dtype=int,
    )

    d9_d10_outcomes_match = bool(
        np.array_equal(
            y_validation,
            d10_outcomes,
        )
    )

    # --------------------------------------------------------
    # 11. Return immutable D11 baseline boundary
    # --------------------------------------------------------

    return {
        "probabilities":
            probabilities,

        "predictions":
            predictions,

        "y_validation":
            y_validation,

        "selected_model":
            d9_bundle["selected_model"],

        "model_sha256":
            observed_model_sha256,

        "d7_preprocessor_sha256":
            observed_d7_preprocessor_sha256,

        "d7_schema_sha256":
            observed_d7_schema_sha256,

        "development_threshold":
            D11_EXPECTED_DEVELOPMENT_THRESHOLD,

        "validation_encounter_count":
            int(len(y_validation)),

        "validation_positive_count":
            observed_positive_count,

        "validation_negative_count":
            observed_negative_count,

        "validation_prevalence":
            float(y_validation.mean()),

        "transformed_feature_count":
            int(d9_bundle["transformed_feature_count"]),

        "probability_count":
            int(len(probabilities)),

        "probability_mean":
            probability_mean,

        "probability_min":
            probability_min,

        "probability_max":
            probability_max,

        "predicted_positive_count":
            predicted_positive_count,

        "predicted_positive_rate":
            predicted_positive_rate,

        "d9_model_identity_matches":
            d9_model_identity_matches,

        "d9_model_sha_matches":
            d9_model_sha_matches,

        "d9_preprocessor_sha_matches":
            d9_preprocessor_sha_matches,

        "d9_schema_sha_matches":
            d9_schema_sha_matches,

        "d9_feature_count_matches":
            d9_feature_count_matches,

        "d9_d10_outcomes_match_elementwise":
            d9_d10_outcomes_match,

        "baseline_source":
            "AUTHORITATIVE_FROZEN_D9_VALIDATION_BOUNDARY",

        "independent_baseline_preprocessor_refit":
            False,

        "model_retrained":
            False,

        "hyperparameters_retuned":
            False,

        "preprocessor_refitted_in_d11":
            False,

        "threshold_retuned":
            False,

        "subgroup_specific_thresholds_created":
            False,

        "model_recalibrated":
            False,

        "automatic_robustness_mitigation_applied":
            False,

        "locked_test_accessed":
            False,

        "external_validation_established":
            False,

        "temporal_validation_established":
            False,

        "geographic_transportability_established":
            False,

        "institutional_transportability_established":
            False,

        "prospective_validation_established":
            False,

        "deployment_authorized":
            False,
    }


# ============================================================
# D11.10 — AUTHORITATIVE BASELINE VALIDATION
# ============================================================

def validate_d11_frozen_system_boundary() -> dict:
    """
    Validate the immutable D11 baseline against the frozen
    D7-D10 lifecycle evidence.
    """

    boundary = build_d11_frozen_system_boundary()

    checks = {
        # ----------------------------------------------------
        # Frozen D7 artifact integrity
        # ----------------------------------------------------

        "d7_preprocessor_sha_matches":
            boundary["d7_preprocessor_sha256"]
            == D11_EXPECTED_D7_PREPROCESSOR_SHA256,

        "d7_schema_sha_matches":
            boundary["d7_schema_sha256"]
            == D11_EXPECTED_D7_SCHEMA_SHA256,

        # ----------------------------------------------------
        # Frozen D8 model integrity
        # ----------------------------------------------------

        "selected_model_matches":
            boundary["selected_model"]
            == D11_EXPECTED_SELECTED_MODEL,

        "model_sha256_matches":
            boundary["model_sha256"]
            == D11_EXPECTED_MODEL_SHA256,

        # ----------------------------------------------------
        # Frozen D9 operating baseline
        # ----------------------------------------------------

        "development_threshold_matches":
            boundary["development_threshold"]
            == D11_EXPECTED_DEVELOPMENT_THRESHOLD,

        "validation_encounter_count_matches":
            boundary["validation_encounter_count"]
            == D11_EXPECTED_VALIDATION_ENCOUNTERS,

        "validation_positive_count_matches":
            boundary["validation_positive_count"]
            == D11_EXPECTED_VALIDATION_POSITIVES,

        "validation_negative_count_matches":
            boundary["validation_negative_count"]
            == D11_EXPECTED_VALIDATION_NEGATIVES,

        "transformed_feature_count_matches":
            boundary["transformed_feature_count"]
            == D11_EXPECTED_TRANSFORMED_FEATURE_COUNT,

        "probability_count_matches":
            boundary["probability_count"]
            == D11_EXPECTED_VALIDATION_ENCOUNTERS,

        "baseline_alert_count_matches":
            boundary["predicted_positive_count"]
            == D11_EXPECTED_BASELINE_PREDICTED_POSITIVE_COUNT,

        "baseline_alert_rate_matches":
            np.isclose(
                boundary["predicted_positive_rate"],
                D11_EXPECTED_BASELINE_PREDICTED_POSITIVE_RATE,
                rtol=0.0,
                atol=1e-15,
            ),

        "baseline_probability_mean_matches":
            np.isclose(
                boundary["probability_mean"],
                D11_EXPECTED_BASELINE_MEAN_PROBABILITY,
                rtol=0.0,
                atol=1e-15,
            ),

        "baseline_probability_min_matches":
            np.isclose(
                boundary["probability_min"],
                D11_EXPECTED_BASELINE_MIN_PROBABILITY,
                rtol=0.0,
                atol=1e-15,
            ),

        "baseline_probability_max_matches":
            np.isclose(
                boundary["probability_max"],
                D11_EXPECTED_BASELINE_MAX_PROBABILITY,
                rtol=0.0,
                atol=1e-15,
            ),

        # ----------------------------------------------------
        # Cross-stage lineage
        # ----------------------------------------------------

        "d9_model_identity_matches":
            boundary["d9_model_identity_matches"] is True,

        "d9_model_sha_matches":
            boundary["d9_model_sha_matches"] is True,

        "d9_preprocessor_sha_matches":
            boundary["d9_preprocessor_sha_matches"] is True,

        "d9_schema_sha_matches":
            boundary["d9_schema_sha_matches"] is True,

        "d9_feature_count_matches":
            boundary["d9_feature_count_matches"] is True,

        "d9_d10_outcomes_match_elementwise":
            boundary[
                "d9_d10_outcomes_match_elementwise"
            ] is True,

        # ----------------------------------------------------
        # D11 governance protections
        # ----------------------------------------------------

        "authoritative_baseline_source":
            boundary["baseline_source"]
            == "AUTHORITATIVE_FROZEN_D9_VALIDATION_BOUNDARY",

        "no_independent_baseline_preprocessor_refit":
            boundary[
                "independent_baseline_preprocessor_refit"
            ] is False,

        "model_not_retrained":
            boundary["model_retrained"] is False,

        "hyperparameters_not_retuned":
            boundary["hyperparameters_retuned"] is False,

        "preprocessor_not_refitted_in_d11":
            boundary["preprocessor_refitted_in_d11"] is False,

        "threshold_not_retuned":
            boundary["threshold_retuned"] is False,

        "subgroup_thresholds_not_created":
            boundary[
                "subgroup_specific_thresholds_created"
            ] is False,

        "model_not_recalibrated":
            boundary["model_recalibrated"] is False,

        "automatic_mitigation_not_applied":
            boundary[
                "automatic_robustness_mitigation_applied"
            ] is False,

        "locked_test_not_accessed":
            boundary["locked_test_accessed"] is False,

        # ----------------------------------------------------
        # Transportability claims remain constrained
        # ----------------------------------------------------

        "external_validation_not_established":
            boundary[
                "external_validation_established"
            ] is False,

        "temporal_validation_not_established":
            boundary[
                "temporal_validation_established"
            ] is False,

        "geographic_transportability_not_established":
            boundary[
                "geographic_transportability_established"
            ] is False,

        "institutional_transportability_not_established":
            boundary[
                "institutional_transportability_established"
            ] is False,

        "prospective_validation_not_established":
            boundary[
                "prospective_validation_established"
            ] is False,

        "deployment_not_authorized":
            boundary["deployment_authorized"] is False,
    }

    failed_checks = [
        name
        for name, passed in checks.items()
        if not passed
    ]

    return {
        "stage":
            D11_STAGE,

        "stage_name":
            D11_STAGE_NAME,

        "baseline_source":
            boundary["baseline_source"],

        "selected_model":
            boundary["selected_model"],

        "model_sha256":
            boundary["model_sha256"],

        "d7_preprocessor_sha256":
            boundary["d7_preprocessor_sha256"],

        "d7_schema_sha256":
            boundary["d7_schema_sha256"],

        "development_threshold":
            boundary["development_threshold"],

        "validation_encounter_count":
            boundary["validation_encounter_count"],

        "validation_positive_count":
            boundary["validation_positive_count"],

        "validation_negative_count":
            boundary["validation_negative_count"],

        "validation_prevalence":
            boundary["validation_prevalence"],

        "transformed_feature_count":
            boundary["transformed_feature_count"],

        "probability_count":
            boundary["probability_count"],

        "probability_mean":
            boundary["probability_mean"],

        "probability_min":
            boundary["probability_min"],

        "probability_max":
            boundary["probability_max"],

        "predicted_positive_count":
            boundary["predicted_positive_count"],

        "predicted_positive_rate":
            boundary["predicted_positive_rate"],

        "d9_model_identity_matches":
            boundary["d9_model_identity_matches"],

        "d9_model_sha_matches":
            boundary["d9_model_sha_matches"],

        "d9_preprocessor_sha_matches":
            boundary["d9_preprocessor_sha_matches"],

        "d9_schema_sha_matches":
            boundary["d9_schema_sha_matches"],

        "d9_feature_count_matches":
            boundary["d9_feature_count_matches"],

        "d9_d10_outcomes_match_elementwise":
            boundary[
                "d9_d10_outcomes_match_elementwise"
            ],

        "independent_baseline_preprocessor_refit":
            boundary[
                "independent_baseline_preprocessor_refit"
            ],

        "model_retrained":
            boundary["model_retrained"],

        "hyperparameters_retuned":
            boundary["hyperparameters_retuned"],

        "preprocessor_refitted_in_d11":
            boundary["preprocessor_refitted_in_d11"],

        "threshold_retuned":
            boundary["threshold_retuned"],

        "subgroup_specific_thresholds_created":
            boundary[
                "subgroup_specific_thresholds_created"
            ],

        "model_recalibrated":
            boundary["model_recalibrated"],

        "automatic_robustness_mitigation_applied":
            boundary[
                "automatic_robustness_mitigation_applied"
            ],

        "locked_test_accessed":
            boundary["locked_test_accessed"],

        "external_validation_established":
            boundary[
                "external_validation_established"
            ],

        "temporal_validation_established":
            boundary[
                "temporal_validation_established"
            ],

        "geographic_transportability_established":
            boundary[
                "geographic_transportability_established"
            ],

        "institutional_transportability_established":
            boundary[
                "institutional_transportability_established"
            ],

        "prospective_validation_established":
            boundary[
                "prospective_validation_established"
            ],

        "deployment_authorized":
            boundary["deployment_authorized"],

        "checks":
            checks,

        "failed_checks":
            failed_checks,

        "validation_status":
            "PASS" if not failed_checks else "FAIL",
    }


# ============================================================
# D11.11 — EXECUTABLE AUTHORITATIVE BASELINE CHECK
# ============================================================

if __name__ == "__main__":
    boundary_result = validate_d11_frozen_system_boundary()

    print()
    print("=" * 60)
    print("D11 AUTHORITATIVE FROZEN BASELINE")
    print("=" * 60)

    for key, value in boundary_result.items():
        if key != "checks":
            print(f"{key}: {value}")

# ============================================================
# D11.12 — BASELINE PERFORMANCE & OPERATING-POINT REFERENCE
# ============================================================
#
# PURPOSE
# -------
# Freeze the performance, calibration, classification, and
# operational metrics of the authoritative D9 validation
# boundary before any D11 perturbation or stress condition.
#
# Every subsequent D11 robustness experiment must be compared
# against this baseline rather than against another perturbed
# condition.
#
# This section:
#   - does NOT retrain the model;
#   - does NOT refit preprocessing;
#   - does NOT retune hyperparameters;
#   - does NOT change the threshold;
#   - does NOT recalibrate probabilities;
#   - does NOT access the locked TEST partition.
# ============================================================

from sklearn.metrics import (
    average_precision_score,
    roc_auc_score,
    brier_score_loss,
    log_loss,
    confusion_matrix,
)


# ============================================================
# D11.12A — BASELINE METRIC ENGINE
# ============================================================

def build_d11_baseline_metric_reference() -> dict:
    """
    Calculate the immutable D11 baseline metric vector from the
    authoritative frozen D9 validation probability boundary.

    These metrics form the reference against which subsequent
    robustness and stress-test conditions will be evaluated.
    """

    boundary = build_d11_frozen_system_boundary()

    y_true = np.asarray(
        boundary["y_validation"],
        dtype=int,
    )

    probabilities = np.asarray(
        boundary["probabilities"],
        dtype=float,
    )

    threshold = float(
        boundary["development_threshold"]
    )

    predictions = (
        probabilities >= threshold
    ).astype(int)

    # --------------------------------------------------------
    # 1. Basic population integrity
    # --------------------------------------------------------

    encounter_count = int(
        len(y_true)
    )

    positive_count = int(
        y_true.sum()
    )

    negative_count = int(
        encounter_count - positive_count
    )

    prevalence = float(
        y_true.mean()
    )

    # --------------------------------------------------------
    # 2. Threshold-independent discrimination
    # --------------------------------------------------------

    roc_auc = float(
        roc_auc_score(
            y_true,
            probabilities,
        )
    )

    pr_auc = float(
        average_precision_score(
            y_true,
            probabilities,
        )
    )

    # --------------------------------------------------------
    # 3. Probability / calibration reference
    # --------------------------------------------------------

    brier_score = float(
        brier_score_loss(
            y_true,
            probabilities,
        )
    )

    probability_log_loss = float(
        log_loss(
            y_true,
            probabilities,
            labels=[0, 1],
        )
    )

    mean_predicted_probability = float(
        probabilities.mean()
    )

    calibration_in_the_large_gap = float(
        mean_predicted_probability - prevalence
    )

    # --------------------------------------------------------
    # 4. Confusion matrix at frozen D9 threshold
    # --------------------------------------------------------

    tn, fp, fn, tp = confusion_matrix(
        y_true,
        predictions,
        labels=[0, 1],
    ).ravel()

    tn = int(tn)
    fp = int(fp)
    fn = int(fn)
    tp = int(tp)

    # --------------------------------------------------------
    # 5. Threshold-dependent clinical metrics
    # --------------------------------------------------------

    sensitivity = float(
        tp / (tp + fn)
    ) if (tp + fn) > 0 else float("nan")

    specificity = float(
        tn / (tn + fp)
    ) if (tn + fp) > 0 else float("nan")

    precision = float(
        tp / (tp + fp)
    ) if (tp + fp) > 0 else float("nan")

    negative_predictive_value = float(
        tn / (tn + fn)
    ) if (tn + fn) > 0 else float("nan")

    false_negative_rate = float(
        fn / (fn + tp)
    ) if (fn + tp) > 0 else float("nan")

    false_positive_rate = float(
        fp / (fp + tn)
    ) if (fp + tn) > 0 else float("nan")

    f1_score = float(
        (2.0 * precision * sensitivity)
        / (precision + sensitivity)
    ) if (
        np.isfinite(precision)
        and np.isfinite(sensitivity)
        and (precision + sensitivity) > 0
    ) else float("nan")

    # --------------------------------------------------------
    # 6. Operational burden
    # --------------------------------------------------------

    predicted_positive_count = int(
        predictions.sum()
    )

    predicted_positive_rate = float(
        predictions.mean()
    )

    alerts_per_100_patients = float(
        predicted_positive_rate * 100.0
    )

    number_needed_to_evaluate = float(
        predicted_positive_count / tp
    ) if tp > 0 else float("inf")

    # --------------------------------------------------------
    # 7. Return governed baseline metric vector
    # --------------------------------------------------------

    return {
        "stage":
            D11_STAGE,

        "reference_type":
            "AUTHORITATIVE_D11_BASELINE",

        "source":
            boundary["baseline_source"],

        "evaluation_partition":
            D11_EVALUATION_PARTITION,

        "selected_model":
            boundary["selected_model"],

        "model_sha256":
            boundary["model_sha256"],

        "threshold":
            threshold,

        "encounter_count":
            encounter_count,

        "positive_count":
            positive_count,

        "negative_count":
            negative_count,

        "prevalence":
            prevalence,

        "roc_auc":
            roc_auc,

        "pr_auc":
            pr_auc,

        "brier_score":
            brier_score,

        "log_loss":
            probability_log_loss,

        "mean_predicted_probability":
            mean_predicted_probability,

        "calibration_in_the_large_gap":
            calibration_in_the_large_gap,

        "true_positive":
            tp,

        "false_positive":
            fp,

        "true_negative":
            tn,

        "false_negative":
            fn,

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

        "f1_score":
            f1_score,

        "predicted_positive_count":
            predicted_positive_count,

        "predicted_positive_rate":
            predicted_positive_rate,

        "alerts_per_100_patients":
            alerts_per_100_patients,

        "number_needed_to_evaluate":
            number_needed_to_evaluate,

        "model_retrained":
            False,

        "hyperparameters_retuned":
            False,

        "preprocessor_refitted":
            False,

        "threshold_retuned":
            False,

        "model_recalibrated":
            False,

        "locked_test_accessed":
            False,

        "deployment_authorized":
            False,
    }


# ============================================================
# D11.12B — BASELINE METRIC VALIDATION
# ============================================================

def validate_d11_baseline_metric_reference() -> dict:
    """
    Validate internal consistency of the D11 baseline metric
    reference before robustness testing begins.
    """

    metrics = build_d11_baseline_metric_reference()

    checks = {
        # ----------------------------------------------------
        # Population
        # ----------------------------------------------------

        "encounter_count_matches":
            metrics["encounter_count"]
            == D11_EXPECTED_VALIDATION_ENCOUNTERS,

        "positive_count_matches":
            metrics["positive_count"]
            == D11_EXPECTED_VALIDATION_POSITIVES,

        "negative_count_matches":
            metrics["negative_count"]
            == D11_EXPECTED_VALIDATION_NEGATIVES,

        # ----------------------------------------------------
        # Frozen operating point
        # ----------------------------------------------------

        "threshold_matches":
            metrics["threshold"]
            == D11_EXPECTED_DEVELOPMENT_THRESHOLD,

        "predicted_positive_count_matches":
            metrics["predicted_positive_count"]
            == D11_EXPECTED_BASELINE_PREDICTED_POSITIVE_COUNT,

        "predicted_positive_rate_matches":
            np.isclose(
                metrics["predicted_positive_rate"],
                D11_EXPECTED_BASELINE_PREDICTED_POSITIVE_RATE,
                rtol=0.0,
                atol=1e-15,
            ),

        # ----------------------------------------------------
        # Probability boundary
        # ----------------------------------------------------

        "mean_probability_matches":
            np.isclose(
                metrics["mean_predicted_probability"],
                D11_EXPECTED_BASELINE_MEAN_PROBABILITY,
                rtol=0.0,
                atol=1e-15,
            ),

        # ----------------------------------------------------
        # Metric sanity
        # ----------------------------------------------------

        "roc_auc_valid":
            0.0 <= metrics["roc_auc"] <= 1.0,

        "pr_auc_valid":
            0.0 <= metrics["pr_auc"] <= 1.0,

        "brier_score_valid":
            0.0 <= metrics["brier_score"] <= 1.0,

        "log_loss_nonnegative":
            metrics["log_loss"] >= 0.0,

        "sensitivity_valid":
            0.0 <= metrics["sensitivity"] <= 1.0,

        "specificity_valid":
            0.0 <= metrics["specificity"] <= 1.0,

        "precision_valid":
            0.0 <= metrics["precision"] <= 1.0,

        "npv_valid":
            0.0
            <= metrics["negative_predictive_value"]
            <= 1.0,

        "fnr_valid":
            0.0
            <= metrics["false_negative_rate"]
            <= 1.0,

        "fpr_valid":
            0.0
            <= metrics["false_positive_rate"]
            <= 1.0,

        # ----------------------------------------------------
        # Mathematical identities
        # ----------------------------------------------------

        "sensitivity_fnr_identity":
            np.isclose(
                metrics["sensitivity"]
                + metrics["false_negative_rate"],
                1.0,
                atol=1e-12,
            ),

        "specificity_fpr_identity":
            np.isclose(
                metrics["specificity"]
                + metrics["false_positive_rate"],
                1.0,
                atol=1e-12,
            ),

        "confusion_matrix_total_matches":
            (
                metrics["true_positive"]
                + metrics["false_positive"]
                + metrics["true_negative"]
                + metrics["false_negative"]
            )
            == D11_EXPECTED_VALIDATION_ENCOUNTERS,

        "confusion_matrix_positive_total_matches":
            (
                metrics["true_positive"]
                + metrics["false_negative"]
            )
            == D11_EXPECTED_VALIDATION_POSITIVES,

        "confusion_matrix_negative_total_matches":
            (
                metrics["true_negative"]
                + metrics["false_positive"]
            )
            == D11_EXPECTED_VALIDATION_NEGATIVES,

        "alert_count_identity":
            (
                metrics["true_positive"]
                + metrics["false_positive"]
            )
            == metrics["predicted_positive_count"],

        # ----------------------------------------------------
        # Governance protections
        # ----------------------------------------------------

        "model_not_retrained":
            metrics["model_retrained"] is False,

        "hyperparameters_not_retuned":
            metrics["hyperparameters_retuned"] is False,

        "preprocessor_not_refitted":
            metrics["preprocessor_refitted"] is False,

        "threshold_not_retuned":
            metrics["threshold_retuned"] is False,

        "model_not_recalibrated":
            metrics["model_recalibrated"] is False,

        "locked_test_not_accessed":
            metrics["locked_test_accessed"] is False,

        "deployment_not_authorized":
            metrics["deployment_authorized"] is False,
    }

    failed_checks = [
        name
        for name, passed in checks.items()
        if not passed
    ]

    return {
        **metrics,

        "checks":
            checks,

        "failed_checks":
            failed_checks,

        "validation_status":
            "PASS" if not failed_checks else "FAIL",
    }


# ============================================================
# D11.12C — EXECUTABLE BASELINE METRIC CHECK
# ============================================================

def print_d11_baseline_metric_reference() -> None:
    """
    Print the governed D11 baseline metric reference.
    """

    result = validate_d11_baseline_metric_reference()

    print()
    print("=" * 60)
    print("D11 BASELINE PERFORMANCE & OPERATING-POINT REFERENCE")
    print("=" * 60)

    for key, value in result.items():
        if key != "checks":
            print(f"{key}: {value}")

# ============================================================
# D11.12D — RUN BASELINE METRIC REFERENCE
# ============================================================

if __name__ == "__main__":
    print_d11_baseline_metric_reference()

# ============================================================
# D11.13 — GOVERNED ROBUSTNESS STRESS-TEST SPECIFICATION
# ============================================================
#
# PURPOSE
# -------
# Pre-specify the development-stage robustness experiments that
# will be evaluated against the immutable D11.12 baseline.
#
# These scenarios are controlled synthetic stress conditions.
# They are NOT:
#   - external validation;
#   - temporal validation;
#   - geographic validation;
#   - institutional validation;
#   - prospective validation.
#
# No stress scenario may trigger automatic model retraining,
# threshold retuning, preprocessing refitting, recalibration,
# subgroup-specific thresholds, or deployment authorization.
# ============================================================


# ============================================================
# D11.13A — STRESS-TEST GOVERNANCE CONSTANTS
# ============================================================

D11_STRESS_TEST_REFERENCE: Final[str] = (
    "AUTHORITATIVE_D11_BASELINE"
)

D11_STRESS_TEST_EVIDENCE_CLASS: Final[str] = (
    "DEVELOPMENT_STAGE_SYNTHETIC_ROBUSTNESS_EVIDENCE"
)

D11_STRESS_TEST_INTERPRETATION: Final[str] = (
    "Controlled development-stage sensitivity analysis against "
    "the frozen D11 baseline. Results characterize internal "
    "robustness under specified synthetic stress conditions and "
    "must not be interpreted as external, temporal, geographic, "
    "institutional, or prospective validation."
)

D11_STRESS_TEST_FEATURES: Final[tuple[str, ...]] = (
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

D11_CATEGORICAL_STRESS_FEATURES: Final[tuple[str, ...]] = (
    "race",
    "gender",
    "age",
    "admission_type_id",
    "admission_source_id",
)

D11_UTILIZATION_STRESS_FEATURES: Final[tuple[str, ...]] = (
    "prior_outpatient_use",
    "prior_emergency_use",
    "prior_inpatient_use",
    "prior_utilization_intensity",
    "prior_utilization_domain_count",
)

D11_ALLOWED_STRESS_SEVERITIES: Final[tuple[str, ...]] = (
    "MILD",
    "MODERATE",
    "STRUCTURAL",
)

D11_ALLOWED_STRESS_DOMAINS: Final[tuple[str, ...]] = (
    "missingness_stress",
    "category_stability",
    "utilization_shift",
    "population_slice_stability",
)

D11_STRESS_TEST_COMPARISON_METRICS: Final[tuple[str, ...]] = (
    "roc_auc",
    "pr_auc",
    "brier_score",
    "log_loss",
    "mean_predicted_probability",
    "sensitivity",
    "specificity",
    "precision",
    "negative_predictive_value",
    "false_negative_rate",
    "false_positive_rate",
    "predicted_positive_rate",
    "alerts_per_100_patients",
    "number_needed_to_evaluate",
)

D11_STRESS_TEST_PROHIBITED_CLAIMS: Final[tuple[str, ...]] = (
    "external_validation_established",
    "temporal_validation_established",
    "geographic_transportability_established",
    "institutional_transportability_established",
    "prospective_validation_established",
    "deployment_authorized",
)


# ============================================================
# D11.13B — PRE-SPECIFIED STRESS-TEST REGISTRY
# ============================================================

D11_STRESS_TEST_REGISTRY: Final[tuple[dict, ...]] = (

    # --------------------------------------------------------
    # Missingness / unknown-category stress
    # --------------------------------------------------------

    {
        "scenario_id": "D11-STRESS-001",
        "scenario_name": "Race Unknown-Category Stress",
        "domain": "missingness_stress",
        "severity": "MODERATE",
        "feature_scope": ("race",),
        "perturbation_type": "controlled_unknown_category_injection",
        "perturbation_level": 0.10,
        "unit": "eligible_validation_encounters",
        "rationale": (
            "Evaluate sensitivity to increased demographic data "
            "quality degradation by replacing race with the "
            "governed unknown-category representation in a "
            "controlled subset of validation encounters."
        ),
        "permitted_interpretation": (
            "Internal sensitivity to increased race-category "
            "unknownness under a synthetic development-stage "
            "stress condition."
        ),
    },

    {
        "scenario_id": "D11-STRESS-002",
        "scenario_name": "Gender Unknown-Category Stress",
        "domain": "missingness_stress",
        "severity": "MODERATE",
        "feature_scope": ("gender",),
        "perturbation_type": "controlled_unknown_category_injection",
        "perturbation_level": 0.10,
        "unit": "eligible_validation_encounters",
        "rationale": (
            "Evaluate sensitivity to degradation in recorded "
            "gender information using the governed unknown "
            "category representation."
        ),
        "permitted_interpretation": (
            "Internal sensitivity to synthetic gender-category "
            "unknownness."
        ),
    },

    # --------------------------------------------------------
    # Categorical stability stress
    # --------------------------------------------------------

    {
        "scenario_id": "D11-STRESS-003",
        "scenario_name": "Admission Type Category Stability",
        "domain": "category_stability",
        "severity": "STRUCTURAL",
        "feature_scope": ("admission_type_id",),
        "perturbation_type": "category_distribution_stress",
        "perturbation_level": None,
        "unit": "governed_category_slice",
        "rationale": (
            "Evaluate model behavior across admission-type "
            "categories without changing the frozen model or "
            "operating threshold."
        ),
        "permitted_interpretation": (
            "Internal category-specific stability evidence "
            "within the development validation population."
        ),
    },

    {
        "scenario_id": "D11-STRESS-004",
        "scenario_name": "Admission Source Category Stability",
        "domain": "category_stability",
        "severity": "STRUCTURAL",
        "feature_scope": ("admission_source_id",),
        "perturbation_type": "category_distribution_stress",
        "perturbation_level": None,
        "unit": "governed_category_slice",
        "rationale": (
            "Evaluate stability across observed admission-source "
            "categories within the validation population."
        ),
        "permitted_interpretation": (
            "Internal category-specific stability evidence; "
            "not institutional transportability evidence."
        ),
    },

   
    # --------------------------------------------------------
    # Observed prior-utilization population stability
    # --------------------------------------------------------

    {
        "scenario_id": "D11-STRESS-005",
        "scenario_name": "No Prior Utilization Stability",
        "domain": "population_slice_stability",
        "severity": "STRUCTURAL",
        "feature_scope": D11_UTILIZATION_STRESS_FEATURES,
        "perturbation_type": "observed_population_slice_analysis",
        "perturbation_level": 0,
        "unit": "prior_utilization_domain_count",
        "rationale": (
            "Evaluate discrimination, calibration, threshold "
            "performance, and alert burden among validation "
            "encounters with no recorded prior outpatient, "
            "emergency, or inpatient utilization."
        ),
        "permitted_interpretation": (
            "Internal robustness evidence for the observed "
            "zero-prior-utilization validation population. "
            "This is not external transportability evidence."
        ),
    },

    {
        "scenario_id": "D11-STRESS-006",
        "scenario_name": "Single-Domain Prior Utilization Stability",
        "domain": "population_slice_stability",
        "severity": "STRUCTURAL",
        "feature_scope": D11_UTILIZATION_STRESS_FEATURES,
        "perturbation_type": "observed_population_slice_analysis",
        "perturbation_level": 1,
        "unit": "prior_utilization_domain_count",
        "rationale": (
            "Evaluate model stability among validation "
            "encounters with prior utilization recorded in "
            "exactly one healthcare-utilization domain."
        ),
        "permitted_interpretation": (
            "Internal robustness evidence for the observed "
            "single-domain prior-utilization population."
        ),
    },

    {
        "scenario_id": "D11-STRESS-007",
        "scenario_name": "Multi-Domain Prior Utilization Stability",
        "domain": "population_slice_stability",
        "severity": "STRUCTURAL",
        "feature_scope": D11_UTILIZATION_STRESS_FEATURES,
        "perturbation_type": "observed_population_slice_analysis",
        "perturbation_level": ">=2",
        "unit": "prior_utilization_domain_count",
        "rationale": (
            "Evaluate model stability among validation "
            "encounters with prior utilization recorded in "
            "two or three healthcare-utilization domains."
        ),
        "permitted_interpretation": (
            "Internal robustness evidence for the observed "
            "multi-domain prior-utilization population."
        ),
    },

    {
        "scenario_id": "D11-STRESS-008",
        "scenario_name": "Higher Prior Utilization Intensity Stability",
        "domain": "population_slice_stability",
        "severity": "STRUCTURAL",
        "feature_scope": D11_UTILIZATION_STRESS_FEATURES,
        "perturbation_type": "observed_population_slice_analysis",
        "perturbation_level": ">=3",
        "unit": "prior_utilization_intensity",
        "rationale": (
            "Evaluate model stability among validation "
            "encounters with prior-utilization intensity of "
            "three or more historical utilization events. "
            "The threshold is pre-specified from the observed "
            "distribution above the validation 75th percentile "
            "of two."
        ),
        "permitted_interpretation": (
            "Internal robustness evidence for the observed "
            "higher prior-utilization-intensity population. "
            "This does not establish temporal, institutional, "
            "or external transportability."
        ),
    },
    # --------------------------------------------------------
    # Population-slice stability
    # --------------------------------------------------------

    {
        "scenario_id": "D11-STRESS-009",
        "scenario_name": "Age Population-Slice Stability",
        "domain": "population_slice_stability",
        "severity": "STRUCTURAL",
        "feature_scope": ("age",),
        "perturbation_type": "observed_population_slice_analysis",
        "perturbation_level": None,
        "unit": "observed_validation_slice",
        "rationale": (
            "Evaluate performance, calibration, and operating "
            "stability across observed age categories without "
            "creating synthetic demographic identities."
        ),
        "permitted_interpretation": (
            "Internal population-slice robustness evidence "
            "within the development validation cohort."
        ),
    },
)


# ============================================================
# D11.13C — STRESS-TEST REGISTRY VALIDATION
# ============================================================

def validate_d11_stress_test_registry() -> dict:
    """
    Validate the pre-specified D11 robustness stress-test
    registry before any perturbation is executed.
    """

    registry = list(
        D11_STRESS_TEST_REGISTRY
    )

    scenario_ids = [
        scenario["scenario_id"]
        for scenario in registry
    ]

    required_fields = {
        "scenario_id",
        "scenario_name",
        "domain",
        "severity",
        "feature_scope",
        "perturbation_type",
        "perturbation_level",
        "unit",
        "rationale",
        "permitted_interpretation",
    }

    missing_required_fields = {}

    for scenario in registry:
        missing = sorted(
            required_fields.difference(
                scenario.keys()
            )
        )

        if missing:
            missing_required_fields[
                scenario.get(
                    "scenario_id",
                    "UNKNOWN_SCENARIO",
                )
            ] = missing

    unauthorized_features = {}

    for scenario in registry:
        invalid_features = sorted(
            set(
                scenario["feature_scope"]
            ).difference(
                D11_STRESS_TEST_FEATURES
            )
        )

        if invalid_features:
            unauthorized_features[
                scenario["scenario_id"]
            ] = invalid_features

    invalid_domains = [
        scenario["scenario_id"]
        for scenario in registry
        if scenario["domain"]
        not in D11_ALLOWED_STRESS_DOMAINS
    ]

    invalid_severities = [
        scenario["scenario_id"]
        for scenario in registry
        if scenario["severity"]
        not in D11_ALLOWED_STRESS_SEVERITIES
    ]

    checks = {
        "registry_not_empty":
            len(registry) > 0,

        "scenario_ids_unique":
            len(scenario_ids)
            == len(set(scenario_ids)),

        "all_required_fields_present":
            not missing_required_fields,

        "all_features_governed":
            not unauthorized_features,

        "all_domains_authorized":
            not invalid_domains,

        "all_severities_authorized":
            not invalid_severities,

        "comparison_metric_registry_not_empty":
            len(
                D11_STRESS_TEST_COMPARISON_METRICS
            ) > 0,

        "baseline_reference_frozen":
            D11_STRESS_TEST_REFERENCE
            == "AUTHORITATIVE_D11_BASELINE",

        "evidence_class_is_development_stage":
            D11_STRESS_TEST_EVIDENCE_CLASS
            == (
                "DEVELOPMENT_STAGE_SYNTHETIC_"
                "ROBUSTNESS_EVIDENCE"
            ),

        "external_validation_not_claimed":
            D11_EXTERNAL_VALIDATION_ESTABLISHED
            is False,

        "temporal_validation_not_claimed":
            D11_TEMPORAL_VALIDATION_ESTABLISHED
            is False,

        "geographic_transportability_not_claimed":
            D11_GEOGRAPHIC_TRANSPORTABILITY_ESTABLISHED
            is False,

        "institutional_transportability_not_claimed":
            D11_INSTITUTIONAL_TRANSPORTABILITY_ESTABLISHED
            is False,

        "prospective_validation_not_claimed":
            D11_PROSPECTIVE_VALIDATION_ESTABLISHED
            is False,

        "locked_test_access_prohibited":
            D11_LOCKED_TEST_ACCESS_PERMITTED
            is False,

        "deployment_not_authorized":
            D11_DEPLOYMENT_AUTHORIZED
            is False,
    }

    failed_checks = [
        name
        for name, passed in checks.items()
        if not passed
    ]

    domain_counts = {}

    for scenario in registry:
        domain = scenario["domain"]

        domain_counts[domain] = (
            domain_counts.get(domain, 0)
            + 1
        )

    severity_counts = {}

    for scenario in registry:
        severity = scenario["severity"]

        severity_counts[severity] = (
            severity_counts.get(severity, 0)
            + 1
        )

    return {
        "stage":
            D11_STAGE,

        "stage_name":
            D11_STAGE_NAME,

        "registry_name":
            "D11_GOVERNED_ROBUSTNESS_STRESS_TEST_REGISTRY",

        "baseline_reference":
            D11_STRESS_TEST_REFERENCE,

        "evidence_class":
            D11_STRESS_TEST_EVIDENCE_CLASS,

        "scenario_count":
            len(registry),

        "scenario_ids":
            scenario_ids,

        "domain_counts":
            domain_counts,

        "severity_counts":
            severity_counts,

        "governed_feature_count":
            len(
                D11_STRESS_TEST_FEATURES
            ),

        "governed_features":
            list(
                D11_STRESS_TEST_FEATURES
            ),

        "comparison_metric_count":
            len(
                D11_STRESS_TEST_COMPARISON_METRICS
            ),

        "comparison_metrics":
            list(
                D11_STRESS_TEST_COMPARISON_METRICS
            ),

        "missing_required_fields":
            missing_required_fields,

        "unauthorized_features":
            unauthorized_features,

        "invalid_domains":
            invalid_domains,

        "invalid_severities":
            invalid_severities,

        "external_validation_established":
            False,

        "temporal_validation_established":
            False,

        "geographic_transportability_established":
            False,

        "institutional_transportability_established":
            False,

        "prospective_validation_established":
            False,

        "model_retraining_permitted":
            False,

        "hyperparameter_retuning_permitted":
            False,

        "preprocessor_refitting_permitted":
            False,

        "threshold_retuning_permitted":
            False,

        "subgroup_specific_thresholds_permitted":
            False,

        "model_recalibration_permitted":
            False,

        "automatic_robustness_mitigation_permitted":
            False,

        "locked_test_accessed":
            False,

        "deployment_authorized":
            False,

        "checks":
            checks,

        "failed_checks":
            failed_checks,

        "validation_status":
            "PASS"
            if not failed_checks
            else "FAIL",
    }


# ============================================================
# D11.13D — EXECUTABLE STRESS-TEST SPECIFICATION CHECK
# ============================================================

def print_d11_stress_test_registry() -> None:
    """
    Print the governed D11 stress-test specification.
    """

    result = validate_d11_stress_test_registry()

    print()
    print("=" * 60)
    print("D11 GOVERNED ROBUSTNESS STRESS-TEST SPECIFICATION")
    print("=" * 60)

    for key, value in result.items():
        if key != "checks":
            print(f"{key}: {value}")


# ============================================================
# D11.13E — RUN STRESS-TEST SPECIFICATION CHECK
# ============================================================

if __name__ == "__main__":
    print_d11_stress_test_registry()

# ============================================================
# D11.14 — GOVERNED ROBUSTNESS STRESS-TEST EXECUTION ENGINE
# ============================================================
#
# PURPOSE
# -------
# Execute the pre-specified D11.13 robustness scenarios against
# the immutable D11.12 baseline using the frozen computational
# pathway:
#
#   governed raw validation features
#       -> persisted D7 preprocessor.transform() ONLY
#       -> frozen 49-feature representation
#       -> frozen D8 model.predict_proba() ONLY
#       -> frozen D9 threshold = 0.12
#       -> comparison against D11.12 baseline
#
# Two evidence modes are supported:
#
# 1. SYNTHETIC_INPUT_PERTURBATION
#    Used only for governed unknown-category injection scenarios.
#
# 2. OBSERVED_POPULATION_SLICE
#    Used for category and utilization stability scenarios.
#
# No retraining, refitting, retuning, recalibration, threshold
# modification, locked-test access, or deployment authorization
# is permitted.
# ============================================================

import joblib
import pandas as pd


# ============================================================
# D11.14A — EXECUTION CONSTANTS
# ============================================================

D11_STRESS_RANDOM_SEED: Final[int] = 42

D11_UNKNOWN_CATEGORY_VALUE: Final[str] = (
    "__MISSING_OR_UNKNOWN__"
)

D11_MIN_SLICE_ENCOUNTERS: Final[int] = 100
D11_MIN_SLICE_POSITIVES: Final[int] = 20
D11_MIN_SLICE_NEGATIVES: Final[int] = 20

D11_EXECUTION_MODES: Final[tuple[str, ...]] = (
    "SYNTHETIC_INPUT_PERTURBATION",
    "OBSERVED_POPULATION_SLICE",
)


# ============================================================
# D11.14AA — GOVERNED D7 SOURCE-UNKNOWN NORMALIZATION
# ============================================================

D11_SOURCE_UNKNOWN_CATEGORY_VALUES: Final[dict[str, frozenset[str]]] = {
    "race": frozenset({"?"}),
    "gender": frozenset({"Unknown/Invalid", "?"}),
    "age": frozenset({"?"}),
    "admission_type_id": frozenset(),
    "admission_source_id": frozenset(),
}


def normalize_d11_source_unknown_categories(
    X_input: pd.DataFrame,
) -> pd.DataFrame:
    """
    Apply the frozen D7 source-unknown normalization policy to a
    D11 raw feature matrix without fitting or modifying persisted
    preprocessing state.

    This is a deterministic representation transform only. Source
    values such as race='?' and gender='Unknown/Invalid' are mapped
    to the canonical category learned by the frozen D7 preprocessor.
    """

    expected_columns = list(D11_STRESS_TEST_FEATURES)

    if list(X_input.columns) != expected_columns:
        raise RuntimeError(
            "D11 normalization input does not preserve the governed "
            "raw feature order."
        )

    X_normalized = X_input.copy(deep=True)

    for feature, source_unknown_values in (
        D11_SOURCE_UNKNOWN_CATEGORY_VALUES.items()
    ):
        if feature not in X_normalized.columns:
            continue

        if not source_unknown_values:
            continue

        source_mask = (
            X_normalized[feature]
            .astype(str)
            .isin(source_unknown_values)
        )

        X_normalized.loc[
            source_mask,
            feature,
        ] = D11_UNKNOWN_CATEGORY_VALUE

    return X_normalized


# ============================================================
# D11.14B — LOAD FROZEN EXECUTION COMPONENTS
# ============================================================

def load_d11_frozen_execution_components() -> dict:
    """
    Load the governed raw validation matrix, persisted D7
    preprocessor, transformed schema, and frozen D8 model.

    The function performs no fitting or model modification.
    """

    from src.features import preprocessing as d7

    # --------------------------------------------------------
    # 1. Recover governed raw validation boundary
    # --------------------------------------------------------

    partitions = d7.build_d7_train_validation_partitions()

    required_partition_keys = {
        "X_validation",
        "y_validation",
        "validation_encounter_ids",
    }

    missing_partition_keys = sorted(
        required_partition_keys.difference(
            partitions.keys()
        )
    )

    if missing_partition_keys:
        raise RuntimeError(
            "D7 validation boundary is missing required keys: "
            f"{missing_partition_keys}"
        )

    X_validation = partitions[
        "X_validation"
    ].copy(deep=True)

    y_validation = np.asarray(
        partitions["y_validation"],
        dtype=int,
    )

    validation_encounter_ids = np.asarray(
        partitions["validation_encounter_ids"]
    )

    # --------------------------------------------------------
    # 2. Validate raw governed feature boundary
    # --------------------------------------------------------

    if tuple(X_validation.columns) != tuple(
        D11_STRESS_TEST_FEATURES
    ):
        raise RuntimeError(
            "D11 raw validation feature order does not match "
            "the governed D11 feature registry."
        )

    if X_validation.shape != (
        D11_EXPECTED_VALIDATION_ENCOUNTERS,
        len(D11_STRESS_TEST_FEATURES),
    ):
        raise RuntimeError(
            "D11 raw validation feature matrix has an "
            "unexpected shape."
        )

    if len(y_validation) != (
        D11_EXPECTED_VALIDATION_ENCOUNTERS
    ):
        raise RuntimeError(
            "D11 validation outcome count is unexpected."
        )

    if len(validation_encounter_ids) != (
        D11_EXPECTED_VALIDATION_ENCOUNTERS
    ):
        raise RuntimeError(
            "D11 validation encounter-ID count is unexpected."
        )

    # --------------------------------------------------------
    # 3. Verify persisted D7 artifacts before loading
    # --------------------------------------------------------

    observed_preprocessor_sha = _d11_sha256_file(
        D11_FROZEN_PREPROCESSOR_PATH
    )

    observed_schema_sha = _d11_sha256_file(
        D11_FROZEN_SCHEMA_PATH
    )

    if (
        observed_preprocessor_sha
        != D11_EXPECTED_D7_PREPROCESSOR_SHA256
    ):
        raise RuntimeError(
            "Persisted D7 preprocessor failed D11 integrity "
            "verification."
        )

    if (
        observed_schema_sha
        != D11_EXPECTED_D7_SCHEMA_SHA256
    ):
        raise RuntimeError(
            "Persisted D7 transformed schema failed D11 "
            "integrity verification."
        )

    # --------------------------------------------------------
    # 4. Load persisted fitted D7 preprocessor and schema
    # --------------------------------------------------------

    preprocessor = (
        d7.load_persisted_primary_preprocessor()
    )

    transformed_schema = list(
        d7.load_persisted_transformed_schema()
    )

    if len(transformed_schema) != (
        D11_EXPECTED_TRANSFORMED_FEATURE_COUNT
    ):
        raise RuntimeError(
            "Persisted D7 transformed schema has unexpected "
            "feature count."
        )

    # --------------------------------------------------------
    # 5. Verify and load frozen D8 model
    # --------------------------------------------------------

    observed_model_sha = _d11_sha256_file(
        D11_FROZEN_MODEL_PATH
    )

    if observed_model_sha != D11_EXPECTED_MODEL_SHA256:
        raise RuntimeError(
            "Frozen D8 model failed D11 integrity verification."
        )

    model = joblib.load(
        D11_FROZEN_MODEL_PATH
    )

    return {
        "X_validation":
            X_validation,

        "y_validation":
            y_validation,

        "validation_encounter_ids":
            validation_encounter_ids,

        "preprocessor":
            preprocessor,

        "transformed_schema":
            transformed_schema,

        "model":
            model,

        "d7_preprocessor_sha256":
            observed_preprocessor_sha,

        "d7_schema_sha256":
            observed_schema_sha,

        "model_sha256":
            observed_model_sha,

        "preprocessor_fit_called":
            False,

        "model_fit_called":
            False,

        "locked_test_accessed":
            False,
    }


# ============================================================
# D11.14C — FROZEN SCORING FUNCTION
# ============================================================

def score_d11_feature_matrix(
    X_input: pd.DataFrame,
    components: dict,
) -> dict:
    """
    Score a governed D11 feature matrix using only the persisted
    fitted D7 transformer and frozen D8 model.

    No fit() operation is performed.
    """

    expected_columns = list(
        D11_STRESS_TEST_FEATURES
    )

    if list(X_input.columns) != expected_columns:
        raise RuntimeError(
            "D11 scoring input does not preserve the governed "
            "raw feature order."
        )

    X_normalized = normalize_d11_source_unknown_categories(
        X_input
    )

    transformed = components[
        "preprocessor"
    ].transform(
        X_normalized
    )

    transformed_array = np.asarray(
        transformed,
        dtype=np.float64,
    )

    if transformed_array.shape[1] != (
        D11_EXPECTED_TRANSFORMED_FEATURE_COUNT
    ):
        raise RuntimeError(
            "D11 transformed feature count does not match the "
            "frozen D7 schema."
        )

    probabilities = np.asarray(
        components["model"].predict_proba(
            transformed_array
        )[:, 1],
        dtype=float,
    )

    predictions = (
        probabilities
        >= D11_EXPECTED_DEVELOPMENT_THRESHOLD
    ).astype(int)

    return {
        "probabilities":
            probabilities,

        "predictions":
            predictions,

        "transformed_feature_count":
            int(transformed_array.shape[1]),

        "source_unknown_normalization_applied":
            True,

        "preprocessor_fit_called":
            False,

        "model_fit_called":
            False,

        "threshold_retuned":
            False,

        "locked_test_accessed":
            False,
    }


# ============================================================
# D11.14D — GENERIC METRIC ENGINE
# ============================================================

def calculate_d11_stress_metrics(
    y_true: np.ndarray,
    probabilities: np.ndarray,
) -> dict:
    """
    Calculate the governed D11 comparison metric vector for a
    baseline, perturbation, or observed population slice.
    """

    y_true = np.asarray(
        y_true,
        dtype=int,
    )

    probabilities = np.asarray(
        probabilities,
        dtype=float,
    )

    if len(y_true) != len(probabilities):
        raise RuntimeError(
            "D11 metric inputs have unequal lengths."
        )

    if len(y_true) == 0:
        raise RuntimeError(
            "D11 metric evaluation received an empty cohort."
        )

    if not np.isfinite(probabilities).all():
        raise RuntimeError(
            "D11 probabilities contain non-finite values."
        )

    predictions = (
        probabilities
        >= D11_EXPECTED_DEVELOPMENT_THRESHOLD
    ).astype(int)

    encounter_count = int(
        len(y_true)
    )

    positive_count = int(
        y_true.sum()
    )

    negative_count = int(
        encounter_count - positive_count
    )

    prevalence = float(
        y_true.mean()
    )

    # --------------------------------------------------------
    # Discrimination
    # --------------------------------------------------------

    if positive_count > 0 and negative_count > 0:
        roc_auc = float(
            roc_auc_score(
                y_true,
                probabilities,
            )
        )

        pr_auc = float(
            average_precision_score(
                y_true,
                probabilities,
            )
        )
    else:
        roc_auc = float("nan")
        pr_auc = float("nan")

    # --------------------------------------------------------
    # Calibration / probability quality
    # --------------------------------------------------------

    brier_score = float(
        brier_score_loss(
            y_true,
            probabilities,
        )
    )

    probability_log_loss = float(
        log_loss(
            y_true,
            probabilities,
            labels=[0, 1],
        )
    )

    mean_probability = float(
        probabilities.mean()
    )

    calibration_gap = float(
        mean_probability - prevalence
    )

    # --------------------------------------------------------
    # Frozen-threshold operating point
    # --------------------------------------------------------

    tn, fp, fn, tp = confusion_matrix(
        y_true,
        predictions,
        labels=[0, 1],
    ).ravel()

    tn = int(tn)
    fp = int(fp)
    fn = int(fn)
    tp = int(tp)

    sensitivity = (
        float(tp / (tp + fn))
        if (tp + fn) > 0
        else float("nan")
    )

    specificity = (
        float(tn / (tn + fp))
        if (tn + fp) > 0
        else float("nan")
    )

    precision = (
        float(tp / (tp + fp))
        if (tp + fp) > 0
        else float("nan")
    )

    npv = (
        float(tn / (tn + fn))
        if (tn + fn) > 0
        else float("nan")
    )

    fnr = (
        float(fn / (fn + tp))
        if (fn + tp) > 0
        else float("nan")
    )

    fpr = (
        float(fp / (fp + tn))
        if (fp + tn) > 0
        else float("nan")
    )

    predicted_positive_count = int(
        predictions.sum()
    )

    predicted_positive_rate = float(
        predictions.mean()
    )

    alerts_per_100 = float(
        predicted_positive_rate * 100.0
    )

    nne = (
        float(predicted_positive_count / tp)
        if tp > 0
        else float("inf")
    )

    return {
        "encounter_count":
            encounter_count,

        "positive_count":
            positive_count,

        "negative_count":
            negative_count,

        "prevalence":
            prevalence,

        "roc_auc":
            roc_auc,

        "pr_auc":
            pr_auc,

        "brier_score":
            brier_score,

        "log_loss":
            probability_log_loss,

        "mean_predicted_probability":
            mean_probability,

        "calibration_in_the_large_gap":
            calibration_gap,

        "true_positive":
            tp,

        "false_positive":
            fp,

        "true_negative":
            tn,

        "false_negative":
            fn,

        "sensitivity":
            sensitivity,

        "specificity":
            specificity,

        "precision":
            precision,

        "negative_predictive_value":
            npv,

        "false_negative_rate":
            fnr,

        "false_positive_rate":
            fpr,

        "predicted_positive_count":
            predicted_positive_count,

        "predicted_positive_rate":
            predicted_positive_rate,

        "alerts_per_100_patients":
            alerts_per_100,

        "number_needed_to_evaluate":
            nne,
    }


# ============================================================
# D11.14E — BASELINE EXECUTION-PATH REPRODUCTION
# ============================================================

def validate_d11_frozen_execution_path() -> dict:
    """
    Prove that the D11 execution engine reproduces the
    authoritative D9 probability vector exactly before any
    robustness scenario is executed.
    """

    components = (
        load_d11_frozen_execution_components()
    )

    scored = score_d11_feature_matrix(
        components["X_validation"],
        components,
    )

    authoritative = (
        build_d11_frozen_system_boundary()
    )

    probabilities_match = bool(
        np.array_equal(
            scored["probabilities"],
            authoritative["probabilities"],
        )
    )

    predictions_match = bool(
        np.array_equal(
            scored["predictions"],
            authoritative["predictions"],
        )
    )

    maximum_absolute_probability_difference = float(
        np.max(
            np.abs(
                scored["probabilities"]
                - authoritative["probabilities"]
            )
        )
    )

    checks = {
        "probabilities_match_exactly":
            probabilities_match,

        "predictions_match_exactly":
            predictions_match,

        "maximum_probability_difference_zero":
            maximum_absolute_probability_difference
            == 0.0,

        "transformed_feature_count_matches":
            scored["transformed_feature_count"]
            == D11_EXPECTED_TRANSFORMED_FEATURE_COUNT,

        "source_unknown_normalization_applied":
            scored["source_unknown_normalization_applied"]
            is True,

        "preprocessor_not_refitted":
            scored["preprocessor_fit_called"]
            is False,

        "model_not_retrained":
            scored["model_fit_called"]
            is False,

        "threshold_not_retuned":
            scored["threshold_retuned"]
            is False,

        "locked_test_not_accessed":
            scored["locked_test_accessed"]
            is False,
    }

    failed_checks = [
        name
        for name, passed in checks.items()
        if not passed
    ]

    return {
        "stage":
            D11_STAGE,

        "engine":
            "D11_FROZEN_STRESS_TEST_EXECUTION_ENGINE",

        "raw_validation_shape":
            tuple(
                components["X_validation"].shape
            ),

        "transformed_feature_count":
            scored["transformed_feature_count"],

        "probability_count":
            int(
                len(scored["probabilities"])
            ),

        "mean_probability":
            float(
                scored["probabilities"].mean()
            ),

        "predicted_positive_count":
            int(
                scored["predictions"].sum()
            ),

        "predicted_positive_rate":
            float(
                scored["predictions"].mean()
            ),

        "authoritative_d9_probability_match":
            probabilities_match,

        "authoritative_d9_prediction_match":
            predictions_match,

        "maximum_absolute_probability_difference":
            maximum_absolute_probability_difference,

        "preprocessor_refitted":
            False,

        "model_retrained":
            False,

        "threshold_retuned":
            False,

        "locked_test_accessed":
            False,

        "deployment_authorized":
            False,

        "failed_checks":
            failed_checks,

        "validation_status":
            "PASS"
            if not failed_checks
            else "FAIL",
    }


# ============================================================
# D11.14F — SYNTHETIC UNKNOWN-CATEGORY PERTURBATION
# ============================================================

def execute_d11_unknown_category_stress(
    scenario: dict,
    components: dict,
) -> dict:
    """
    Execute a deterministic governed unknown-category injection
    stress test for D11-STRESS-001 or D11-STRESS-002.

    Exactly the pre-specified fraction of eligible encounters is
    selected using the fixed D11 random seed.

    Existing unknown-category rows are not counted as newly
    perturbed encounters.
    """

    feature_scope = tuple(
        scenario["feature_scope"]
    )

    if len(feature_scope) != 1:
        raise RuntimeError(
            "Unknown-category stress must target exactly one "
            "categorical feature."
        )

    feature = feature_scope[0]

    if feature not in (
        "race",
        "gender",
    ):
        raise RuntimeError(
            "D11 unknown-category injection is authorized only "
            "for race or gender."
        )

    perturbation_level = float(
        scenario["perturbation_level"]
    )

    X_stressed = components[
        "X_validation"
    ].copy(deep=True)

    # --------------------------------------------------------
    # Identify rows not already governed as unknown
    # --------------------------------------------------------

    X_normalized_baseline = (
        normalize_d11_source_unknown_categories(
            X_stressed
        )
    )

    existing_unknown_mask = (
        X_normalized_baseline[feature].astype(str)
        == D11_UNKNOWN_CATEGORY_VALUE
    )

    eligible_indices = np.flatnonzero(
        ~existing_unknown_mask.to_numpy()
    )

    perturbation_count = int(
        np.floor(
            len(eligible_indices)
            * perturbation_level
        )
    )

    if perturbation_count <= 0:
        raise RuntimeError(
            "D11 unknown-category perturbation selected zero "
            "encounters."
        )

    rng = np.random.default_rng(
        D11_STRESS_RANDOM_SEED
    )

    selected_positions = rng.choice(
        eligible_indices,
        size=perturbation_count,
        replace=False,
    )

    feature_column_index = (
        X_stressed.columns.get_loc(feature)
    )

    X_stressed.iloc[
        selected_positions,
        feature_column_index,
    ] = D11_UNKNOWN_CATEGORY_VALUE

    # --------------------------------------------------------
    # Score stressed population
    # --------------------------------------------------------

    scored = score_d11_feature_matrix(
        X_stressed,
        components,
    )

    metrics = calculate_d11_stress_metrics(
        components["y_validation"],
        scored["probabilities"],
    )

    return {
        "scenario_id":
            scenario["scenario_id"],

        "scenario_name":
            scenario["scenario_name"],

        "domain":
            scenario["domain"],

        "severity":
            scenario["severity"],

        "execution_mode":
            "SYNTHETIC_INPUT_PERTURBATION",

        "feature_scope":
            list(feature_scope),

        "perturbation_type":
            scenario["perturbation_type"],

        "perturbation_level":
            perturbation_level,

        "existing_unknown_encounter_count":
            int(existing_unknown_mask.sum()),

        "eligible_encounter_count":
            int(len(eligible_indices)),

        "perturbed_encounter_count":
            perturbation_count,

        "random_seed":
            D11_STRESS_RANDOM_SEED,

        **metrics,

        "model_retrained":
            False,

        "preprocessor_refitted":
            False,

        "threshold_retuned":
            False,

        "model_recalibrated":
            False,

        "locked_test_accessed":
            False,

        "external_validation_established":
            False,

        "deployment_authorized":
            False,
    }


# ============================================================
# D11.14G — OBSERVED POPULATION-SLICE MASKS
# ============================================================

def build_d11_observed_slice_masks(
    X_validation: pd.DataFrame,
    scenario: dict,
) -> dict[str, np.ndarray]:
    """
    Build observed validation-population masks for D11
    structural stability scenarios.
    """

    scenario_id = scenario[
        "scenario_id"
    ]

    masks: dict[str, np.ndarray] = {}

    # --------------------------------------------------------
    # Admission type
    # --------------------------------------------------------

    if scenario_id == "D11-STRESS-003":

        values = sorted(
            X_validation[
                "admission_type_id"
            ].dropna().unique().tolist()
        )

        for value in values:
            masks[
                f"admission_type_id={value}"
            ] = (
                X_validation[
                    "admission_type_id"
                ].to_numpy()
                == value
            )

    # --------------------------------------------------------
    # Admission source
    # --------------------------------------------------------

    elif scenario_id == "D11-STRESS-004":

        values = sorted(
            X_validation[
                "admission_source_id"
            ].dropna().unique().tolist()
        )

        for value in values:
            masks[
                f"admission_source_id={value}"
            ] = (
                X_validation[
                    "admission_source_id"
                ].to_numpy()
                == value
            )

    # --------------------------------------------------------
    # No prior utilization
    # --------------------------------------------------------

    elif scenario_id == "D11-STRESS-005":

        masks[
            "prior_utilization_domain_count=0"
        ] = (
            X_validation[
                "prior_utilization_domain_count"
            ].to_numpy()
            == 0
        )

    # --------------------------------------------------------
    # Single-domain prior utilization
    # --------------------------------------------------------

    elif scenario_id == "D11-STRESS-006":

        masks[
            "prior_utilization_domain_count=1"
        ] = (
            X_validation[
                "prior_utilization_domain_count"
            ].to_numpy()
            == 1
        )

    # --------------------------------------------------------
    # Multi-domain prior utilization
    # --------------------------------------------------------

    elif scenario_id == "D11-STRESS-007":

        masks[
            "prior_utilization_domain_count>=2"
        ] = (
            X_validation[
                "prior_utilization_domain_count"
            ].to_numpy()
            >= 2
        )

    # --------------------------------------------------------
    # Higher utilization intensity
    # --------------------------------------------------------

    elif scenario_id == "D11-STRESS-008":

        masks[
            "prior_utilization_intensity>=3"
        ] = (
            X_validation[
                "prior_utilization_intensity"
            ].to_numpy()
            >= 3
        )

    # --------------------------------------------------------
    # Age categories
    # --------------------------------------------------------

    elif scenario_id == "D11-STRESS-009":

        values = (
            X_validation[
                "age"
            ].dropna().astype(str).unique().tolist()
        )

        values = sorted(values)

        for value in values:
            masks[
                f"age={value}"
            ] = (
                X_validation[
                    "age"
                ].astype(str)
                .to_numpy()
                == value
            )

    else:
        raise RuntimeError(
            "Unsupported observed-slice scenario: "
            f"{scenario_id}"
        )

    return masks


# ============================================================
# D11.14H — OBSERVED POPULATION-SLICE EXECUTION
# ============================================================

def execute_d11_observed_slice_stress(
    scenario: dict,
    components: dict,
    baseline_probabilities: np.ndarray,
) -> list[dict]:
    """
    Evaluate observed validation slices using the authoritative
    frozen baseline probability vector.

    No synthetic modification is performed.
    """

    X_validation = components[
        "X_validation"
    ]

    y_validation = components[
        "y_validation"
    ]

    masks = build_d11_observed_slice_masks(
        X_validation,
        scenario,
    )

    results = []

    for slice_name, mask in masks.items():

        mask = np.asarray(
            mask,
            dtype=bool,
        )

        y_slice = y_validation[
            mask
        ]

        probability_slice = (
            baseline_probabilities[
                mask
            ]
        )

        encounter_count = int(
            len(y_slice)
        )

        positive_count = int(
            y_slice.sum()
        )

        negative_count = int(
            encounter_count - positive_count
        )

        support_status = (
            "ADEQUATE_SUPPORT"
            if (
                encounter_count
                >= D11_MIN_SLICE_ENCOUNTERS

                and positive_count
                >= D11_MIN_SLICE_POSITIVES

                and negative_count
                >= D11_MIN_SLICE_NEGATIVES
            )
            else "LOW_SUPPORT"
        )

        metrics = calculate_d11_stress_metrics(
            y_slice,
            probability_slice,
        )

        results.append(
            {
                "scenario_id":
                    scenario["scenario_id"],

                "scenario_name":
                    scenario["scenario_name"],

                "domain":
                    scenario["domain"],

                "severity":
                    scenario["severity"],

                "execution_mode":
                    "OBSERVED_POPULATION_SLICE",

                "slice_name":
                    slice_name,

                "support_status":
                    support_status,

                **metrics,

                "synthetic_perturbation_applied":
                    False,

                "model_retrained":
                    False,

                "preprocessor_refitted":
                    False,

                "threshold_retuned":
                    False,

                "model_recalibrated":
                    False,

                "locked_test_accessed":
                    False,

                "external_validation_established":
                    False,

                "deployment_authorized":
                    False,
            }
        )

    return results


# ============================================================
# D11.14I — COMPLETE STRESS-TEST EXECUTION
# ============================================================

def execute_d11_governed_stress_tests() -> dict:
    """
    Execute all nine pre-specified D11 stress scenarios.
    """

    registry_validation = (
        validate_d11_stress_test_registry()
    )

    if (
        registry_validation["validation_status"]
        != "PASS"
    ):
        raise RuntimeError(
            "D11 stress-test registry failed governance "
            "validation."
        )

    execution_validation = (
        validate_d11_frozen_execution_path()
    )

    if (
        execution_validation["validation_status"]
        != "PASS"
    ):
        raise RuntimeError(
            "D11 frozen execution pathway failed baseline "
            "reproduction."
        )

    components = (
        load_d11_frozen_execution_components()
    )

    baseline = (
        build_d11_frozen_system_boundary()
    )

    baseline_probabilities = np.asarray(
        baseline["probabilities"],
        dtype=float,
    )

    synthetic_results = []
    observed_slice_results = []

    for scenario in D11_STRESS_TEST_REGISTRY:

        scenario_id = scenario[
            "scenario_id"
        ]

        if scenario_id in {
            "D11-STRESS-001",
            "D11-STRESS-002",
        }:

            result = (
                execute_d11_unknown_category_stress(
                    scenario,
                    components,
                )
            )

            synthetic_results.append(
                result
            )

        else:

            results = (
                execute_d11_observed_slice_stress(
                    scenario,
                    components,
                    baseline_probabilities,
                )
            )

            observed_slice_results.extend(
                results
            )

    return {
        "stage":
            D11_STAGE,

        "engine":
            "D11_GOVERNED_ROBUSTNESS_STRESS_TEST_ENGINE",

        "scenario_count":
            len(D11_STRESS_TEST_REGISTRY),

        "synthetic_scenario_count":
            len(synthetic_results),

        "observed_slice_scenario_count":
            (
                len(D11_STRESS_TEST_REGISTRY)
                - len(synthetic_results)
            ),

        "synthetic_results":
            synthetic_results,

        "observed_slice_results":
            observed_slice_results,

        "model_retrained":
            False,

        "hyperparameters_retuned":
            False,

        "preprocessor_refitted":
            False,

        "threshold_retuned":
            False,

        "model_recalibrated":
            False,

        "locked_test_accessed":
            False,

        "external_validation_established":
            False,

        "temporal_validation_established":
            False,

        "geographic_transportability_established":
            False,

        "institutional_transportability_established":
            False,

        "prospective_validation_established":
            False,

        "deployment_authorized":
            False,
    }


# ============================================================
# D11.14J — EXECUTION ENGINE VALIDATION
# ============================================================

def validate_d11_stress_test_execution_engine() -> dict:
    """
    Validate execution-engine integrity without interpreting
    robustness results as deployment evidence.
    """

    baseline_path = (
        validate_d11_frozen_execution_path()
    )

    checks = {
        "baseline_execution_path_passes":
            baseline_path[
                "validation_status"
            ] == "PASS",

        "authoritative_probabilities_reproduced":
            baseline_path[
                "authoritative_d9_probability_match"
            ] is True,

        "authoritative_predictions_reproduced":
            baseline_path[
                "authoritative_d9_prediction_match"
            ] is True,

        "zero_baseline_probability_difference":
            baseline_path[
                "maximum_absolute_probability_difference"
            ] == 0.0,

        "preprocessor_not_refitted":
            baseline_path[
                "preprocessor_refitted"
            ] is False,

        "model_not_retrained":
            baseline_path[
                "model_retrained"
            ] is False,

        "threshold_not_retuned":
            baseline_path[
                "threshold_retuned"
            ] is False,

        "locked_test_not_accessed":
            baseline_path[
                "locked_test_accessed"
            ] is False,

        "deployment_not_authorized":
            baseline_path[
                "deployment_authorized"
            ] is False,
    }

    failed_checks = [
        name
        for name, passed in checks.items()
        if not passed
    ]

    return {
        **baseline_path,

        "checks":
            checks,

        "failed_checks":
            failed_checks,

        "validation_status":
            "PASS"
            if not failed_checks
            else "FAIL",
    }


# ============================================================
# D11.14K — RUN EXECUTION-PATH VALIDATION ONLY
# ============================================================

def print_d11_stress_execution_validation() -> None:
    """
    Print execution-path validation before running the complete
    stress suite.
    """

    result = (
        validate_d11_stress_test_execution_engine()
    )

    print()
    print("=" * 60)
    print("D11 STRESS-TEST EXECUTION ENGINE VALIDATION")
    print("=" * 60)

    for key, value in result.items():
        if key != "checks":
            print(f"{key}: {value}")


if __name__ == "__main__":
    print_d11_stress_execution_validation()

# ============================================================
# D11.15 — ROBUSTNESS COMPARISON & DEGRADATION ASSESSMENT
# ============================================================
#
# PURPOSE
# -------
# Convert D11.14 stress-test outputs into governed comparison
# evidence without conflating two fundamentally different forms
# of evidence:
#
#   1. synthetic perturbation evidence — the SAME validation
#      population is deliberately perturbed and may therefore be
#      compared directly with the immutable D11.12 baseline;
#
#   2. observed population-slice evidence — naturally occurring
#      validation subpopulations are characterized descriptively.
#      Differences from the whole-cohort baseline are heterogeneity
#      signals, NOT automatic evidence of model degradation.
#
# Review thresholds below are internal governance triggers. They
# are not clinical acceptance criteria, statistical significance
# tests, external-validation standards, or deployment gates.
# ============================================================


# ============================================================
# D11.15A — GOVERNANCE REVIEW THRESHOLDS
# ============================================================

D11_SYNTHETIC_REVIEW_THRESHOLDS: Final[dict[str, float]] = {
    "roc_auc_adverse_delta": 0.02,
    "pr_auc_adverse_delta": 0.02,
    "brier_score_adverse_delta": 0.02,
    "log_loss_adverse_delta": 0.05,
    "sensitivity_adverse_delta": 0.05,
    "specificity_adverse_delta": 0.05,
    "precision_adverse_delta": 0.05,
    "predicted_positive_rate_absolute_delta": 0.05,
}

D11_SYNTHETIC_MATERIAL_REVIEW_MULTIPLIER: Final[float] = 2.0

D11_OBSERVED_SLICE_ALERT_RATE_LOW_TRIGGER: Final[float] = 0.05
D11_OBSERVED_SLICE_ALERT_RATE_HIGH_TRIGGER: Final[float] = 0.75
D11_OBSERVED_SLICE_SENSITIVITY_DIFFERENCE_TRIGGER: Final[float] = 0.15
D11_OBSERVED_SLICE_SPECIFICITY_DIFFERENCE_TRIGGER: Final[float] = 0.15
D11_OBSERVED_SLICE_PR_AUC_DIFFERENCE_TRIGGER: Final[float] = 0.10
D11_OBSERVED_SLICE_ROC_AUC_DIFFERENCE_TRIGGER: Final[float] = 0.10

D11_COMPARISON_EPSILON: Final[float] = 1e-12


# ============================================================
# D11.15B — NUMERIC COMPARISON HELPERS
# ============================================================

def _d11_is_finite_number(value) -> bool:
    """Return True only for finite numeric values."""

    try:
        return bool(np.isfinite(float(value)))
    except (TypeError, ValueError):
        return False


def _d11_absolute_delta(value, reference) -> float:
    """Return value minus reference, or NaN when unavailable."""

    if not (
        _d11_is_finite_number(value)
        and _d11_is_finite_number(reference)
    ):
        return float("nan")

    return float(value) - float(reference)


def _d11_relative_delta(value, reference) -> float:
    """Return proportional change from reference, or NaN."""

    if not (
        _d11_is_finite_number(value)
        and _d11_is_finite_number(reference)
    ):
        return float("nan")

    reference = float(reference)

    if abs(reference) <= D11_COMPARISON_EPSILON:
        return float("nan")

    return (float(value) - reference) / abs(reference)


def _d11_metric_delta_vector(
    result: dict,
    baseline: dict,
) -> dict:
    """
    Calculate absolute and relative deltas for every governed D11
    comparison metric available in both records.
    """

    deltas = {}

    for metric in D11_STRESS_TEST_COMPARISON_METRICS:
        result_value = result.get(metric, float("nan"))
        baseline_value = baseline.get(metric, float("nan"))

        deltas[f"delta_{metric}"] = _d11_absolute_delta(
            result_value,
            baseline_value,
        )

        deltas[f"relative_delta_{metric}"] = _d11_relative_delta(
            result_value,
            baseline_value,
        )

    return deltas


# ============================================================
# D11.15C — SYNTHETIC PERTURBATION REVIEW CLASSIFICATION
# ============================================================

def _d11_synthetic_adverse_changes(
    result: dict,
    baseline: dict,
) -> dict:
    """
    Measure direction-aware adverse changes for synthetic stress.

    Positive values mean deterioration relative to baseline.
    """

    return {
        "roc_auc_adverse_delta": max(
            0.0,
            float(baseline["roc_auc"]) - float(result["roc_auc"]),
        ),
        "pr_auc_adverse_delta": max(
            0.0,
            float(baseline["pr_auc"]) - float(result["pr_auc"]),
        ),
        "brier_score_adverse_delta": max(
            0.0,
            float(result["brier_score"]) - float(baseline["brier_score"]),
        ),
        "log_loss_adverse_delta": max(
            0.0,
            float(result["log_loss"]) - float(baseline["log_loss"]),
        ),
        "sensitivity_adverse_delta": max(
            0.0,
            float(baseline["sensitivity"]) - float(result["sensitivity"]),
        ),
        "specificity_adverse_delta": max(
            0.0,
            float(baseline["specificity"]) - float(result["specificity"]),
        ),
        "precision_adverse_delta": max(
            0.0,
            float(baseline["precision"]) - float(result["precision"]),
        ),
        "predicted_positive_rate_absolute_delta": abs(
            float(result["predicted_positive_rate"])
            - float(baseline["predicted_positive_rate"])
        ),
    }


def _d11_classify_synthetic_stress(
    adverse_changes: dict,
) -> tuple[str, list[str]]:
    """
    Classify synthetic perturbation evidence using internal review
    triggers. This classification does not accept or reject a model.
    """

    review_triggers = []
    material_triggers = []

    for metric, threshold in D11_SYNTHETIC_REVIEW_THRESHOLDS.items():
        observed = float(adverse_changes[metric])

        if observed >= threshold:
            review_triggers.append(metric)

        if observed >= (
            threshold * D11_SYNTHETIC_MATERIAL_REVIEW_MULTIPLIER
        ):
            material_triggers.append(metric)

    if material_triggers:
        classification = "MATERIAL_GOVERNANCE_REVIEW"
    elif review_triggers:
        classification = "GOVERNANCE_REVIEW"
    else:
        classification = "NO_PRE_SPECIFIED_REVIEW_TRIGGER"

    return classification, review_triggers


def build_d11_synthetic_degradation_assessment() -> list[dict]:
    """
    Compare synthetic perturbations directly with the immutable
    whole-validation D11.12 baseline.
    """

    baseline = build_d11_baseline_metric_reference()
    stress = execute_d11_governed_stress_tests()

    assessments = []

    for result in stress["synthetic_results"]:
        deltas = _d11_metric_delta_vector(result, baseline)
        adverse = _d11_synthetic_adverse_changes(result, baseline)
        classification, triggers = _d11_classify_synthetic_stress(
            adverse
        )

        assessments.append({
            "scenario_id": result["scenario_id"],
            "scenario_name": result["scenario_name"],
            "evidence_mode": "SYNTHETIC_PERTURBATION",
            "comparison_reference": "AUTHORITATIVE_D11_BASELINE",
            "direct_baseline_degradation_comparison_permitted": True,
            "encounter_count": result["encounter_count"],
            "positive_count": result["positive_count"],
            "perturbed_encounter_count": result.get(
                "perturbed_encounter_count"
            ),
            "review_classification": classification,
            "review_trigger_count": len(triggers),
            "review_triggers": triggers,
            **adverse,
            **deltas,
            "model_retrained": False,
            "hyperparameters_retuned": False,
            "preprocessor_refitted": False,
            "threshold_retuned": False,
            "model_recalibrated": False,
            "locked_test_accessed": False,
            "deployment_authorized": False,
        })

    return assessments


# ============================================================
# D11.15D — OBSERVED-SLICE HETEROGENEITY ASSESSMENT
# ============================================================

def _d11_observed_slice_review_signals(
    result: dict,
    baseline: dict,
) -> list[str]:
    """
    Generate descriptive governance-review signals for an observed
    validation slice. These are NOT degradation determinations.
    """

    signals = []

    alert_rate = result.get("predicted_positive_rate")

    if _d11_is_finite_number(alert_rate):
        alert_rate = float(alert_rate)

        if alert_rate <= D11_OBSERVED_SLICE_ALERT_RATE_LOW_TRIGGER:
            signals.append("VERY_LOW_ALERT_RATE")

        if alert_rate >= D11_OBSERVED_SLICE_ALERT_RATE_HIGH_TRIGGER:
            signals.append("VERY_HIGH_ALERT_RATE")

    for metric, trigger, label in (
        (
            "sensitivity",
            D11_OBSERVED_SLICE_SENSITIVITY_DIFFERENCE_TRIGGER,
            "SENSITIVITY_HETEROGENEITY",
        ),
        (
            "specificity",
            D11_OBSERVED_SLICE_SPECIFICITY_DIFFERENCE_TRIGGER,
            "SPECIFICITY_HETEROGENEITY",
        ),
        (
            "pr_auc",
            D11_OBSERVED_SLICE_PR_AUC_DIFFERENCE_TRIGGER,
            "PR_AUC_HETEROGENEITY",
        ),
        (
            "roc_auc",
            D11_OBSERVED_SLICE_ROC_AUC_DIFFERENCE_TRIGGER,
            "ROC_AUC_HETEROGENEITY",
        ),
    ):
        value = result.get(metric)
        reference = baseline.get(metric)

        if (
            _d11_is_finite_number(value)
            and _d11_is_finite_number(reference)
            and abs(float(value) - float(reference)) >= trigger
        ):
            signals.append(label)

    return signals


def build_d11_observed_slice_heterogeneity_assessment() -> list[dict]:
    """
    Characterize naturally occurring validation slices without
    mislabelling case-mix or prevalence differences as degradation.
    """

    baseline = build_d11_baseline_metric_reference()
    stress = execute_d11_governed_stress_tests()

    assessments = []

    for result in stress["observed_slice_results"]:
        support_status = result.get("support_status", "UNKNOWN_SUPPORT")
        deltas = _d11_metric_delta_vector(result, baseline)

        if support_status != "ADEQUATE_SUPPORT":
            signals = ["LOW_SUPPORT_LIMITS_INTERPRETATION"]
            classification = "INSUFFICIENT_SUPPORT_FOR_STRONG_INTERPRETATION"
        else:
            signals = _d11_observed_slice_review_signals(
                result,
                baseline,
            )

            classification = (
                "HETEROGENEITY_REVIEW_SIGNAL"
                if signals
                else "DESCRIPTIVE_HETEROGENEITY_NO_PRE_SPECIFIED_TRIGGER"
            )

        assessments.append({
            "scenario_id": result["scenario_id"],
            "scenario_name": result["scenario_name"],
            "slice_name": result.get("slice_name"),
            "evidence_mode": "OBSERVED_VALIDATION_SLICE",
            "comparison_reference": "WHOLE_VALIDATION_BASELINE_CONTEXT_ONLY",
            "direct_baseline_degradation_comparison_permitted": False,
            "support_status": support_status,
            "encounter_count": result["encounter_count"],
            "positive_count": result["positive_count"],
            "prevalence": result["prevalence"],
            "review_classification": classification,
            "review_signal_count": len(signals),
            "review_signals": signals,
            **deltas,
            "model_retrained": False,
            "hyperparameters_retuned": False,
            "preprocessor_refitted": False,
            "threshold_retuned": False,
            "model_recalibrated": False,
            "locked_test_accessed": False,
            "external_validation_established": False,
            "temporal_validation_established": False,
            "geographic_transportability_established": False,
            "institutional_transportability_established": False,
            "prospective_validation_established": False,
            "deployment_authorized": False,
        })

    return assessments


# ============================================================
# D11.15E — COMPLETE COMPARISON & DEGRADATION ASSESSMENT
# ============================================================

def build_d11_robustness_comparison_assessment() -> dict:
    """
    Build the complete D11.15 governance assessment.

    Synthetic perturbations are assessed for degradation against the
    same-population baseline. Observed slices are assessed separately
    for support-aware heterogeneity signals.
    """

    baseline = build_d11_baseline_metric_reference()
    synthetic = build_d11_synthetic_degradation_assessment()
    observed = build_d11_observed_slice_heterogeneity_assessment()

    synthetic_review_count = sum(
        row["review_classification"]
        != "NO_PRE_SPECIFIED_REVIEW_TRIGGER"
        for row in synthetic
    )

    observed_low_support_count = sum(
        row["support_status"] != "ADEQUATE_SUPPORT"
        for row in observed
    )

    observed_review_signal_count = sum(
        row["review_classification"] == "HETEROGENEITY_REVIEW_SIGNAL"
        for row in observed
    )

    return {
        "stage": D11_STAGE,
        "assessment": "D11_ROBUSTNESS_COMPARISON_AND_DEGRADATION_ASSESSMENT",
        "baseline_reference_type": baseline["reference_type"],
        "baseline_encounter_count": baseline["encounter_count"],
        "baseline_positive_count": baseline["positive_count"],
        "baseline_prevalence": baseline["prevalence"],
        "baseline_roc_auc": baseline["roc_auc"],
        "baseline_pr_auc": baseline["pr_auc"],
        "baseline_brier_score": baseline["brier_score"],
        "baseline_log_loss": baseline["log_loss"],
        "baseline_sensitivity": baseline["sensitivity"],
        "baseline_specificity": baseline["specificity"],
        "baseline_precision": baseline["precision"],
        "baseline_predicted_positive_rate": baseline[
            "predicted_positive_rate"
        ],
        "synthetic_assessment_count": len(synthetic),
        "synthetic_review_count": int(synthetic_review_count),
        "observed_slice_assessment_count": len(observed),
        "observed_low_support_count": int(observed_low_support_count),
        "observed_review_signal_count": int(observed_review_signal_count),
        "synthetic_assessments": synthetic,
        "observed_slice_assessments": observed,
        "synthetic_interpretation": (
            "Direct same-population comparison with the immutable D11 "
            "baseline is permitted for controlled perturbations."
        ),
        "observed_slice_interpretation": (
            "Whole-cohort metric differences are descriptive context for "
            "population heterogeneity and must not be labelled automatic "
            "model degradation or external transportability failure."
        ),
        "review_threshold_interpretation": (
            "Pre-specified internal governance triggers only; not clinical "
            "acceptance criteria, statistical significance tests, external "
            "validation standards, or deployment gates."
        ),
        "model_retrained": False,
        "hyperparameters_retuned": False,
        "preprocessor_refitted": False,
        "threshold_retuned": False,
        "model_recalibrated": False,
        "locked_test_accessed": False,
        "external_validation_established": False,
        "temporal_validation_established": False,
        "geographic_transportability_established": False,
        "institutional_transportability_established": False,
        "prospective_validation_established": False,
        "deployment_authorized": False,
    }


# ============================================================
# D11.15F — ASSESSMENT VALIDATION
# ============================================================

def validate_d11_robustness_comparison_assessment() -> dict:
    """Validate the D11.15 comparison and interpretation boundary."""

    assessment = build_d11_robustness_comparison_assessment()

    synthetic = assessment["synthetic_assessments"]
    observed = assessment["observed_slice_assessments"]

    checks = {
        "stage_identity": assessment["stage"] == "D11",
        "synthetic_assessment_count_is_two":
            assessment["synthetic_assessment_count"] == 2,
        "observed_slice_assessment_count_is_thirty_five":
            assessment["observed_slice_assessment_count"] == 35,
        "total_assessment_rows_are_thirty_seven":
            len(synthetic) + len(observed) == 37,
        "synthetic_direct_comparison_permitted": all(
            row["direct_baseline_degradation_comparison_permitted"] is True
            for row in synthetic
        ),
        "observed_direct_degradation_comparison_prohibited": all(
            row["direct_baseline_degradation_comparison_permitted"] is False
            for row in observed
        ),
        "synthetic_reference_is_frozen_baseline": all(
            row["comparison_reference"] == "AUTHORITATIVE_D11_BASELINE"
            for row in synthetic
        ),
        "observed_reference_is_context_only": all(
            row["comparison_reference"]
            == "WHOLE_VALIDATION_BASELINE_CONTEXT_ONLY"
            for row in observed
        ),
        "model_not_retrained": assessment["model_retrained"] is False,
        "hyperparameters_not_retuned":
            assessment["hyperparameters_retuned"] is False,
        "preprocessor_not_refitted":
            assessment["preprocessor_refitted"] is False,
        "threshold_not_retuned": assessment["threshold_retuned"] is False,
        "model_not_recalibrated":
            assessment["model_recalibrated"] is False,
        "locked_test_not_accessed":
            assessment["locked_test_accessed"] is False,
        "external_validation_not_established":
            assessment["external_validation_established"] is False,
        "temporal_validation_not_established":
            assessment["temporal_validation_established"] is False,
        "geographic_transportability_not_established":
            assessment["geographic_transportability_established"] is False,
        "institutional_transportability_not_established":
            assessment["institutional_transportability_established"] is False,
        "prospective_validation_not_established":
            assessment["prospective_validation_established"] is False,
        "deployment_not_authorized":
            assessment["deployment_authorized"] is False,
    }

    failed_checks = [
        name
        for name, passed in checks.items()
        if not passed
    ]

    return {
        **assessment,
        "checks": checks,
        "failed_checks": failed_checks,
        "validation_status": "PASS" if not failed_checks else "FAIL",
    }


# ============================================================
# D11.15G — EXECUTABLE COMPARISON CHECK
# ============================================================

def print_d11_robustness_comparison_assessment() -> None:
    """Print the governed D11.15 comparison assessment summary."""

    result = validate_d11_robustness_comparison_assessment()

    print()
    print("=" * 60)
    print("D11 ROBUSTNESS COMPARISON & DEGRADATION ASSESSMENT")
    print("=" * 60)

    summary_keys = (
        "validation_status",
        "synthetic_assessment_count",
        "synthetic_review_count",
        "observed_slice_assessment_count",
        "observed_low_support_count",
        "observed_review_signal_count",
        "model_retrained",
        "hyperparameters_retuned",
        "preprocessor_refitted",
        "threshold_retuned",
        "model_recalibrated",
        "locked_test_accessed",
        "external_validation_established",
        "deployment_authorized",
    )

    for key in summary_keys:
        print(f"{key}: {result[key]}")
# ============================================================
# D11.16 — ROBUSTNESS GOVERNANCE FINDINGS & LIFECYCLE DISPOSITION
# ============================================================
#
# PURPOSE
# -------
# Convert the validated D11.15 robustness evidence into a formal,
# reproducible development-stage governance disposition.
#
# This section does NOT convert observed population heterogeneity into
# causal degradation claims. It does NOT establish external
# transportability, authorize deployment, alter the D9 threshold, or
# modify any frozen upstream artifact.
# ============================================================


# ============================================================
# D11.16A — DISPOSITION CONSTANTS
# ============================================================

D11_ROBUSTNESS_DISPOSITION: Final[str] = (
    "CONDITIONAL_PASS_PROGRESS_WITH_DOCUMENTED_ROBUSTNESS_FINDINGS"
)

D11_EXPECTED_SYNTHETIC_REVIEW_COUNT: Final[int] = 0
D11_EXPECTED_OBSERVED_HETEROGENEITY_REVIEW_COUNT: Final[int] = 6
D11_EXPECTED_LOW_SUPPORT_LIMITATION_COUNT: Final[int] = 12

D11_NEXT_LIFECYCLE_STAGE: Final[str] = "D12"
D11_NEXT_LIFECYCLE_STAGE_NAME: Final[str] = "Explainability"

D11_DISPOSITION_INTERPRETATION: Final[str] = (
    "D11 development-stage robustness evaluation is complete and may "
    "progress to D12 Explainability with documented carry-forward "
    "findings. This conditional pass is not deployment authorization "
    "and does not establish external, temporal, geographic, "
    "institutional, or prospective transportability."
)

D11_MANDATORY_CARRY_FORWARD_ACTIONS: Final[tuple[str, ...]] = (
    "D12: investigate the contribution of prior-utilization features to the observed operating-point heterogeneity without changing the frozen D9 threshold.",
    "D12: examine feature-attribution behavior for admission_source_id and age while avoiding causal interpretation of attribution values.",
    "D12: document whether the observed utilization pattern is consistent with model feature dependence, population case-mix differences, or both; do not infer causality from D11 alone.",
    "Governance evidence: retain all 12 low-support observed slices as interpretation limitations rather than treating unstable small-sample metrics as strong evidence.",
    "D14: reassess discrimination, calibration, operating-point behavior, and relevant subgroup/slice findings once on the locked TEST partition without validation-driven threshold retuning.",
    "Deployment governance: do not authorize clinical deployment from D11 evidence; external, temporal, institutional/geographic, and prospective validation remain unestablished.",
)


# ============================================================
# D11.16B — BUILD FORMAL GOVERNANCE FINDINGS
# ============================================================

def build_d11_robustness_governance_findings() -> dict:
    """Build formal D11 governance findings from validated D11.15 evidence."""

    assessment = validate_d11_robustness_comparison_assessment()

    if assessment["validation_status"] != "PASS":
        raise RuntimeError(
            "D11.15 comparison assessment must PASS before D11.16 "
            "governance disposition can be generated."
        )

    synthetic = assessment["synthetic_assessments"]
    observed = assessment["observed_slice_assessments"]

    synthetic_review_rows = [
        row
        for row in synthetic
        if row["review_classification"]
        != "NO_PRE_SPECIFIED_REVIEW_TRIGGER"
    ]

    low_support_rows = [
        row
        for row in observed
        if row["support_status"] != "ADEQUATE_SUPPORT"
    ]

    heterogeneity_rows = [
        row
        for row in observed
        if row["review_classification"] == "HETEROGENEITY_REVIEW_SIGNAL"
    ]

    heterogeneity_findings = [
        {
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "slice_name": row["slice_name"],
            "encounter_count": row["encounter_count"],
            "positive_count": row["positive_count"],
            "prevalence": row["prevalence"],
            "support_status": row["support_status"],
            "review_signals": list(row["review_signals"]),
            "delta_roc_auc": row["delta_roc_auc"],
            "delta_pr_auc": row["delta_pr_auc"],
            "delta_sensitivity": row["delta_sensitivity"],
            "delta_specificity": row["delta_specificity"],
            "delta_predicted_positive_rate": row[
                "delta_predicted_positive_rate"
            ],
            "interpretation": (
                "Observed validation-population heterogeneity requiring "
                "governance review; not direct same-population degradation "
                "evidence and not an external transportability conclusion."
            ),
        }
        for row in heterogeneity_rows
    ]

    low_support_limitations = [
        {
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "slice_name": row["slice_name"],
            "encounter_count": row["encounter_count"],
            "positive_count": row["positive_count"],
            "support_status": row["support_status"],
            "limitation": "LOW_SUPPORT_LIMITS_STRONG_INTERPRETATION",
        }
        for row in low_support_rows
    ]

    if synthetic_review_rows:
        disposition = "HOLD_FOR_GOVERNANCE_REVIEW"
        progression_authorized = False
    else:
        disposition = D11_ROBUSTNESS_DISPOSITION
        progression_authorized = True

    return {
        "stage": D11_STAGE,
        "governance_layer": (
            "D11_ROBUSTNESS_GOVERNANCE_FINDINGS_AND_LIFECYCLE_DISPOSITION"
        ),
        "source_assessment": assessment["assessment"],
        "source_assessment_validation_status": assessment[
            "validation_status"
        ],
        "disposition": disposition,
        "disposition_interpretation": D11_DISPOSITION_INTERPRETATION,
        "progression_authorized": progression_authorized,
        "next_lifecycle_stage": D11_NEXT_LIFECYCLE_STAGE,
        "next_lifecycle_stage_name": D11_NEXT_LIFECYCLE_STAGE_NAME,
        "synthetic_assessment_count": assessment[
            "synthetic_assessment_count"
        ],
        "synthetic_review_count": len(synthetic_review_rows),
        "synthetic_review_rows": synthetic_review_rows,
        "observed_slice_assessment_count": assessment[
            "observed_slice_assessment_count"
        ],
        "observed_heterogeneity_review_count": len(heterogeneity_rows),
        "observed_heterogeneity_findings": heterogeneity_findings,
        "low_support_limitation_count": len(low_support_rows),
        "low_support_limitations": low_support_limitations,
        "mandatory_carry_forward_action_count": len(
            D11_MANDATORY_CARRY_FORWARD_ACTIONS
        ),
        "mandatory_carry_forward_actions": list(
            D11_MANDATORY_CARRY_FORWARD_ACTIONS
        ),
        "direct_observed_slice_degradation_claim_permitted": False,
        "causal_interpretation_permitted": False,
        "model_retrained": False,
        "hyperparameters_retuned": False,
        "preprocessor_refitted": False,
        "threshold_retuned": False,
        "model_recalibrated": False,
        "locked_test_accessed": False,
        "external_validation_established": False,
        "temporal_validation_established": False,
        "geographic_transportability_established": False,
        "institutional_transportability_established": False,
        "prospective_validation_established": False,
        "deployment_authorized": False,
    }


# ============================================================
# D11.16C — VALIDATE GOVERNANCE DISPOSITION
# ============================================================

def validate_d11_robustness_governance_disposition() -> dict:
    """Validate the D11.16 findings, disposition, and lifecycle boundary."""

    findings = build_d11_robustness_governance_findings()

    checks = {
        "stage_identity": findings["stage"] == "D11",
        "source_d11_15_passed": (
            findings["source_assessment_validation_status"] == "PASS"
        ),
        "synthetic_review_count_matches": (
            findings["synthetic_review_count"]
            == D11_EXPECTED_SYNTHETIC_REVIEW_COUNT
        ),
        "observed_heterogeneity_count_matches": (
            findings["observed_heterogeneity_review_count"]
            == D11_EXPECTED_OBSERVED_HETEROGENEITY_REVIEW_COUNT
        ),
        "low_support_count_matches": (
            findings["low_support_limitation_count"]
            == D11_EXPECTED_LOW_SUPPORT_LIMITATION_COUNT
        ),
        "conditional_pass_disposition_matches": (
            findings["disposition"] == D11_ROBUSTNESS_DISPOSITION
        ),
        "progression_to_d12_authorized": (
            findings["progression_authorized"] is True
            and findings["next_lifecycle_stage"] == "D12"
        ),
        "carry_forward_actions_present": (
            findings["mandatory_carry_forward_action_count"]
            == len(D11_MANDATORY_CARRY_FORWARD_ACTIONS)
            and findings["mandatory_carry_forward_action_count"] > 0
        ),
        "observed_slice_degradation_claim_prohibited": (
            findings[
                "direct_observed_slice_degradation_claim_permitted"
            ] is False
        ),
        "causal_interpretation_prohibited": (
            findings["causal_interpretation_permitted"] is False
        ),
        "model_not_retrained": findings["model_retrained"] is False,
        "hyperparameters_not_retuned": (
            findings["hyperparameters_retuned"] is False
        ),
        "preprocessor_not_refitted": (
            findings["preprocessor_refitted"] is False
        ),
        "threshold_not_retuned": findings["threshold_retuned"] is False,
        "model_not_recalibrated": (
            findings["model_recalibrated"] is False
        ),
        "locked_test_not_accessed": (
            findings["locked_test_accessed"] is False
        ),
        "external_validation_not_established": (
            findings["external_validation_established"] is False
        ),
        "temporal_validation_not_established": (
            findings["temporal_validation_established"] is False
        ),
        "geographic_transportability_not_established": (
            findings["geographic_transportability_established"] is False
        ),
        "institutional_transportability_not_established": (
            findings[
                "institutional_transportability_established"
            ] is False
        ),
        "prospective_validation_not_established": (
            findings["prospective_validation_established"] is False
        ),
        "deployment_not_authorized": (
            findings["deployment_authorized"] is False
        ),
    }

    failed_checks = [
        name
        for name, passed in checks.items()
        if not passed
    ]

    return {
        **findings,
        "checks": checks,
        "failed_checks": failed_checks,
        "validation_status": "PASS" if not failed_checks else "FAIL",
    }


# ============================================================
# D11.16D — EXECUTABLE GOVERNANCE DISPOSITION CHECK
# ============================================================

def print_d11_robustness_governance_disposition() -> None:
    """Print the formal D11.16 governance disposition summary."""

    result = validate_d11_robustness_governance_disposition()

    print()
    print("=" * 70)
    print("D11 ROBUSTNESS GOVERNANCE FINDINGS & LIFECYCLE DISPOSITION")
    print("=" * 70)

    summary_keys = (
        "validation_status",
        "disposition",
        "progression_authorized",
        "next_lifecycle_stage",
        "synthetic_review_count",
        "observed_heterogeneity_review_count",
        "low_support_limitation_count",
        "mandatory_carry_forward_action_count",
        "model_retrained",
        "hyperparameters_retuned",
        "preprocessor_refitted",
        "threshold_retuned",
        "model_recalibrated",
        "locked_test_accessed",
        "external_validation_established",
        "deployment_authorized",
    )

    for key in summary_keys:
        print(f"{key}: {result[key]}")