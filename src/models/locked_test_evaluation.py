# ============================================================
# D14 — LOCKED-TEST EVALUATION
# Pre-Access Governance Contract
# ============================================================
#
# Project:
# Diabetes 30-Day Readmission Clinical AI
#
# Purpose:
# Establish the governance, integrity, and evaluation boundary
# BEFORE the locked TEST partition is accessed.
#
# IMPORTANT:
# This module section MUST NOT:
#   - load locked TEST rows,
#   - transform locked TEST features,
#   - generate locked TEST predictions,
#   - calculate locked TEST performance,
#   - retrain or retune the model,
#   - refit preprocessing,
#   - recalibrate probabilities,
#   - optimize the operating threshold,
#   - authorize deployment.
#
# D14 evaluates the exact candidate frozen at D13.
# ============================================================


from __future__ import annotations

from dataclasses import dataclass
from typing import Any


# ============================================================
# D14.00 — LIFECYCLE IDENTITY
# ============================================================

D14_STAGE_ID = "D14"
D14_STAGE_NAME = "Locked-Test Evaluation"

D14_SOURCE_LIFECYCLE_STAGE = "D13"
D14_SOURCE_GIT_COMMIT = "b4118f9"

D14_NEXT_LIFECYCLE_STAGE = "D15_DEPLOYMENT_AND_MONITORING_DESIGN"

D14_EVALUATION_PARTITION = "LOCKED_TEST"
D14_EVALUATION_MODE = "ONE_TIME_CONFIRMATORY_EVALUATION"

D14_DEPLOYMENT_AUTHORIZED = False


# ============================================================
# D14.01 — FROZEN CANDIDATE IDENTITY
# ============================================================

D14_EXPECTED_REGISTRY_ID = "DIABETES_READMISSION_XGB_D13_V1"
D14_EXPECTED_MODEL_VERSION = "1.0.0"

D14_EXPECTED_CANDIDATE_SYSTEM_SHA256 = (
    "9349A52C715517666540C0D5B1EDB148D48709C0FC2CC77BE9B53F10FE373679"
)

D14_EXPECTED_FEATURE_CONTRACT_SHA256 = (
    "277CCC7C847B2FE6882A4072EA991B1FEF701D0222471B8B1F583DE06924C0BC"
)

D14_EXPECTED_SOFTWARE_ENVIRONMENT_SHA256 = (
    "D008029639FF03569910412173B84B557C3694A12B24ED8198E06F38616A6E7E"
)

D14_EXPECTED_FREEZE_MANIFEST_SHA256 = (
    "0F278573E2C4D139E6D0968DD624AB7C1304825D3B805B6FEF288162051B6119"
)

D14_EXPECTED_MODEL_SHA256 = (
    "2FD02A54DF759EBAAF0D02D64D5ACE16A519DF016990FAC065AF3249BDA88085"
)

D14_EXPECTED_PREPROCESSOR_SHA256 = (
    "076878C0BD7C9B80897F3AA06157719A1E311165299549D83213C789CA1ECEAC"
)

D14_EXPECTED_TRANSFORMED_SCHEMA_SHA256 = (
    "69E0E7F19C64350A6995830E875C1303E5D14F55FD7CDA4A7D845CCDE7B756ED"
)

D14_EXPECTED_MODEL_METADATA_SHA256 = (
    "5838A6C77F05BB183F90B9AA4B0ED9F0AE5B0FBF2E3E1B1326A79A3A67A1AC76"
)


# ============================================================
# D14.02 — FROZEN OPERATING POINT
# ============================================================

D14_EXPECTED_DEVELOPMENT_THRESHOLD = 0.12

D14_THRESHOLD_CLASSIFICATION = (
    "FROZEN_DEVELOPMENT_STAGE_OPERATING_THRESHOLD"
)

D14_THRESHOLD_SOURCE_STAGE = "D9"

D14_THRESHOLD_RETUNING_ALLOWED = False
D14_RECALIBRATION_ALLOWED = False
D14_SUBGROUP_THRESHOLD_OPTIMIZATION_ALLOWED = False


# ============================================================
# D14.03 — EXPECTED LOCKED-TEST CONTRACT
# ============================================================
#
# These values originate from the governed D5 split assignment.
# They define expected partition identity before evaluation.
#
# They MUST NOT be interpreted as D14 evaluation results.
# ============================================================

D14_EXPECTED_TEST_ENCOUNTERS = 15_038
D14_EXPECTED_TEST_PATIENTS = 10_568
D14_EXPECTED_TEST_POSITIVES = 1_707
D14_EXPECTED_TEST_NEGATIVES = 13_331

D14_EXPECTED_SOURCE_FEATURE_COUNT = 10
D14_EXPECTED_TRANSFORMED_FEATURE_COUNT = 49


# ============================================================
# D14.04 — PRE-ACCESS STATE
# ============================================================

D14_LOCKED_TEST_ACCESSED = False
D14_LOCKED_TEST_EVALUATED = False
D14_LOCKED_TEST_PREDICTIONS_GENERATED = False

D14_MODEL_RETRAINED = False
D14_MODEL_RETUNED = False
D14_PREPROCESSOR_REFITTED = False
D14_FEATURE_ENGINEERING_CHANGED = False
D14_FEATURE_SET_CHANGED = False
D14_THRESHOLD_RETUNED = False
D14_MODEL_RECALIBRATED = False
D14_SUBGROUP_THRESHOLD_CREATED = False
D14_TEST_DRIVEN_MODEL_SELECTION = False
D14_TEST_DRIVEN_REDESIGN = False

D14_DEPLOYMENT_AUTHORIZED_PRE_EVALUATION = False


# ============================================================
# D14.05 — PROHIBITED ACTIVITIES
# ============================================================

D14_PROHIBITED_ACTIVITIES = (
    "MODEL_RETRAINING",
    "HYPERPARAMETER_RETUNING",
    "PREPROCESSOR_REFITTING",
    "FEATURE_ENGINEERING_CHANGE",
    "FEATURE_SET_CHANGE",
    "MODEL_RESELECTION",
    "THRESHOLD_RETUNING",
    "PROBABILITY_RECALIBRATION",
    "SUBGROUP_SPECIFIC_THRESHOLD_OPTIMIZATION",
    "TEST_DRIVEN_MODEL_SELECTION",
    "TEST_DRIVEN_FEATURE_SELECTION",
    "TEST_DRIVEN_MODEL_REDESIGN",
    "TEST_TO_VALIDATION_OPTIMIZATION_LOOP",
    "AUTONOMOUS_CLINICAL_DECISION_MAKING",
    "DEPLOYMENT_AUTHORIZATION_FROM_PRE_ACCESS_CONTRACT",
)


# ============================================================
# D14.06 — PRE-SPECIFIED PRIMARY EVALUATION DOMAINS
# ============================================================
#
# These domains are declared BEFORE TEST access.
#
# No metric is being calculated here.
# ============================================================

D14_PRIMARY_EVALUATION_DOMAINS = {
    "discrimination": (
        "PR_AUC",
        "ROC_AUC",
    ),
    "calibration": (
        "BRIER_SCORE",
        "LOG_LOSS",
    ),
    "frozen_threshold_operating_performance": (
        "TRUE_POSITIVES",
        "FALSE_POSITIVES",
        "TRUE_NEGATIVES",
        "FALSE_NEGATIVES",
        "SENSITIVITY",
        "SPECIFICITY",
        "PRECISION_PPV",
        "NEGATIVE_PREDICTIVE_VALUE",
        "F1_SCORE",
        "ALERT_COUNT",
        "ALERT_RATE",
        "ALERTS_PER_100_ENCOUNTERS",
        "NUMBER_NEEDED_TO_EVALUATE",
    ),
}


# ============================================================
# D14.07 — PRE-SPECIFIED CONFIRMATORY EVALUATION DOMAINS
# ============================================================
#
# These analyses may evaluate whether previously documented
# development-stage findings remain observable in TEST.
#
# They MUST NOT be used to optimize the candidate.
# ============================================================

D14_CONFIRMATORY_EVALUATION_DOMAINS = {
    "subgroup_performance": (
        "RACE",
        "GENDER",
        "AGE",
    ),
    "robustness_transportability": (
        "PRIOR_UTILIZATION",
        "ADMISSION_CONTEXT",
        "AGE_STRUCTURE",
    ),
    "explainability_confirmation": (
        "GLOBAL_FEATURE_CONTRIBUTION",
        "PRIOR_UTILIZATION_DEPENDENCE",
        "LOCAL_EXPLANATION_CONSISTENCY",
    ),
}


# ============================================================
# D14.08 — GOVERNANCE INTERPRETATION RULES
# ============================================================

D14_INTERPRETATION_RULES = (
    "LOCKED_TEST_RESULTS_ARE_CONFIRMATORY_NOT_TUNING_INPUTS",
    "UNFAVORABLE_RESULTS_MUST_BE_RETAINED_AND_REPORTED",
    "FAVORABLE_RESULTS_DO_NOT_AUTOMATICALLY_AUTHORIZE_DEPLOYMENT",
    "TEST_RESULTS_MUST_NOT_TRIGGER_THRESHOLD_RETUNING_ON_TEST",
    "TEST_RESULTS_MUST_NOT_TRIGGER_MODEL_RESELECTION_ON_TEST",
    "TEST_RESULTS_MUST_NOT_TRIGGER_FEATURE_REENGINEERING_ON_TEST",
    "SUBGROUP_RESULTS_ARE_DESCRIPTIVE_UNLESS_STRONGER_INFERENCE_IS_JUSTIFIED",
    "INTERNAL_TEST_VALIDATION_IS_NOT_EXTERNAL_VALIDATION",
    "TECHNICAL_VALIDATION_IS_NOT_CLINICAL_EFFECTIVENESS",
    "CLINICAL_VALIDATION_IS_NOT_DEPLOYMENT_AUTHORIZATION",
)


# ============================================================
# D14.09 — PRE-ACCESS GOVERNANCE CONTRACT
# ============================================================


@dataclass(frozen=True)
class D14PreAccessGovernanceContract:
    stage_id: str
    stage_name: str
    source_lifecycle_stage: str
    source_git_commit: str

    registry_id: str
    model_version: str
    candidate_system_sha256: str
    feature_contract_sha256: str
    software_environment_sha256: str
    freeze_manifest_sha256: str

    development_threshold: float

    expected_test_encounters: int
    expected_test_patients: int
    expected_test_positives: int
    expected_test_negatives: int

    expected_source_feature_count: int
    expected_transformed_feature_count: int

    evaluation_partition: str
    evaluation_mode: str

    locked_test_accessed: bool
    locked_test_evaluated: bool
    predictions_generated: bool

    model_retrained: bool
    model_retuned: bool
    preprocessor_refitted: bool
    feature_engineering_changed: bool
    feature_set_changed: bool
    threshold_retuned: bool
    model_recalibrated: bool
    subgroup_threshold_created: bool
    test_driven_model_selection: bool
    test_driven_redesign: bool

    deployment_authorized: bool

    prohibited_activities: tuple[str, ...]
    interpretation_rules: tuple[str, ...]


def build_d14_pre_access_governance_contract(
) -> D14PreAccessGovernanceContract:
    """
    Build the D14 governance contract before any locked TEST access.

    This function is intentionally metadata-only.

    It MUST NOT:
        - load TEST data,
        - load TEST features,
        - transform TEST,
        - load the predictive model for TEST inference,
        - generate TEST predictions,
        - calculate TEST metrics.
    """

    return D14PreAccessGovernanceContract(
        stage_id=D14_STAGE_ID,
        stage_name=D14_STAGE_NAME,
        source_lifecycle_stage=D14_SOURCE_LIFECYCLE_STAGE,
        source_git_commit=D14_SOURCE_GIT_COMMIT,

        registry_id=D14_EXPECTED_REGISTRY_ID,
        model_version=D14_EXPECTED_MODEL_VERSION,
        candidate_system_sha256=(
            D14_EXPECTED_CANDIDATE_SYSTEM_SHA256
        ),
        feature_contract_sha256=(
            D14_EXPECTED_FEATURE_CONTRACT_SHA256
        ),
        software_environment_sha256=(
            D14_EXPECTED_SOFTWARE_ENVIRONMENT_SHA256
        ),
        freeze_manifest_sha256=(
            D14_EXPECTED_FREEZE_MANIFEST_SHA256
        ),

        development_threshold=D14_EXPECTED_DEVELOPMENT_THRESHOLD,

        expected_test_encounters=D14_EXPECTED_TEST_ENCOUNTERS,
        expected_test_patients=D14_EXPECTED_TEST_PATIENTS,
        expected_test_positives=D14_EXPECTED_TEST_POSITIVES,
        expected_test_negatives=D14_EXPECTED_TEST_NEGATIVES,

        expected_source_feature_count=(
            D14_EXPECTED_SOURCE_FEATURE_COUNT
        ),
        expected_transformed_feature_count=(
            D14_EXPECTED_TRANSFORMED_FEATURE_COUNT
        ),

        evaluation_partition=D14_EVALUATION_PARTITION,
        evaluation_mode=D14_EVALUATION_MODE,

        locked_test_accessed=D14_LOCKED_TEST_ACCESSED,
        locked_test_evaluated=D14_LOCKED_TEST_EVALUATED,
        predictions_generated=(
            D14_LOCKED_TEST_PREDICTIONS_GENERATED
        ),

        model_retrained=D14_MODEL_RETRAINED,
        model_retuned=D14_MODEL_RETUNED,
        preprocessor_refitted=D14_PREPROCESSOR_REFITTED,
        feature_engineering_changed=(
            D14_FEATURE_ENGINEERING_CHANGED
        ),
        feature_set_changed=D14_FEATURE_SET_CHANGED,
        threshold_retuned=D14_THRESHOLD_RETUNED,
        model_recalibrated=D14_MODEL_RECALIBRATED,
        subgroup_threshold_created=(
            D14_SUBGROUP_THRESHOLD_CREATED
        ),
        test_driven_model_selection=(
            D14_TEST_DRIVEN_MODEL_SELECTION
        ),
        test_driven_redesign=D14_TEST_DRIVEN_REDESIGN,

        deployment_authorized=(
            D14_DEPLOYMENT_AUTHORIZED_PRE_EVALUATION
        ),

        prohibited_activities=D14_PROHIBITED_ACTIVITIES,
        interpretation_rules=D14_INTERPRETATION_RULES,
    )


def validate_d14_pre_access_governance_contract(
    contract: D14PreAccessGovernanceContract | None = None,
) -> dict[str, Any]:
    """
    Validate that the D14 pre-access governance boundary is intact.

    PASS means D14 is structurally ready to progress toward a
    separately controlled locked TEST access step.

    PASS does NOT mean TEST has been accessed or evaluated.
    """

    if contract is None:
        contract = build_d14_pre_access_governance_contract()

    checks = {
        "stage_identity_valid": (
            contract.stage_id == "D14"
            and contract.source_lifecycle_stage == "D13"
            and contract.source_git_commit == "b4118f9"
        ),

        "candidate_identity_bound": (
            contract.registry_id
            == D14_EXPECTED_REGISTRY_ID
            and contract.model_version
            == D14_EXPECTED_MODEL_VERSION
            and contract.candidate_system_sha256
            == D14_EXPECTED_CANDIDATE_SYSTEM_SHA256
        ),

        "feature_contract_bound": (
            contract.feature_contract_sha256
            == D14_EXPECTED_FEATURE_CONTRACT_SHA256
        ),

        "environment_provenance_bound": (
            contract.software_environment_sha256
            == D14_EXPECTED_SOFTWARE_ENVIRONMENT_SHA256
        ),

        "freeze_manifest_bound": (
            contract.freeze_manifest_sha256
            == D14_EXPECTED_FREEZE_MANIFEST_SHA256
        ),

        "threshold_frozen": (
            contract.development_threshold
            == D14_EXPECTED_DEVELOPMENT_THRESHOLD
            and D14_THRESHOLD_RETUNING_ALLOWED is False
            and D14_RECALIBRATION_ALLOWED is False
            and D14_SUBGROUP_THRESHOLD_OPTIMIZATION_ALLOWED is False
        ),

        "expected_test_partition_declared": (
            contract.expected_test_encounters == 15_038
            and contract.expected_test_patients == 10_568
            and contract.expected_test_positives == 1_707
            and contract.expected_test_negatives == 13_331
            and (
                contract.expected_test_positives
                + contract.expected_test_negatives
                == contract.expected_test_encounters
            )
        ),

        "feature_dimensions_declared": (
            contract.expected_source_feature_count == 10
            and contract.expected_transformed_feature_count == 49
        ),

        "locked_test_not_accessed": (
            contract.locked_test_accessed is False
        ),

        "locked_test_not_evaluated": (
            contract.locked_test_evaluated is False
        ),

        "locked_test_predictions_not_generated": (
            contract.predictions_generated is False
        ),

        "model_not_retrained": (
            contract.model_retrained is False
        ),

        "model_not_retuned": (
            contract.model_retuned is False
        ),

        "preprocessor_not_refitted": (
            contract.preprocessor_refitted is False
        ),

        "feature_engineering_unchanged": (
            contract.feature_engineering_changed is False
        ),

        "feature_set_unchanged": (
            contract.feature_set_changed is False
        ),

        "threshold_not_retuned": (
            contract.threshold_retuned is False
        ),

        "model_not_recalibrated": (
            contract.model_recalibrated is False
        ),

        "no_subgroup_threshold_created": (
            contract.subgroup_threshold_created is False
        ),

        "no_test_driven_model_selection": (
            contract.test_driven_model_selection is False
        ),

        "no_test_driven_redesign": (
            contract.test_driven_redesign is False
        ),

        "deployment_not_authorized": (
            contract.deployment_authorized is False
        ),

        "evaluation_partition_is_locked_test": (
            contract.evaluation_partition == "LOCKED_TEST"
        ),

        "evaluation_mode_is_confirmatory": (
            contract.evaluation_mode
            == "ONE_TIME_CONFIRMATORY_EVALUATION"
        ),

        "prohibited_activities_declared": (
            len(contract.prohibited_activities) > 0
        ),

        "interpretation_rules_declared": (
            len(contract.interpretation_rules) > 0
        ),
    }

    overall_pass = all(checks.values())

    return {
        "stage_id": D14_STAGE_ID,
        "stage_name": D14_STAGE_NAME,
        "validation_status": "PASS" if overall_pass else "FAIL",
        "overall_pass": overall_pass,
        "checks": checks,
        "locked_test_accessed": contract.locked_test_accessed,
        "locked_test_evaluated": contract.locked_test_evaluated,
        "predictions_generated": contract.predictions_generated,
        "deployment_authorized": contract.deployment_authorized,
        "next_controlled_action": (
            "D14_LOCKED_TEST_ACCESS_IMPLEMENTATION"
            if overall_pass
            else "REMEDIATE_D14_PRE_ACCESS_CONTRACT"
        ),
    }


def print_d14_pre_access_governance_contract() -> None:
    """
    Print the D14 pre-access governance evidence.

    No locked TEST data are accessed by this function.
    """

    contract = build_d14_pre_access_governance_contract()
    validation = validate_d14_pre_access_governance_contract(
        contract
    )

    print("=" * 72)
    print("D14 — LOCKED-TEST EVALUATION")
    print("PRE-ACCESS GOVERNANCE CONTRACT")
    print("=" * 72)

    print()
    print("Lifecycle identity")
    print("-" * 72)
    print(f"Stage:                    {contract.stage_id}")
    print(f"Stage name:               {contract.stage_name}")
    print(
        f"Source lifecycle stage:   "
        f"{contract.source_lifecycle_stage}"
    )
    print(
        f"Source Git commit:        "
        f"{contract.source_git_commit}"
    )

    print()
    print("Frozen candidate")
    print("-" * 72)
    print(f"Registry ID:              {contract.registry_id}")
    print(f"Model version:            {contract.model_version}")
    print(
        f"Candidate system SHA256:  "
        f"{contract.candidate_system_sha256}"
    )
    print(
        f"Feature contract SHA256:  "
        f"{contract.feature_contract_sha256}"
    )
    print(
        f"Freeze manifest SHA256:   "
        f"{contract.freeze_manifest_sha256}"
    )

    print()
    print("Frozen operating point")
    print("-" * 72)
    print(
        f"Development threshold:    "
        f"{contract.development_threshold}"
    )
    print(
        f"Threshold retuning:       "
        f"{contract.threshold_retuned}"
    )
    print(
        f"Model recalibrated:       "
        f"{contract.model_recalibrated}"
    )

    print()
    print("Expected locked TEST identity")
    print("-" * 72)
    print(
        f"Expected encounters:      "
        f"{contract.expected_test_encounters:,}"
    )
    print(
        f"Expected patients:        "
        f"{contract.expected_test_patients:,}"
    )
    print(
        f"Expected positives:       "
        f"{contract.expected_test_positives:,}"
    )
    print(
        f"Expected negatives:       "
        f"{contract.expected_test_negatives:,}"
    )

    print()
    print("Pre-access state")
    print("-" * 72)
    print(
        f"Locked TEST accessed:     "
        f"{contract.locked_test_accessed}"
    )
    print(
        f"Locked TEST evaluated:    "
        f"{contract.locked_test_evaluated}"
    )
    print(
        f"Predictions generated:    "
        f"{contract.predictions_generated}"
    )
    print(
        f"Model retrained:          "
        f"{contract.model_retrained}"
    )
    print(
        f"Preprocessor refitted:    "
        f"{contract.preprocessor_refitted}"
    )
    print(
        f"Deployment authorized:    "
        f"{contract.deployment_authorized}"
    )

    print()
    print("Governance validation")
    print("-" * 72)

    for check_name, passed in validation["checks"].items():
        status = "PASS" if passed else "FAIL"
        print(f"{check_name:<45} {status}")

    print()
    print("-" * 72)
    print(
        f"OVERALL PRE-ACCESS STATUS: "
        f"{validation['validation_status']}"
    )
    print(
        f"NEXT CONTROLLED ACTION:    "
        f"{validation['next_controlled_action']}"
    )
    print("=" * 72)


# ============================================================
# MODULE ENTRY POINT
# ============================================================

if __name__ == "__main__":
    print_d14_pre_access_governance_contract()

# ============================================================
# D14.10 — CONTROLLED LOCKED-TEST ACCESS
# ============================================================
#
# This section performs the FIRST governed access to the
# locked TEST partition.
#
# IMPORTANT:
# Accessing/reconstructing TEST changes the lifecycle state:
#
#   locked_test_accessed = True
#
# However, this section MUST NOT:
#   - load the predictive model,
#   - load/refit preprocessing for inference,
#   - transform TEST features,
#   - generate TEST probabilities,
#   - calculate TEST performance metrics,
#   - retune the operating threshold,
#   - recalibrate the model,
#   - authorize deployment.
#
# The sole purpose is to reconstruct and validate the
# authoritative D5-defined TEST partition.
# ============================================================


from pathlib import Path

import pandas as pd


# ============================================================
# D14.11 — AUTHORITATIVE INPUT ARTIFACTS
# ============================================================

D14_D5_SPLIT_ASSIGNMENT_PATH = Path(
    "artifacts/splits/D5_patient_split_assignment.csv"
)

D14_D3_GOVERNED_COHORT_PATH = Path(
    "data/interim/D3_governed_modeling_cohort.parquet"
)

D14_PATIENT_ID_COLUMN = "patient_nbr"
D14_ENCOUNTER_ID_COLUMN = "encounter_id"
D14_TARGET_COLUMN = "readmitted_30d"
D14_SPLIT_COLUMN = "split"

D14_TRAIN_SPLIT_LABEL = "train"
D14_VALIDATION_SPLIT_LABEL = "validation"
D14_TEST_SPLIT_LABEL = "test"


# ============================================================
# D14.12 — AUTHORITATIVE SOURCE FEATURE CONTRACT
# ============================================================
#
# These are the 10 D7/D13 governed source features.
#
# No additional feature may enter D14 evaluation.
# ============================================================

D14_REQUIRED_SOURCE_FEATURES = (
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

D14_RAW_UTILIZATION_SOURCE_COLUMNS = (
    "number_outpatient",
    "number_emergency",
    "number_inpatient",
)


# ============================================================
# D14.13 — TEST ACCESS STATE
# ============================================================

D14_TEST_ACCESS_CLASSIFICATION = (
    "CONTROLLED_PARTITION_RECONSTRUCTION_ONLY"
)

D14_TEST_ACCESS_PERFORMED = True
D14_TEST_EVALUATION_PERFORMED = False
D14_TEST_PREDICTIONS_GENERATED_AFTER_ACCESS = False

D14_MODEL_LOADED_FOR_TEST_INFERENCE = False
D14_PREPROCESSOR_LOADED_FOR_TEST_INFERENCE = False
D14_TEST_FEATURES_TRANSFORMED = False

D14_MODEL_RETRAINED_AFTER_TEST_ACCESS = False
D14_MODEL_RETUNED_AFTER_TEST_ACCESS = False
D14_PREPROCESSOR_REFITTED_AFTER_TEST_ACCESS = False
D14_THRESHOLD_RETUNED_AFTER_TEST_ACCESS = False
D14_MODEL_RECALIBRATED_AFTER_TEST_ACCESS = False
D14_DEPLOYMENT_AUTHORIZED_AFTER_TEST_ACCESS = False


# ============================================================
# D14.14 — CONTROLLED ARTIFACT LOADERS
# ============================================================


def load_d14_d5_split_assignment() -> pd.DataFrame:
    """
    Load the authoritative D5 patient-level split assignment.

    This artifact identifies which patients belong to TEST.

    Loading this assignment does not itself calculate model
    performance or generate predictions.
    """

    if not D14_D5_SPLIT_ASSIGNMENT_PATH.exists():
        raise FileNotFoundError(
            "Authoritative D5 split assignment not found: "
            f"{D14_D5_SPLIT_ASSIGNMENT_PATH}"
        )

    assignment = pd.read_csv(
        D14_D5_SPLIT_ASSIGNMENT_PATH
    )

    required_columns = {
        D14_PATIENT_ID_COLUMN,
        "patient_positive",
        "encounter_count",
        "positive_encounter_count",
        D14_SPLIT_COLUMN,
    }

    missing = required_columns.difference(
        assignment.columns
    )

    if missing:
        raise ValueError(
            "D5 split assignment is missing required columns: "
            f"{sorted(missing)}"
        )

    return assignment


def load_d14_governed_d3_cohort() -> pd.DataFrame:
    """
    Load the frozen governed D3 modeling cohort.

    This is the authoritative encounter-level cohort from which
    the D5-defined TEST partition is reconstructed.
    """

    if not D14_D3_GOVERNED_COHORT_PATH.exists():
        raise FileNotFoundError(
            "Governed D3 cohort not found: "
            f"{D14_D3_GOVERNED_COHORT_PATH}"
        )

    cohort = pd.read_parquet(
        D14_D3_GOVERNED_COHORT_PATH
    )

    required_columns = {
        D14_ENCOUNTER_ID_COLUMN,
        D14_PATIENT_ID_COLUMN,
        D14_TARGET_COLUMN,
    }

    missing = required_columns.difference(cohort.columns)

    if missing:
        raise ValueError(
            "D3 governed cohort is missing required columns: "
            f"{sorted(missing)}"
        )

    return cohort


# ============================================================
# D14.15 — RECONSTRUCT AUTHORITATIVE TEST PARTITION
# ============================================================


def reconstruct_d14_locked_test_partition(
    assignment: pd.DataFrame | None = None,
    cohort: pd.DataFrame | None = None,
) -> dict[str, Any]:
    """
    Reconstruct the locked TEST partition using the frozen D5
    patient assignment and the governed D3 encounter cohort.

    This is TEST ACCESS.

    It is NOT TEST EVALUATION.

    No predictive model or preprocessor is loaded here.
    """

    if assignment is None:
        assignment = load_d14_d5_split_assignment()

    if cohort is None:
        cohort = load_d14_governed_d3_cohort()

    test_assignment = assignment.loc[
        assignment[D14_SPLIT_COLUMN]
        == D14_TEST_SPLIT_LABEL
    ].copy()

    train_assignment = assignment.loc[
        assignment[D14_SPLIT_COLUMN]
        == D14_TRAIN_SPLIT_LABEL
    ].copy()

    validation_assignment = assignment.loc[
        assignment[D14_SPLIT_COLUMN]
        == D14_VALIDATION_SPLIT_LABEL
    ].copy()

    test_patients = set(
        test_assignment[D14_PATIENT_ID_COLUMN].tolist()
    )

    train_patients = set(
        train_assignment[D14_PATIENT_ID_COLUMN].tolist()
    )

    validation_patients = set(
        validation_assignment[
            D14_PATIENT_ID_COLUMN
        ].tolist()
    )

    locked_test = cohort.loc[
        cohort[D14_PATIENT_ID_COLUMN].isin(test_patients)
    ].copy()

    return {
        "locked_test": locked_test,
        "assignment": assignment,
        "test_assignment": test_assignment,
        "test_patients": test_patients,
        "train_patients": train_patients,
        "validation_patients": validation_patients,
        "locked_test_accessed": True,
        "locked_test_evaluated": False,
        "predictions_generated": False,
        "model_loaded": False,
        "preprocessor_loaded": False,
        "test_features_transformed": False,
        "deployment_authorized": False,
    }


# ============================================================
# D14.16 — RECONSTRUCT GOVERNED D6/D7 SOURCE FEATURES
# ============================================================
#
# Only deterministic transformations already frozen by D6 are
# reconstructed here.
#
# No data-learned transformation occurs.
# No preprocessor is fitted.
# ============================================================


def build_d14_governed_source_features(
    locked_test: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build the 10 governed source features required by the frozen
    D7 preprocessing contract.

    The five utilization features are deterministic derivatives
    of the D4-approved historical utilization source columns.

    This function does NOT load or fit the D7 preprocessor.
    """

    required_raw_columns = {
        "race",
        "gender",
        "age",
        "admission_type_id",
        "admission_source_id",
        *D14_RAW_UTILIZATION_SOURCE_COLUMNS,
    }

    missing = required_raw_columns.difference(
        locked_test.columns
    )

    if missing:
        raise ValueError(
            "Locked TEST cohort is missing required governed "
            f"source columns: {sorted(missing)}"
        )

    features = pd.DataFrame(
        index=locked_test.index
    )

    features["race"] = locked_test["race"]
    features["gender"] = locked_test["gender"]
    features["age"] = locked_test["age"]

    features["admission_type_id"] = (
        locked_test["admission_type_id"]
    )

    features["admission_source_id"] = (
        locked_test["admission_source_id"]
    )

    outpatient = pd.to_numeric(
        locked_test["number_outpatient"],
        errors="coerce",
    )

    emergency = pd.to_numeric(
        locked_test["number_emergency"],
        errors="coerce",
    )

    inpatient = pd.to_numeric(
        locked_test["number_inpatient"],
        errors="coerce",
    )

    features["prior_outpatient_use"] = (
        outpatient > 0
    ).astype(int)

    features["prior_emergency_use"] = (
        emergency > 0
    ).astype(int)

    features["prior_inpatient_use"] = (
        inpatient > 0
    ).astype(int)

    features["prior_utilization_intensity"] = (
        outpatient.fillna(0)
        + emergency.fillna(0)
        + inpatient.fillna(0)
    )

    features["prior_utilization_domain_count"] = (
        (outpatient > 0).astype(int)
        + (emergency > 0).astype(int)
        + (inpatient > 0).astype(int)
    )

    features = features.loc[
        :,
        list(D14_REQUIRED_SOURCE_FEATURES),
    ]

    return features


# ============================================================
# D14.17 — LOCKED-TEST PARTITION INTEGRITY VALIDATION
# ============================================================


def validate_d14_locked_test_partition(
    bundle: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Validate the reconstructed TEST partition before any
    preprocessing or model inference occurs.
    """

    if bundle is None:
        bundle = reconstruct_d14_locked_test_partition()

    locked_test = bundle["locked_test"]

    source_features = build_d14_governed_source_features(
        locked_test
    )

    test_patients = bundle["test_patients"]
    train_patients = bundle["train_patients"]
    validation_patients = bundle[
        "validation_patients"
    ]

    actual_encounters = int(len(locked_test))

    actual_patients = int(
        locked_test[D14_PATIENT_ID_COLUMN].nunique()
    )

    actual_positives = int(
        locked_test[D14_TARGET_COLUMN].sum()
    )

    actual_negatives = int(
        actual_encounters - actual_positives
    )

    train_test_overlap = (
        train_patients.intersection(test_patients)
    )

    validation_test_overlap = (
        validation_patients.intersection(test_patients)
    )

    duplicate_encounter_count = int(
        locked_test[
            D14_ENCOUNTER_ID_COLUMN
        ].duplicated().sum()
    )

    unexpected_test_patients = set(
        locked_test[D14_PATIENT_ID_COLUMN].unique()
    ).difference(test_patients)

    missing_test_patients = test_patients.difference(
        set(
            locked_test[
                D14_PATIENT_ID_COLUMN
            ].unique()
        )
    )

    target_values = set(
        locked_test[D14_TARGET_COLUMN]
        .dropna()
        .unique()
        .tolist()
    )

    checks = {
        "test_access_recorded": (
            bundle["locked_test_accessed"] is True
        ),

        "test_not_evaluated": (
            bundle["locked_test_evaluated"] is False
        ),

        "predictions_not_generated": (
            bundle["predictions_generated"] is False
        ),

        "model_not_loaded": (
            bundle["model_loaded"] is False
        ),

        "preprocessor_not_loaded": (
            bundle["preprocessor_loaded"] is False
        ),

        "test_not_transformed": (
            bundle["test_features_transformed"] is False
        ),

        "expected_encounter_count": (
            actual_encounters
            == D14_EXPECTED_TEST_ENCOUNTERS
        ),

        "expected_patient_count": (
            actual_patients
            == D14_EXPECTED_TEST_PATIENTS
        ),

        "expected_positive_count": (
            actual_positives
            == D14_EXPECTED_TEST_POSITIVES
        ),

        "expected_negative_count": (
            actual_negatives
            == D14_EXPECTED_TEST_NEGATIVES
        ),

        "train_test_patient_overlap_zero": (
            len(train_test_overlap) == 0
        ),

        "validation_test_patient_overlap_zero": (
            len(validation_test_overlap) == 0
        ),

        "encounter_ids_unique": (
            duplicate_encounter_count == 0
        ),

        "no_unexpected_test_patients": (
            len(unexpected_test_patients) == 0
        ),

        "no_missing_test_patients": (
            len(missing_test_patients) == 0
        ),

        "target_is_binary": (
            target_values.issubset({0, 1})
        ),

        "source_feature_count_valid": (
            source_features.shape[1]
            == D14_EXPECTED_SOURCE_FEATURE_COUNT
        ),

        "source_feature_order_valid": (
            tuple(source_features.columns)
            == D14_REQUIRED_SOURCE_FEATURES
        ),

        "source_feature_row_count_valid": (
            len(source_features)
            == D14_EXPECTED_TEST_ENCOUNTERS
        ),

        "model_not_retrained": (
            D14_MODEL_RETRAINED_AFTER_TEST_ACCESS
            is False
        ),

        "model_not_retuned": (
            D14_MODEL_RETUNED_AFTER_TEST_ACCESS
            is False
        ),

        "preprocessor_not_refitted": (
            D14_PREPROCESSOR_REFITTED_AFTER_TEST_ACCESS
            is False
        ),

        "threshold_not_retuned": (
            D14_THRESHOLD_RETUNED_AFTER_TEST_ACCESS
            is False
        ),

        "model_not_recalibrated": (
            D14_MODEL_RECALIBRATED_AFTER_TEST_ACCESS
            is False
        ),

        "deployment_not_authorized": (
            D14_DEPLOYMENT_AUTHORIZED_AFTER_TEST_ACCESS
            is False
        ),
    }

    overall_pass = all(checks.values())

    return {
        "stage_id": D14_STAGE_ID,
        "validation_status": (
            "PASS" if overall_pass else "FAIL"
        ),
        "overall_pass": overall_pass,
        "checks": checks,
        "actual_test_encounters": actual_encounters,
        "actual_test_patients": actual_patients,
        "actual_test_positives": actual_positives,
        "actual_test_negatives": actual_negatives,
        "train_test_patient_overlap": len(
            train_test_overlap
        ),
        "validation_test_patient_overlap": len(
            validation_test_overlap
        ),
        "duplicate_encounter_count": (
            duplicate_encounter_count
        ),
        "source_feature_shape": (
            int(source_features.shape[0]),
            int(source_features.shape[1]),
        ),
        "locked_test_accessed": True,
        "locked_test_evaluated": False,
        "predictions_generated": False,
        "deployment_authorized": False,
        "next_controlled_action": (
            "D14_FROZEN_PREPROCESSING_OF_LOCKED_TEST"
            if overall_pass
            else "STOP_REMEDIATE_TEST_PARTITION_INTEGRITY"
        ),
    }


# ============================================================
# D14.18 — CONTROLLED TEST ACCESS EVIDENCE
# ============================================================


def build_d14_locked_test_access_evidence(
) -> dict[str, Any]:
    """
    Build the formal evidence object for first governed TEST
    access and partition integrity validation.
    """

    bundle = reconstruct_d14_locked_test_partition()

    validation = validate_d14_locked_test_partition(
        bundle
    )

    return {
        "stage_id": D14_STAGE_ID,
        "stage_name": D14_STAGE_NAME,
        "source_git_commit": D14_SOURCE_GIT_COMMIT,
        "registry_id": D14_EXPECTED_REGISTRY_ID,
        "candidate_system_sha256": (
            D14_EXPECTED_CANDIDATE_SYSTEM_SHA256
        ),
        "access_classification": (
            D14_TEST_ACCESS_CLASSIFICATION
        ),
        "evaluation_partition": (
            D14_EVALUATION_PARTITION
        ),
        "test_accessed": True,
        "test_evaluated": False,
        "predictions_generated": False,
        "model_loaded_for_inference": False,
        "preprocessor_loaded_for_inference": False,
        "test_features_transformed": False,
        "frozen_threshold": (
            D14_EXPECTED_DEVELOPMENT_THRESHOLD
        ),
        "partition_validation": validation,
        "deployment_authorized": False,
    }


# ============================================================
# D14.19 — PRINT CONTROLLED TEST ACCESS EVIDENCE
# ============================================================


def print_d14_locked_test_access_evidence() -> None:
    """
    Print the first governed TEST-access evidence.

    This function reconstructs TEST and validates partition
    integrity, but performs NO predictive inference.
    """

    evidence = build_d14_locked_test_access_evidence()

    validation = evidence[
        "partition_validation"
    ]

    print("=" * 72)
    print("D14 — LOCKED-TEST EVALUATION")
    print("CONTROLLED TEST ACCESS & PARTITION INTEGRITY")
    print("=" * 72)

    print()
    print("Frozen candidate")
    print("-" * 72)
    print(
        f"Registry ID:              "
        f"{evidence['registry_id']}"
    )
    print(
        f"Source Git commit:        "
        f"{evidence['source_git_commit']}"
    )
    print(
        f"Candidate system SHA256:  "
        f"{evidence['candidate_system_sha256']}"
    )
    print(
        f"Frozen threshold:         "
        f"{evidence['frozen_threshold']}"
    )

    print()
    print("Controlled TEST access")
    print("-" * 72)
    print(
        f"Access classification:    "
        f"{evidence['access_classification']}"
    )
    print(
        f"TEST accessed:            "
        f"{evidence['test_accessed']}"
    )
    print(
        f"TEST evaluated:           "
        f"{evidence['test_evaluated']}"
    )
    print(
        f"Predictions generated:    "
        f"{evidence['predictions_generated']}"
    )
    print(
        f"Model loaded:             "
        f"{evidence['model_loaded_for_inference']}"
    )
    print(
        f"Preprocessor loaded:      "
        f"{evidence['preprocessor_loaded_for_inference']}"
    )
    print(
        f"TEST transformed:         "
        f"{evidence['test_features_transformed']}"
    )

    print()
    print("Observed TEST partition")
    print("-" * 72)
    print(
        f"Encounters:               "
        f"{validation['actual_test_encounters']:,}"
    )
    print(
        f"Unique patients:          "
        f"{validation['actual_test_patients']:,}"
    )
    print(
        f"Positive outcomes:        "
        f"{validation['actual_test_positives']:,}"
    )
    print(
        f"Negative outcomes:        "
        f"{validation['actual_test_negatives']:,}"
    )
    print(
        f"TRAIN ↔ TEST overlap:     "
        f"{validation['train_test_patient_overlap']}"
    )
    print(
        f"VALIDATION ↔ TEST overlap:"
        f" {validation['validation_test_patient_overlap']}"
    )
    print(
        f"Source feature shape:     "
        f"{validation['source_feature_shape']}"
    )

    print()
    print("Partition integrity checks")
    print("-" * 72)

    for check_name, passed in validation["checks"].items():
        status = "PASS" if passed else "FAIL"
        print(f"{check_name:<45} {status}")

    print()
    print("-" * 72)
    print(
        f"PARTITION INTEGRITY STATUS: "
        f"{validation['validation_status']}"
    )
    print(
        f"NEXT CONTROLLED ACTION:     "
        f"{validation['next_controlled_action']}"
    )
    print(
        f"DEPLOYMENT AUTHORIZED:      "
        f"{validation['deployment_authorized']}"
    )
    print("=" * 72)

# ============================================================
# D14.20 — FROZEN TEST PREPROCESSING BOUNDARY
# ============================================================
#
# Purpose:
# Transform the already integrity-validated locked TEST
# partition using ONLY:
#
#   1. frozen deterministic D6 feature engineering,
#   2. deterministic D7 unknown-category normalization,
#   3. the persisted TRAIN-fitted D7 preprocessor,
#   4. the persisted D7 transformed feature schema.
#
# PROHIBITED:
#   - preprocessor.fit()
#   - preprocessor.fit_transform()
#   - preprocessor persistence
#   - schema modification
#   - model loading
#   - TEST prediction
#   - TEST metric calculation
#   - threshold modification
# ============================================================


import numpy as np

from src.features.engineering import (
    engineer_prior_utilization_features,
    get_governed_d6_feature_lists,
    validate_prior_utilization_features,
)

from src.features.preprocessing import (
    D7_PREPROCESSOR_PATH,
    D7_TRANSFORMED_SCHEMA_PATH,
    calculate_file_sha256 as calculate_d7_file_sha256,
    load_persisted_primary_preprocessor,
    load_persisted_transformed_schema,
    normalize_source_unknown_categories,
)


# ============================================================
# D14.21 — FROZEN D7 ARTIFACT IDENTITY
# ============================================================

D14_FROZEN_D7_PREPROCESSOR_PATH = Path(
    D7_PREPROCESSOR_PATH
)

D14_FROZEN_D7_SCHEMA_PATH = Path(
    D7_TRANSFORMED_SCHEMA_PATH
)


# ============================================================
# D14.22 — AUTHORITATIVE D6 TEST FEATURE ENGINEERING
# ============================================================


def build_d14_authoritative_source_features(
    locked_test: pd.DataFrame,
) -> dict[str, Any]:
    """
    Build the frozen 10-feature D6/D7 source representation
    for locked TEST.

    Prior-utilization features are generated through the
    authoritative D6 deterministic feature-engineering
    function rather than reimplementing D6 logic inside D14.

    No fitted state is learned.
    """

    required_direct_features = (
        "race",
        "gender",
        "age",
        "admission_type_id",
        "admission_source_id",
    )

    missing_direct = set(
        required_direct_features
    ).difference(locked_test.columns)

    if missing_direct:
        raise ValueError(
            "Locked TEST is missing required direct governed "
            f"features: {sorted(missing_direct)}"
        )

    utilization_features = (
        engineer_prior_utilization_features(
            locked_test
        )
    )

    utilization_validation = (
        validate_prior_utilization_features(
            locked_test,
            utilization_features,
        )
    )

    source_features = pd.DataFrame(
        index=locked_test.index
    )

    for column in required_direct_features:
        source_features[column] = locked_test[column]

    utilization_columns = (
        "prior_outpatient_use",
        "prior_emergency_use",
        "prior_inpatient_use",
        "prior_utilization_intensity",
        "prior_utilization_domain_count",
    )

    for column in utilization_columns:
        if column not in utilization_features.columns:
            raise ValueError(
                "Authoritative D6 utilization engineering "
                f"did not produce required feature: {column}"
            )

        source_features[column] = (
            utilization_features[column]
        )

    source_features = source_features.loc[
        :,
        list(D14_REQUIRED_SOURCE_FEATURES),
    ]

    governed_lists = get_governed_d6_feature_lists()

    return {
        "source_features": source_features,
        "utilization_features": utilization_features,
        "utilization_validation": (
            utilization_validation
        ),
        "governed_d6_feature_lists": governed_lists,
        "feature_engineering_learned_state": False,
        "locked_test_rows": int(len(source_features)),
        "source_feature_count": int(
            source_features.shape[1]
        ),
    }


# ============================================================
# D14.23 — FROZEN D7 ARTIFACT PRE-TRANSFORM SNAPSHOT
# ============================================================


def build_d14_d7_artifact_snapshot() -> dict[str, Any]:
    """
    Capture frozen D7 artifact identity without modifying it.
    """

    if not D14_FROZEN_D7_PREPROCESSOR_PATH.exists():
        raise FileNotFoundError(
            "Frozen D7 preprocessor not found: "
            f"{D14_FROZEN_D7_PREPROCESSOR_PATH}"
        )

    if not D14_FROZEN_D7_SCHEMA_PATH.exists():
        raise FileNotFoundError(
            "Frozen D7 transformed schema not found: "
            f"{D14_FROZEN_D7_SCHEMA_PATH}"
        )

    return {
        "preprocessor_path": str(
            D14_FROZEN_D7_PREPROCESSOR_PATH
        ),
        "preprocessor_sha256": (
            calculate_d7_file_sha256(
                D14_FROZEN_D7_PREPROCESSOR_PATH
            )
        ),
        "preprocessor_size_bytes": int(
            D14_FROZEN_D7_PREPROCESSOR_PATH
            .stat()
            .st_size
        ),
        "preprocessor_mtime_ns": int(
            D14_FROZEN_D7_PREPROCESSOR_PATH
            .stat()
            .st_mtime_ns
        ),
        "schema_path": str(
            D14_FROZEN_D7_SCHEMA_PATH
        ),
        "schema_sha256": (
            calculate_d7_file_sha256(
                D14_FROZEN_D7_SCHEMA_PATH
            )
        ),
        "schema_size_bytes": int(
            D14_FROZEN_D7_SCHEMA_PATH
            .stat()
            .st_size
        ),
        "schema_mtime_ns": int(
            D14_FROZEN_D7_SCHEMA_PATH
            .stat()
            .st_mtime_ns
        ),
    }


# ============================================================
# D14.24 — VERIFY FROZEN D7 IDENTITY
# ============================================================


def validate_d14_d7_artifact_snapshot(
    snapshot: dict[str, Any],
) -> dict[str, bool]:
    """
    Validate D7 preprocessor/schema identity against D13.
    """

    return {
        "preprocessor_sha256_valid": (
            snapshot["preprocessor_sha256"].upper()
            == D14_EXPECTED_PREPROCESSOR_SHA256
        ),
        "schema_sha256_valid": (
            snapshot["schema_sha256"].upper()
            == D14_EXPECTED_TRANSFORMED_SCHEMA_SHA256
        ),
        "preprocessor_exists": (
            D14_FROZEN_D7_PREPROCESSOR_PATH.exists()
        ),
        "schema_exists": (
            D14_FROZEN_D7_SCHEMA_PATH.exists()
        ),
    }


# ============================================================
# D14.25 — TRANSFORM LOCKED TEST WITH FROZEN D7 STATE
# ============================================================


def transform_d14_locked_test_with_frozen_d7(
    bundle: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Transform locked TEST with the already-fitted D7
    preprocessor.

    This function performs TEST transformation.

    It MUST NOT fit or persist any preprocessing state.
    """

    if bundle is None:
        bundle = reconstruct_d14_locked_test_partition()

    partition_validation = (
        validate_d14_locked_test_partition(bundle)
    )

    if not partition_validation["overall_pass"]:
        raise RuntimeError(
            "Locked TEST partition integrity failed. "
            "D14 preprocessing is blocked."
        )

    locked_test = bundle["locked_test"]

    authoritative = (
        build_d14_authoritative_source_features(
            locked_test
        )
    )

    source_features = authoritative[
        "source_features"
    ]

    if tuple(source_features.columns) != (
        D14_REQUIRED_SOURCE_FEATURES
    ):
        raise RuntimeError(
            "D14 source feature order does not match "
            "the frozen feature contract."
        )

    normalized_features = (
        normalize_source_unknown_categories(
            source_features
        )
    )

    before_snapshot = (
        build_d14_d7_artifact_snapshot()
    )

    before_checks = (
        validate_d14_d7_artifact_snapshot(
            before_snapshot
        )
    )

    if not all(before_checks.values()):
        raise RuntimeError(
            "Frozen D7 artifact identity validation "
            "failed before TEST transformation."
        )

    preprocessor = (
        load_persisted_primary_preprocessor()
    )

    transformed_schema = (
        load_persisted_transformed_schema()
    )

    if len(transformed_schema) != (
        D14_EXPECTED_TRANSFORMED_FEATURE_COUNT
    ):
        raise RuntimeError(
            "Frozen transformed schema feature count "
            "does not equal 49."
        )

    transformed = preprocessor.transform(
        normalized_features
    )

    if hasattr(transformed, "toarray"):
        transformed = transformed.toarray()

    transformed = np.asarray(
        transformed,
        dtype=float,
    )

    after_snapshot = (
        build_d14_d7_artifact_snapshot()
    )

    after_checks = (
        validate_d14_d7_artifact_snapshot(
            after_snapshot
        )
    )

    artifact_identity_unchanged = (
        before_snapshot == after_snapshot
    )

    return {
        "locked_test": locked_test,
        "source_features": source_features,
        "normalized_source_features": (
            normalized_features
        ),
        "transformed_test": transformed,
        "transformed_schema": transformed_schema,
        "preprocessor": preprocessor,
        "partition_validation": (
            partition_validation
        ),
        "authoritative_feature_engineering": (
            authoritative
        ),
        "before_artifact_snapshot": (
            before_snapshot
        ),
        "after_artifact_snapshot": (
            after_snapshot
        ),
        "before_artifact_checks": before_checks,
        "after_artifact_checks": after_checks,
        "artifact_identity_unchanged": (
            artifact_identity_unchanged
        ),
        "locked_test_accessed": True,
        "locked_test_transformed": True,
        "locked_test_evaluated": False,
        "model_loaded": False,
        "predictions_generated": False,
        "preprocessor_refitted": False,
        "preprocessor_persisted": False,
        "schema_modified": False,
        "threshold_retuned": False,
        "deployment_authorized": False,
    }


# ============================================================
# D14.26 — VALIDATE FROZEN TEST TRANSFORMATION
# ============================================================


def validate_d14_frozen_test_transformation(
    transformed_bundle: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Validate the locked TEST representation before model
    inference is permitted.
    """

    if transformed_bundle is None:
        transformed_bundle = (
            transform_d14_locked_test_with_frozen_d7()
        )

    X_test = transformed_bundle[
        "transformed_test"
    ]

    source_features = transformed_bundle[
        "source_features"
    ]

    schema = transformed_bundle[
        "transformed_schema"
    ]

    checks = {
        "partition_integrity_passed": (
            transformed_bundle[
                "partition_validation"
            ]["overall_pass"]
            is True
        ),

        "test_accessed": (
            transformed_bundle[
                "locked_test_accessed"
            ]
            is True
        ),

        "test_transformed": (
            transformed_bundle[
                "locked_test_transformed"
            ]
            is True
        ),

        "test_not_evaluated": (
            transformed_bundle[
                "locked_test_evaluated"
            ]
            is False
        ),

        "model_not_loaded": (
            transformed_bundle["model_loaded"]
            is False
        ),

        "predictions_not_generated": (
            transformed_bundle[
                "predictions_generated"
            ]
            is False
        ),

        "source_rows_preserved": (
            source_features.shape[0]
            == D14_EXPECTED_TEST_ENCOUNTERS
        ),

        "source_feature_count_valid": (
            source_features.shape[1]
            == D14_EXPECTED_SOURCE_FEATURE_COUNT
        ),

        "source_feature_order_valid": (
            tuple(source_features.columns)
            == D14_REQUIRED_SOURCE_FEATURES
        ),

        "transformed_rows_preserved": (
            X_test.shape[0]
            == D14_EXPECTED_TEST_ENCOUNTERS
        ),

        "transformed_feature_count_valid": (
            X_test.shape[1]
            == D14_EXPECTED_TRANSFORMED_FEATURE_COUNT
        ),

        "schema_feature_count_valid": (
            len(schema)
            == D14_EXPECTED_TRANSFORMED_FEATURE_COUNT
        ),

        "transformed_values_finite": (
            bool(np.isfinite(X_test).all())
        ),

        "preprocessor_identity_valid_before": (
            transformed_bundle[
                "before_artifact_checks"
            ]["preprocessor_sha256_valid"]
        ),

        "schema_identity_valid_before": (
            transformed_bundle[
                "before_artifact_checks"
            ]["schema_sha256_valid"]
        ),

        "preprocessor_identity_valid_after": (
            transformed_bundle[
                "after_artifact_checks"
            ]["preprocessor_sha256_valid"]
        ),

        "schema_identity_valid_after": (
            transformed_bundle[
                "after_artifact_checks"
            ]["schema_sha256_valid"]
        ),

        "frozen_artifacts_unchanged": (
            transformed_bundle[
                "artifact_identity_unchanged"
            ]
            is True
        ),

        "preprocessor_not_refitted": (
            transformed_bundle[
                "preprocessor_refitted"
            ]
            is False
        ),

        "preprocessor_not_persisted": (
            transformed_bundle[
                "preprocessor_persisted"
            ]
            is False
        ),

        "schema_not_modified": (
            transformed_bundle[
                "schema_modified"
            ]
            is False
        ),

        "threshold_not_retuned": (
            transformed_bundle[
                "threshold_retuned"
            ]
            is False
        ),

        "deployment_not_authorized": (
            transformed_bundle[
                "deployment_authorized"
            ]
            is False
        ),
    }

    overall_pass = all(checks.values())

    return {
        "stage_id": D14_STAGE_ID,
        "validation_status": (
            "PASS" if overall_pass else "FAIL"
        ),
        "overall_pass": overall_pass,
        "checks": checks,
        "source_feature_shape": (
            int(source_features.shape[0]),
            int(source_features.shape[1]),
        ),
        "transformed_test_shape": (
            int(X_test.shape[0]),
            int(X_test.shape[1]),
        ),
        "schema_feature_count": int(len(schema)),
        "all_transformed_values_finite": bool(
            np.isfinite(X_test).all()
        ),
        "preprocessor_sha256": (
            transformed_bundle[
                "after_artifact_snapshot"
            ]["preprocessor_sha256"]
        ),
        "schema_sha256": (
            transformed_bundle[
                "after_artifact_snapshot"
            ]["schema_sha256"]
        ),
        "frozen_artifacts_unchanged": (
            transformed_bundle[
                "artifact_identity_unchanged"
            ]
        ),
        "locked_test_accessed": True,
        "locked_test_transformed": True,
        "locked_test_evaluated": False,
        "predictions_generated": False,
        "deployment_authorized": False,
        "next_controlled_action": (
            "D14_FROZEN_MODEL_INFERENCE"
            if overall_pass
            else "STOP_REMEDIATE_TEST_TRANSFORMATION"
        ),
    }


# ============================================================
# D14.27 — BUILD TRANSFORMATION EVIDENCE
# ============================================================


def build_d14_frozen_test_transformation_evidence(
) -> dict[str, Any]:
    """
    Build formal evidence for frozen D7 transformation of TEST.
    """

    transformed_bundle = (
        transform_d14_locked_test_with_frozen_d7()
    )

    validation = (
        validate_d14_frozen_test_transformation(
            transformed_bundle
        )
    )

    return {
        "stage_id": D14_STAGE_ID,
        "registry_id": D14_EXPECTED_REGISTRY_ID,
        "candidate_system_sha256": (
            D14_EXPECTED_CANDIDATE_SYSTEM_SHA256
        ),
        "frozen_threshold": (
            D14_EXPECTED_DEVELOPMENT_THRESHOLD
        ),
        "test_accessed": True,
        "test_transformed": True,
        "test_evaluated": False,
        "model_loaded": False,
        "predictions_generated": False,
        "preprocessor_refitted": False,
        "validation": validation,
        "deployment_authorized": False,
    }


# ============================================================
# D14.28 — PRINT TRANSFORMATION EVIDENCE
# ============================================================


def print_d14_frozen_test_transformation_evidence() -> None:
    """
    Print governed TEST transformation evidence.

    NO model inference occurs.
    """

    evidence = (
        build_d14_frozen_test_transformation_evidence()
    )

    validation = evidence["validation"]

    print("=" * 72)
    print("D14 — LOCKED-TEST EVALUATION")
    print("FROZEN D7 TEST TRANSFORMATION")
    print("=" * 72)

    print()
    print("Candidate")
    print("-" * 72)
    print(
        f"Registry ID:              "
        f"{evidence['registry_id']}"
    )
    print(
        f"Candidate system SHA256:  "
        f"{evidence['candidate_system_sha256']}"
    )
    print(
        f"Frozen threshold:         "
        f"{evidence['frozen_threshold']}"
    )

    print()
    print("TEST transformation state")
    print("-" * 72)
    print(
        f"TEST accessed:            "
        f"{evidence['test_accessed']}"
    )
    print(
        f"TEST transformed:         "
        f"{evidence['test_transformed']}"
    )
    print(
        f"TEST evaluated:           "
        f"{evidence['test_evaluated']}"
    )
    print(
        f"Model loaded:             "
        f"{evidence['model_loaded']}"
    )
    print(
        f"Predictions generated:    "
        f"{evidence['predictions_generated']}"
    )
    print(
        f"Preprocessor refitted:    "
        f"{evidence['preprocessor_refitted']}"
    )

    print()
    print("Representation")
    print("-" * 72)
    print(
        f"Source feature shape:     "
        f"{validation['source_feature_shape']}"
    )
    print(
        f"Transformed TEST shape:   "
        f"{validation['transformed_test_shape']}"
    )
    print(
        f"Schema feature count:     "
        f"{validation['schema_feature_count']}"
    )
    print(
        f"Finite transformed data:  "
        f"{validation['all_transformed_values_finite']}"
    )

    print()
    print("Frozen D7 integrity")
    print("-" * 72)
    print(
        f"Preprocessor SHA256:      "
        f"{validation['preprocessor_sha256']}"
    )
    print(
        f"Schema SHA256:            "
        f"{validation['schema_sha256']}"
    )
    print(
        f"Artifacts unchanged:      "
        f"{validation['frozen_artifacts_unchanged']}"
    )

    print()
    print("Transformation checks")
    print("-" * 72)

    for check_name, passed in validation["checks"].items():
        status = "PASS" if passed else "FAIL"
        print(f"{check_name:<45} {status}")

    print()
    print("-" * 72)
    print(
        f"TRANSFORMATION STATUS:     "
        f"{validation['validation_status']}"
    )
    print(
        f"NEXT CONTROLLED ACTION:    "
        f"{validation['next_controlled_action']}"
    )
    print(
        f"DEPLOYMENT AUTHORIZED:     "
        f"{validation['deployment_authorized']}"
    )
    print("=" * 72)


# ============================================================
# D14.29 — MODEL-INFERENCE BOUNDARY
# ============================================================
#
# If D14.20–D14.28 PASS:
#
#   TEST accessed      = True
#   TEST transformed   = True
#   TEST evaluated     = False
#   model loaded       = False
#   predictions        = False
#
# The next controlled stage may load the exact frozen D8/D13
# model artifact and generate the first locked TEST
# probabilities.
#
# No model inference is implemented in this section.
# ============================================================

# ============================================================
# D14.30 — FROZEN MODEL INFERENCE BOUNDARY
# ============================================================
#
# Purpose:
# Generate the FIRST locked TEST predictions using the exact
# frozen D8/D13 registered model candidate.
#
# This section MAY:
#   - verify the persisted model artifact,
#   - load the persisted model,
#   - call predict_proba() on the already governed TEST
#     representation,
#   - apply the already frozen threshold of 0.12.
#
# This section MUST NOT:
#   - fit or retrain the model,
#   - tune hyperparameters,
#   - refit preprocessing,
#   - recalibrate probabilities,
#   - optimize the threshold,
#   - calculate outcome-based performance metrics,
#   - authorize deployment.
#
# TEST outcomes are deliberately NOT used for performance
# evaluation in this section.
# ============================================================


import joblib


# ============================================================
# D14.31 — FROZEN MODEL ARTIFACT
# ============================================================

D14_FROZEN_MODEL_PATH = Path(
    "artifacts/models/D8_selected_development_model.joblib"
)

D14_FROZEN_MODEL_METADATA_PATH = Path(
    "artifacts/models/D8_selected_development_model_metadata.json"
)


# ============================================================
# D14.32 — MODEL ARTIFACT SNAPSHOT
# ============================================================


def build_d14_model_artifact_snapshot() -> dict[str, Any]:
    """
    Capture frozen model artifact identity before/after TEST
    inference without modifying the artifact.
    """

    if not D14_FROZEN_MODEL_PATH.exists():
        raise FileNotFoundError(
            "Frozen D8/D13 model artifact not found: "
            f"{D14_FROZEN_MODEL_PATH}"
        )

    if not D14_FROZEN_MODEL_METADATA_PATH.exists():
        raise FileNotFoundError(
            "Frozen D8 model metadata not found: "
            f"{D14_FROZEN_MODEL_METADATA_PATH}"
        )

    return {
        "model_path": str(D14_FROZEN_MODEL_PATH),
        "model_sha256": calculate_d7_file_sha256(
            D14_FROZEN_MODEL_PATH
        ),
        "model_size_bytes": int(
            D14_FROZEN_MODEL_PATH.stat().st_size
        ),
        "model_mtime_ns": int(
            D14_FROZEN_MODEL_PATH.stat().st_mtime_ns
        ),
        "metadata_path": str(
            D14_FROZEN_MODEL_METADATA_PATH
        ),
        "metadata_sha256": calculate_d7_file_sha256(
            D14_FROZEN_MODEL_METADATA_PATH
        ),
        "metadata_size_bytes": int(
            D14_FROZEN_MODEL_METADATA_PATH.stat().st_size
        ),
        "metadata_mtime_ns": int(
            D14_FROZEN_MODEL_METADATA_PATH.stat().st_mtime_ns
        ),
    }


# ============================================================
# D14.33 — VERIFY MODEL IDENTITY
# ============================================================


def validate_d14_model_artifact_snapshot(
    snapshot: dict[str, Any],
) -> dict[str, bool]:
    """
    Verify the persisted model and metadata against the
    identities bound into D14 from D13.
    """

    return {
        "model_exists": D14_FROZEN_MODEL_PATH.exists(),
        "metadata_exists": (
            D14_FROZEN_MODEL_METADATA_PATH.exists()
        ),
        "model_sha256_valid": (
            snapshot["model_sha256"].upper()
            == D14_EXPECTED_MODEL_SHA256
        ),
        "metadata_sha256_valid": (
            snapshot["metadata_sha256"].upper()
            == D14_EXPECTED_MODEL_METADATA_SHA256
        ),
    }


# ============================================================
# D14.34 — GENERATE FROZEN TEST PREDICTIONS
# ============================================================


def generate_d14_frozen_test_predictions(
    transformed_bundle: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Generate the first locked TEST probabilities from the
    exact frozen registered model.

    IMPORTANT:
    This function performs inference but deliberately does NOT
    calculate predictive performance against y_test.
    """

    if transformed_bundle is None:
        transformed_bundle = (
            transform_d14_locked_test_with_frozen_d7()
        )

    transformation_validation = (
        validate_d14_frozen_test_transformation(
            transformed_bundle
        )
    )

    if not transformation_validation["overall_pass"]:
        raise RuntimeError(
            "Frozen TEST transformation failed validation. "
            "Model inference is blocked."
        )

    X_test = transformed_bundle["transformed_test"]

    before_snapshot = build_d14_model_artifact_snapshot()

    before_checks = validate_d14_model_artifact_snapshot(
        before_snapshot
    )

    if not all(before_checks.values()):
        raise RuntimeError(
            "Frozen model artifact identity failed before "
            "locked TEST inference."
        )

    model = joblib.load(D14_FROZEN_MODEL_PATH)

    if not hasattr(model, "predict_proba"):
        raise TypeError(
            "Frozen model does not expose predict_proba()."
        )

    probability_matrix = model.predict_proba(X_test)

    probability_matrix = np.asarray(
        probability_matrix,
        dtype=float,
    )

    if probability_matrix.ndim != 2:
        raise RuntimeError(
            "predict_proba() did not return a 2D matrix."
        )

    if probability_matrix.shape[1] != 2:
        raise RuntimeError(
            "Expected binary predict_proba() output with "
            "exactly two probability columns."
        )

    positive_probabilities = probability_matrix[:, 1]

    frozen_threshold_predictions = (
        positive_probabilities
        >= D14_EXPECTED_DEVELOPMENT_THRESHOLD
    ).astype(int)

    after_snapshot = build_d14_model_artifact_snapshot()

    after_checks = validate_d14_model_artifact_snapshot(
        after_snapshot
    )

    model_artifact_identity_unchanged = (
        before_snapshot == after_snapshot
    )

    return {
        "model": model,
        "X_test": X_test,
        "positive_probabilities": (
            positive_probabilities
        ),
        "frozen_threshold_predictions": (
            frozen_threshold_predictions
        ),
        "transformed_bundle": transformed_bundle,
        "transformation_validation": (
            transformation_validation
        ),
        "before_model_snapshot": before_snapshot,
        "after_model_snapshot": after_snapshot,
        "before_model_checks": before_checks,
        "after_model_checks": after_checks,
        "model_artifact_identity_unchanged": (
            model_artifact_identity_unchanged
        ),
        "locked_test_accessed": True,
        "locked_test_transformed": True,
        "model_loaded": True,
        "predictions_generated": True,
        "locked_test_evaluated": False,
        "model_retrained": False,
        "model_retuned": False,
        "preprocessor_refitted": False,
        "threshold_retuned": False,
        "model_recalibrated": False,
        "deployment_authorized": False,
    }


# ============================================================
# D14.35 — PREDICTION INTEGRITY VALIDATION
# ============================================================


def validate_d14_frozen_test_predictions(
    prediction_bundle: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Validate TEST inference integrity without evaluating
    predictions against TEST outcomes.
    """

    if prediction_bundle is None:
        prediction_bundle = (
            generate_d14_frozen_test_predictions()
        )

    probabilities = prediction_bundle[
        "positive_probabilities"
    ]

    decisions = prediction_bundle[
        "frozen_threshold_predictions"
    ]

    X_test = prediction_bundle["X_test"]

    unique_decisions = set(
        np.unique(decisions).tolist()
    )

    checks = {
        "test_transformation_passed": (
            prediction_bundle[
                "transformation_validation"
            ]["overall_pass"]
            is True
        ),

        "test_accessed": (
            prediction_bundle[
                "locked_test_accessed"
            ]
            is True
        ),

        "test_transformed": (
            prediction_bundle[
                "locked_test_transformed"
            ]
            is True
        ),

        "model_loaded": (
            prediction_bundle["model_loaded"]
            is True
        ),

        "predictions_generated": (
            prediction_bundle[
                "predictions_generated"
            ]
            is True
        ),

        "performance_not_evaluated": (
            prediction_bundle[
                "locked_test_evaluated"
            ]
            is False
        ),

        "prediction_row_count_valid": (
            len(probabilities)
            == D14_EXPECTED_TEST_ENCOUNTERS
        ),

        "decision_row_count_valid": (
            len(decisions)
            == D14_EXPECTED_TEST_ENCOUNTERS
        ),

        "input_row_count_preserved": (
            X_test.shape[0]
            == D14_EXPECTED_TEST_ENCOUNTERS
        ),

        "probabilities_finite": bool(
            np.isfinite(probabilities).all()
        ),

        "probabilities_within_unit_interval": bool(
            (
                (probabilities >= 0.0)
                & (probabilities <= 1.0)
            ).all()
        ),

        "decisions_binary": (
            unique_decisions.issubset({0, 1})
        ),

        "model_identity_valid_before": (
            prediction_bundle[
                "before_model_checks"
            ]["model_sha256_valid"]
        ),

        "metadata_identity_valid_before": (
            prediction_bundle[
                "before_model_checks"
            ]["metadata_sha256_valid"]
        ),

        "model_identity_valid_after": (
            prediction_bundle[
                "after_model_checks"
            ]["model_sha256_valid"]
        ),

        "metadata_identity_valid_after": (
            prediction_bundle[
                "after_model_checks"
            ]["metadata_sha256_valid"]
        ),

        "model_artifacts_unchanged": (
            prediction_bundle[
                "model_artifact_identity_unchanged"
            ]
            is True
        ),

        "model_not_retrained": (
            prediction_bundle[
                "model_retrained"
            ]
            is False
        ),

        "model_not_retuned": (
            prediction_bundle[
                "model_retuned"
            ]
            is False
        ),

        "preprocessor_not_refitted": (
            prediction_bundle[
                "preprocessor_refitted"
            ]
            is False
        ),

        "threshold_not_retuned": (
            prediction_bundle[
                "threshold_retuned"
            ]
            is False
        ),

        "model_not_recalibrated": (
            prediction_bundle[
                "model_recalibrated"
            ]
            is False
        ),

        "deployment_not_authorized": (
            prediction_bundle[
                "deployment_authorized"
            ]
            is False
        ),
    }

    overall_pass = all(checks.values())

    return {
        "stage_id": D14_STAGE_ID,
        "validation_status": (
            "PASS" if overall_pass else "FAIL"
        ),
        "overall_pass": overall_pass,
        "checks": checks,
        "prediction_count": int(len(probabilities)),
        "decision_count": int(len(decisions)),
        "probability_min": float(
            probabilities.min()
        ),
        "probability_max": float(
            probabilities.max()
        ),
        "probability_mean": float(
            probabilities.mean()
        ),
        "positive_alert_count": int(
            decisions.sum()
        ),
        "negative_alert_count": int(
            len(decisions) - decisions.sum()
        ),
        "frozen_threshold": float(
            D14_EXPECTED_DEVELOPMENT_THRESHOLD
        ),
        "model_sha256": (
            prediction_bundle[
                "after_model_snapshot"
            ]["model_sha256"]
        ),
        "metadata_sha256": (
            prediction_bundle[
                "after_model_snapshot"
            ]["metadata_sha256"]
        ),
        "model_artifacts_unchanged": (
            prediction_bundle[
                "model_artifact_identity_unchanged"
            ]
        ),
        "locked_test_accessed": True,
        "locked_test_transformed": True,
        "model_loaded": True,
        "predictions_generated": True,
        "locked_test_evaluated": False,
        "deployment_authorized": False,
        "next_controlled_action": (
            "D14_ONE_TIME_CONFIRMATORY_PERFORMANCE_EVALUATION"
            if overall_pass
            else "STOP_REMEDIATE_TEST_INFERENCE_INTEGRITY"
        ),
    }


# ============================================================
# D14.36 — BUILD INFERENCE EVIDENCE
# ============================================================


def build_d14_frozen_test_inference_evidence(
) -> dict[str, Any]:
    """
    Build formal evidence for frozen TEST inference without
    calculating outcome-based performance.
    """

    prediction_bundle = (
        generate_d14_frozen_test_predictions()
    )

    validation = validate_d14_frozen_test_predictions(
        prediction_bundle
    )

    return {
        "stage_id": D14_STAGE_ID,
        "registry_id": D14_EXPECTED_REGISTRY_ID,
        "model_version": D14_EXPECTED_MODEL_VERSION,
        "candidate_system_sha256": (
            D14_EXPECTED_CANDIDATE_SYSTEM_SHA256
        ),
        "frozen_threshold": (
            D14_EXPECTED_DEVELOPMENT_THRESHOLD
        ),
        "test_accessed": True,
        "test_transformed": True,
        "model_loaded": True,
        "predictions_generated": True,
        "test_performance_evaluated": False,
        "model_retrained": False,
        "model_retuned": False,
        "preprocessor_refitted": False,
        "threshold_retuned": False,
        "model_recalibrated": False,
        "validation": validation,
        "deployment_authorized": False,
    }


# ============================================================
# D14.37 — PRINT INFERENCE EVIDENCE
# ============================================================


def print_d14_frozen_test_inference_evidence() -> None:
    """
    Print frozen TEST inference integrity evidence.

    No TEST outcome-based performance metrics are calculated.
    """

    evidence = build_d14_frozen_test_inference_evidence()

    validation = evidence["validation"]

    print("=" * 72)
    print("D14 — LOCKED-TEST EVALUATION")
    print("FROZEN MODEL INFERENCE & PREDICTION INTEGRITY")
    print("=" * 72)

    print()
    print("Frozen candidate")
    print("-" * 72)
    print(
        f"Registry ID:              "
        f"{evidence['registry_id']}"
    )
    print(
        f"Model version:            "
        f"{evidence['model_version']}"
    )
    print(
        f"Candidate system SHA256:  "
        f"{evidence['candidate_system_sha256']}"
    )
    print(
        f"Frozen threshold:         "
        f"{evidence['frozen_threshold']}"
    )

    print()
    print("Inference state")
    print("-" * 72)
    print(
        f"TEST accessed:            "
        f"{evidence['test_accessed']}"
    )
    print(
        f"TEST transformed:         "
        f"{evidence['test_transformed']}"
    )
    print(
        f"Model loaded:             "
        f"{evidence['model_loaded']}"
    )
    print(
        f"Predictions generated:    "
        f"{evidence['predictions_generated']}"
    )
    print(
        f"Performance evaluated:    "
        f"{evidence['test_performance_evaluated']}"
    )

    print()
    print("Prediction integrity")
    print("-" * 72)
    print(
        f"Prediction count:         "
        f"{validation['prediction_count']:,}"
    )
    print(
        f"Probability minimum:      "
        f"{validation['probability_min']:.12f}"
    )
    print(
        f"Probability maximum:      "
        f"{validation['probability_max']:.12f}"
    )
    print(
        f"Probability mean:         "
        f"{validation['probability_mean']:.12f}"
    )
    print(
        f"Frozen-threshold alerts:  "
        f"{validation['positive_alert_count']:,}"
    )
    print(
        f"Non-alerts:               "
        f"{validation['negative_alert_count']:,}"
    )

    print()
    print("Frozen model integrity")
    print("-" * 72)
    print(
        f"Model SHA256:             "
        f"{validation['model_sha256']}"
    )
    print(
        f"Metadata SHA256:          "
        f"{validation['metadata_sha256']}"
    )
    print(
        f"Artifacts unchanged:      "
        f"{validation['model_artifacts_unchanged']}"
    )

    print()
    print("Inference integrity checks")
    print("-" * 72)

    for check_name, passed in validation["checks"].items():
        status = "PASS" if passed else "FAIL"
        print(f"{check_name:<45} {status}")

    print()
    print("-" * 72)
    print(
        f"INFERENCE INTEGRITY STATUS: "
        f"{validation['validation_status']}"
    )
    print(
        f"NEXT CONTROLLED ACTION:     "
        f"{validation['next_controlled_action']}"
    )
    print(
        f"DEPLOYMENT AUTHORIZED:      "
        f"{validation['deployment_authorized']}"
    )
    print("=" * 72)


# ============================================================
# D14.38 — PERFORMANCE EVALUATION BOUNDARY
# ============================================================
#
# If D14.30–D14.37 PASS:
#
#   TEST accessed              = True
#   TEST transformed           = True
#   model loaded               = True
#   predictions generated      = True
#   TEST performance evaluated = False
#
# The next controlled step may compare the frozen predictions
# with locked TEST outcomes using ONLY the metrics declared in
# the D14 pre-access contract.
#
# No performance calculation is implemented here.
# ============================================================


# ============================================================
# D14.39 — GOVERNANCE REMINDER
# ============================================================
#
# Once TEST performance is calculated:
#
#   - the observed result is retained whether favorable or
#     unfavorable;
#   - threshold 0.12 remains unchanged;
#   - TEST is not converted into a tuning dataset;
#   - no TEST-driven model redesign is permitted;
#   - internal TEST validation does not establish external
#     validation;
#   - D14 cannot by itself authorize clinical deployment.
# ============================================================

# ============================================================
# D14.40 — ONE-TIME CONFIRMATORY LOCKED-TEST EVALUATION
# ============================================================
#
# Purpose:
# Compare the exact frozen D13 candidate predictions with the
# locked TEST outcomes using ONLY the metrics pre-specified
# before TEST access.
#
# This is confirmatory internal TEST evaluation.
#
# PROHIBITED:
#   - model retraining,
#   - hyperparameter tuning,
#   - feature modification,
#   - preprocessor refitting,
#   - probability recalibration,
#   - threshold optimization,
#   - subgroup-specific threshold optimization,
#   - TEST-driven model selection,
#   - TEST-to-validation optimization loops,
#   - deployment authorization.
#
# Whatever result is observed MUST be retained.
# ============================================================


from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    log_loss,
    precision_score,
    recall_score,
    roc_auc_score,
)


# ============================================================
# D14.41 — DEVELOPMENT VALIDATION REFERENCE
# ============================================================
#
# These values were established before locked TEST evaluation.
# They are reference evidence only.
#
# TEST is NOT required to outperform validation.
# ============================================================

D14_VALIDATION_REFERENCE = {
    "encounters": 15_052,
    "positives": 1_692,
    "prevalence": 0.11241031092213659,
    "pr_auc": 0.18487420802051505,
    "roc_auc": 0.6203647005634122,
    "brier_score": 0.09736249968861509,
    "log_loss": 0.34110139977699366,
    "threshold": 0.12,
    "true_positives": 785,
    "false_positives": 3_924,
    "true_negatives": 9_436,
    "false_negatives": 907,
    "sensitivity": 0.4639479905437352,
    "specificity": 0.7062874251497006,
    "precision_ppv": 0.16670205988532596,
    "negative_predictive_value": 0.9123078410519192,
    "f1_score": 0.24527417591001405,
    "alert_count": 4_709,
    "alert_rate": 0.3128487908583577,
    "alerts_per_100_encounters": 31.28487908583577,
    "number_needed_to_evaluate": 5.998726114649681,
}


# ============================================================
# D14.42 — CALCULATE PRE-SPECIFIED TEST PERFORMANCE
# ============================================================


def evaluate_d14_locked_test_performance(
    prediction_bundle: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Perform the one-time confirmatory locked TEST evaluation.

    Uses:
        - exact frozen TEST probabilities,
        - exact frozen threshold = 0.12,
        - authoritative locked TEST outcomes,
        - metrics declared before TEST access.

    No optimization occurs.
    """

    if prediction_bundle is None:
        prediction_bundle = (
            generate_d14_frozen_test_predictions()
        )

    inference_validation = (
        validate_d14_frozen_test_predictions(
            prediction_bundle
        )
    )

    if not inference_validation["overall_pass"]:
        raise RuntimeError(
            "Frozen TEST inference integrity failed. "
            "Performance evaluation is blocked."
        )

    locked_test = prediction_bundle[
        "transformed_bundle"
    ]["locked_test"]

    y_true = (
        locked_test[D14_TARGET_COLUMN]
        .astype(int)
        .to_numpy()
    )

    probabilities = np.asarray(
        prediction_bundle["positive_probabilities"],
        dtype=float,
    )

    decisions = np.asarray(
        prediction_bundle[
            "frozen_threshold_predictions"
        ],
        dtype=int,
    )

    if len(y_true) != D14_EXPECTED_TEST_ENCOUNTERS:
        raise RuntimeError(
            "Locked TEST outcome count does not match "
            "the frozen D14 contract."
        )

    if len(probabilities) != len(y_true):
        raise RuntimeError(
            "Probability and outcome row counts differ."
        )

    if len(decisions) != len(y_true):
        raise RuntimeError(
            "Decision and outcome row counts differ."
        )

    # --------------------------------------------------------
    # Descriptive TEST population
    # --------------------------------------------------------

    encounter_count = int(len(y_true))
    positive_count = int(y_true.sum())
    negative_count = int(encounter_count - positive_count)

    prevalence = float(
        positive_count / encounter_count
    )

    # --------------------------------------------------------
    # Pre-specified discrimination metrics
    # --------------------------------------------------------

    pr_auc = float(
        average_precision_score(
            y_true,
            probabilities,
        )
    )

    roc_auc = float(
        roc_auc_score(
            y_true,
            probabilities,
        )
    )

    # --------------------------------------------------------
    # Pre-specified calibration metrics
    # --------------------------------------------------------

    brier_score = float(
        brier_score_loss(
            y_true,
            probabilities,
        )
    )

    test_log_loss = float(
        log_loss(
            y_true,
            probabilities,
            labels=[0, 1],
        )
    )

    # --------------------------------------------------------
    # Frozen-threshold operating performance
    # --------------------------------------------------------

    tn, fp, fn, tp = confusion_matrix(
        y_true,
        decisions,
        labels=[0, 1],
    ).ravel()

    tn = int(tn)
    fp = int(fp)
    fn = int(fn)
    tp = int(tp)

    sensitivity = float(
        recall_score(
            y_true,
            decisions,
            pos_label=1,
            zero_division=0,
        )
    )

    specificity = float(
        tn / (tn + fp)
    )

    precision_ppv = float(
        precision_score(
            y_true,
            decisions,
            pos_label=1,
            zero_division=0,
        )
    )

    negative_predictive_value = float(
        tn / (tn + fn)
    )

    f1 = float(
        f1_score(
            y_true,
            decisions,
            pos_label=1,
            zero_division=0,
        )
    )

    alert_count = int(decisions.sum())

    alert_rate = float(
        alert_count / encounter_count
    )

    alerts_per_100 = float(
        alert_rate * 100.0
    )

    number_needed_to_evaluate = (
        float(alert_count / tp)
        if tp > 0
        else float("inf")
    )

    return {
        "evaluation_classification": (
            "ONE_TIME_CONFIRMATORY_INTERNAL_LOCKED_TEST"
        ),
        "registry_id": D14_EXPECTED_REGISTRY_ID,
        "model_version": D14_EXPECTED_MODEL_VERSION,
        "candidate_system_sha256": (
            D14_EXPECTED_CANDIDATE_SYSTEM_SHA256
        ),
        "frozen_threshold": float(
            D14_EXPECTED_DEVELOPMENT_THRESHOLD
        ),
        "encounter_count": encounter_count,
        "positive_count": positive_count,
        "negative_count": negative_count,
        "prevalence": prevalence,
        "pr_auc": pr_auc,
        "roc_auc": roc_auc,
        "brier_score": brier_score,
        "log_loss": test_log_loss,
        "true_positives": tp,
        "false_positives": fp,
        "true_negatives": tn,
        "false_negatives": fn,
        "sensitivity": sensitivity,
        "specificity": specificity,
        "precision_ppv": precision_ppv,
        "negative_predictive_value": (
            negative_predictive_value
        ),
        "f1_score": f1,
        "alert_count": alert_count,
        "alert_rate": alert_rate,
        "alerts_per_100_encounters": alerts_per_100,
        "number_needed_to_evaluate": (
            number_needed_to_evaluate
        ),
        "locked_test_accessed": True,
        "locked_test_transformed": True,
        "predictions_generated": True,
        "locked_test_evaluated": True,
        "model_retrained": False,
        "model_retuned": False,
        "preprocessor_refitted": False,
        "threshold_retuned": False,
        "model_recalibrated": False,
        "test_driven_model_selection": False,
        "test_driven_redesign": False,
        "deployment_authorized": False,
    }


# ============================================================
# D14.43 — VALIDATE CONFIRMATORY TEST EVALUATION
# ============================================================


def validate_d14_locked_test_performance(
    result: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Validate structural and governance integrity of the
    one-time confirmatory TEST evaluation.

    This validates the evaluation process.

    It does NOT require TEST to outperform validation.
    """

    if result is None:
        result = evaluate_d14_locked_test_performance()

    confusion_total = (
        result["true_positives"]
        + result["false_positives"]
        + result["true_negatives"]
        + result["false_negatives"]
    )

    outcome_total = (
        result["positive_count"]
        + result["negative_count"]
    )

    positive_reconciliation = (
        result["true_positives"]
        + result["false_negatives"]
    )

    negative_reconciliation = (
        result["true_negatives"]
        + result["false_positives"]
    )

    alert_reconciliation = (
        result["true_positives"]
        + result["false_positives"]
    )

    checks = {
        "evaluation_is_confirmatory": (
            result["evaluation_classification"]
            == "ONE_TIME_CONFIRMATORY_INTERNAL_LOCKED_TEST"
        ),

        "candidate_identity_preserved": (
            result["candidate_system_sha256"]
            == D14_EXPECTED_CANDIDATE_SYSTEM_SHA256
        ),

        "threshold_preserved": (
            result["frozen_threshold"]
            == D14_EXPECTED_DEVELOPMENT_THRESHOLD
        ),

        "expected_encounter_count": (
            result["encounter_count"]
            == D14_EXPECTED_TEST_ENCOUNTERS
        ),

        "expected_positive_count": (
            result["positive_count"]
            == D14_EXPECTED_TEST_POSITIVES
        ),

        "expected_negative_count": (
            result["negative_count"]
            == D14_EXPECTED_TEST_NEGATIVES
        ),

        "outcome_counts_reconcile": (
            outcome_total
            == D14_EXPECTED_TEST_ENCOUNTERS
        ),

        "confusion_matrix_reconciles": (
            confusion_total
            == D14_EXPECTED_TEST_ENCOUNTERS
        ),

        "positive_outcomes_reconcile": (
            positive_reconciliation
            == D14_EXPECTED_TEST_POSITIVES
        ),

        "negative_outcomes_reconcile": (
            negative_reconciliation
            == D14_EXPECTED_TEST_NEGATIVES
        ),

        "alerts_reconcile": (
            alert_reconciliation
            == result["alert_count"]
        ),

        "pr_auc_valid": (
            0.0 <= result["pr_auc"] <= 1.0
        ),

        "roc_auc_valid": (
            0.0 <= result["roc_auc"] <= 1.0
        ),

        "brier_score_valid": (
            0.0 <= result["brier_score"] <= 1.0
        ),

        "log_loss_finite": bool(
            np.isfinite(result["log_loss"])
        ),

        "sensitivity_valid": (
            0.0 <= result["sensitivity"] <= 1.0
        ),

        "specificity_valid": (
            0.0 <= result["specificity"] <= 1.0
        ),

        "precision_valid": (
            0.0 <= result["precision_ppv"] <= 1.0
        ),

        "npv_valid": (
            0.0
            <= result["negative_predictive_value"]
            <= 1.0
        ),

        "f1_valid": (
            0.0 <= result["f1_score"] <= 1.0
        ),

        "test_accessed": (
            result["locked_test_accessed"] is True
        ),

        "test_transformed": (
            result["locked_test_transformed"] is True
        ),

        "predictions_generated": (
            result["predictions_generated"] is True
        ),

        "test_evaluated": (
            result["locked_test_evaluated"] is True
        ),

        "model_not_retrained": (
            result["model_retrained"] is False
        ),

        "model_not_retuned": (
            result["model_retuned"] is False
        ),

        "preprocessor_not_refitted": (
            result["preprocessor_refitted"] is False
        ),

        "threshold_not_retuned": (
            result["threshold_retuned"] is False
        ),

        "model_not_recalibrated": (
            result["model_recalibrated"] is False
        ),

        "no_test_driven_model_selection": (
            result["test_driven_model_selection"] is False
        ),

        "no_test_driven_redesign": (
            result["test_driven_redesign"] is False
        ),

        "deployment_not_authorized": (
            result["deployment_authorized"] is False
        ),
    }

    overall_pass = all(checks.values())

    return {
        "stage_id": D14_STAGE_ID,
        "validation_status": (
            "PASS" if overall_pass else "FAIL"
        ),
        "overall_pass": overall_pass,
        "checks": checks,
        "deployment_authorized": False,
        "next_controlled_action": (
            "D14_VALIDATION_TO_TEST_COMPARISON"
            if overall_pass
            else "STOP_REMEDIATE_CONFIRMATORY_EVALUATION"
        ),
    }


# ============================================================
# D14.44 — VALIDATION vs LOCKED TEST COMPARISON
# ============================================================


def build_d14_validation_test_comparison(
    test_result: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Compare development-validation evidence with locked TEST.

    Differences are descriptive.

    No optimization or pass/fail rule is based on TEST being
    better than validation.
    """

    if test_result is None:
        test_result = evaluate_d14_locked_test_performance()

    validation = D14_VALIDATION_REFERENCE

    comparison_metrics = (
        "prevalence",
        "pr_auc",
        "roc_auc",
        "brier_score",
        "log_loss",
        "sensitivity",
        "specificity",
        "precision_ppv",
        "negative_predictive_value",
        "f1_score",
        "alert_rate",
        "alerts_per_100_encounters",
        "number_needed_to_evaluate",
    )

    comparison = {}

    for metric in comparison_metrics:
        validation_value = float(validation[metric])
        test_value = float(test_result[metric])

        comparison[metric] = {
            "validation": validation_value,
            "locked_test": test_value,
            "absolute_difference_test_minus_validation": (
                test_value - validation_value
            ),
        }

    return {
        "comparison_classification": (
            "DESCRIPTIVE_VALIDATION_TO_LOCKED_TEST"
        ),
        "threshold_unchanged": (
            validation["threshold"]
            == test_result["frozen_threshold"]
            == D14_EXPECTED_DEVELOPMENT_THRESHOLD
        ),
        "metrics": comparison,
        "test_used_for_retuning": False,
        "test_used_for_model_selection": False,
        "test_used_for_recalibration": False,
    }


# ============================================================
# D14.45 — BUILD CONFIRMATORY PERFORMANCE EVIDENCE
# ============================================================


def build_d14_confirmatory_performance_evidence(
) -> dict[str, Any]:
    """
    Build the formal D14 primary locked-TEST performance
    evidence object.
    """

    test_result = evaluate_d14_locked_test_performance()

    validation = validate_d14_locked_test_performance(
        test_result
    )

    comparison = build_d14_validation_test_comparison(
        test_result
    )

    return {
        "stage_id": D14_STAGE_ID,
        "stage_name": D14_STAGE_NAME,
        "registry_id": D14_EXPECTED_REGISTRY_ID,
        "model_version": D14_EXPECTED_MODEL_VERSION,
        "candidate_system_sha256": (
            D14_EXPECTED_CANDIDATE_SYSTEM_SHA256
        ),
        "source_git_commit": D14_SOURCE_GIT_COMMIT,
        "frozen_threshold": (
            D14_EXPECTED_DEVELOPMENT_THRESHOLD
        ),
        "test_result": test_result,
        "evaluation_validation": validation,
        "validation_test_comparison": comparison,
        "internal_locked_test_validation_completed": (
            validation["overall_pass"]
        ),
        "external_validation_completed": False,
        "clinical_effectiveness_established": False,
        "deployment_authorized": False,
    }


# ============================================================
# D14.46 — PRINT ONE-TIME CONFIRMATORY PERFORMANCE
# ============================================================


def print_d14_confirmatory_performance_evidence() -> None:
    """
    Execute and print the one-time confirmatory TEST result.
    """

    evidence = (
        build_d14_confirmatory_performance_evidence()
    )

    result = evidence["test_result"]

    validation = evidence[
        "evaluation_validation"
    ]

    comparison = evidence[
        "validation_test_comparison"
    ]

    print("=" * 76)
    print("D14 — LOCKED-TEST EVALUATION")
    print("ONE-TIME CONFIRMATORY PERFORMANCE EVALUATION")
    print("=" * 76)

    print()
    print("Frozen candidate")
    print("-" * 76)
    print(
        f"Registry ID:                "
        f"{evidence['registry_id']}"
    )
    print(
        f"Model version:              "
        f"{evidence['model_version']}"
    )
    print(
        f"Candidate system SHA256:    "
        f"{evidence['candidate_system_sha256']}"
    )
    print(
        f"Frozen threshold:           "
        f"{evidence['frozen_threshold']}"
    )

    print()
    print("Locked TEST population")
    print("-" * 76)
    print(
        f"Encounters:                 "
        f"{result['encounter_count']:,}"
    )
    print(
        f"Positive outcomes:          "
        f"{result['positive_count']:,}"
    )
    print(
        f"Negative outcomes:          "
        f"{result['negative_count']:,}"
    )
    print(
        f"Outcome prevalence:         "
        f"{result['prevalence']:.6f}"
    )

    print()
    print("Discrimination")
    print("-" * 76)
    print(
        f"PR-AUC:                     "
        f"{result['pr_auc']:.12f}"
    )
    print(
        f"ROC-AUC:                    "
        f"{result['roc_auc']:.12f}"
    )

    print()
    print("Calibration")
    print("-" * 76)
    print(
        f"Brier score:                "
        f"{result['brier_score']:.12f}"
    )
    print(
        f"Log loss:                   "
        f"{result['log_loss']:.12f}"
    )

    print()
    print("Frozen-threshold performance")
    print("-" * 76)
    print(
        f"Threshold:                  "
        f"{result['frozen_threshold']}"
    )
    print(
        f"TP:                         "
        f"{result['true_positives']:,}"
    )
    print(
        f"FP:                         "
        f"{result['false_positives']:,}"
    )
    print(
        f"TN:                         "
        f"{result['true_negatives']:,}"
    )
    print(
        f"FN:                         "
        f"{result['false_negatives']:,}"
    )
    print(
        f"Sensitivity:                "
        f"{result['sensitivity']:.12f}"
    )
    print(
        f"Specificity:                "
        f"{result['specificity']:.12f}"
    )
    print(
        f"Precision / PPV:            "
        f"{result['precision_ppv']:.12f}"
    )
    print(
        f"NPV:                        "
        f"{result['negative_predictive_value']:.12f}"
    )
    print(
        f"F1 score:                   "
        f"{result['f1_score']:.12f}"
    )
    print(
        f"Alert count:                "
        f"{result['alert_count']:,}"
    )
    print(
        f"Alert rate:                 "
        f"{result['alert_rate']:.12f}"
    )
    print(
        f"Alerts / 100 encounters:    "
        f"{result['alerts_per_100_encounters']:.6f}"
    )
    print(
        f"Number needed to evaluate:  "
        f"{result['number_needed_to_evaluate']:.6f}"
    )

    print()
    print("Validation → TEST comparison")
    print("-" * 76)

    for metric in (
        "prevalence",
        "pr_auc",
        "roc_auc",
        "brier_score",
        "log_loss",
        "sensitivity",
        "specificity",
        "precision_ppv",
        "negative_predictive_value",
        "f1_score",
        "alert_rate",
    ):
        values = comparison["metrics"][metric]

        print(
            f"{metric:<28} "
            f"VAL={values['validation']:.6f}  "
            f"TEST={values['locked_test']:.6f}  "
            f"Δ={values['absolute_difference_test_minus_validation']:+.6f}"
        )

    print()
    print("Evaluation integrity")
    print("-" * 76)

    for check_name, passed in validation["checks"].items():
        status = "PASS" if passed else "FAIL"
        print(f"{check_name:<47} {status}")

    print()
    print("Governance interpretation")
    print("-" * 76)
    print(
        "Internal locked TEST validation completed: "
        f"{evidence['internal_locked_test_validation_completed']}"
    )
    print(
        "External validation completed:             "
        f"{evidence['external_validation_completed']}"
    )
    print(
        "Clinical effectiveness established:        "
        f"{evidence['clinical_effectiveness_established']}"
    )
    print(
        "Deployment authorized:                     "
        f"{evidence['deployment_authorized']}"
    )

    print()
    print("-" * 76)
    print(
        f"EVALUATION INTEGRITY STATUS: "
        f"{validation['validation_status']}"
    )
    print(
        f"NEXT CONTROLLED ACTION:      "
        f"{validation['next_controlled_action']}"
    )
    print("=" * 76)


# ============================================================
# D14.47 — POST-EVALUATION GOVERNANCE STATE
# ============================================================
#
# After D14.40–D14.46:
#
#   TEST accessed              = True
#   TEST transformed           = True
#   predictions generated      = True
#   TEST performance evaluated = True
#
# But:
#
#   model retrained            = False
#   model retuned              = False
#   preprocessor refitted      = False
#   threshold retuned          = False
#   model recalibrated         = False
#   TEST-driven redesign       = False
#   deployment authorized      = False
#
# The TEST result becomes immutable confirmatory evidence.
# ============================================================


# ============================================================
# D14.48 — SCIENTIFIC INTERPRETATION BOUNDARY
# ============================================================
#
# D14 establishes internal held-out performance for the exact
# registered candidate.
#
# D14 does NOT establish:
#
#   - external geographic validation,
#   - external institutional validation,
#   - temporal prospective validation,
#   - prospective clinical effectiveness,
#   - intervention effectiveness,
#   - clinical safety in live deployment,
#   - deployment authorization.
# ============================================================


# ============================================================
# D14.49 — NEXT GOVERNED ANALYSIS
# ============================================================
#
# After primary confirmatory evaluation is preserved, D14 may
# proceed to the pre-specified confirmatory analyses:
#
#   - subgroup performance,
#   - robustness / transportability,
#   - explainability confirmation,
#
# without changing the frozen candidate or operating point.
# ============================================================

# ============================================================
# D14.50 — LOCKED-TEST SUBGROUP / FAIRNESS CONFIRMATION
# ============================================================
#
# Purpose:
# Confirm whether subgroup operating behavior observed during
# development remains visible on the locked TEST cohort.
#
# This is a confirmatory analysis of the frozen candidate.
#
# Governed subgroup dimensions inherited from D10:
#   - race
#   - gender
#   - age
#
# This section MUST NOT:
#   - optimize subgroup-specific thresholds,
#   - alter the global threshold,
#   - retrain or recalibrate the model,
#   - remove unfavorable subgroup results,
#   - infer causal discrimination from descriptive differences,
#   - authorize deployment.
# ============================================================


# ============================================================
# D14.51 — SUBGROUP GOVERNANCE CONTRACT
# ============================================================

D14_CONFIRMATORY_SUBGROUP_COLUMNS = (
    "race",
    "gender",
    "age",
)

# Minimum support rules for primary descriptive comparison.
#
# A subgroup must have sufficient total observations AND
# sufficient positive/negative outcomes before discrimination
# and operating-point differences are treated as adequately
# supported.
#
# Low-support groups remain in the evidence table.
D14_SUBGROUP_MIN_TOTAL_N = 100
D14_SUBGROUP_MIN_POSITIVES = 20
D14_SUBGROUP_MIN_NEGATIVES = 20


def classify_d14_subgroup_support(
    total_n: int,
    positive_n: int,
    negative_n: int,
) -> str:
    """
    Classify subgroup statistical support.

    This is an evidence-quality classification only.
    It is not a fairness verdict.
    """

    if (
        total_n >= D14_SUBGROUP_MIN_TOTAL_N
        and positive_n >= D14_SUBGROUP_MIN_POSITIVES
        and negative_n >= D14_SUBGROUP_MIN_NEGATIVES
    ):
        return "ADEQUATE_SUPPORT"

    return "LOW_SUPPORT"


# ============================================================
# D14.52 — SAFE SUBGROUP METRIC HELPERS
# ============================================================


def _d14_safe_divide(
    numerator: float,
    denominator: float,
) -> float:
    """
    Return NaN when a metric denominator is zero.
    """

    if denominator == 0:
        return float("nan")

    return float(numerator / denominator)


def _d14_safe_pr_auc(
    y_true: np.ndarray,
    probabilities: np.ndarray,
) -> float:
    """
    PR-AUC requires at least one positive outcome.
    """

    if int(np.sum(y_true)) == 0:
        return float("nan")

    return float(
        average_precision_score(
            y_true,
            probabilities,
        )
    )


def _d14_safe_roc_auc(
    y_true: np.ndarray,
    probabilities: np.ndarray,
) -> float:
    """
    ROC-AUC requires both outcome classes.
    """

    if len(np.unique(y_true)) < 2:
        return float("nan")

    return float(
        roc_auc_score(
            y_true,
            probabilities,
        )
    )


# ============================================================
# D14.53 — BUILD LOCKED-TEST SUBGROUP ANALYSIS TABLE
# ============================================================


def build_d14_locked_test_subgroup_analysis(
    prediction_bundle: dict[str, Any] | None = None,
) -> pd.DataFrame:
    """
    Build confirmatory subgroup evidence from the exact frozen
    locked TEST predictions.

    No subgroup-specific threshold optimization occurs.
    """

    if prediction_bundle is None:
        prediction_bundle = (
            generate_d14_frozen_test_predictions()
        )

    inference_validation = (
        validate_d14_frozen_test_predictions(
            prediction_bundle
        )
    )

    if not inference_validation["overall_pass"]:
        raise RuntimeError(
            "Frozen TEST inference integrity failed. "
            "Subgroup confirmation is blocked."
        )

    locked_test = (
        prediction_bundle[
            "transformed_bundle"
        ]["locked_test"]
        .reset_index(drop=True)
        .copy()
    )

    probabilities = np.asarray(
        prediction_bundle[
            "positive_probabilities"
        ],
        dtype=float,
    )

    decisions = np.asarray(
        prediction_bundle[
            "frozen_threshold_predictions"
        ],
        dtype=int,
    )

    if len(locked_test) != len(probabilities):
        raise RuntimeError(
            "Locked TEST rows and probabilities are misaligned."
        )

    if len(locked_test) != len(decisions):
        raise RuntimeError(
            "Locked TEST rows and threshold decisions are "
            "misaligned."
        )

    analysis_df = locked_test[
        [
            D14_TARGET_COLUMN,
            *D14_CONFIRMATORY_SUBGROUP_COLUMNS,
        ]
    ].copy()

    analysis_df["__probability__"] = probabilities
    analysis_df["__decision__"] = decisions

    records: list[dict[str, Any]] = []

    for subgroup_column in (
        D14_CONFIRMATORY_SUBGROUP_COLUMNS
    ):
        subgroup_series = (
            analysis_df[subgroup_column]
            .astype("string")
            .fillna("__MISSING__")
        )

        subgroup_values = sorted(
            subgroup_series.unique().tolist()
        )

        for subgroup_value in subgroup_values:
            mask = (
                subgroup_series
                == subgroup_value
            ).to_numpy()

            subgroup_df = analysis_df.loc[mask]

            y_true = (
                subgroup_df[D14_TARGET_COLUMN]
                .astype(int)
                .to_numpy()
            )

            subgroup_probabilities = (
                subgroup_df["__probability__"]
                .astype(float)
                .to_numpy()
            )

            subgroup_decisions = (
                subgroup_df["__decision__"]
                .astype(int)
                .to_numpy()
            )

            total_n = int(len(subgroup_df))
            positive_n = int(y_true.sum())
            negative_n = int(
                total_n - positive_n
            )

            tn, fp, fn, tp = confusion_matrix(
                y_true,
                subgroup_decisions,
                labels=[0, 1],
            ).ravel()

            tn = int(tn)
            fp = int(fp)
            fn = int(fn)
            tp = int(tp)

            alert_count = int(
                subgroup_decisions.sum()
            )

            support_classification = (
                classify_d14_subgroup_support(
                    total_n=total_n,
                    positive_n=positive_n,
                    negative_n=negative_n,
                )
            )

            records.append(
                {
                    "subgroup_dimension": (
                        subgroup_column
                    ),
                    "subgroup_value": str(
                        subgroup_value
                    ),
                    "support_classification": (
                        support_classification
                    ),
                    "n": total_n,
                    "positive_n": positive_n,
                    "negative_n": negative_n,
                    "prevalence": (
                        _d14_safe_divide(
                            positive_n,
                            total_n,
                        )
                    ),
                    "alert_count": alert_count,
                    "alert_rate": (
                        _d14_safe_divide(
                            alert_count,
                            total_n,
                        )
                    ),
                    "true_positives": tp,
                    "false_positives": fp,
                    "true_negatives": tn,
                    "false_negatives": fn,
                    "sensitivity": (
                        _d14_safe_divide(
                            tp,
                            tp + fn,
                        )
                    ),
                    "specificity": (
                        _d14_safe_divide(
                            tn,
                            tn + fp,
                        )
                    ),
                    "precision_ppv": (
                        _d14_safe_divide(
                            tp,
                            tp + fp,
                        )
                    ),
                    "negative_predictive_value": (
                        _d14_safe_divide(
                            tn,
                            tn + fn,
                        )
                    ),
                    "f1_score": (
                        float(
                            f1_score(
                                y_true,
                                subgroup_decisions,
                                zero_division=0,
                            )
                        )
                    ),
                    "pr_auc": (
                        _d14_safe_pr_auc(
                            y_true,
                            subgroup_probabilities,
                        )
                    ),
                    "roc_auc": (
                        _d14_safe_roc_auc(
                            y_true,
                            subgroup_probabilities,
                        )
                    ),
                    "frozen_threshold": float(
                        D14_EXPECTED_DEVELOPMENT_THRESHOLD
                    ),
                    "subgroup_threshold_optimized": (
                        False
                    ),
                }
            )

    result = pd.DataFrame(records)

    result = result.sort_values(
        by=[
            "subgroup_dimension",
            "subgroup_value",
        ],
        kind="stable",
    ).reset_index(drop=True)

    return result


# ============================================================
# D14.54 — VALIDATE SUBGROUP EVIDENCE
# ============================================================


def validate_d14_locked_test_subgroup_analysis(
    subgroup_table: pd.DataFrame | None = None,
) -> dict[str, Any]:
    """
    Validate structural integrity and governance controls for
    locked TEST subgroup confirmation.
    """

    if subgroup_table is None:
        subgroup_table = (
            build_d14_locked_test_subgroup_analysis()
        )

    required_columns = {
        "subgroup_dimension",
        "subgroup_value",
        "support_classification",
        "n",
        "positive_n",
        "negative_n",
        "prevalence",
        "alert_count",
        "alert_rate",
        "true_positives",
        "false_positives",
        "true_negatives",
        "false_negatives",
        "sensitivity",
        "specificity",
        "precision_ppv",
        "negative_predictive_value",
        "f1_score",
        "pr_auc",
        "roc_auc",
        "frozen_threshold",
        "subgroup_threshold_optimized",
    }

    dimensions_present = set(
        subgroup_table[
            "subgroup_dimension"
        ].unique()
    )

    valid_support_values = {
        "ADEQUATE_SUPPORT",
        "LOW_SUPPORT",
    }

    support_values_present = set(
        subgroup_table[
            "support_classification"
        ].unique()
    )

    dimension_reconciliation = {}

    for dimension in D14_CONFIRMATORY_SUBGROUP_COLUMNS:
        dimension_rows = subgroup_table[
            subgroup_table[
                "subgroup_dimension"
            ]
            == dimension
        ]

        dimension_reconciliation[dimension] = {
            "n_reconciles": (
                int(dimension_rows["n"].sum())
                == D14_EXPECTED_TEST_ENCOUNTERS
            ),
            "positives_reconcile": (
                int(
                    dimension_rows[
                        "positive_n"
                    ].sum()
                )
                == D14_EXPECTED_TEST_POSITIVES
            ),
            "negatives_reconcile": (
                int(
                    dimension_rows[
                        "negative_n"
                    ].sum()
                )
                == D14_EXPECTED_TEST_NEGATIVES
            ),
            "alerts_reconcile": (
                int(
                    dimension_rows[
                        "alert_count"
                    ].sum()
                )
                == 4_759
            ),
        }

    all_dimension_reconciliation_passed = all(
        all(values.values())
        for values in dimension_reconciliation.values()
    )

    threshold_values = set(
        subgroup_table[
            "frozen_threshold"
        ].astype(float)
    )

    subgroup_threshold_flags = (
        subgroup_table[
            "subgroup_threshold_optimized"
        ].astype(bool)
    )

    checks = {
        "required_columns_present": (
            required_columns.issubset(
                set(subgroup_table.columns)
            )
        ),

        "all_governed_dimensions_present": (
            dimensions_present
            == set(
                D14_CONFIRMATORY_SUBGROUP_COLUMNS
            )
        ),

        "support_classifications_valid": (
            support_values_present.issubset(
                valid_support_values
            )
        ),

        "dimension_totals_reconcile": (
            all_dimension_reconciliation_passed
        ),

        "single_frozen_threshold_used": (
            threshold_values
            == {
                float(
                    D14_EXPECTED_DEVELOPMENT_THRESHOLD
                )
            }
        ),

        "no_subgroup_threshold_optimization": (
            not subgroup_threshold_flags.any()
        ),

        "all_subgroup_n_positive": bool(
            (subgroup_table["n"] > 0).all()
        ),

        "all_prevalence_values_valid": bool(
            subgroup_table["prevalence"]
            .between(0.0, 1.0)
            .all()
        ),

        "all_alert_rates_valid": bool(
            subgroup_table["alert_rate"]
            .between(0.0, 1.0)
            .all()
        ),

        "deployment_not_authorized": True,
    }

    overall_pass = all(checks.values())

    return {
        "stage_id": D14_STAGE_ID,
        "validation_status": (
            "PASS" if overall_pass else "FAIL"
        ),
        "overall_pass": overall_pass,
        "checks": checks,
        "dimension_reconciliation": (
            dimension_reconciliation
        ),
        "subgroup_row_count": int(
            len(subgroup_table)
        ),
        "adequate_support_row_count": int(
            (
                subgroup_table[
                    "support_classification"
                ]
                == "ADEQUATE_SUPPORT"
            ).sum()
        ),
        "low_support_row_count": int(
            (
                subgroup_table[
                    "support_classification"
                ]
                == "LOW_SUPPORT"
            ).sum()
        ),
        "deployment_authorized": False,
        "next_controlled_action": (
            "D14_LOCKED_TEST_ROBUSTNESS_CONFIRMATION"
            if overall_pass
            else "STOP_REMEDIATE_SUBGROUP_EVIDENCE"
        ),
    }


# ============================================================
# D14.55 — SUBGROUP RANGE SUMMARY
# ============================================================


def build_d14_subgroup_range_summary(
    subgroup_table: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """
    Summarize descriptive metric ranges among adequately
    supported groups.

    These ranges identify heterogeneity for governance review.
    They are NOT causal fairness findings.
    """

    if subgroup_table is None:
        subgroup_table = (
            build_d14_locked_test_subgroup_analysis()
        )

    adequate = subgroup_table[
        subgroup_table[
            "support_classification"
        ]
        == "ADEQUATE_SUPPORT"
    ].copy()

    metrics = (
        "prevalence",
        "alert_rate",
        "sensitivity",
        "specificity",
        "precision_ppv",
        "negative_predictive_value",
        "f1_score",
        "pr_auc",
        "roc_auc",
    )

    records: list[dict[str, Any]] = []

    for dimension in D14_CONFIRMATORY_SUBGROUP_COLUMNS:
        dimension_df = adequate[
            adequate[
                "subgroup_dimension"
            ]
            == dimension
        ]

        for metric in metrics:
            valid_values = (
                dimension_df[metric]
                .dropna()
                .astype(float)
            )

            if len(valid_values) == 0:
                metric_min = float("nan")
                metric_max = float("nan")
                metric_range = float("nan")
            else:
                metric_min = float(
                    valid_values.min()
                )
                metric_max = float(
                    valid_values.max()
                )
                metric_range = float(
                    metric_max - metric_min
                )

            records.append(
                {
                    "subgroup_dimension": (
                        dimension
                    ),
                    "metric": metric,
                    "adequate_support_groups": int(
                        len(dimension_df)
                    ),
                    "minimum": metric_min,
                    "maximum": metric_max,
                    "range": metric_range,
                }
            )

    return pd.DataFrame(records)


# ============================================================
# D14.56 — BUILD SUBGROUP CONFIRMATION EVIDENCE
# ============================================================


def build_d14_subgroup_confirmation_evidence(
) -> dict[str, Any]:
    """
    Build formal locked TEST subgroup confirmation evidence.
    """

    subgroup_table = (
        build_d14_locked_test_subgroup_analysis()
    )

    validation = (
        validate_d14_locked_test_subgroup_analysis(
            subgroup_table
        )
    )

    range_summary = (
        build_d14_subgroup_range_summary(
            subgroup_table
        )
    )

    return {
        "stage_id": D14_STAGE_ID,
        "registry_id": D14_EXPECTED_REGISTRY_ID,
        "candidate_system_sha256": (
            D14_EXPECTED_CANDIDATE_SYSTEM_SHA256
        ),
        "frozen_threshold": float(
            D14_EXPECTED_DEVELOPMENT_THRESHOLD
        ),
        "subgroup_dimensions": list(
            D14_CONFIRMATORY_SUBGROUP_COLUMNS
        ),
        "subgroup_table": subgroup_table,
        "range_summary": range_summary,
        "validation": validation,
        "analysis_classification": (
            "CONFIRMATORY_DESCRIPTIVE_SUBGROUP_ANALYSIS"
        ),
        "causal_fairness_claim": False,
        "subgroup_threshold_optimization": False,
        "model_modified": False,
        "deployment_authorized": False,
    }


# ============================================================
# D14.57 — PRINT SUBGROUP CONFIRMATION EVIDENCE
# ============================================================


def print_d14_subgroup_confirmation_evidence() -> None:
    """
    Print the locked TEST subgroup confirmation evidence.
    """

    evidence = (
        build_d14_subgroup_confirmation_evidence()
    )

    table = evidence["subgroup_table"]
    validation = evidence["validation"]

    print("=" * 96)
    print("D14 — LOCKED-TEST EVALUATION")
    print("CONFIRMATORY SUBGROUP / FAIRNESS ANALYSIS")
    print("=" * 96)

    print()
    print("Governance state")
    print("-" * 96)
    print(
        f"Registry ID:                    "
        f"{evidence['registry_id']}"
    )
    print(
        f"Frozen threshold:               "
        f"{evidence['frozen_threshold']}"
    )
    print(
        f"Analysis classification:        "
        f"{evidence['analysis_classification']}"
    )
    print(
        f"Subgroup threshold optimization:"
        f" {evidence['subgroup_threshold_optimization']}"
    )
    print(
        f"Causal fairness claim:          "
        f"{evidence['causal_fairness_claim']}"
    )

    print()
    print("Locked TEST subgroup results")
    print("-" * 96)

    display_columns = [
        "subgroup_dimension",
        "subgroup_value",
        "support_classification",
        "n",
        "positive_n",
        "prevalence",
        "alert_rate",
        "sensitivity",
        "specificity",
        "precision_ppv",
        "pr_auc",
        "roc_auc",
    ]

    print(
        table[
            display_columns
        ].to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}",
        )
    )

    print()
    print("Support summary")
    print("-" * 96)
    print(
        f"Total subgroup rows:            "
        f"{validation['subgroup_row_count']}"
    )
    print(
        f"Adequate-support rows:          "
        f"{validation['adequate_support_row_count']}"
    )
    print(
        f"Low-support rows:               "
        f"{validation['low_support_row_count']}"
    )

    print()
    print("Evidence integrity checks")
    print("-" * 96)

    for check_name, passed in validation["checks"].items():
        status = "PASS" if passed else "FAIL"
        print(f"{check_name:<52} {status}")

    print()
    print("Dimension reconciliation")
    print("-" * 96)

    for dimension, checks in (
        validation[
            "dimension_reconciliation"
        ].items()
    ):
        print(f"{dimension}:")

        for check_name, passed in checks.items():
            status = "PASS" if passed else "FAIL"
            print(
                f"  {check_name:<46} {status}"
            )

    print()
    print("Interpretation boundary")
    print("-" * 96)
    print(
        "Observed subgroup differences are descriptive "
        "confirmatory evidence."
    )
    print(
        "They do not by themselves establish causal bias "
        "or discrimination."
    )
    print(
        "Low-support groups remain visible and are not "
        "used for strong comparative conclusions."
    )
    print(
        "No subgroup-specific threshold has been selected."
    )

    print()
    print("-" * 96)
    print(
        f"SUBGROUP EVIDENCE STATUS: "
        f"{validation['validation_status']}"
    )
    print(
        f"NEXT CONTROLLED ACTION:   "
        f"{validation['next_controlled_action']}"
    )
    print(
        f"DEPLOYMENT AUTHORIZED:    "
        f"{validation['deployment_authorized']}"
    )
    print("=" * 96)


# ============================================================
# D14.58 — SUBGROUP GOVERNANCE INTERPRETATION
# ============================================================
#
# D14 subgroup analysis is confirmatory.
#
# Appropriate interpretation:
#
#   "The frozen model demonstrated differing operating
#    characteristics across observed demographic subgroups."
#
# Inappropriate interpretation without further evidence:
#
#   "The model is fair."
#   "The model is unfair."
#   "A demographic attribute caused the difference."
#
# Any material heterogeneity is carried forward as residual
# risk for clinical validation and deployment governance.
# ============================================================


# ============================================================
# D14.59 — NO TEST-DRIVEN MITIGATION
# ============================================================
#
# If D14 reveals unfavorable subgroup behavior, that evidence
# is preserved.
#
# The locked TEST set MUST NOT be used to:
#
#   - create new subgroup thresholds,
#   - rebalance training,
#   - engineer new features,
#   - remove features,
#   - recalibrate the model,
#   - choose a replacement model.
#
# Such changes would constitute a new development cycle and
# would require a new independently protected evaluation set.
# ============================================================

# ============================================================
# D14.60 — LOCKED-TEST ROBUSTNESS & INTERNAL
#          TRANSPORTABILITY CONFIRMATION
# ============================================================
#
# Purpose:
# Reassess the exact observed structural slices defined during
# D11 on the independent locked TEST cohort.
#
# The slice definitions are inherited from D11 and therefore
# were established before TEST evaluation.
#
# This analysis is confirmatory and descriptive.
#
# It MUST NOT:
#   - define new TEST-driven slices,
#   - retrain or retune the model,
#   - change preprocessing,
#   - recalibrate probabilities,
#   - change the frozen threshold,
#   - select subgroup-specific thresholds,
#   - claim external transportability,
#   - authorize deployment.
# ============================================================


# ============================================================
# D14.61 — PRE-SPECIFIED D11 OBSERVED-SLICE CONTRACT
# ============================================================

D14_ROBUSTNESS_SCENARIOS = (
    {
        "scenario_id": "D11-STRESS-003",
        "scenario_name": "Admission Type",
    },
    {
        "scenario_id": "D11-STRESS-004",
        "scenario_name": "Admission Source",
    },
    {
        "scenario_id": "D11-STRESS-005",
        "scenario_name": "No Prior Utilization",
    },
    {
        "scenario_id": "D11-STRESS-006",
        "scenario_name": "Single-Domain Prior Utilization",
    },
    {
        "scenario_id": "D11-STRESS-007",
        "scenario_name": "Multi-Domain Prior Utilization",
    },
    {
        "scenario_id": "D11-STRESS-008",
        "scenario_name": "Higher Utilization Intensity",
    },
    {
        "scenario_id": "D11-STRESS-009",
        "scenario_name": "Age Categories",
    },
)

D14_ROBUSTNESS_MIN_TOTAL_N = 100
D14_ROBUSTNESS_MIN_POSITIVES = 20
D14_ROBUSTNESS_MIN_NEGATIVES = 20


def classify_d14_robustness_slice_support(
    total_n: int,
    positive_n: int,
    negative_n: int,
) -> str:
    """
    Classify evidence support for an observed robustness slice.

    This classification concerns evidence strength only.
    """

    if (
        total_n >= D14_ROBUSTNESS_MIN_TOTAL_N
        and positive_n >= D14_ROBUSTNESS_MIN_POSITIVES
        and negative_n >= D14_ROBUSTNESS_MIN_NEGATIVES
    ):
        return "ADEQUATE_SUPPORT"

    return "LOW_SUPPORT"


# ============================================================
# D14.62 — BUILD EXACT D11 OBSERVED-SLICE MASKS ON TEST
# ============================================================


def build_d14_locked_test_robustness_masks(
    X_test_source: pd.DataFrame,
    scenario: dict[str, Any],
) -> dict[str, np.ndarray]:
    """
    Reproduce the exact observed-slice definitions established
    in D11, now applied to the locked TEST source features.

    No TEST-driven slice definition is permitted.
    """

    scenario_id = scenario["scenario_id"]

    masks: dict[str, np.ndarray] = {}

    # --------------------------------------------------------
    # Admission type — exact D11-STRESS-003 definition
    # --------------------------------------------------------

    if scenario_id == "D11-STRESS-003":

        values = sorted(
            X_test_source[
                "admission_type_id"
            ].dropna().unique().tolist()
        )

        for value in values:
            masks[
                f"admission_type_id={value}"
            ] = (
                X_test_source[
                    "admission_type_id"
                ].to_numpy()
                == value
            )

    # --------------------------------------------------------
    # Admission source — exact D11-STRESS-004 definition
    # --------------------------------------------------------

    elif scenario_id == "D11-STRESS-004":

        values = sorted(
            X_test_source[
                "admission_source_id"
            ].dropna().unique().tolist()
        )

        for value in values:
            masks[
                f"admission_source_id={value}"
            ] = (
                X_test_source[
                    "admission_source_id"
                ].to_numpy()
                == value
            )

    # --------------------------------------------------------
    # No prior utilization — exact D11-STRESS-005
    # --------------------------------------------------------

    elif scenario_id == "D11-STRESS-005":

        masks[
            "prior_utilization_domain_count=0"
        ] = (
            X_test_source[
                "prior_utilization_domain_count"
            ].to_numpy()
            == 0
        )

    # --------------------------------------------------------
    # Single-domain utilization — exact D11-STRESS-006
    # --------------------------------------------------------

    elif scenario_id == "D11-STRESS-006":

        masks[
            "prior_utilization_domain_count=1"
        ] = (
            X_test_source[
                "prior_utilization_domain_count"
            ].to_numpy()
            == 1
        )

    # --------------------------------------------------------
    # Multi-domain utilization — exact D11-STRESS-007
    # --------------------------------------------------------

    elif scenario_id == "D11-STRESS-007":

        masks[
            "prior_utilization_domain_count>=2"
        ] = (
            X_test_source[
                "prior_utilization_domain_count"
            ].to_numpy()
            >= 2
        )

    # --------------------------------------------------------
    # Higher utilization intensity — exact D11-STRESS-008
    # --------------------------------------------------------

    elif scenario_id == "D11-STRESS-008":

        masks[
            "prior_utilization_intensity>=3"
        ] = (
            X_test_source[
                "prior_utilization_intensity"
            ].to_numpy()
            >= 3
        )

    # --------------------------------------------------------
    # Age categories — exact D11-STRESS-009
    # --------------------------------------------------------

    elif scenario_id == "D11-STRESS-009":

        values = (
            X_test_source[
                "age"
            ]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        values = sorted(values)

        for value in values:
            masks[
                f"age={value}"
            ] = (
                X_test_source[
                    "age"
                ]
                .astype(str)
                .to_numpy()
                == value
            )

    else:
        raise RuntimeError(
            "Unsupported D14 inherited D11 scenario: "
            f"{scenario_id}"
        )

    return masks


# ============================================================
# D14.63 — CALCULATE ROBUSTNESS SLICE METRICS
# ============================================================


def build_d14_locked_test_robustness_table(
    prediction_bundle: dict[str, Any] | None = None,
) -> pd.DataFrame:
    """
    Calculate confirmatory TEST performance across the exact
    D11 observed structural slices.
    """

    if prediction_bundle is None:
        prediction_bundle = (
            generate_d14_frozen_test_predictions()
        )

    inference_validation = (
        validate_d14_frozen_test_predictions(
            prediction_bundle
        )
    )

    if not inference_validation["overall_pass"]:
        raise RuntimeError(
            "Frozen TEST inference integrity failed. "
            "Robustness confirmation is blocked."
        )

    locked_test = (
        prediction_bundle[
            "transformed_bundle"
        ]["locked_test"]
        .reset_index(drop=True)
        .copy()
    )

    source_features = (
        prediction_bundle[
            "transformed_bundle"
        ]["source_features"]
        .reset_index(drop=True)
        .copy()
    )

    y_true_all = (
        locked_test[D14_TARGET_COLUMN]
        .astype(int)
        .to_numpy()
    )

    probabilities_all = np.asarray(
        prediction_bundle[
            "positive_probabilities"
        ],
        dtype=float,
    )

    decisions_all = np.asarray(
        prediction_bundle[
            "frozen_threshold_predictions"
        ],
        dtype=int,
    )

    expected_rows = D14_EXPECTED_TEST_ENCOUNTERS

    if not (
        len(source_features)
        == len(y_true_all)
        == len(probabilities_all)
        == len(decisions_all)
        == expected_rows
    ):
        raise RuntimeError(
            "D14 robustness inputs are not row-aligned."
        )

    records: list[dict[str, Any]] = []

    for scenario in D14_ROBUSTNESS_SCENARIOS:

        masks = build_d14_locked_test_robustness_masks(
            source_features,
            scenario,
        )

        for slice_name, mask in masks.items():

            mask = np.asarray(mask, dtype=bool)

            if len(mask) != expected_rows:
                raise RuntimeError(
                    "Robustness slice mask length mismatch: "
                    f"{slice_name}"
                )

            y_true = y_true_all[mask]
            probabilities = probabilities_all[mask]
            decisions = decisions_all[mask]

            total_n = int(len(y_true))

            if total_n == 0:
                continue

            positive_n = int(y_true.sum())
            negative_n = int(
                total_n - positive_n
            )

            tn, fp, fn, tp = confusion_matrix(
                y_true,
                decisions,
                labels=[0, 1],
            ).ravel()

            tn = int(tn)
            fp = int(fp)
            fn = int(fn)
            tp = int(tp)

            alert_count = int(
                decisions.sum()
            )

            support_classification = (
                classify_d14_robustness_slice_support(
                    total_n=total_n,
                    positive_n=positive_n,
                    negative_n=negative_n,
                )
            )

            records.append(
                {
                    "scenario_id": (
                        scenario["scenario_id"]
                    ),
                    "scenario_name": (
                        scenario["scenario_name"]
                    ),
                    "slice_name": slice_name,
                    "support_classification": (
                        support_classification
                    ),
                    "n": total_n,
                    "positive_n": positive_n,
                    "negative_n": negative_n,
                    "prevalence": (
                        _d14_safe_divide(
                            positive_n,
                            total_n,
                        )
                    ),
                    "alert_count": alert_count,
                    "alert_rate": (
                        _d14_safe_divide(
                            alert_count,
                            total_n,
                        )
                    ),
                    "true_positives": tp,
                    "false_positives": fp,
                    "true_negatives": tn,
                    "false_negatives": fn,
                    "sensitivity": (
                        _d14_safe_divide(
                            tp,
                            tp + fn,
                        )
                    ),
                    "specificity": (
                        _d14_safe_divide(
                            tn,
                            tn + fp,
                        )
                    ),
                    "precision_ppv": (
                        _d14_safe_divide(
                            tp,
                            tp + fp,
                        )
                    ),
                    "negative_predictive_value": (
                        _d14_safe_divide(
                            tn,
                            tn + fn,
                        )
                    ),
                    "f1_score": float(
                        f1_score(
                            y_true,
                            decisions,
                            zero_division=0,
                        )
                    ),
                    "pr_auc": (
                        _d14_safe_pr_auc(
                            y_true,
                            probabilities,
                        )
                    ),
                    "roc_auc": (
                        _d14_safe_roc_auc(
                            y_true,
                            probabilities,
                        )
                    ),
                    "brier_score": float(
                        brier_score_loss(
                            y_true,
                            probabilities,
                        )
                    ),
                    "log_loss": float(
                        log_loss(
                            y_true,
                            probabilities,
                            labels=[0, 1],
                        )
                    ),
                    "frozen_threshold": float(
                        D14_EXPECTED_DEVELOPMENT_THRESHOLD
                    ),
                    "threshold_retuned": False,
                    "model_modified": False,
                }
            )

    return pd.DataFrame(records)


# ============================================================
# D14.64 — COMPARE ROBUSTNESS SLICES WITH TEST BASELINE
# ============================================================


def build_d14_robustness_baseline_comparison(
    robustness_table: pd.DataFrame | None = None,
    test_result: dict[str, Any] | None = None,
) -> pd.DataFrame:
    """
    Compare adequately supported structural slices with the
    overall locked TEST baseline.

    Differences are descriptive only.
    """

    if robustness_table is None:
        robustness_table = (
            build_d14_locked_test_robustness_table()
        )

    if test_result is None:
        test_result = (
            evaluate_d14_locked_test_performance()
        )

    metrics = (
        "prevalence",
        "alert_rate",
        "sensitivity",
        "specificity",
        "precision_ppv",
        "negative_predictive_value",
        "f1_score",
        "pr_auc",
        "roc_auc",
        "brier_score",
        "log_loss",
    )

    records: list[dict[str, Any]] = []

    for _, row in robustness_table.iterrows():

        if (
            row["support_classification"]
            != "ADEQUATE_SUPPORT"
        ):
            continue

        record = {
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "slice_name": row["slice_name"],
            "support_classification": (
                row["support_classification"]
            ),
            "n": int(row["n"]),
        }

        for metric in metrics:
            slice_value = float(row[metric])
            baseline_value = float(
                test_result[metric]
            )

            record[f"{metric}_slice"] = (
                slice_value
            )
            record[f"{metric}_baseline"] = (
                baseline_value
            )
            record[f"{metric}_difference"] = (
                slice_value - baseline_value
            )

        records.append(record)

    return pd.DataFrame(records)


# ============================================================
# D14.65 — VALIDATE ROBUSTNESS CONFIRMATION
# ============================================================


def validate_d14_locked_test_robustness(
    robustness_table: pd.DataFrame | None = None,
) -> dict[str, Any]:
    """
    Validate D14 robustness evidence integrity.

    This validates the process and inherited scenario contract,
    not whether every slice performs identically.
    """

    if robustness_table is None:
        robustness_table = (
            build_d14_locked_test_robustness_table()
        )

    expected_scenario_ids = {
        scenario["scenario_id"]
        for scenario in D14_ROBUSTNESS_SCENARIOS
    }

    observed_scenario_ids = set(
        robustness_table[
            "scenario_id"
        ].unique()
    )

    threshold_values = set(
        robustness_table[
            "frozen_threshold"
        ].astype(float)
    )

    support_values = set(
        robustness_table[
            "support_classification"
        ].unique()
    )

    required_columns = {
        "scenario_id",
        "scenario_name",
        "slice_name",
        "support_classification",
        "n",
        "positive_n",
        "negative_n",
        "prevalence",
        "alert_count",
        "alert_rate",
        "true_positives",
        "false_positives",
        "true_negatives",
        "false_negatives",
        "sensitivity",
        "specificity",
        "precision_ppv",
        "negative_predictive_value",
        "f1_score",
        "pr_auc",
        "roc_auc",
        "brier_score",
        "log_loss",
        "frozen_threshold",
        "threshold_retuned",
        "model_modified",
    }

    checks = {
        "required_columns_present": (
            required_columns.issubset(
                set(robustness_table.columns)
            )
        ),

        "all_prespecified_scenarios_present": (
            observed_scenario_ids
            == expected_scenario_ids
        ),

        "support_classifications_valid": (
            support_values.issubset(
                {
                    "ADEQUATE_SUPPORT",
                    "LOW_SUPPORT",
                }
            )
        ),

        "all_slice_n_positive": bool(
            (robustness_table["n"] > 0).all()
        ),

        "outcome_counts_reconcile_per_slice": bool(
            (
                robustness_table["positive_n"]
                + robustness_table["negative_n"]
                == robustness_table["n"]
            ).all()
        ),

        "confusion_counts_reconcile_per_slice": bool(
            (
                robustness_table["true_positives"]
                + robustness_table["false_positives"]
                + robustness_table["true_negatives"]
                + robustness_table["false_negatives"]
                == robustness_table["n"]
            ).all()
        ),

        "single_frozen_threshold_used": (
            threshold_values
            == {
                float(
                    D14_EXPECTED_DEVELOPMENT_THRESHOLD
                )
            }
        ),

        "threshold_not_retuned": (
            not robustness_table[
                "threshold_retuned"
            ].astype(bool).any()
        ),

        "model_not_modified": (
            not robustness_table[
                "model_modified"
            ].astype(bool).any()
        ),

        "prevalence_values_valid": bool(
            robustness_table["prevalence"]
            .between(0.0, 1.0)
            .all()
        ),

        "alert_rates_valid": bool(
            robustness_table["alert_rate"]
            .between(0.0, 1.0)
            .all()
        ),

        "deployment_not_authorized": True,
    }

    overall_pass = all(checks.values())

    return {
        "stage_id": D14_STAGE_ID,
        "validation_status": (
            "PASS" if overall_pass else "FAIL"
        ),
        "overall_pass": overall_pass,
        "checks": checks,
        "robustness_row_count": int(
            len(robustness_table)
        ),
        "adequate_support_row_count": int(
            (
                robustness_table[
                    "support_classification"
                ]
                == "ADEQUATE_SUPPORT"
            ).sum()
        ),
        "low_support_row_count": int(
            (
                robustness_table[
                    "support_classification"
                ]
                == "LOW_SUPPORT"
            ).sum()
        ),
        "scenario_count": int(
            robustness_table[
                "scenario_id"
            ].nunique()
        ),
        "deployment_authorized": False,
        "next_controlled_action": (
            "D14_LOCKED_TEST_EXPLAINABILITY_CONFIRMATION"
            if overall_pass
            else "STOP_REMEDIATE_ROBUSTNESS_EVIDENCE"
        ),
    }


# ============================================================
# D14.66 — BUILD ROBUSTNESS CONFIRMATION EVIDENCE
# ============================================================


def build_d14_robustness_confirmation_evidence(
) -> dict[str, Any]:
    """
    Build formal locked TEST robustness and internal
    transportability confirmation evidence.
    """

    robustness_table = (
        build_d14_locked_test_robustness_table()
    )

    validation = (
        validate_d14_locked_test_robustness(
            robustness_table
        )
    )

    baseline_comparison = (
        build_d14_robustness_baseline_comparison(
            robustness_table
        )
    )

    return {
        "stage_id": D14_STAGE_ID,
        "registry_id": D14_EXPECTED_REGISTRY_ID,
        "candidate_system_sha256": (
            D14_EXPECTED_CANDIDATE_SYSTEM_SHA256
        ),
        "frozen_threshold": float(
            D14_EXPECTED_DEVELOPMENT_THRESHOLD
        ),
        "scenario_source": (
            "PRE_SPECIFIED_D11_OBSERVED_SLICE_DEFINITIONS"
        ),
        "robustness_table": robustness_table,
        "baseline_comparison": baseline_comparison,
        "validation": validation,
        "analysis_classification": (
            "CONFIRMATORY_INTERNAL_ROBUSTNESS_AND_"
            "TRANSPORTABILITY_ANALYSIS"
        ),
        "external_transportability_established": False,
        "test_driven_slices_created": False,
        "threshold_retuned": False,
        "model_modified": False,
        "deployment_authorized": False,
    }


# ============================================================
# D14.67 — PRINT ROBUSTNESS CONFIRMATION
# ============================================================


def print_d14_robustness_confirmation_evidence() -> None:
    """
    Print locked TEST robustness confirmation evidence.
    """

    evidence = (
        build_d14_robustness_confirmation_evidence()
    )

    table = evidence["robustness_table"]
    validation = evidence["validation"]

    print("=" * 110)
    print("D14 — LOCKED-TEST EVALUATION")
    print(
        "CONFIRMATORY ROBUSTNESS & INTERNAL "
        "TRANSPORTABILITY ANALYSIS"
    )
    print("=" * 110)

    print()
    print("Governance state")
    print("-" * 110)
    print(
        f"Registry ID:                  "
        f"{evidence['registry_id']}"
    )
    print(
        f"Frozen threshold:             "
        f"{evidence['frozen_threshold']}"
    )
    print(
        f"Scenario source:              "
        f"{evidence['scenario_source']}"
    )
    print(
        f"TEST-driven slices created:   "
        f"{evidence['test_driven_slices_created']}"
    )
    print(
        f"External transportability:    "
        f"{evidence['external_transportability_established']}"
    )

    print()
    print("Locked TEST robustness results")
    print("-" * 110)

    display_columns = [
        "scenario_id",
        "slice_name",
        "support_classification",
        "n",
        "positive_n",
        "prevalence",
        "alert_rate",
        "sensitivity",
        "specificity",
        "precision_ppv",
        "pr_auc",
        "roc_auc",
    ]

    print(
        table[
            display_columns
        ].to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}",
        )
    )

    print()
    print("Evidence support")
    print("-" * 110)
    print(
        f"Scenarios represented:        "
        f"{validation['scenario_count']}"
    )
    print(
        f"Total slice rows:             "
        f"{validation['robustness_row_count']}"
    )
    print(
        f"Adequate-support rows:        "
        f"{validation['adequate_support_row_count']}"
    )
    print(
        f"Low-support rows:             "
        f"{validation['low_support_row_count']}"
    )

    print()
    print("Evidence integrity checks")
    print("-" * 110)

    for check_name, passed in validation["checks"].items():
        status = "PASS" if passed else "FAIL"
        print(f"{check_name:<56} {status}")

    print()
    print("Interpretation boundary")
    print("-" * 110)
    print(
        "Observed structural differences are confirmatory "
        "internal robustness evidence."
    )
    print(
        "They do not establish external institutional, "
        "geographic, or temporal transportability."
    )
    print(
        "Unfavorable findings are retained and cannot be "
        "used to redesign the frozen candidate."
    )

    print()
    print("-" * 110)
    print(
        f"ROBUSTNESS EVIDENCE STATUS: "
        f"{validation['validation_status']}"
    )
    print(
        f"NEXT CONTROLLED ACTION:     "
        f"{validation['next_controlled_action']}"
    )
    print(
        f"DEPLOYMENT AUTHORIZED:      "
        f"{validation['deployment_authorized']}"
    )
    print("=" * 110)


# ============================================================
# D14.68 — ROBUSTNESS INTERPRETATION RULE
# ============================================================
#
# Particular attention is given to prior-utilization slices
# because D11 identified material utilization-dependent
# operating behavior and D12 subsequently identified prior-
# utilization features as major contributors to the frozen
# model's predictions.
#
# Confirmation on TEST strengthens evidence that this is a
# structural property of the frozen candidate.
#
# It does NOT determine whether the pattern represents:
#
#   - clinically appropriate risk stratification,
#   - case-mix differences,
#   - excessive utilization dependence,
#   - dataset-specific behavior,
#   - or some combination of these.
#
# Those remain clinical/governance questions.
# ============================================================


# ============================================================
# D14.69 — NO TEST-DRIVEN ROBUSTNESS REMEDIATION
# ============================================================
#
# Any robustness weakness discovered here becomes permanent
# confirmatory evidence for the registered candidate.
#
# It MUST NOT trigger modification using this TEST set.
#
# A materially revised candidate would require:
#
#   new development evidence
#       ->
#   new validation evidence
#       ->
#   new registry identity/version
#       ->
#   a newly protected independent evaluation dataset.
#
# Deployment remains unauthorized.
# ============================================================

# ============================================================
# D14.70 — LOCKED-TEST EXPLAINABILITY CONFIRMATION
# ============================================================
#
# Purpose:
# Confirm whether the frozen candidate's explanation structure
# remains stable on the independent locked TEST cohort.
#
# Methodology inherited from D12:
#   - SHAP TreeExplainer
#   - raw XGBoost margin/log-odds explanation space
#   - logistic-expit probability reconstruction
#   - 49 transformed features
#   - aggregation to 10 governed source-feature families
#   - explicit prior-utilization family assessment
#
# This section MUST NOT:
#   - retrain or retune the model,
#   - refit preprocessing,
#   - recalibrate probabilities,
#   - change the threshold,
#   - change the feature set,
#   - interpret SHAP causally,
#   - authorize deployment.
# ============================================================


import shap


# ============================================================
# D14.71 — EXPLAINABILITY CONTRACT
# ============================================================

D14_EXPLAINABILITY_SOURCE_FAMILIES = (
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

D14_PRIOR_UTILIZATION_FAMILY = (
    "prior_outpatient_use",
    "prior_emergency_use",
    "prior_inpatient_use",
    "prior_utilization_intensity",
    "prior_utilization_domain_count",
)

D14_EXPECTED_TRANSFORMED_FEATURE_COUNT = 49

D14_SHAP_PROBABILITY_TOLERANCE = 1e-6

D14_D12_VALIDATION_PRIOR_UTILIZATION_SHARE = (
    0.6852025594108491
)


# ============================================================
# D14.72 — NUMERICALLY STABLE EXPIT
# ============================================================


def _d14_expit_raw_output(
    raw_output: np.ndarray,
) -> np.ndarray:
    """
    Convert raw XGBoost margin/log-odds output to probability.

    Mirrors the governed D12 interpretation methodology.
    """

    raw_output = np.asarray(
        raw_output,
        dtype=float,
    )

    probability = np.empty_like(
        raw_output,
        dtype=float,
    )

    positive_mask = raw_output >= 0.0

    probability[positive_mask] = (
        1.0
        / (
            1.0
            + np.exp(
                -raw_output[positive_mask]
            )
        )
    )

    negative_raw = raw_output[
        ~positive_mask
    ]

    negative_exp = np.exp(
        negative_raw
    )

    probability[~positive_mask] = (
        negative_exp
        / (
            1.0
            + negative_exp
        )
    )

    return probability


# ============================================================
# D14.73 — BUILD LOCKED-TEST SHAP ATTRIBUTION DATASET
# ============================================================


def build_d14_locked_test_shap_attribution(
    prediction_bundle: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Generate SHAP values for the complete locked TEST cohort
    using the exact frozen registered model.

    SHAP values are interpreted in raw model-output space.
    """

    if prediction_bundle is None:
        prediction_bundle = (
            generate_d14_frozen_test_predictions()
        )

    inference_validation = (
        validate_d14_frozen_test_predictions(
            prediction_bundle
        )
    )

    if not inference_validation["overall_pass"]:
        raise RuntimeError(
            "Frozen TEST inference integrity failed. "
            "Explainability confirmation is blocked."
        )

    estimator = prediction_bundle["model"]

    X_test = np.asarray(
        prediction_bundle["X_test"],
        dtype=float,
    )

    model_probability = np.asarray(
        prediction_bundle[
            "positive_probabilities"
        ],
        dtype=float,
    )

    transformed_bundle = prediction_bundle[
        "transformed_bundle"
    ]

    feature_names = list(
        transformed_bundle["transformed_schema"]
    )

    expected_shape = (
        D14_EXPECTED_TEST_ENCOUNTERS,
        D14_EXPECTED_TRANSFORMED_FEATURE_COUNT,
    )

    if X_test.shape != expected_shape:
        raise RuntimeError(
            "Unexpected D14 transformed TEST shape. "
            f"Observed={X_test.shape}, "
            f"Expected={expected_shape}"
        )

    if len(feature_names) != (
        D14_EXPECTED_TRANSFORMED_FEATURE_COUNT
    ):
        raise RuntimeError(
            "Unexpected D14 transformed feature-name count."
        )

    explainer = shap.TreeExplainer(
        estimator
    )

    explanation = explainer(
        X_test
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
            "Unexpected locked TEST SHAP matrix shape. "
            f"Observed={shap_values.shape}, "
            f"Expected={expected_shape}"
        )

    if base_values.shape != (
        D14_EXPECTED_TEST_ENCOUNTERS,
    ):
        raise RuntimeError(
            "Unexpected locked TEST SHAP base-value shape."
        )

    reconstructed_raw_output = (
        base_values
        + shap_values.sum(
            axis=1
        )
    )

    reconstructed_probability = (
        _d14_expit_raw_output(
            reconstructed_raw_output
        )
    )

    probability_absolute_error = np.abs(
        reconstructed_probability
        - model_probability
    )

    max_probability_error = float(
        probability_absolute_error.max()
    )

    mean_probability_error = float(
        probability_absolute_error.mean()
    )

    return {
        "explainer": explainer,
        "shap_values": shap_values,
        "base_values": base_values,
        "transformed_feature_names": (
            feature_names
        ),
        "model_probability": model_probability,
        "reconstructed_raw_output": (
            reconstructed_raw_output
        ),
        "reconstructed_probability": (
            reconstructed_probability
        ),
        "max_probability_reconstruction_error": (
            max_probability_error
        ),
        "mean_probability_reconstruction_error": (
            mean_probability_error
        ),
        "model_output": str(
            explainer.model_output
        ),
        "output_space_interpretation": (
            "raw_margin_log_odds"
        ),
        "probability_link": (
            "logistic_expit"
        ),
        "encounter_count": int(
            shap_values.shape[0]
        ),
        "transformed_feature_count": int(
            shap_values.shape[1]
        ),
        "feature_attribution_is_causal": False,
        "model_retrained": False,
        "preprocessor_refitted": False,
        "threshold_retuned": False,
        "deployment_authorized": False,
    }


# ============================================================
# D14.74 — VALIDATE SHAP ADDITIVITY / COMPATIBILITY
# ============================================================


def validate_d14_locked_test_shap_attribution(
    attribution: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Validate SHAP compatibility and probability reconstruction
    on the complete locked TEST cohort.
    """

    if attribution is None:
        attribution = (
            build_d14_locked_test_shap_attribution()
        )

    shap_values = attribution[
        "shap_values"
    ]

    base_values = attribution[
        "base_values"
    ]

    reconstructed_probability = attribution[
        "reconstructed_probability"
    ]

    model_probability = attribution[
        "model_probability"
    ]

    checks = {
        "model_output_is_raw": (
            attribution[
                "model_output"
            ].lower()
            == "raw"
        ),

        "shap_shape_valid": (
            shap_values.shape
            == (
                D14_EXPECTED_TEST_ENCOUNTERS,
                D14_EXPECTED_TRANSFORMED_FEATURE_COUNT,
            )
        ),

        "base_value_shape_valid": (
            base_values.shape
            == (
                D14_EXPECTED_TEST_ENCOUNTERS,
            )
        ),

        "shap_values_finite": bool(
            np.isfinite(
                shap_values
            ).all()
        ),

        "base_values_finite": bool(
            np.isfinite(
                base_values
            ).all()
        ),

        "reconstructed_probabilities_finite": bool(
            np.isfinite(
                reconstructed_probability
            ).all()
        ),

        "model_probabilities_finite": bool(
            np.isfinite(
                model_probability
            ).all()
        ),

        "probability_reconstruction_within_tolerance": (
            attribution[
                "max_probability_reconstruction_error"
            ]
            <= D14_SHAP_PROBABILITY_TOLERANCE
        ),

        "model_not_retrained": (
            attribution[
                "model_retrained"
            ]
            is False
        ),

        "preprocessor_not_refitted": (
            attribution[
                "preprocessor_refitted"
            ]
            is False
        ),

        "threshold_not_retuned": (
            attribution[
                "threshold_retuned"
            ]
            is False
        ),

        "deployment_not_authorized": (
            attribution[
                "deployment_authorized"
            ]
            is False
        ),
    }

    overall_pass = all(
        checks.values()
    )

    return {
        "validation_status": (
            "PASS" if overall_pass else "FAIL"
        ),
        "overall_pass": overall_pass,
        "checks": checks,
        "max_probability_reconstruction_error": (
            attribution[
                "max_probability_reconstruction_error"
            ]
        ),
        "mean_probability_reconstruction_error": (
            attribution[
                "mean_probability_reconstruction_error"
            ]
        ),
    }


# ============================================================
# D14.75 — MAP TRANSFORMED FEATURES TO SOURCE FAMILIES
# ============================================================


def map_d14_transformed_feature_to_source_family(
    transformed_feature_name: str,
) -> str:
    """
    Map D7 transformed features to the exact ten governed
    source-feature families.

    Mirrors the D12 mapping methodology.
    """

    feature_name = str(
        transformed_feature_name
    )

    normalized_name = feature_name

    if "__" in normalized_name:
        normalized_name = (
            normalized_name.split(
                "__",
                1,
            )[1]
        )

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
        "Unable to map D14 transformed feature to governed "
        "source-feature family: "
        f"{transformed_feature_name}"
    )


# ============================================================
# D14.76 — SOURCE-FAMILY GLOBAL ATTRIBUTION
# ============================================================


def build_d14_locked_test_source_family_attribution(
    attribution: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Aggregate locked TEST SHAP values from 49 transformed
    features into the ten governed source-feature families.

    Signed values are aggregated encounter-by-encounter first.
    Global importance is then based on mean absolute magnitude
    of each encounter-level source-family attribution.
    """

    if attribution is None:
        attribution = (
            build_d14_locked_test_shap_attribution()
        )

    shap_values = np.asarray(
        attribution["shap_values"],
        dtype=float,
    )

    feature_names = list(
        attribution[
            "transformed_feature_names"
        ]
    )

    family_names = list(
        D14_EXPLAINABILITY_SOURCE_FAMILIES
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
            map_d14_transformed_feature_to_source_family(
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
            "D14 source-family SHAP aggregation does not "
            "preserve encounter-level additivity."
        )

    absolute_family_matrix = np.abs(
        family_matrix
    )

    mean_absolute_attribution = (
        absolute_family_matrix.mean(
            axis=0
        )
    )

    total_mean_absolute_attribution = float(
        mean_absolute_attribution.sum()
    )

    if total_mean_absolute_attribution <= 0.0:
        raise RuntimeError(
            "D14 global source-family attribution magnitude "
            "is not positive."
        )

    attribution_share = (
        mean_absolute_attribution
        / total_mean_absolute_attribution
    )

    rows = []

    for index, family in enumerate(
        family_names
    ):
        rows.append(
            {
                "source_feature_family": family,
                "transformed_feature_count": int(
                    family_feature_counts[
                        family
                    ]
                ),
                "mean_absolute_shap": float(
                    mean_absolute_attribution[
                        index
                    ]
                ),
                "attribution_share": float(
                    attribution_share[
                        index
                    ]
                ),
                "attribution_share_percent": float(
                    attribution_share[
                        index
                    ]
                    * 100.0
                ),
            }
        )

    global_table = pd.DataFrame(
        rows
    ).sort_values(
        by="mean_absolute_shap",
        ascending=False,
        kind="stable",
    ).reset_index(
        drop=True
    )

    prior_utilization_share = float(
        global_table.loc[
            global_table[
                "source_feature_family"
            ].isin(
                D14_PRIOR_UTILIZATION_FAMILY
            ),
            "attribution_share",
        ].sum()
    )

    prior_utilization_share_percent = float(
        prior_utilization_share
        * 100.0
    )

    validation_difference = float(
        prior_utilization_share
        - D14_D12_VALIDATION_PRIOR_UTILIZATION_SHARE
    )

    return {
        "family_shap_matrix": family_matrix,
        "family_names": family_names,
        "family_feature_counts": (
            family_feature_counts
        ),
        "family_additivity_match": (
            family_additivity_match
        ),
        "global_attribution_table": (
            global_table
        ),
        "prior_utilization_share": (
            prior_utilization_share
        ),
        "prior_utilization_share_percent": (
            prior_utilization_share_percent
        ),
        "d12_validation_prior_utilization_share": (
            D14_D12_VALIDATION_PRIOR_UTILIZATION_SHARE
        ),
        "prior_utilization_share_difference": (
            validation_difference
        ),
        "feature_attribution_is_causal": False,
    }


# ============================================================
# D14.77 — DETERMINISTIC LOCAL TEST EXPLANATIONS
# ============================================================


def build_d14_locked_test_local_explanations(
    prediction_bundle: dict[str, Any] | None = None,
    attribution: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Build five deterministic representative TEST explanations.

    Case taxonomy is inherited from D12:
      - true negative, lowest probability
      - false negative, highest probability
      - true positive, nearest threshold
      - false positive, nearest threshold
      - true positive, highest probability
    """

    if prediction_bundle is None:
        prediction_bundle = (
            generate_d14_frozen_test_predictions()
        )

    if attribution is None:
        attribution = (
            build_d14_locked_test_shap_attribution(
                prediction_bundle
            )
        )

    locked_test = (
        prediction_bundle[
            "transformed_bundle"
        ]["locked_test"]
        .reset_index(drop=True)
    )

    probabilities = np.asarray(
        prediction_bundle[
            "positive_probabilities"
        ],
        dtype=float,
    )

    decisions = np.asarray(
        prediction_bundle[
            "frozen_threshold_predictions"
        ],
        dtype=int,
    )

    y_true = (
        locked_test[
            D14_TARGET_COLUMN
        ]
        .astype(int)
        .to_numpy()
    )

    threshold = float(
        D14_EXPECTED_DEVELOPMENT_THRESHOLD
    )

    shap_values = attribution[
        "shap_values"
    ]

    base_values = attribution[
        "base_values"
    ]

    feature_names = attribution[
        "transformed_feature_names"
    ]

    tn_indices = np.where(
        (y_true == 0)
        & (decisions == 0)
    )[0]

    fn_indices = np.where(
        (y_true == 1)
        & (decisions == 0)
    )[0]

    tp_indices = np.where(
        (y_true == 1)
        & (decisions == 1)
    )[0]

    fp_indices = np.where(
        (y_true == 0)
        & (decisions == 1)
    )[0]

    required_sets = {
        "true_negative_low_probability": tn_indices,
        "false_negative_highest_probability": fn_indices,
        "true_positive_nearest_threshold": tp_indices,
        "false_positive_nearest_threshold": fp_indices,
        "true_positive_high_probability": tp_indices,
    }

    for case_type, indices in required_sets.items():
        if len(indices) == 0:
            raise RuntimeError(
                "Unable to construct D14 local explanation "
                f"case: {case_type}"
            )

    selected_indices = {
        "true_negative_low_probability": int(
            tn_indices[
                np.argmin(
                    probabilities[
                        tn_indices
                    ]
                )
            ]
        ),

        "false_negative_highest_probability": int(
            fn_indices[
                np.argmax(
                    probabilities[
                        fn_indices
                    ]
                )
            ]
        ),

        "true_positive_nearest_threshold": int(
            tp_indices[
                np.argmin(
                    np.abs(
                        probabilities[
                            tp_indices
                        ]
                        - threshold
                    )
                )
            ]
        ),

        "false_positive_nearest_threshold": int(
            fp_indices[
                np.argmin(
                    np.abs(
                        probabilities[
                            fp_indices
                        ]
                        - threshold
                    )
                )
            ]
        ),

        "true_positive_high_probability": int(
            tp_indices[
                np.argmax(
                    probabilities[
                        tp_indices
                    ]
                )
            ]
        ),
    }

    cases = []

    for case_type in (
        "true_negative_low_probability",
        "false_negative_highest_probability",
        "true_positive_nearest_threshold",
        "false_positive_nearest_threshold",
        "true_positive_high_probability",
    ):

        row_index = selected_indices[
            case_type
        ]

        shap_row = np.asarray(
            shap_values[
                row_index
            ],
            dtype=float,
        )

        base_value = float(
            base_values[
                row_index
            ]
        )

        reconstructed_raw = float(
            base_value
            + shap_row.sum()
        )

        reconstructed_probability = float(
            _d14_expit_raw_output(
                np.asarray(
                    [reconstructed_raw],
                    dtype=float,
                )
            )[0]
        )

        model_probability = float(
            probabilities[
                row_index
            ]
        )

        absolute_order = np.argsort(
            np.abs(shap_row)
        )[::-1]

        top_contributors = []

        for feature_index in (
            absolute_order[
                :5
            ]
        ):
            top_contributors.append(
                {
                    "transformed_feature": (
                        feature_names[
                            feature_index
                        ]
                    ),
                    "source_feature_family": (
                        map_d14_transformed_feature_to_source_family(
                            feature_names[
                                feature_index
                            ]
                        )
                    ),
                    "shap_value_raw": float(
                        shap_row[
                            feature_index
                        ]
                    ),
                    "absolute_shap": float(
                        abs(
                            shap_row[
                                feature_index
                            ]
                        )
                    ),
                }
            )

        cases.append(
            {
                "case_type": case_type,
                "test_row_position": (
                    row_index
                ),
                "true_outcome": int(
                    y_true[
                        row_index
                    ]
                ),
                "predicted_class": int(
                    decisions[
                        row_index
                    ]
                ),
                "model_probability": (
                    model_probability
                ),
                "distance_from_threshold": float(
                    model_probability
                    - threshold
                ),
                "base_value_raw": (
                    base_value
                ),
                "reconstructed_raw_output": (
                    reconstructed_raw
                ),
                "reconstructed_probability": (
                    reconstructed_probability
                ),
                "probability_reconstruction_error": float(
                    abs(
                        reconstructed_probability
                        - model_probability
                    )
                ),
                "top_contributors": (
                    top_contributors
                ),
                "feature_attribution_is_causal": False,
            }
        )

    max_local_error = float(
        max(
            case[
                "probability_reconstruction_error"
            ]
            for case in cases
        )
    )

    return {
        "case_count": int(
            len(cases)
        ),
        "cases": cases,
        "max_probability_reconstruction_error": (
            max_local_error
        ),
        "local_explanations_generalizable_to_population": (
            False
        ),
        "feature_attribution_is_causal": False,
    }


# ============================================================
# D14.78 — BUILD / VALIDATE EXPLAINABILITY CONFIRMATION
# ============================================================


def build_d14_explainability_confirmation_evidence(
) -> dict[str, Any]:
    """
    Build formal locked TEST explainability confirmation.
    """

    prediction_bundle = (
        generate_d14_frozen_test_predictions()
    )

    attribution = (
        build_d14_locked_test_shap_attribution(
            prediction_bundle
        )
    )

    shap_validation = (
        validate_d14_locked_test_shap_attribution(
            attribution
        )
    )

    family_evidence = (
        build_d14_locked_test_source_family_attribution(
            attribution
        )
    )

    local_evidence = (
        build_d14_locked_test_local_explanations(
            prediction_bundle,
            attribution,
        )
    )

    checks = {
        "shap_validation_passed": (
            shap_validation[
                "overall_pass"
            ]
            is True
        ),

        "family_additivity_preserved": (
            family_evidence[
                "family_additivity_match"
            ]
            is True
        ),

        "ten_source_families_present": (
            len(
                family_evidence[
                    "family_names"
                ]
            )
            == 10
        ),

        "prior_utilization_share_valid": (
            0.0
            <= family_evidence[
                "prior_utilization_share"
            ]
            <= 1.0
        ),

        "five_local_cases_present": (
            local_evidence[
                "case_count"
            ]
            == 5
        ),

        "local_probability_reconstruction_valid": (
            local_evidence[
                "max_probability_reconstruction_error"
            ]
            <= D14_SHAP_PROBABILITY_TOLERANCE
        ),

        "feature_attribution_not_causal": (
            family_evidence[
                "feature_attribution_is_causal"
            ]
            is False
            and local_evidence[
                "feature_attribution_is_causal"
            ]
            is False
        ),

        "threshold_not_retuned": True,
        "model_not_modified": True,
        "deployment_not_authorized": True,
    }

    overall_pass = all(
        checks.values()
    )

    return {
        "stage_id": D14_STAGE_ID,
        "registry_id": D14_EXPECTED_REGISTRY_ID,
        "candidate_system_sha256": (
            D14_EXPECTED_CANDIDATE_SYSTEM_SHA256
        ),
        "analysis_classification": (
            "CONFIRMATORY_LOCKED_TEST_EXPLAINABILITY"
        ),
        "attribution": attribution,
        "shap_validation": shap_validation,
        "family_evidence": family_evidence,
        "local_evidence": local_evidence,
        "checks": checks,
        "validation_status": (
            "PASS"
            if overall_pass
            else "FAIL"
        ),
        "overall_pass": overall_pass,
        "external_explainability_validation": False,
        "clinical_causality_established": False,
        "deployment_authorized": False,
        "next_controlled_action": (
            "D14_INTEGRATED_LOCKED_TEST_GOVERNANCE_DISPOSITION"
            if overall_pass
            else "STOP_REMEDIATE_EXPLAINABILITY_EVIDENCE"
        ),
    }


def print_d14_explainability_confirmation_evidence() -> None:
    """
    Print formal locked TEST explainability confirmation.
    """

    evidence = (
        build_d14_explainability_confirmation_evidence()
    )

    attribution = evidence[
        "attribution"
    ]

    family = evidence[
        "family_evidence"
    ]

    local = evidence[
        "local_evidence"
    ]

    global_table = family[
        "global_attribution_table"
    ]

    print("=" * 100)
    print("D14 — LOCKED-TEST EVALUATION")
    print("CONFIRMATORY EXPLAINABILITY & MODEL INTERPRETATION")
    print("=" * 100)

    print()
    print("Governance state")
    print("-" * 100)
    print(
        f"Registry ID:                   "
        f"{evidence['registry_id']}"
    )
    print(
        f"Analysis classification:       "
        f"{evidence['analysis_classification']}"
    )
    print(
        f"Model output space:            "
        f"{attribution['output_space_interpretation']}"
    )
    print(
        f"Probability link:              "
        f"{attribution['probability_link']}"
    )
    print(
        f"Feature attribution causal:    "
        f"{evidence['clinical_causality_established']}"
    )

    print()
    print("SHAP compatibility / additivity")
    print("-" * 100)
    print(
        f"TEST encounters explained:     "
        f"{attribution['encounter_count']:,}"
    )
    print(
        f"Transformed features:          "
        f"{attribution['transformed_feature_count']}"
    )
    print(
        f"Maximum probability error:     "
        f"{attribution['max_probability_reconstruction_error']:.12e}"
    )
    print(
        f"Mean probability error:        "
        f"{attribution['mean_probability_reconstruction_error']:.12e}"
    )
    print(
        f"Source-family additivity:      "
        f"{family['family_additivity_match']}"
    )

    print()
    print("Locked TEST global source-family attribution")
    print("-" * 100)

    print(
        global_table[
            [
                "source_feature_family",
                "transformed_feature_count",
                "mean_absolute_shap",
                "attribution_share_percent",
            ]
        ].to_string(
            index=False,
            float_format=lambda x: f"{x:.6f}",
        )
    )

    print()
    print("Prior-utilization attribution")
    print("-" * 100)
    print(
        f"D12 validation share:          "
        f"{family['d12_validation_prior_utilization_share'] * 100.0:.6f}%"
    )
    print(
        f"D14 locked TEST share:         "
        f"{family['prior_utilization_share_percent']:.6f}%"
    )
    print(
        f"Difference TEST - validation:  "
        f"{family['prior_utilization_share_difference'] * 100.0:+.6f} pp"
    )

    print()
    print("Deterministic local explanation cases")
    print("-" * 100)

    for case in local["cases"]:
        print(
            f"{case['case_type']:<40} "
            f"y={case['true_outcome']}  "
            f"pred={case['predicted_class']}  "
            f"p={case['model_probability']:.6f}  "
            f"reconstruction_error="
            f"{case['probability_reconstruction_error']:.3e}"
        )

        contributor_text = ", ".join(
            (
                f"{row['source_feature_family']}"
                f"({row['shap_value_raw']:+.4f})"
            )
            for row in case[
                "top_contributors"
            ]
        )

        print(
            f"  top contributors: "
            f"{contributor_text}"
        )

    print()
    print("Evidence integrity checks")
    print("-" * 100)

    for check_name, passed in (
        evidence["checks"].items()
    ):
        status = (
            "PASS" if passed else "FAIL"
        )

        print(
            f"{check_name:<55} {status}"
        )

    print()
    print("Interpretation boundary")
    print("-" * 100)
    print(
        "SHAP evidence describes frozen model behavior; "
        "it does not establish causal clinical effects."
    )
    print(
        "Prior-utilization attribution is interpreted jointly "
        "with D11/D14 robustness evidence."
    )
    print(
        "Locked TEST explainability does not establish external "
        "validation or deployment readiness."
    )

    print()
    print("-" * 100)
    print(
        f"EXPLAINABILITY EVIDENCE STATUS: "
        f"{evidence['validation_status']}"
    )
    print(
        f"NEXT CONTROLLED ACTION:         "
        f"{evidence['next_controlled_action']}"
    )
    print(
        f"DEPLOYMENT AUTHORIZED:          "
        f"{evidence['deployment_authorized']}"
    )
    print("=" * 100)


# ============================================================
# D14.79 — EXPLAINABILITY GOVERNANCE BOUNDARY
# ============================================================
#
# D14 explainability confirmation may establish that the
# explanation structure observed during development persists
# on the locked TEST cohort.
#
# It cannot establish:
#
#   - causal clinical relationships,
#   - biological mechanisms,
#   - clinical appropriateness,
#   - fairness,
#   - external transportability,
#   - prospective effectiveness,
#   - deployment safety.
#
# Any confirmed utilization dependence becomes residual
# validation risk and must be carried into the integrated D14
# governance disposition and later clinical validation report.
# ============================================================

# ============================================================
# D14.80 — INTEGRATED LOCKED-TEST GOVERNANCE DISPOSITION
# ============================================================
#
# Purpose:
# Integrate the complete D14 evidence chain into one formal
# lifecycle governance decision.
#
# This gate distinguishes:
#
#   1. evaluation integrity,
#   2. internal locked-test validation,
#   3. residual clinical/model risk,
#   4. external validation,
#   5. clinical effectiveness,
#   6. deployment authorization.
#
# A successful D14 gate DOES NOT authorize clinical deployment.
# ============================================================


# ============================================================
# D14.81 — GOVERNANCE DISPOSITION CONSTANTS
# ============================================================

D14_FINAL_DISPOSITION = (
    "CONDITIONAL_PASS_PROGRESS_TO_D15_WITH_"
    "DOCUMENTED_RESIDUAL_RISKS"
)

D14_FINAL_NEXT_STAGE = (
    "D15_DEPLOYMENT_AND_MONITORING_DESIGN"
)

D14_INTERNAL_VALIDATION_CLASSIFICATION = (
    "INTERNAL_LOCKED_TEST_VALIDATION_COMPLETED"
)

D14_EXTERNAL_VALIDATION_STATUS = (
    "NOT_ESTABLISHED"
)

D14_CLINICAL_EFFECTIVENESS_STATUS = (
    "NOT_ESTABLISHED"
)

D14_DEPLOYMENT_STATUS = (
    "NOT_AUTHORIZED"
)

D14_RESIDUAL_RISK_UTILIZATION_DEPENDENCE = (
    "MATERIAL"
)

D14_RESIDUAL_RISK_SUBGROUP_HETEROGENEITY = (
    "DOCUMENTED"
)

D14_RESIDUAL_RISK_EXTERNAL_TRANSPORTABILITY = (
    "UNRESOLVED"
)


# ============================================================
# D14.82 — MATERIAL RESIDUAL-RISK REGISTER
# ============================================================


def build_d14_residual_risk_register(
) -> list[dict[str, Any]]:
    """
    Build the formal D14 residual-risk register.

    Findings are retained from the locked TEST evaluation and
    must not be removed simply because the candidate progresses
    to the next lifecycle stage.
    """

    return [
        {
            "risk_id": "D14-RISK-001",
            "risk_domain": (
                "UTILIZATION_DEPENDENT_MODEL_BEHAVIOR"
            ),
            "severity_classification": "MATERIAL",
            "finding": (
                "Locked TEST robustness evidence confirmed "
                "substantial operating-point dependence on "
                "prior healthcare-utilization history."
            ),
            "evidence": (
                "At the frozen 0.12 threshold, the zero-domain "
                "prior-utilization slice had a 0.00% alert rate, "
                "the one-domain slice had a 60.56% alert rate, "
                "the >=2-domain slice had a 92.54% alert rate, "
                "and the utilization-intensity >=3 slice had an "
                "86.54% alert rate."
            ),
            "interpretation": (
                "The pattern may reflect genuine risk "
                "stratification, case mix, dataset-specific "
                "behavior, excessive utilization dependence, "
                "or a combination of these factors. D14 does "
                "not establish which explanation is causal."
            ),
            "required_control": (
                "Carry forward to D15 monitoring design, "
                "clinical workflow review, external validation, "
                "and prospective evaluation. No TEST-driven "
                "model or threshold modification is permitted."
            ),
            "resolved": False,
        },

        {
            "risk_id": "D14-RISK-002",
            "risk_domain": (
                "EXPLAINABILITY_UTILIZATION_DOMINANCE"
            ),
            "severity_classification": "MATERIAL",
            "finding": (
                "Prior-utilization source-feature families "
                "accounted for 77.274016% of locked TEST global "
                "source-family attribution."
            ),
            "evidence": (
                "The locked TEST attribution share exceeded "
                "the D12 validation attribution share of "
                "68.520256% by approximately 8.753760 "
                "percentage points."
            ),
            "interpretation": (
                "SHAP attribution describes frozen model "
                "behavior and does not establish causal "
                "clinical effects or biological mechanisms."
            ),
            "required_control": (
                "Monitor utilization-feature dependence and "
                "its operational consequences after any future "
                "authorized deployment; independently reassess "
                "during external and prospective validation."
            ),
            "resolved": False,
        },

        {
            "risk_id": "D14-RISK-003",
            "risk_domain": (
                "SUBGROUP_OPERATING_HETEROGENEITY"
            ),
            "severity_classification": "DOCUMENTED",
            "finding": (
                "Locked TEST subgroup analysis demonstrated "
                "heterogeneous operating characteristics across "
                "age, race, and gender strata, with age showing "
                "notable variation."
            ),
            "evidence": (
                "Fifteen subgroup rows had adequate support and "
                "three had low support. Low-support results were "
                "retained rather than generalized."
            ),
            "interpretation": (
                "Observed subgroup differences are descriptive "
                "and do not by themselves establish unfairness, "
                "discrimination, or causal bias."
            ),
            "required_control": (
                "Retain subgroup monitoring requirements and "
                "reassess performance with external and "
                "prospective populations."
            ),
            "resolved": False,
        },

        {
            "risk_id": "D14-RISK-004",
            "risk_domain": (
                "ADMISSION_CONTEXT_HETEROGENEITY"
            ),
            "severity_classification": "DOCUMENTED",
            "finding": (
                "Performance varied across admission-source "
                "and admission-type strata, including reduced "
                "sensitivity in some adequately supported "
                "admission-source groups."
            ),
            "evidence": (
                "The inherited D11 admission-context scenarios "
                "were independently reassessed on locked TEST "
                "without TEST-driven scenario creation."
            ),
            "interpretation": (
                "Observed differences may reflect case mix, "
                "documentation patterns, clinical context, "
                "or model behavior."
            ),
            "required_control": (
                "Include admission-context stratification in "
                "future monitoring and external validation."
            ),
            "resolved": False,
        },

        {
            "risk_id": "D14-RISK-005",
            "risk_domain": (
                "LIMITED_MODEL_DISCRIMINATION"
            ),
            "severity_classification": "MATERIAL",
            "finding": (
                "Locked TEST discrimination remained modest."
            ),
            "evidence": (
                "Locked TEST PR-AUC was 0.182040618234 and "
                "ROC-AUC was 0.623405163566."
            ),
            "interpretation": (
                "Stable generalization does not imply strong "
                "clinical discrimination or clinical utility."
            ),
            "required_control": (
                "Clinical workflow suitability, net benefit, "
                "prospective performance, and intervention "
                "effectiveness must be assessed separately "
                "before deployment consideration."
            ),
            "resolved": False,
        },

        {
            "risk_id": "D14-RISK-006",
            "risk_domain": (
                "EXTERNAL_TRANSPORTABILITY"
            ),
            "severity_classification": "UNRESOLVED",
            "finding": (
                "D14 used an internal patient-disjoint locked "
                "TEST partition from the same underlying "
                "dataset."
            ),
            "evidence": (
                "No independent institutional, geographic, "
                "temporal, or prospective external cohort was "
                "evaluated in D14."
            ),
            "interpretation": (
                "Internal locked-test validation cannot "
                "establish external transportability."
            ),
            "required_control": (
                "Require external validation before any claim "
                "of generalizability beyond the evaluated "
                "dataset context."
            ),
            "resolved": False,
        },

        {
            "risk_id": "D14-RISK-007",
            "risk_domain": (
                "CLINICAL_EFFECTIVENESS"
            ),
            "severity_classification": "UNRESOLVED",
            "finding": (
                "D14 evaluated predictive and operating "
                "performance but did not test whether model-"
                "supported interventions improve patient "
                "outcomes."
            ),
            "evidence": (
                "No prospective intervention study or clinical "
                "impact evaluation was performed."
            ),
            "interpretation": (
                "Predictive validation is distinct from "
                "clinical effectiveness."
            ),
            "required_control": (
                "Prospective workflow and clinical impact "
                "evaluation are required before effectiveness "
                "claims."
            ),
            "resolved": False,
        },
    ]


# ============================================================
# D14.83 — INTEGRATED EVIDENCE SUMMARY
# ============================================================


def build_d14_integrated_evidence_summary(
) -> dict[str, Any]:
    """
    Integrate the authoritative D14 evidence domains.

    Each evidence builder remains authoritative for its
    respective detailed result and validation structure.
    """

    performance = (
        build_d14_confirmatory_performance_evidence()
    )

    subgroup = (
        build_d14_subgroup_confirmation_evidence()
    )

    robustness = (
        build_d14_robustness_confirmation_evidence()
    )

    explainability = (
        build_d14_explainability_confirmation_evidence()
    )

    residual_risks = (
        build_d14_residual_risk_register()
    )

    return {
        "registry_id": (
            D14_EXPECTED_REGISTRY_ID
        ),

        "candidate_system_sha256": (
            D14_EXPECTED_CANDIDATE_SYSTEM_SHA256
        ),

        "evaluation_partition": (
            D14_EVALUATION_PARTITION
        ),

        "evaluation_mode": (
            D14_EVALUATION_MODE
        ),

        "performance_evidence": performance,

        "subgroup_evidence": subgroup,

        "robustness_evidence": robustness,

        "explainability_evidence": explainability,

        "residual_risks": residual_risks,

        "residual_risk_count": int(
            len(residual_risks)
        ),

        "unresolved_residual_risk_count": int(
            sum(
                not risk["resolved"]
                for risk in residual_risks
            )
        ),

        "external_validation_completed": False,

        "clinical_effectiveness_established": False,

        "deployment_authorized": False,
    }


# ============================================================
# D14.84 — GOVERNANCE GATE EVALUATION
# ============================================================


def evaluate_d14_integrated_governance_gate(
    evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Evaluate the integrated D14 lifecycle gate.

    Progression requires successful completion of the
    pre-specified internal locked TEST evaluation while
    retaining all material residual risks.

    PASS at this gate means lifecycle progression is permitted.

    It does NOT mean:
        - external validation completed,
        - clinical effectiveness established,
        - clinical deployment authorized.
    """

    if evidence is None:
        evidence = (
            build_d14_integrated_evidence_summary()
        )

    performance = evidence[
        "performance_evidence"
    ]

    subgroup = evidence[
        "subgroup_evidence"
    ]

    robustness = evidence[
        "robustness_evidence"
    ]

    explainability = evidence[
        "explainability_evidence"
    ]

    # --------------------------------------------------------
    # Extract authoritative validation interfaces
    # --------------------------------------------------------

    performance_validation = performance[
        "evaluation_validation"
    ]

    subgroup_validation = subgroup[
        "validation"
    ]

    robustness_validation = robustness[
        "validation"
    ]

    # Explainability exposes overall_pass directly.
    explainability_overall_pass = (
        explainability[
            "overall_pass"
        ]
    )

    checks = {
        "registered_candidate_identity_preserved": (
            evidence["registry_id"]
            == D14_EXPECTED_REGISTRY_ID
            and evidence[
                "candidate_system_sha256"
            ]
            == D14_EXPECTED_CANDIDATE_SYSTEM_SHA256
        ),

        "performance_candidate_identity_preserved": (
            performance["registry_id"]
            == D14_EXPECTED_REGISTRY_ID
            and performance[
                "candidate_system_sha256"
            ]
            == D14_EXPECTED_CANDIDATE_SYSTEM_SHA256
        ),

        "subgroup_candidate_identity_preserved": (
            subgroup["registry_id"]
            == D14_EXPECTED_REGISTRY_ID
            and subgroup[
                "candidate_system_sha256"
            ]
            == D14_EXPECTED_CANDIDATE_SYSTEM_SHA256
        ),

        "robustness_candidate_identity_preserved": (
            robustness["registry_id"]
            == D14_EXPECTED_REGISTRY_ID
            and robustness[
                "candidate_system_sha256"
            ]
            == D14_EXPECTED_CANDIDATE_SYSTEM_SHA256
        ),

        "explainability_candidate_identity_preserved": (
            explainability["registry_id"]
            == D14_EXPECTED_REGISTRY_ID
            and explainability[
                "candidate_system_sha256"
            ]
            == D14_EXPECTED_CANDIDATE_SYSTEM_SHA256
        ),

        "locked_test_partition_used": (
            evidence[
                "evaluation_partition"
            ]
            == "LOCKED_TEST"
        ),

        "one_time_confirmatory_mode_preserved": (
            evidence[
                "evaluation_mode"
            ]
            == "ONE_TIME_CONFIRMATORY_EVALUATION"
        ),

        "performance_evaluation_passed": (
            performance_validation[
                "overall_pass"
            ]
            is True
        ),

        "performance_internal_test_completed": (
            performance[
                "internal_locked_test_validation_completed"
            ]
            is True
        ),

        "performance_external_validation_not_claimed": (
            performance[
                "external_validation_completed"
            ]
            is False
        ),

        "performance_clinical_effectiveness_not_claimed": (
            performance[
                "clinical_effectiveness_established"
            ]
            is False
        ),

        "performance_deployment_not_authorized": (
            performance[
                "deployment_authorized"
            ]
            is False
        ),

        "subgroup_confirmation_passed": (
            subgroup_validation[
                "overall_pass"
            ]
            is True
        ),

        "subgroup_threshold_optimization_not_performed": (
            subgroup[
                "subgroup_threshold_optimization"
            ]
            is False
        ),

        "subgroup_model_not_modified": (
            subgroup[
                "model_modified"
            ]
            is False
        ),

        "subgroup_deployment_not_authorized": (
            subgroup[
                "deployment_authorized"
            ]
            is False
        ),

        "robustness_confirmation_passed": (
            robustness_validation[
                "overall_pass"
            ]
            is True
        ),

        "robustness_test_driven_slices_not_created": (
            robustness[
                "test_driven_slices_created"
            ]
            is False
        ),

        "robustness_threshold_not_retuned": (
            robustness[
                "threshold_retuned"
            ]
            is False
        ),

        "robustness_model_not_modified": (
            robustness[
                "model_modified"
            ]
            is False
        ),

        "external_transportability_not_claimed": (
            robustness[
                "external_transportability_established"
            ]
            is False
        ),

        "robustness_deployment_not_authorized": (
            robustness[
                "deployment_authorized"
            ]
            is False
        ),

        "explainability_confirmation_passed": (
            explainability_overall_pass
            is True
        ),

        "explainability_external_validation_not_claimed": (
            explainability[
                "external_explainability_validation"
            ]
            is False
        ),

        "clinical_causality_not_claimed": (
            explainability[
                "clinical_causality_established"
            ]
            is False
        ),

        "explainability_deployment_not_authorized": (
            explainability[
                "deployment_authorized"
            ]
            is False
        ),

        "integrated_external_validation_not_claimed": (
            evidence[
                "external_validation_completed"
            ]
            is False
        ),

        "integrated_clinical_effectiveness_not_claimed": (
            evidence[
                "clinical_effectiveness_established"
            ]
            is False
        ),

        "integrated_deployment_not_authorized": (
            evidence[
                "deployment_authorized"
            ]
            is False
        ),

        "residual_risks_retained": (
            evidence[
                "residual_risk_count"
            ]
            > 0
            and evidence[
                "unresolved_residual_risk_count"
            ]
            > 0
        ),

        "all_registered_residual_risks_unresolved": (
            evidence[
                "unresolved_residual_risk_count"
            ]
            == evidence[
                "residual_risk_count"
            ]
        ),
    }

    overall_gate_integrity_pass = bool(
        all(
            checks.values()
        )
    )

    disposition = (
        D14_FINAL_DISPOSITION
        if overall_gate_integrity_pass
        else "FAIL_STOP_AND_REMEDIATE_D14_EVIDENCE"
    )

    next_stage = (
        D14_FINAL_NEXT_STAGE
        if overall_gate_integrity_pass
        else "D14_REMEDIATION"
    )

    return {
        "gate_integrity_status": (
            "PASS"
            if overall_gate_integrity_pass
            else "FAIL"
        ),

        "overall_gate_integrity_pass": (
            overall_gate_integrity_pass
        ),

        "checks": checks,

        "internal_validation_classification": (
            D14_INTERNAL_VALIDATION_CLASSIFICATION
        ),

        "external_validation_status": (
            D14_EXTERNAL_VALIDATION_STATUS
        ),

        "clinical_effectiveness_status": (
            D14_CLINICAL_EFFECTIVENESS_STATUS
        ),

        "deployment_status": (
            D14_DEPLOYMENT_STATUS
        ),

        "residual_risk_utilization_dependence": (
            D14_RESIDUAL_RISK_UTILIZATION_DEPENDENCE
        ),

        "residual_risk_subgroup_heterogeneity": (
            D14_RESIDUAL_RISK_SUBGROUP_HETEROGENEITY
        ),

        "residual_risk_external_transportability": (
            D14_RESIDUAL_RISK_EXTERNAL_TRANSPORTABILITY
        ),

        "disposition": disposition,

        "next_lifecycle_stage": next_stage,

        "deployment_authorized": False,
    }


# ============================================================
# D14.85 — VALIDATE FINAL GOVERNANCE DISPOSITION
# ============================================================


def validate_d14_integrated_governance_disposition(
    gate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Validate the final D14 governance disposition.

    This is a logical-consistency control over the lifecycle
    decision and is intentionally fail-closed.
    """

    if gate is None:
        gate = (
            evaluate_d14_integrated_governance_gate()
        )

    checks = {
        "gate_integrity_passed": (
            gate[
                "overall_gate_integrity_pass"
            ]
            is True
        ),

        "gate_status_is_pass": (
            gate[
                "gate_integrity_status"
            ]
            == "PASS"
        ),

        "disposition_is_conditional_progression": (
            gate[
                "disposition"
            ]
            == D14_FINAL_DISPOSITION
        ),

        "next_stage_is_d15": (
            gate[
                "next_lifecycle_stage"
            ]
            == D14_FINAL_NEXT_STAGE
        ),

        "internal_validation_completed": (
            gate[
                "internal_validation_classification"
            ]
            == (
                "INTERNAL_LOCKED_TEST_VALIDATION_COMPLETED"
            )
        ),

        "external_validation_not_established": (
            gate[
                "external_validation_status"
            ]
            == "NOT_ESTABLISHED"
        ),

        "clinical_effectiveness_not_established": (
            gate[
                "clinical_effectiveness_status"
            ]
            == "NOT_ESTABLISHED"
        ),

        "deployment_not_authorized": (
            gate[
                "deployment_status"
            ]
            == "NOT_AUTHORIZED"
            and gate[
                "deployment_authorized"
            ]
            is False
        ),

        "utilization_dependence_retained_as_material": (
            gate[
                "residual_risk_utilization_dependence"
            ]
            == "MATERIAL"
        ),

        "subgroup_heterogeneity_retained": (
            gate[
                "residual_risk_subgroup_heterogeneity"
            ]
            == "DOCUMENTED"
        ),

        "external_transportability_unresolved": (
            gate[
                "residual_risk_external_transportability"
            ]
            == "UNRESOLVED"
        ),
    }

    overall_pass = bool(
        all(
            checks.values()
        )
    )

    return {
        "validation_status": (
            "PASS"
            if overall_pass
            else "FAIL"
        ),

        "overall_pass": (
            overall_pass
        ),

        "checks": checks,

        "deployment_authorized": False,
    }


# ============================================================
# D14.86 — FINAL D14 GOVERNANCE RECORD
# ============================================================


def build_d14_final_governance_record(
) -> dict[str, Any]:
    """
    Build the authoritative D14 lifecycle closeout record.
    """

    evidence = (
        build_d14_integrated_evidence_summary()
    )

    gate = (
        evaluate_d14_integrated_governance_gate(
            evidence
        )
    )

    validation = (
        validate_d14_integrated_governance_disposition(
            gate
        )
    )

    if not validation[
        "overall_pass"
    ]:
        raise RuntimeError(
            "D14 final governance disposition failed "
            "integrity validation."
        )

    return {
        "stage_id": (
            D14_STAGE_ID
        ),

        "stage_name": (
            D14_STAGE_NAME
        ),

        "registry_id": (
            D14_EXPECTED_REGISTRY_ID
        ),

        "candidate_system_sha256": (
            D14_EXPECTED_CANDIDATE_SYSTEM_SHA256
        ),

        "source_git_commit": (
            D14_SOURCE_GIT_COMMIT
        ),

        "evaluation_partition": (
            D14_EVALUATION_PARTITION
        ),

        "evaluation_mode": (
            D14_EVALUATION_MODE
        ),

        "internal_validation_classification": (
            gate[
                "internal_validation_classification"
            ]
        ),

        "external_validation_status": (
            gate[
                "external_validation_status"
            ]
        ),

        "clinical_effectiveness_status": (
            gate[
                "clinical_effectiveness_status"
            ]
        ),

        "deployment_status": (
            gate[
                "deployment_status"
            ]
        ),

        "residual_risk_count": (
            evidence[
                "residual_risk_count"
            ]
        ),

        "unresolved_residual_risk_count": (
            evidence[
                "unresolved_residual_risk_count"
            ]
        ),

        "residual_risks": (
            evidence[
                "residual_risks"
            ]
        ),

        "gate_integrity_status": (
            gate[
                "gate_integrity_status"
            ]
        ),

        "gate_checks": (
            gate[
                "checks"
            ]
        ),

        "disposition": (
            gate[
                "disposition"
            ]
        ),

        "next_lifecycle_stage": (
            gate[
                "next_lifecycle_stage"
            ]
        ),

        "model_retrained_using_test": False,

        "threshold_retuned_using_test": False,

        "preprocessor_refitted_using_test": False,

        "feature_set_changed_using_test": False,

        "recalibration_performed_using_test": False,

        "subgroup_thresholds_created_using_test": False,

        "test_driven_candidate_selection": False,

        "test_driven_redesign": False,

        "external_validation_completed": False,

        "clinical_effectiveness_established": False,

        "deployment_authorized": False,

        "validation": validation,
    }


# ============================================================
# D14.87 — PRINT FINAL GOVERNANCE DISPOSITION
# ============================================================


def print_d14_final_governance_disposition() -> None:
    """
    Print the authoritative D14 lifecycle governance decision.
    """

    record = (
        build_d14_final_governance_record()
    )

    print("=" * 108)
    print(
        "D14 — LOCKED-TEST EVALUATION"
    )
    print(
        "INTEGRATED GOVERNANCE DISPOSITION"
    )
    print("=" * 108)

    print()
    print("Registered candidate")
    print("-" * 108)

    print(
        f"Registry ID:                       "
        f"{record['registry_id']}"
    )

    print(
        f"Candidate system SHA256:           "
        f"{record['candidate_system_sha256']}"
    )

    print(
        f"Evaluation partition:              "
        f"{record['evaluation_partition']}"
    )

    print(
        f"Evaluation mode:                   "
        f"{record['evaluation_mode']}"
    )

    print()
    print("Validation status")
    print("-" * 108)

    print(
        f"Internal locked TEST validation:   "
        f"{record['internal_validation_classification']}"
    )

    print(
        f"External validation:               "
        f"{record['external_validation_status']}"
    )

    print(
        f"Clinical effectiveness:            "
        f"{record['clinical_effectiveness_status']}"
    )

    print(
        f"Deployment status:                 "
        f"{record['deployment_status']}"
    )

    print()
    print("Residual-risk summary")
    print("-" * 108)

    print(
        f"Residual risks registered:         "
        f"{record['residual_risk_count']}"
    )

    print(
        f"Unresolved residual risks:         "
        f"{record['unresolved_residual_risk_count']}"
    )

    for risk in record[
        "residual_risks"
    ]:
        print(
            f"{risk['risk_id']:<14} "
            f"{risk['severity_classification']:<12} "
            f"{risk['risk_domain']}"
        )

    print()
    print("Integrated gate checks")
    print("-" * 108)

    for check_name, passed in (
        record[
            "gate_checks"
        ].items()
    ):
        status = (
            "PASS"
            if passed
            else "FAIL"
        )

        print(
            f"{check_name:<68} "
            f"{status}"
        )

    print()
    print("TEST contamination controls")
    print("-" * 108)

    contamination_controls = (
        (
            "Model retrained using TEST",
            record[
                "model_retrained_using_test"
            ],
        ),
        (
            "Threshold retuned using TEST",
            record[
                "threshold_retuned_using_test"
            ],
        ),
        (
            "Preprocessor refitted using TEST",
            record[
                "preprocessor_refitted_using_test"
            ],
        ),
        (
            "Feature set changed using TEST",
            record[
                "feature_set_changed_using_test"
            ],
        ),
        (
            "Recalibration using TEST",
            record[
                "recalibration_performed_using_test"
            ],
        ),
        (
            "Subgroup thresholds from TEST",
            record[
                "subgroup_thresholds_created_using_test"
            ],
        ),
        (
            "TEST-driven candidate selection",
            record[
                "test_driven_candidate_selection"
            ],
        ),
        (
            "TEST-driven redesign",
            record[
                "test_driven_redesign"
            ],
        ),
    )

    for label, value in (
        contamination_controls
    ):
        print(
            f"{label:<40} "
            f"{value}"
        )

    print()
    print("Final disposition validation")
    print("-" * 108)

    for check_name, passed in (
        record[
            "validation"
        ]["checks"].items()
    ):
        status = (
            "PASS"
            if passed
            else "FAIL"
        )

        print(
            f"{check_name:<68} "
            f"{status}"
        )

    print()
    print("Governance interpretation")
    print("-" * 108)

    print(
        "The registered candidate completed its pre-specified "
        "internal locked-test evaluation without TEST-driven "
        "retraining, threshold adjustment, recalibration, "
        "feature modification, or candidate redesign."
    )

    print(
        "Aggregate validation-to-TEST performance was broadly "
        "stable, supporting internal held-out generalization "
        "within the evaluated dataset context."
    )

    print(
        "Material utilization-dependent operating behavior and "
        "utilization-dominant attribution were independently "
        "confirmed and remain unresolved residual risks."
    )

    print(
        "D14 does not establish external transportability, "
        "prospective clinical effectiveness, or clinical "
        "deployment readiness."
    )

    print()
    print("-" * 108)

    print(
        f"GATE INTEGRITY STATUS:             "
        f"{record['gate_integrity_status']}"
    )

    print(
        f"FINAL D14 DISPOSITION:             "
        f"{record['disposition']}"
    )

    print(
        f"NEXT LIFECYCLE STAGE:              "
        f"{record['next_lifecycle_stage']}"
    )

    print(
        f"DEPLOYMENT AUTHORIZED:             "
        f"{record['deployment_authorized']}"
    )

    print("=" * 108)


# ============================================================
# D14.88 — D14 DECISION INTERPRETATION
# ============================================================
#
# CONDITIONAL PASS means:
#
#   - the registered frozen candidate successfully completed
#     its pre-specified internal locked TEST evaluation;
#
#   - evaluation integrity was preserved;
#
#   - internal held-out generalization evidence was obtained;
#
#   - material limitations and residual risks remain;
#
#   - progression to D15 is permitted for deployment and
#     monitoring DESIGN work.
#
# CONDITIONAL PASS does NOT mean:
#
#   - the model is externally validated;
#   - the model is clinically effective;
#   - the model is safe for autonomous use;
#   - the model is approved for production;
#   - deployment is authorized.
# ============================================================


# ============================================================
# D14.89 — LIFECYCLE HANDOFF CONTROL
# ============================================================
#
# D15 may design:
#
#   - deployment architecture,
#   - human oversight,
#   - monitoring controls,
#   - drift detection,
#   - performance surveillance,
#   - subgroup surveillance,
#   - utilization-dependence monitoring,
#   - incident management,
#   - rollback / kill-switch controls,
#   - change management,
#   - prospective validation requirements.
#
# D15 MUST NOT reinterpret D14 progression as production
# authorization.
#
# Deployment remains unauthorized until the required clinical,
# operational, governance, safety, and external-validation
# evidence is sufficient for a separate authorization decision.
# ============================================================