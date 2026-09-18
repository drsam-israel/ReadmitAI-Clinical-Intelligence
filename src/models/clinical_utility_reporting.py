# ============================================================
# D9 — CLINICAL UTILITY & THRESHOLD GOVERNANCE REPORTING
# ============================================================
#
# Purpose:
#   Persist reproducible D9 evidence derived from the governed
#   clinical-utility analysis.
#
# Architecture:
#
#   clinical_utility.py
#           ↓
#   clinical_utility_reporting.py
#           ↓
#   CSV evidence tables
#   Markdown governance documents
#   YAML lifecycle manifest
#
# Governance boundary:
#   - VALIDATION only
#   - Frozen D8 model
#   - No model retraining
#   - No hyperparameter retuning
#   - No preprocessing refit
#   - Locked TEST remains untouched
#   - Development threshold != deployment authorization
# ============================================================

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import yaml

from src.models.clinical_utility import (
    D9_STAGE,
    D9_STAGE_NAME,
    D9_EXPECTED_MODEL_SHA256,
    D9_EXPECTED_SELECTED_MODEL,
    D9_EXPECTED_VALIDATION_ENCOUNTERS,
    D9_EXPECTED_TRANSFORMED_FEATURE_COUNT,
    D9_THRESHOLD_SELECTION_RULE,
    D9_THRESHOLD_DECISION_CLASSIFICATION,
    D9_DEVELOPMENT_MINIMUM_SENSITIVITY,
    D9_DEVELOPMENT_MAXIMUM_ALERTS_PER_100,
    build_d9_validation_prediction_bundle,
    build_d9_threshold_performance_table,
    build_d9_reference_threshold_table,
    evaluate_d9_operating_scenarios,
    build_d9_capacity_frontier,
    select_d9_development_threshold,
    build_d9_decision_curve_table,
    build_d9_selected_threshold_decision_evidence,
    build_d9_calibration_table,
    build_d9_calibration_summary,
)


# ============================================================
# D9.35 — ARTIFACT PATH CONTRACT
# ============================================================

D9_MANIFEST_PATH = Path(
    "artifacts/manifests/"
    "D9_clinical_utility_threshold_governance_manifest.yaml"
)

D9_CONTRACT_PATH = Path(
    "reports/governance/"
    "D9_clinical_utility_threshold_governance_contract.md"
)

D9_GATE_DECISION_PATH = Path(
    "reports/governance/"
    "D9_clinical_utility_threshold_governance_gate_decision.md"
)

D9_THRESHOLD_PERFORMANCE_PATH = Path(
    "reports/tables/"
    "D9_threshold_performance.csv"
)

D9_REFERENCE_THRESHOLD_PATH = Path(
    "reports/tables/"
    "D9_reference_threshold_tradeoffs.csv"
)

D9_OPERATING_SCENARIO_PATH = Path(
    "reports/tables/"
    "D9_operating_scenario_analysis.csv"
)

D9_CAPACITY_FRONTIER_PATH = Path(
    "reports/tables/"
    "D9_capacity_frontier.csv"
)

D9_THRESHOLD_DECISION_PATH = Path(
    "reports/tables/"
    "D9_development_threshold_decision.csv"
)

D9_DECISION_CURVE_PATH = Path(
    "reports/tables/"
    "D9_decision_curve_analysis.csv"
)

D9_CALIBRATION_TABLE_PATH = Path(
    "reports/tables/"
    "D9_calibration_table.csv"
)

D9_CALIBRATION_SUMMARY_PATH = Path(
    "reports/tables/"
    "D9_calibration_summary.csv"
)


D9_REQUIRED_EVIDENCE_PATHS = (
    D9_MANIFEST_PATH,
    D9_CONTRACT_PATH,
    D9_GATE_DECISION_PATH,
    D9_THRESHOLD_PERFORMANCE_PATH,
    D9_REFERENCE_THRESHOLD_PATH,
    D9_OPERATING_SCENARIO_PATH,
    D9_CAPACITY_FRONTIER_PATH,
    D9_THRESHOLD_DECISION_PATH,
    D9_DECISION_CURVE_PATH,
    D9_CALIBRATION_TABLE_PATH,
    D9_CALIBRATION_SUMMARY_PATH,
)


# ============================================================
# D9.36 — DIRECTORY INITIALIZATION
# ============================================================

def ensure_d9_reporting_directories() -> None:
    """
    Ensure all D9 evidence directories exist.
    """

    for path in D9_REQUIRED_EVIDENCE_PATHS:
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )


# ============================================================
# D9.37 — SERIALIZATION HELPERS
# ============================================================

def _d9_python_scalar(
    value: Any,
) -> Any:
    """
    Convert NumPy scalar values into standard Python values
    suitable for YAML and evidence serialization.
    """

    if isinstance(value, np.generic):
        return value.item()

    return value


def _d9_serializable_mapping(
    mapping: dict[str, Any],
) -> dict[str, Any]:
    """
    Convert a flat result mapping into serialization-safe
    Python values.
    """

    result = {}

    for key, value in mapping.items():

        value = _d9_python_scalar(
            value
        )

        if isinstance(value, Path):
            value = str(value)

        result[key] = value

    return result


# ============================================================
# D9.38 — BUILD COMPLETE REPORTING EVIDENCE BUNDLE
# ============================================================

def build_d9_reporting_evidence_bundle() -> dict[str, Any]:
    """
    Build all governed D9 evidence in memory before persistence.

    This function does not access locked TEST.
    """

    prediction_bundle = (
        build_d9_validation_prediction_bundle()
    )

    threshold_performance = (
        build_d9_threshold_performance_table(
            prediction_bundle
        )
    )

    reference_thresholds = (
        build_d9_reference_threshold_table(
            prediction_bundle
        )
    )

    operating_scenarios = (
        evaluate_d9_operating_scenarios(
            threshold_performance
        )
    )

    capacity_frontier = (
        build_d9_capacity_frontier(
            threshold_performance
        )
    )

    threshold_decision = (
        select_d9_development_threshold(
            threshold_performance
        )
    )

    decision_curve = (
        build_d9_decision_curve_table(
            prediction_bundle
        )
    )

    selected_threshold_decision_evidence = (
        build_d9_selected_threshold_decision_evidence()
    )

    calibration_table = (
        build_d9_calibration_table(
            prediction_bundle
        )
    )

    calibration_summary = (
        build_d9_calibration_summary(
            prediction_bundle
        )
    )

    return {
        "prediction_bundle":
            prediction_bundle,

        "threshold_performance":
            threshold_performance,

        "reference_thresholds":
            reference_thresholds,

        "operating_scenarios":
            operating_scenarios,

        "capacity_frontier":
            capacity_frontier,

        "threshold_decision":
            threshold_decision,

        "decision_curve":
            decision_curve,

        "selected_threshold_decision_evidence":
            selected_threshold_decision_evidence,

        "calibration_table":
            calibration_table,

        "calibration_summary":
            calibration_summary,
    }


# ============================================================
# D9.39 — PERSIST TABULAR EVIDENCE
# ============================================================

def persist_d9_tabular_evidence(
    evidence_bundle: dict[str, Any],
) -> dict[str, str]:
    """
    Persist governed D9 tabular evidence as CSV files.
    """

    ensure_d9_reporting_directories()

    threshold_performance = evidence_bundle[
        "threshold_performance"
    ]

    reference_thresholds = evidence_bundle[
        "reference_thresholds"
    ]

    operating_scenarios = evidence_bundle[
        "operating_scenarios"
    ]

    capacity_frontier = evidence_bundle[
        "capacity_frontier"
    ]

    threshold_decision = evidence_bundle[
        "threshold_decision"
    ]

    decision_curve = evidence_bundle[
        "decision_curve"
    ]

    calibration_table = evidence_bundle[
        "calibration_table"
    ]

    calibration_summary = evidence_bundle[
        "calibration_summary"
    ]

    threshold_performance.to_csv(
        D9_THRESHOLD_PERFORMANCE_PATH,
        index=False,
    )

    reference_thresholds.to_csv(
        D9_REFERENCE_THRESHOLD_PATH,
        index=False,
    )

    operating_scenarios.to_csv(
        D9_OPERATING_SCENARIO_PATH,
        index=False,
    )

    capacity_frontier.to_csv(
        D9_CAPACITY_FRONTIER_PATH,
        index=False,
    )

    pd.DataFrame(
        [
            _d9_serializable_mapping(
                threshold_decision
            )
        ]
    ).to_csv(
        D9_THRESHOLD_DECISION_PATH,
        index=False,
    )

    decision_curve.to_csv(
        D9_DECISION_CURVE_PATH,
        index=False,
    )

    calibration_table.to_csv(
        D9_CALIBRATION_TABLE_PATH,
        index=False,
    )

    pd.DataFrame(
        [
            _d9_serializable_mapping(
                calibration_summary
            )
        ]
    ).to_csv(
        D9_CALIBRATION_SUMMARY_PATH,
        index=False,
    )

    return {
        "threshold_performance":
            str(
                D9_THRESHOLD_PERFORMANCE_PATH
            ),

        "reference_threshold_tradeoffs":
            str(
                D9_REFERENCE_THRESHOLD_PATH
            ),

        "operating_scenario_analysis":
            str(
                D9_OPERATING_SCENARIO_PATH
            ),

        "capacity_frontier":
            str(
                D9_CAPACITY_FRONTIER_PATH
            ),

        "development_threshold_decision":
            str(
                D9_THRESHOLD_DECISION_PATH
            ),

        "decision_curve_analysis":
            str(
                D9_DECISION_CURVE_PATH
            ),

        "calibration_table":
            str(
                D9_CALIBRATION_TABLE_PATH
            ),

        "calibration_summary":
            str(
                D9_CALIBRATION_SUMMARY_PATH
            ),
    }


# ============================================================
# D9.40 — GOVERNANCE CONTRACT DOCUMENT
# ============================================================

def build_d9_governance_contract(
    evidence_bundle: dict[str, Any],
) -> str:
    """
    Build the D9 Clinical Utility & Threshold Governance
    contract.
    """

    prediction = evidence_bundle[
        "prediction_bundle"
    ]

    threshold = evidence_bundle[
        "threshold_decision"
    ]

    calibration = evidence_bundle[
        "calibration_summary"
    ]

    return f"""# D9 — Clinical Utility & Threshold Governance Contract

## 1. Lifecycle Stage

**Stage:** {D9_STAGE}  
**Stage Name:** {D9_STAGE_NAME}

D9 evaluates the clinical and operational consequences of the
frozen D8 development candidate using held-out VALIDATION data.

D9 does not perform final locked-test evaluation and does not
authorize clinical deployment.

## 2. Frozen Upstream Dependencies

**Selected D8 model:** {D9_EXPECTED_SELECTED_MODEL}  
**Frozen model SHA256:** `{D9_EXPECTED_MODEL_SHA256}`  
**Validation encounters:** {D9_EXPECTED_VALIDATION_ENCOUNTERS:,}  
**Transformed feature count:** {D9_EXPECTED_TRANSFORMED_FEATURE_COUNT}

D9 consumes the frozen D7 preprocessing representation and
frozen D8 model without refitting either component.

## 3. Data Partition Governance

Threshold development and clinical-utility analysis are
performed on **VALIDATION only**.

The locked TEST partition remains inaccessible during D9.

TEST is reserved for the later authorized locked-test
evaluation stage.

## 4. Intended Clinical Use

The model is intended to support clinician-reviewed
identification of hospitalized patients with diabetes who may
benefit from intensified 30-day readmission-prevention planning
before discharge.

Primary intended users include:

- discharge planning teams;
- care-management teams;
- treating clinicians.

The model is a **risk-prioritization aid**.

It must not autonomously determine discharge, treatment,
admission, denial of care, or other clinical-management
decisions.

## 5. Development Threshold Governance

**Development operating threshold:** {threshold["selected_threshold"]:.2f}

**Decision classification:**  
`{threshold["decision_classification"]}`

The threshold was derived using the following development-stage
analytical rule:

> {D9_THRESHOLD_SELECTION_RULE}

The analytical constraints were:

- minimum sensitivity: {D9_DEVELOPMENT_MINIMUM_SENSITIVITY:.0%};
- maximum alert burden:
  {D9_DEVELOPMENT_MAXIMUM_ALERTS_PER_100:.1f} alerts per
  100 eligible patients.

These constraints are development assumptions. They do not
represent an approved institutional staffing policy or clinical
standard.

## 6. Validation Operating Characteristics

At threshold **{threshold["selected_threshold"]:.2f}**:

- true positives: {threshold["true_positive"]:,};
- false positives: {threshold["false_positive"]:,};
- true negatives: {threshold["true_negative"]:,};
- false negatives: {threshold["false_negative"]:,};
- sensitivity: {threshold["sensitivity"]:.4f};
- specificity: {threshold["specificity"]:.4f};
- precision: {threshold["precision"]:.4f};
- negative predictive value:
  {threshold["negative_predictive_value"]:.4f};
- F1 score: {threshold["f1_score"]:.4f};
- alerts per 100 patients:
  {threshold["alerts_per_100_patients"]:.2f};
- number needed to evaluate:
  {threshold["number_needed_to_evaluate"]:.2f}.

The model therefore misses
**{threshold["false_negative"]:,} of
{prediction["validation_positive_count"]:,}**
observed 30-day readmissions at this development operating
point.

This limitation must remain visible in downstream clinical and
governance review.

## 7. Probability Calibration Evidence

Observed VALIDATION prevalence:
**{calibration["observed_prevalence"]:.4f}**

Mean predicted probability:
**{calibration["mean_predicted_probability"]:.4f}**

Brier score:
**{calibration["brier_score"]:.4f}**

Calibration intercept:
**{calibration["calibration_intercept"]:.4f}**

Calibration slope:
**{calibration["calibration_slope"]:.4f}**

The validation calibration assessment shows close alignment
between predicted and observed probabilities within this
development validation cohort.

This does not establish calibration on the locked TEST
partition, external institutions, future populations, or
deployment data.

No recalibration was performed in D9.

## 8. Decision-Curve Evidence

Decision-curve analysis is treated as exploratory
development-stage evidence.

It compares the frozen model against treat-all and treat-none
strategies while preserving the limitations of development-only
validation evidence.

Decision-curve evidence does not independently authorize
clinical deployment.

## 9. Explicit Prohibitions

D9 does not permit:

- model retraining;
- hyperparameter retuning;
- preprocessing refitting;
- locked TEST access;
- autonomous clinical decision-making;
- final clinical-performance claims;
- external-validity claims;
- deployment authorization.

## 10. Downstream Requirements

Before clinical deployment can be considered, the system
requires additional lifecycle evidence including:

- subgroup and fairness evaluation;
- robustness and transportability assessment;
- explainability assessment;
- model and artifact freeze;
- locked-test evaluation;
- deployment and monitoring governance.

D9 therefore establishes a governed **development operating
point**, not a production clinical threshold.
"""


# ============================================================
# D9.41 — GOVERNANCE GATE DECISION
# ============================================================

def build_d9_gate_decision(
    evidence_bundle: dict[str, Any],
) -> str:
    """
    Build the D9 lifecycle gate decision.
    """

    threshold = evidence_bundle[
        "threshold_decision"
    ]

    decision = evidence_bundle[
        "selected_threshold_decision_evidence"
    ]

    calibration = evidence_bundle[
        "calibration_summary"
    ]

    return f"""# D9 — Clinical Utility & Threshold Governance Gate Decision

## Gate Status

# PASS — AUTHORIZED TO PROCEED TO D10

D9 has produced sufficient development-stage evidence to
proceed to **D10 — Fairness & Subgroup Evaluation**.

This PASS is a lifecycle progression decision only.

It is **not** authorization for clinical deployment.

## Evidence Supporting the Gate

The frozen D8 `{D9_EXPECTED_SELECTED_MODEL}` development
candidate was evaluated on held-out VALIDATION without model
retraining, hyperparameter retuning, or preprocessing refitting.

The governed development operating threshold is:

**{threshold["selected_threshold"]:.2f}**

At this operating point:

- sensitivity:
  **{threshold["sensitivity"]:.2%}**
- specificity:
  **{threshold["specificity"]:.2%}**
- precision:
  **{threshold["precision"]:.2%}**
- negative predictive value:
  **{threshold["negative_predictive_value"]:.2%}**
- alerts per 100 patients:
  **{threshold["alerts_per_100_patients"]:.2f}**
- true positives:
  **{threshold["true_positive"]:,}**
- false positives:
  **{threshold["false_positive"]:,}**
- false negatives:
  **{threshold["false_negative"]:,}**

## Clinical Utility Evidence

At the selected development operating point:

- model net benefit:
  **{decision["model_net_benefit"]:.6f}**
- treat-all net benefit:
  **{decision["treat_all_net_benefit"]:.6f}**
- treat-none net benefit:
  **{decision["treat_none_net_benefit"]:.6f}**
- incremental net benefit versus best default:
  **{decision["incremental_net_benefit_vs_best_default"]:.6f}**

Within this VALIDATION analysis, the model exceeded both
default strategies under the decision-curve assumptions.

This remains exploratory development evidence.

## Calibration Evidence

- observed prevalence:
  **{calibration["observed_prevalence"]:.4f}**
- mean predicted probability:
  **{calibration["mean_predicted_probability"]:.4f}**
- Brier score:
  **{calibration["brier_score"]:.4f}**
- calibration intercept:
  **{calibration["calibration_intercept"]:.4f}**
- calibration slope:
  **{calibration["calibration_slope"]:.4f}**

Calibration is closely aligned on this held-out development
VALIDATION cohort.

No claim is made regarding calibration on TEST, external
institutions, or future populations.

## Material Clinical Limitation

At threshold **{threshold["selected_threshold"]:.2f}**, the model
misses **{threshold["false_negative"]:,}** observed 30-day
readmissions.

Sensitivity is therefore only
**{threshold["sensitivity"]:.2%}**.

The model must be framed as a **risk-prioritization aid**, not a
high-sensitivity screening system.

This limitation must remain explicit in D10-D15 evidence and in
any future portfolio or deployment documentation.

## Governance Conditions Carried Forward

The following remain prohibited:

- locked TEST access before the authorized lifecycle stage;
- autonomous clinical decision-making;
- deployment;
- institutional clinical-use claims;
- external-validity claims;
- threshold representation as an approved hospital policy.

## Gate Decision

**D9 PASS**

Authorized next lifecycle stage:

**D10 — Fairness & Subgroup Evaluation**

Clinical deployment authorization:

**NO**
"""


# ============================================================
# D9.42 — BUILD YAML MANIFEST
# ============================================================

def build_d9_manifest(
    evidence_bundle: dict[str, Any],
    persisted_tables: dict[str, str],
) -> dict[str, Any]:
    """
    Build the machine-readable D9 lifecycle manifest.
    """

    prediction = evidence_bundle[
        "prediction_bundle"
    ]

    threshold = evidence_bundle[
        "threshold_decision"
    ]

    decision = evidence_bundle[
        "selected_threshold_decision_evidence"
    ]

    calibration = evidence_bundle[
        "calibration_summary"
    ]

    return {
        "stage":
            D9_STAGE,

        "stage_name":
            D9_STAGE_NAME,

        "generated_at_utc":
            datetime.now(
                timezone.utc
            ).isoformat(),

        "upstream_dependencies": {
            "model":
                D9_EXPECTED_SELECTED_MODEL,

            "model_sha256":
                D9_EXPECTED_MODEL_SHA256,

            "d7_preprocessor_sha256":
                prediction[
                    "d7_preprocessor_sha256"
                ],

            "d7_schema_sha256":
                prediction[
                    "d7_schema_sha256"
                ],
        },

        "validation_partition": {
            "encounters":
                prediction[
                    "validation_encounter_count"
                ],

            "positive_outcomes":
                prediction[
                    "validation_positive_count"
                ],

            "prevalence":
                prediction[
                    "validation_prevalence"
                ],

            "transformed_features":
                prediction[
                    "transformed_feature_count"
                ],
        },

        "development_threshold": {
            "threshold":
                threshold[
                    "selected_threshold"
                ],

            "classification":
                threshold[
                    "decision_classification"
                ],

            "selection_partition":
                threshold[
                    "selection_partition"
                ],

            "selection_rule":
                threshold[
                    "selection_rule"
                ],

            "minimum_sensitivity_constraint":
                threshold[
                    "minimum_sensitivity_constraint"
                ],

            "maximum_alerts_per_100_constraint":
                threshold[
                    "maximum_alerts_per_100_constraint"
                ],

            "feasible_threshold_count":
                threshold[
                    "feasible_threshold_count"
                ],
        },

        "operating_characteristics": {
            "true_positive":
                threshold[
                    "true_positive"
                ],

            "false_positive":
                threshold[
                    "false_positive"
                ],

            "true_negative":
                threshold[
                    "true_negative"
                ],

            "false_negative":
                threshold[
                    "false_negative"
                ],

            "sensitivity":
                threshold[
                    "sensitivity"
                ],

            "specificity":
                threshold[
                    "specificity"
                ],

            "precision":
                threshold[
                    "precision"
                ],

            "negative_predictive_value":
                threshold[
                    "negative_predictive_value"
                ],

            "f1_score":
                threshold[
                    "f1_score"
                ],

            "alerts_per_100_patients":
                threshold[
                    "alerts_per_100_patients"
                ],

            "number_needed_to_evaluate":
                threshold[
                    "number_needed_to_evaluate"
                ],
        },

        "decision_curve": {
            "model_net_benefit":
                decision[
                    "model_net_benefit"
                ],

            "treat_all_net_benefit":
                decision[
                    "treat_all_net_benefit"
                ],

            "treat_none_net_benefit":
                decision[
                    "treat_none_net_benefit"
                ],

            "incremental_net_benefit_vs_best_default":
                decision[
                    "incremental_net_benefit_vs_best_default"
                ],

            "model_better_than_both_defaults":
                decision[
                    "model_better_than_both_defaults"
                ],

            "classification":
                decision[
                    "analysis_classification"
                ],
        },

        "calibration": {
            "observed_prevalence":
                calibration[
                    "observed_prevalence"
                ],

            "mean_predicted_probability":
                calibration[
                    "mean_predicted_probability"
                ],

            "brier_score":
                calibration[
                    "brier_score"
                ],

            "log_loss":
                calibration[
                    "log_loss"
                ],

            "weighted_absolute_calibration_error":
                calibration[
                    "weighted_absolute_calibration_error"
                ],

            "maximum_bin_calibration_error":
                calibration[
                    "maximum_bin_calibration_error"
                ],

            "calibration_intercept":
                calibration[
                    "calibration_intercept"
                ],

            "calibration_slope":
                calibration[
                    "calibration_slope"
                ],

            "model_recalibrated":
                False,
        },

        "governance": {
            "model_retrained":
                False,

            "hyperparameters_retuned":
                False,

            "preprocessor_refitted":
                False,

            "locked_test_accessed":
                False,

            "external_validation_completed":
                False,

            "institutional_approval_obtained":
                False,

            "autonomous_clinical_decision_permitted":
                False,

            "deployment_authorized":
                False,
        },

        "evidence_artifacts": {
            **persisted_tables,

            "governance_contract":
                str(
                    D9_CONTRACT_PATH
                ),

            "gate_decision":
                str(
                    D9_GATE_DECISION_PATH
                ),

            "manifest":
                str(
                    D9_MANIFEST_PATH
                ),
        },

        "gate": {
            "status":
                "PASS",

            "authorized_next_stage":
                "D10",

            "authorized_next_stage_name":
                "Fairness & Subgroup Evaluation",

            "clinical_deployment_authorized":
                False,
        },
    }


# ============================================================
# D9.43 — PERSIST GOVERNANCE DOCUMENTS
# ============================================================

def persist_d9_governance_documents(
    evidence_bundle: dict[str, Any],
    persisted_tables: dict[str, str],
) -> dict[str, str]:
    """
    Persist D9 Markdown governance documents and YAML manifest.
    """

    ensure_d9_reporting_directories()

    contract = (
        build_d9_governance_contract(
            evidence_bundle
        )
    )

    gate_decision = (
        build_d9_gate_decision(
            evidence_bundle
        )
    )

    manifest = (
        build_d9_manifest(
            evidence_bundle,
            persisted_tables,
        )
    )

    D9_CONTRACT_PATH.write_text(
        contract,
        encoding="utf-8",
    )

    D9_GATE_DECISION_PATH.write_text(
        gate_decision,
        encoding="utf-8",
    )

    D9_MANIFEST_PATH.write_text(
        yaml.safe_dump(
            manifest,
            sort_keys=False,
            allow_unicode=True,
        ),
        encoding="utf-8",
    )

    return {
        "governance_contract":
            str(
                D9_CONTRACT_PATH
            ),

        "gate_decision":
            str(
                D9_GATE_DECISION_PATH
            ),

        "manifest":
            str(
                D9_MANIFEST_PATH
            ),
    }


# ============================================================
# D9.44 — VALIDATE PERSISTED EVIDENCE PACKAGE
# ============================================================

def validate_d9_persisted_evidence_package(
    evidence_bundle: dict[str, Any],
) -> dict[str, Any]:
    """
    Validate existence and basic integrity of the complete
    persisted D9 evidence package.
    """

    threshold = evidence_bundle[
        "threshold_decision"
    ]

    checks = {
        "all_required_artifacts_exist":
            all(
                path.exists()
                for path
                in D9_REQUIRED_EVIDENCE_PATHS
            ),

        "all_required_artifacts_nonempty":
            all(
                path.exists()
                and path.stat().st_size > 0
                for path
                in D9_REQUIRED_EVIDENCE_PATHS
            ),

        "threshold_performance_has_50_rows":
            len(
                pd.read_csv(
                    D9_THRESHOLD_PERFORMANCE_PATH
                )
            )
            == 50,

        "reference_threshold_table_has_11_rows":
            len(
                pd.read_csv(
                    D9_REFERENCE_THRESHOLD_PATH
                )
            )
            == 11,

        "operating_scenario_table_has_4_rows":
            len(
                pd.read_csv(
                    D9_OPERATING_SCENARIO_PATH
                )
            )
            == 4,

        "capacity_frontier_has_8_rows":
            len(
                pd.read_csv(
                    D9_CAPACITY_FRONTIER_PATH
                )
            )
            == 8,

        "decision_curve_has_50_rows":
            len(
                pd.read_csv(
                    D9_DECISION_CURVE_PATH
                )
            )
            == 50,

        "calibration_table_has_10_rows":
            len(
                pd.read_csv(
                    D9_CALIBRATION_TABLE_PATH
                )
            )
            == 10,

        "development_threshold_is_0_12":
            np.isclose(
                threshold[
                    "selected_threshold"
                ],
                0.12,
            ),

        "locked_test_not_accessed":
            evidence_bundle[
                "prediction_bundle"
            ][
                "locked_test_accessed"
            ]
            is False,

        "deployment_not_authorized":
            threshold[
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
        "required_artifact_count":
            len(
                D9_REQUIRED_EVIDENCE_PATHS
            ),

        "selected_development_threshold":
            float(
                threshold[
                    "selected_threshold"
                ]
            ),

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
            "D9 persisted evidence validation failed: "
            f"{failed_checks}"
        )

    return result


# ============================================================
# D9.45 — COMPLETE D9 REPORTING ORCHESTRATION
# ============================================================

def run_d9_reporting_pipeline() -> dict[str, Any]:
    """
    Generate, persist, and validate the complete D9 evidence
    package.

    This function is the authoritative D9 reporting
    orchestration entry point.
    """

    ensure_d9_reporting_directories()

    evidence_bundle = (
        build_d9_reporting_evidence_bundle()
    )

    persisted_tables = (
        persist_d9_tabular_evidence(
            evidence_bundle
        )
    )

    governance_documents = (
        persist_d9_governance_documents(
            evidence_bundle,
            persisted_tables,
        )
    )

    validation = (
        validate_d9_persisted_evidence_package(
            evidence_bundle
        )
    )

    return {
        "stage":
            D9_STAGE,

        "stage_name":
            D9_STAGE_NAME,

        "selected_model":
            D9_EXPECTED_SELECTED_MODEL,

        "model_sha256":
            D9_EXPECTED_MODEL_SHA256,

        "validation_encounter_count":
            int(
                evidence_bundle[
                    "prediction_bundle"
                ][
                    "validation_encounter_count"
                ]
            ),

        "selected_development_threshold":
            float(
                evidence_bundle[
                    "threshold_decision"
                ][
                    "selected_threshold"
                ]
            ),

        "sensitivity":
            float(
                evidence_bundle[
                    "threshold_decision"
                ][
                    "sensitivity"
                ]
            ),

        "specificity":
            float(
                evidence_bundle[
                    "threshold_decision"
                ][
                    "specificity"
                ]
            ),

        "precision":
            float(
                evidence_bundle[
                    "threshold_decision"
                ][
                    "precision"
                ]
            ),

        "alerts_per_100_patients":
            float(
                evidence_bundle[
                    "threshold_decision"
                ][
                    "alerts_per_100_patients"
                ]
            ),

        "false_negative":
            int(
                evidence_bundle[
                    "threshold_decision"
                ][
                    "false_negative"
                ]
            ),

        "model_net_benefit":
            float(
                evidence_bundle[
                    "selected_threshold_decision_evidence"
                ][
                    "model_net_benefit"
                ]
            ),

        "brier_score":
            float(
                evidence_bundle[
                    "calibration_summary"
                ][
                    "brier_score"
                ]
            ),

        "calibration_intercept":
            float(
                evidence_bundle[
                    "calibration_summary"
                ][
                    "calibration_intercept"
                ]
            ),

        "calibration_slope":
            float(
                evidence_bundle[
                    "calibration_summary"
                ][
                    "calibration_slope"
                ]
            ),

        "persisted_tables":
            persisted_tables,

        "governance_documents":
            governance_documents,

        "required_artifact_count":
            validation[
                "required_artifact_count"
            ],

        "locked_test_accessed":
            False,

        "deployment_authorized":
            False,

        "failed_checks":
            validation[
                "failed_checks"
            ],

        "validation_status":
            validation[
                "validation_status"
            ],
    }


# ============================================================
# D9.46 — COMMAND-LINE ENTRY POINT
# ============================================================

if __name__ == "__main__":

    import pprint

    pprint.pp(
        run_d9_reporting_pipeline()
    )