"""
ReadmitAI Clinical Intelligence
D14 Model Evidence Service

Purpose
-------
Expose authoritative locked-test performance, validation-to-test
comparison, and final D14 governance evidence to the ReadmitAI
Model Evidence workspace.

Governance principles
---------------------
- Reads persisted D14 evidence artifacts.
- Does not recompute model performance.
- Does not retrain or modify the frozen candidate.
- Does not retune the frozen operating threshold.
- Preserves internal-vs-external validation boundaries.
- Preserves deployment and clinical-effectiveness limitations.
"""

from pathlib import Path
from typing import Any
import json

import pandas as pd


# ============================================================
# AUTHORITATIVE D14 EVIDENCE SOURCES
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PERFORMANCE_PATH = (
    PROJECT_ROOT
    / "reports"
    / "tables"
    / "D14_locked_test_performance.csv"
)

COMPARISON_PATH = (
    PROJECT_ROOT
    / "reports"
    / "tables"
    / "D14_validation_test_comparison.csv"
)

GOVERNANCE_PATH = (
    PROJECT_ROOT
    / "reports"
    / "governance"
    / "D14_final_governance_record.json"
)


# ============================================================
# EXPECTED FROZEN CANDIDATE IDENTITY
# ============================================================

EXPECTED_REGISTRY_ID = "DIABETES_READMISSION_XGB_D13_V1"

EXPECTED_CANDIDATE_SHA256 = (
    "9349A52C715517666540C0D5B1EDB148"
    "D48709C0FC2CC77BE9B53F10FE373679"
)

EXPECTED_THRESHOLD = 0.12


# ============================================================
# REQUIRED PERFORMANCE FIELDS
# ============================================================

REQUIRED_PERFORMANCE_FIELDS = (
    "registry_id",
    "candidate_system_sha256",
    "frozen_threshold",
    "encounter_count",
    "positive_count",
    "negative_count",
    "prevalence",
    "pr_auc",
    "roc_auc",
    "brier_score",
    "log_loss",
    "true_positives",
    "false_positives",
    "true_negatives",
    "false_negatives",
    "sensitivity",
    "specificity",
    "precision_ppv",
    "negative_predictive_value",
    "f1_score",
    "alert_count",
    "alert_rate",
    "alerts_per_100_encounters",
    "number_needed_to_evaluate",
)


# ============================================================
# LOAD LOCKED-TEST PERFORMANCE
# ============================================================

def load_d14_locked_test_performance() -> dict[str, Any]:
    """
    Load the persisted D14 locked-test performance record.
    """

    if not PERFORMANCE_PATH.exists():
        raise FileNotFoundError(
            "D14 locked-test performance artifact not found: "
            f"{PERFORMANCE_PATH}"
        )

    performance_df = pd.read_csv(PERFORMANCE_PATH)

    if len(performance_df) != 1:
        raise RuntimeError(
            "D14 locked-test performance artifact must contain "
            "exactly one frozen-candidate record."
        )

    missing_fields = [
        field
        for field in REQUIRED_PERFORMANCE_FIELDS
        if field not in performance_df.columns
    ]

    if missing_fields:
        raise RuntimeError(
            "D14 locked-test performance artifact is missing "
            "required fields: "
            + ", ".join(missing_fields)
        )

    record = performance_df.iloc[0].to_dict()

    # --------------------------------------------------------
    # Frozen candidate identity controls
    # --------------------------------------------------------

    if str(record["registry_id"]) != EXPECTED_REGISTRY_ID:
        raise RuntimeError(
            "D14 performance registry identity does not match "
            "the frozen ReadmitAI candidate."
        )

    if (
        str(record["candidate_system_sha256"])
        != EXPECTED_CANDIDATE_SHA256
    ):
        raise RuntimeError(
            "D14 candidate-system hash does not match the "
            "registered frozen candidate."
        )

    threshold = float(record["frozen_threshold"])

    if abs(threshold - EXPECTED_THRESHOLD) > 1e-12:
        raise RuntimeError(
            "D14 frozen threshold does not match the governed "
            f"operating point. Observed={threshold}"
        )

    return record


# ============================================================
# LOAD VALIDATION → LOCKED-TEST COMPARISON
# ============================================================

def load_d14_validation_test_comparison() -> pd.DataFrame:
    """
    Load persisted D14 validation-versus-locked-test comparison.
    """

    if not COMPARISON_PATH.exists():
        raise FileNotFoundError(
            "D14 validation/test comparison artifact not found: "
            f"{COMPARISON_PATH}"
        )

    comparison_df = pd.read_csv(COMPARISON_PATH)

    required_columns = {
        "metric",
        "validation",
        "locked_test",
        "absolute_difference_test_minus_validation",
    }

    missing_columns = (
        required_columns
        - set(comparison_df.columns)
    )

    if missing_columns:
        raise RuntimeError(
            "D14 validation/test comparison artifact is missing "
            "required columns: "
            + ", ".join(sorted(missing_columns))
        )

    if comparison_df.empty:
        raise RuntimeError(
            "D14 validation/test comparison artifact is empty."
        )

    return comparison_df


# ============================================================
# LOAD FINAL D14 GOVERNANCE RECORD
# ============================================================

def load_d14_governance_record() -> dict[str, Any]:
    """
    Load the final persisted D14 governance record.
    """

    if not GOVERNANCE_PATH.exists():
        raise FileNotFoundError(
            "D14 final governance record not found: "
            f"{GOVERNANCE_PATH}"
        )

    with GOVERNANCE_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        governance = json.load(file)

    if not isinstance(governance, dict):
        raise RuntimeError(
            "D14 governance record did not load as a dictionary."
        )

    required_fields = (
        "candidate_system_sha256",
        "clinical_effectiveness_established",
        "clinical_effectiveness_status",
        "deployment_authorized",
        "deployment_status",
        "disposition",
        "evaluation_mode",
        "evaluation_partition",
        "external_validation_completed",
        "external_validation_status",
        "gate_integrity_status",
        "internal_validation_classification",
        "registry_id",
        "residual_risk_count",
        "residual_risks",
        "stage_id",
        "stage_name",
        "unresolved_residual_risk_count",
    )

    missing_fields = [
        field
        for field in required_fields
        if field not in governance
    ]

    if missing_fields:
        raise RuntimeError(
            "D14 governance record is missing required fields: "
            + ", ".join(missing_fields)
        )

    if governance["registry_id"] != EXPECTED_REGISTRY_ID:
        raise RuntimeError(
            "D14 governance registry identity does not match "
            "the frozen candidate."
        )

    if (
        governance["candidate_system_sha256"]
        != EXPECTED_CANDIDATE_SHA256
    ):
        raise RuntimeError(
            "D14 governance candidate hash does not match "
            "the frozen candidate."
        )

    return governance


# ============================================================
# APPLICATION-READY MODEL EVIDENCE
# ============================================================

def get_model_evidence() -> dict[str, Any]:
    """
    Return application-ready D14 model evidence.

    All quantitative values originate from persisted D14 evidence.
    """

    performance = load_d14_locked_test_performance()
    comparison_df = load_d14_validation_test_comparison()
    governance = load_d14_governance_record()

    residual_risks = governance["residual_risks"]

    if not isinstance(residual_risks, list):
        raise RuntimeError(
            "D14 residual risk register is not represented as a list."
        )

    if len(residual_risks) != int(
        governance["residual_risk_count"]
    ):
        raise RuntimeError(
            "D14 residual-risk count does not match the "
            "persisted residual-risk register."
        )

    return {
        # ----------------------------------------------------
        # Candidate identity
        # ----------------------------------------------------
        "registry_id":
            str(performance["registry_id"]),

        "candidate_system_sha256":
            str(performance["candidate_system_sha256"]),

        "frozen_threshold":
            float(performance["frozen_threshold"]),

        # ----------------------------------------------------
        # Locked-test cohort
        # ----------------------------------------------------
        "encounter_count":
            int(performance["encounter_count"]),

        "positive_count":
            int(performance["positive_count"]),

        "negative_count":
            int(performance["negative_count"]),

        "prevalence":
            float(performance["prevalence"]),

        # ----------------------------------------------------
        # Discrimination / probability performance
        # ----------------------------------------------------
        "pr_auc":
            float(performance["pr_auc"]),

        "roc_auc":
            float(performance["roc_auc"]),

        "brier_score":
            float(performance["brier_score"]),

        "log_loss":
            float(performance["log_loss"]),

        # ----------------------------------------------------
        # Frozen operating-point performance
        # ----------------------------------------------------
        "sensitivity":
            float(performance["sensitivity"]),

        "specificity":
            float(performance["specificity"]),

        "precision_ppv":
            float(performance["precision_ppv"]),

        "negative_predictive_value":
            float(
                performance["negative_predictive_value"]
            ),

        "f1_score":
            float(performance["f1_score"]),

        # ----------------------------------------------------
        # Confusion matrix
        # ----------------------------------------------------
        "true_positives":
            int(performance["true_positives"]),

        "false_positives":
            int(performance["false_positives"]),

        "true_negatives":
            int(performance["true_negatives"]),

        "false_negatives":
            int(performance["false_negatives"]),

        # ----------------------------------------------------
        # Operational consequences
        # ----------------------------------------------------
        "alert_count":
            int(performance["alert_count"]),

        "alert_rate":
            float(performance["alert_rate"]),

        "alerts_per_100_encounters":
            float(
                performance[
                    "alerts_per_100_encounters"
                ]
            ),

        "number_needed_to_evaluate":
            float(
                performance[
                    "number_needed_to_evaluate"
                ]
            ),

        # ----------------------------------------------------
        # Validation-to-test comparison
        # ----------------------------------------------------
        "validation_test_comparison":
            comparison_df.to_dict(
                orient="records"
            ),

        # ----------------------------------------------------
        # Governance status
        # ----------------------------------------------------
        "evaluation_mode":
            str(governance["evaluation_mode"]),

        "evaluation_partition":
            str(governance["evaluation_partition"]),

        "stage_id":
            str(governance["stage_id"]),

        "stage_name":
            str(governance["stage_name"]),

        "gate_integrity_status":
            str(
                governance[
                    "gate_integrity_status"
                ]
            ),

        "internal_validation_classification":
            str(
                governance[
                    "internal_validation_classification"
                ]
            ),

        "external_validation_completed":
            bool(
                governance[
                    "external_validation_completed"
                ]
            ),

        "external_validation_status":
            str(
                governance[
                    "external_validation_status"
                ]
            ),

        "clinical_effectiveness_established":
            bool(
                governance[
                    "clinical_effectiveness_established"
                ]
            ),

        "clinical_effectiveness_status":
            str(
                governance[
                    "clinical_effectiveness_status"
                ]
            ),

        "deployment_authorized":
            bool(
                governance[
                    "deployment_authorized"
                ]
            ),

        "deployment_status":
            str(
                governance[
                    "deployment_status"
                ]
            ),

        "disposition":
            str(governance["disposition"]),

        # ----------------------------------------------------
        # Residual risks
        # ----------------------------------------------------
        "residual_risk_count":
            int(
                governance[
                    "residual_risk_count"
                ]
            ),

        "unresolved_residual_risk_count":
            int(
                governance[
                    "unresolved_residual_risk_count"
                ]
            ),

        "residual_risks":
            residual_risks,

        # ----------------------------------------------------
        # Evidence provenance
        # ----------------------------------------------------
        "performance_evidence_source":
            "D14_locked_test_performance.csv",

        "comparison_evidence_source":
            "D14_validation_test_comparison.csv",

        "governance_evidence_source":
            "D14_final_governance_record.json",

        "runtime_performance_recomputed":
            False,

        "model_retrained":
            False,

        "threshold_retuned":
            False,
    }