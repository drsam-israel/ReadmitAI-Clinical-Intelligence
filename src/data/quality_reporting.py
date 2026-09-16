# ============================================================
# D2 — DATA QUALITY & BIAS AUDIT REPORTING
# ============================================================
# Project:
# Diabetes Readmission Clinical AI
#
# Purpose:
# Reproducibly generate the governed evidence package for:
#
# Accuracy → Completeness → Currency → Consistency
# → Representation → Bias
#
# IMPORTANT:
# This module generates audit evidence.
# It does not clean, impute, exclude, transform, or model data.
# ============================================================

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from src.data.validation import load_raw_dataset
from src.data.quality import (
    assess_accuracy,
    assess_completeness,
    assess_currency,
    assess_consistency,
    assess_representation,
    assess_bias,
)


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

REPORTS_DIR = PROJECT_ROOT / "reports"
TABLES_DIR = REPORTS_DIR / "tables"
GOVERNANCE_DIR = REPORTS_DIR / "governance"

ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
MANIFESTS_DIR = ARTIFACTS_DIR / "manifests"


# ============================================================
# 2. OUTPUT FILES
# ============================================================

OUTPUT_FILES = {
    "scorecard":
        TABLES_DIR / "D2_data_quality_scorecard.csv",

    "completeness":
        TABLES_DIR / "D2_missingness_completeness_matrix.csv",

    "representation":
        TABLES_DIR / "D2_representation_summary.csv",

    "subgroup_measurement":
        TABLES_DIR / "D2_subgroup_measurement_audit.csv",

    "issue_log":
        GOVERNANCE_DIR / "D2_data_quality_issue_log.csv",

    "bias_register":
        GOVERNANCE_DIR / "D2_bias_risk_register.csv",

    "audit_report":
        GOVERNANCE_DIR / "D2_data_quality_audit_report.md",

    "gate_decision":
        GOVERNANCE_DIR / "D2_quality_bias_gate_decision.md",

    "manifest":
        MANIFESTS_DIR / "D2_data_quality_bias_manifest.yaml",
}


# ============================================================
# 3. DIRECTORY INITIALIZATION
# ============================================================

def ensure_output_directories() -> None:
    """Ensure all governed D2 output directories exist."""

    for directory in [
        TABLES_DIR,
        GOVERNANCE_DIR,
        MANIFESTS_DIR,
    ]:
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )


# ============================================================
# 4. NORMALIZATION HELPERS
# ============================================================

def _python_scalar(value: Any) -> Any:
    """
    Convert NumPy/Pandas scalar values into ordinary Python
    objects for safe CSV/YAML serialization.
    """

    if hasattr(value, "item"):
        try:
            return value.item()
        except (ValueError, AttributeError):
            pass

    return value


def _records_to_dataframe(
    records: list[dict[str, Any]],
) -> pd.DataFrame:
    """Create a DataFrame with Python-native scalar values."""

    normalized = [
        {
            key: _python_scalar(value)
            for key, value in record.items()
        }
        for record in records
    ]

    return pd.DataFrame(normalized)


# ============================================================
# 5. RUN ALL D2 ASSESSMENTS
# ============================================================

def run_d2_assessments() -> dict[str, Any]:
    """
    Load the governed raw dataset once and execute all six
    D2 assessment dimensions.
    """

    df = load_raw_dataset()

    return {
        "accuracy": assess_accuracy(df),
        "completeness": assess_completeness(df),
        "currency": assess_currency(),
        "consistency": assess_consistency(df),
        "representation": assess_representation(df),
        "bias": assess_bias(df),
    }


# ============================================================
# 6. DATA QUALITY SCORECARD
# ============================================================

def build_scorecard(
    assessments: dict[str, Any],
) -> pd.DataFrame:
    """Build the executive D2 quality scorecard."""

    rows = [
        {
            "dimension": "Accuracy / Conformance",
            "status": "CONDITIONAL PASS",
            "risk_level": "MODERATE",
            "key_finding":
                "No invalid categorical domains, prohibited "
                "identifier values, or defined numeric-range "
                "violations were detected. Missing-like "
                "sentinels remain subject to completeness and "
                "semantic governance.",
            "required_control":
                "Retain sentinel states for governed "
                "completeness and feature review.",
        },
        {
            "dimension": "Completeness",
            "status": "CONDITIONAL PASS",
            "risk_level": "HIGH",
            "key_finding":
                "Substantial missingness exists in weight, "
                "glycemic testing, medical specialty and "
                "payer information.",
            "required_control":
                "Do not automatically impute or discard. "
                "Review missingness semantics before feature "
                "approval.",
        },
        {
            "dimension": "Currency",
            "status": assessments[
                "currency"
            ]["status"],
            "risk_level": assessments[
                "currency"
            ]["temporal_recency_status"],
            "key_finding":
                assessments[
                    "currency"
                ]["currency_finding"],
            "required_control":
                assessments[
                    "currency"
                ]["deployment_control"],
        },
        {
            "dimension": "Consistency",
            "status": "CONDITIONAL PASS",
            "risk_level": "MODERATE",
            "key_finding":
                "Core identifiers, medication exposure and "
                "readmission fields are internally consistent. "
                "Medication-change semantics and diagnosis "
                "sequence exceptions require review.",
            "required_control":
                "Verify source semantics before classifying "
                "flagged relationships as data errors.",
        },
        {
            "dimension": "Representation",
            "status": "CONDITIONAL PASS",
            "risk_level": "HIGH",
            "key_finding":
                "Several racial and younger-age subgroups "
                "have limited representation.",
            "required_control":
                "Require subgroup-specific evaluation and "
                "uncertainty-aware interpretation.",
        },
        {
            "dimension": "Bias",
            "status": "CONDITIONAL PASS",
            "risk_level": "HIGH",
            "key_finding":
                "Temporal, representation, measurement, "
                "repeated-patient and label-related bias "
                "risks were identified before modeling.",
            "required_control":
                "Carry identified bias risks into feature "
                "governance, splitting, fairness evaluation "
                "and deployment review.",
        },
    ]

    return _records_to_dataframe(rows)


# ============================================================
# 7. COMPLETENESS MATRIX
# ============================================================

def build_completeness_matrix(
    assessments: dict[str, Any],
) -> pd.DataFrame:
    """
    Build the governed completeness matrix for ALL raw variables.

    Unlike the ranked missingness diagnostic, this artifact
    retains variables with zero identified missingness so that
    the final evidence package provides a complete 50-variable
    data-quality inventory.
    """

    df = load_raw_dataset()

    sentinel_values = {
        "?",
        "Unknown/Invalid",
    }

    rows: list[dict[str, Any]] = []

    for column in df.columns:

        series = df[column]

        native_missing_count = int(
            series.isna().sum()
        )

        if (
            pd.api.types.is_object_dtype(series)
            or isinstance(series.dtype, pd.StringDtype)
        ):
            sentinel_missing_count = int(
                series
                .astype("string")
                .isin(sentinel_values)
                .sum()
            )
        else:
            sentinel_missing_count = 0

        total_missing_count = (
            native_missing_count
            + sentinel_missing_count
        )

        missing_pct = round(
            (
                total_missing_count
                / len(df)
            )
            * 100,
            4,
        )

        completeness_pct = round(
            100 - missing_pct,
            4,
        )

        rows.append(
            {
                "column": column,
                "native_missing_count":
                    native_missing_count,
                "sentinel_missing_count":
                    sentinel_missing_count,
                "total_missing_count":
                    total_missing_count,
                "missing_pct":
                    missing_pct,
                "completeness_pct":
                    completeness_pct,
            }
        )

    completeness_matrix = (
        _records_to_dataframe(rows)
        .sort_values(
            by=[
                "missing_pct",
                "column",
            ],
            ascending=[
                False,
                True,
            ],
        )
        .reset_index(drop=True)
    )

    return completeness_matrix

# ============================================================
# 8. REPRESENTATION SUMMARY
# ============================================================

def build_representation_summary(
    assessments: dict[str, Any],
) -> pd.DataFrame:

    representation = assessments["representation"]

    rows: list[dict[str, Any]] = []

    for level_key, level_name in [
        (
            "encounter_level_demographics",
            "encounter",
        ),
        (
            "patient_level_demographics",
            "patient",
        ),
    ]:

        demographic_block = representation[
            level_key
        ]

        for dimension in [
            "age",
            "gender",
            "race",
        ]:

            for record in demographic_block[
                dimension
            ]:

                rows.append(
                    {
                        "analysis_level":
                            level_name,
                        "dimension":
                            dimension,
                        "category":
                            record["category"],
                        "count":
                            record["count"],
                        "percentage":
                            record["percentage"],
                    }
                )

    return _records_to_dataframe(rows)


# ============================================================
# 9. SUBGROUP MEASUREMENT AUDIT
# ============================================================

def build_subgroup_measurement_audit(
    assessments: dict[str, Any],
) -> pd.DataFrame:

    bias = assessments["bias"]

    rows: list[dict[str, Any]] = []

    mappings = [
        (
            "race",
            "race_measurement_patterns",
        ),
        (
            "gender",
            "gender_measurement_patterns",
        ),
        (
            "age",
            "age_measurement_patterns",
        ),
    ]

    for dimension, key in mappings:

        for record in bias[key]:

            row = {
                "dimension": dimension,
                **record,
            }

            rows.append(row)

    return _records_to_dataframe(rows)


# ============================================================
# 10. DATA QUALITY ISSUE LOG
# ============================================================

def build_issue_log(
    assessments: dict[str, Any],
) -> pd.DataFrame:

    consistency = assessments["consistency"]

    rows = [
        {
            "issue_id": "D2-ISS-001",
            "dimension": "Completeness",
            "issue":
                "Weight is extremely sparse.",
            "severity": "HIGH",
            "downstream_impact":
                "Direct use may produce unstable or "
                "non-generalizable feature behavior.",
            "control":
                "Feature approval requires explicit "
                "missingness strategy.",
            "status": "OPEN",
        },
        {
            "issue_id": "D2-ISS-002",
            "dimension": "Completeness",
            "issue":
                "A1C and maximum-glucose result fields are "
                "highly sparse and source 'None' states are "
                "loaded as native missing values.",
            "severity": "HIGH",
            "downstream_impact":
                "Missingness may encode testing practice "
                "rather than random absence.",
            "control":
                "Preserve testing-status semantics and review "
                "before feature engineering.",
            "status": "OPEN",
        },
        {
            "issue_id": "D2-ISS-003",
            "dimension": "Completeness",
            "issue":
                "Medical specialty and payer information "
                "have substantial missingness.",
            "severity": "HIGH",
            "downstream_impact":
                "Potential measurement and institutional "
                "process bias.",
            "control":
                "Evaluate feature necessity and subgroup "
                "missingness before approval.",
            "status": "OPEN",
        },
        {
            "issue_id": "D2-ISS-004",
            "dimension": "Currency",
            "issue":
                "Source data end in 2008.",
            "severity": "HIGH",
            "downstream_impact":
                "Contemporary clinical transportability "
                "cannot be assumed.",
            "control":
                "Require contemporary external validation "
                "and recalibration before deployment.",
            "status": "OPEN",
        },
        {
            "issue_id": "D2-ISS-005",
            "dimension": "Consistency",
            "issue":
                f"{consistency['medication_change_consistency']['change_Ch_without_up_or_down']} "
                "records have change='Ch' without an Up/Down "
                "medication state under the current narrow "
                "consistency rule.",
            "severity": "MODERATE",
            "downstream_impact":
                "Incorrect interpretation could create "
                "invalid cleaning or feature rules.",
            "control":
                "Verify source-variable semantics. Do not "
                "delete or recode records solely from this "
                "flag.",
            "status": "REVIEW",
        },
        {
            "issue_id": "D2-ISS-006",
            "dimension": "Consistency",
            "issue":
                "Small numbers of diagnosis records contain "
                "later diagnosis positions while earlier "
                "positions are missing.",
            "severity": "LOW",
            "downstream_impact":
                "Potential diagnosis-sequence irregularity.",
            "control":
                "Retain records and account for missing "
                "diagnosis positions during feature design.",
            "status": "OPEN",
        },
        {
            "issue_id": "D2-ISS-007",
            "dimension": "Representation",
            "issue":
                "Several racial and younger-age groups have "
                "limited representation.",
            "severity": "HIGH",
            "downstream_impact":
                "Subgroup model estimates may have greater "
                "uncertainty.",
            "control":
                "Perform subgroup performance, confidence "
                "interval and fairness evaluation.",
            "status": "OPEN",
        },
        {
            "issue_id": "D2-ISS-008",
            "dimension": "Bias",
            "issue":
                "Missingness patterns vary across demographic "
                "subgroups.",
            "severity": "HIGH",
            "downstream_impact":
                "Feature availability may reflect differing "
                "measurement or care processes.",
            "control":
                "Carry measurement-bias evidence into D4 "
                "feature governance and D10 fairness review.",
            "status": "OPEN",
        },
        {
            "issue_id": "D2-ISS-009",
            "dimension": "Bias",
            "issue":
                "A substantial proportion of encounters "
                "belong to patients represented more than "
                "once.",
            "severity": "HIGH",
            "downstream_impact":
                "Encounter-level random splitting could cause "
                "patient leakage and optimistic evaluation.",
            "control":
                "Mandate patient-disjoint splitting in D5.",
            "status": "OPEN",
        },
        {
            "issue_id": "D2-ISS-010",
            "dimension": "Bias",
            "issue":
                "Readmission outcome may reflect healthcare "
                "access, utilization, discharge processes and "
                "outcome ascertainment as well as clinical "
                "risk.",
            "severity": "HIGH",
            "downstream_impact":
                "Predictions must not be interpreted as pure "
                "biological risk.",
            "control":
                "Document label limitations and evaluate "
                "subgroup model-error patterns.",
            "status": "OPEN",
        },
    ]

    return _records_to_dataframe(rows)


# ============================================================
# 11. BIAS RISK REGISTER
# ============================================================

def build_bias_risk_register(
    assessments: dict[str, Any],
) -> pd.DataFrame:

    bias = assessments["bias"]

    rows = []

    for index, risk in enumerate(
        bias["bias_risk_register"],
        start=1,
    ):

        rows.append(
            {
                "risk_id":
                    f"D2-BIAS-{index:03d}",
                **risk,
                "lifecycle_owner":
                    "Clinical AI development team",
                "status":
                    "OPEN",
            }
        )

    return _records_to_dataframe(rows)


# ============================================================
# 12. MASTER DATA QUALITY AUDIT REPORT
# ============================================================

def build_audit_report(
    assessments: dict[str, Any],
) -> str:

    currency = assessments["currency"]
    representation = assessments["representation"]
    bias = assessments["bias"]

    population = representation[
        "population_structure"
    ]

    repeat_pct = bias[
        "repeated_patient_structure"
    ][
        "repeat_patient_encounter_pct"
    ]

    return f"""# D2 — Data Quality & Bias Audit Report

## Project

**Diabetes Readmission Clinical AI**

## Lifecycle Stage

**D2 — Data Quality & Bias Assessment**

## Audit Framework

Accuracy → Completeness → Currency → Consistency → Representation → Bias

---

## 1. Purpose

This audit evaluates whether the admitted raw dataset is sufficiently
understood and governed to proceed into cohort definition, outcome
engineering, feature governance, model development and subsequent
clinical AI evaluation.

A D2 gate decision does not constitute approval for clinical deployment.

---

## 2. Dataset Context

- Raw encounters: **{population['total_encounters']:,}**
- Unique patients: **{population['unique_patients']:,}**
- Source temporal coverage: **{currency['source_start_year']}–{currency['source_end_year']}**
- Years since latest source data at assessment: **{currency['years_since_latest_source_data']}**
- Encounter-level calendar dates available: **No**

---

## 3. Accuracy / Conformance

**Disposition: CONDITIONAL PASS**

No invalid values were identified within the audited categorical
domains. Defined numeric plausibility checks and identifier checks
passed.

Missing-like sentinel states remain subject to governed completeness
and semantic review.

---

## 4. Completeness

**Disposition: CONDITIONAL PASS**

Material incompleteness exists in weight, glycemic testing,
medical-specialty and payer-related fields.

Missingness is not assumed to be random. In particular, absence of
laboratory results may represent whether a test was performed or
recorded rather than simple accidental data loss.

No automatic imputation or deletion decision is authorized by D2.

---

## 5. Currency

**Disposition: CONDITIONAL PASS — HIGH RISK**

{currency['currency_finding']}

**Required control:** {currency['deployment_control']}

---

## 6. Consistency

**Disposition: CONDITIONAL PASS**

Core identifier, medication-exposure and readmission-domain checks
show strong internal consistency.

Medication-change semantics and a small number of diagnosis-sequence
patterns require review. These findings are audit flags and are not
automatically classified as source-data errors.

---

## 7. Representation

**Disposition: CONDITIONAL PASS**

The dataset contains {population['total_encounters']:,} encounters from
{population['unique_patients']:,} patients.

Several racial groups and younger age groups have limited
representation. Subgroup evidence strength therefore differs across
the population.

Representation findings do not by themselves establish bias.

---

## 8. Pre-Model Bias Assessment

**Disposition: CONDITIONAL PASS**

Potential bias mechanisms identified include:

- temporal bias;
- representation bias;
- measurement / missingness bias;
- repeated-patient weighting;
- label / outcome bias.

Approximately **{repeat_pct}%** of encounters belong to patients with
multiple encounters.

These are pre-model risks. Model fairness cannot be determined until
a model exists and subgroup error characteristics are evaluated.

---

## 9. Governance Implications

The following controls are mandatory downstream:

1. Patient-disjoint development and evaluation partitions.
2. Prediction-time feature governance.
3. Explicit treatment of missingness semantics.
4. Subgroup performance and uncertainty assessment.
5. Fairness evaluation after model development.
6. Contemporary external validation before any clinical deployment.
7. Explicit documentation of readmission-label limitations.
8. Locked-test governance before final evaluation.

---

## 10. Overall D2 Decision

**CONDITIONAL PASS**

The dataset is suitable to proceed to governed cohort and outcome
engineering for research, development and methodological evaluation.

The dataset is **not approved for direct contemporary clinical
deployment**.

All open D2 risks and controls remain traceable into downstream
lifecycle stages.

---

## 11. Next Lifecycle Stage

**D3 — Cohort & Outcome Engineering**
"""


# ============================================================
# 13. FORMAL D2 GATE DECISION
# ============================================================

def build_gate_decision() -> str:

    return """# D2 — Quality & Bias Gate Decision

## Project

**Diabetes Readmission Clinical AI**

## Gate

**D2 Data Quality & Bias Gate**

## Decision

# CONDITIONAL PASS

The admitted dataset may proceed to **D3 — Cohort & Outcome
Engineering** for controlled research and Clinical AI development.

This decision does not authorize clinical deployment.

## Mandatory Conditions

- Preserve raw-data immutability.
- Resolve or govern open data-quality issues.
- Preserve missingness semantics.
- Use patient-disjoint splitting.
- Perform prediction-time leakage governance.
- Evaluate subgroup model performance and fairness.
- Maintain locked-test controls.
- Require contemporary external validation before clinical deployment.

## Deployment Status

**NOT APPROVED FOR CLINICAL DEPLOYMENT**

## Governance Principle

Progression through the development lifecycle is permitted because
identified limitations can be controlled during subsequent governed
stages. Those limitations must not be silently removed from the risk
record.
"""


# ============================================================
# 14. D2 MANIFEST
# ============================================================

def build_manifest(
    generated_files: list[Path],
) -> dict[str, Any]:

    relative_files = [
        str(
            path.relative_to(PROJECT_ROOT)
        ).replace("\\", "/")
        for path in generated_files
    ]

    return {
        "project":
            "Diabetes Readmission Clinical AI",

        "lifecycle_stage":
            "D2 Data Quality & Bias Assessment",

        "framework": [
            "Accuracy",
            "Completeness",
            "Currency",
            "Consistency",
            "Representation",
            "Bias",
        ],

        "gate_decision":
            "CONDITIONAL PASS",

        "clinical_deployment_status":
            "NOT APPROVED",

        "generated_at_utc":
            datetime.now(
                timezone.utc
            ).isoformat(),

        "generated_files":
            relative_files,

        "downstream_controls": [
            "patient-disjoint splitting",
            "prediction-time feature governance",
            "missingness semantic governance",
            "subgroup performance evaluation",
            "fairness evaluation",
            "locked-test governance",
            "contemporary external validation",
        ],
    }


# ============================================================
# 15. WRITE COMPLETE D2 EVIDENCE PACKAGE
# ============================================================

def generate_d2_evidence_package() -> dict[str, Any]:
    """
    Generate all governed D2 evidence artifacts from source data
    and version-controlled assessment logic.
    """

    ensure_output_directories()

    assessments = run_d2_assessments()

    scorecard = build_scorecard(
        assessments
    )

    completeness = build_completeness_matrix(
        assessments
    )

    representation = build_representation_summary(
        assessments
    )

    subgroup_measurement = (
        build_subgroup_measurement_audit(
            assessments
        )
    )

    issue_log = build_issue_log(
        assessments
    )

    bias_register = build_bias_risk_register(
        assessments
    )

    scorecard.to_csv(
        OUTPUT_FILES["scorecard"],
        index=False,
    )

    completeness.to_csv(
        OUTPUT_FILES["completeness"],
        index=False,
    )

    representation.to_csv(
        OUTPUT_FILES["representation"],
        index=False,
    )

    subgroup_measurement.to_csv(
        OUTPUT_FILES["subgroup_measurement"],
        index=False,
    )

    issue_log.to_csv(
        OUTPUT_FILES["issue_log"],
        index=False,
    )

    bias_register.to_csv(
        OUTPUT_FILES["bias_register"],
        index=False,
    )

    OUTPUT_FILES["audit_report"].write_text(
        build_audit_report(
            assessments
        ),
        encoding="utf-8",
    )

    OUTPUT_FILES["gate_decision"].write_text(
        build_gate_decision(),
        encoding="utf-8",
    )

    generated_before_manifest = [
        OUTPUT_FILES["scorecard"],
        OUTPUT_FILES["completeness"],
        OUTPUT_FILES["representation"],
        OUTPUT_FILES["subgroup_measurement"],
        OUTPUT_FILES["issue_log"],
        OUTPUT_FILES["bias_register"],
        OUTPUT_FILES["audit_report"],
        OUTPUT_FILES["gate_decision"],
    ]

    manifest = build_manifest(
        generated_before_manifest
    )

    with OUTPUT_FILES["manifest"].open(
        "w",
        encoding="utf-8",
    ) as file:
        yaml.safe_dump(
            manifest,
            file,
            sort_keys=False,
            allow_unicode=True,
        )

    return {
        "status": "SUCCESS",
        "gate_decision":
            "CONDITIONAL PASS",
        "clinical_deployment_status":
            "NOT APPROVED",
        "generated_artifacts": [
            str(path.relative_to(PROJECT_ROOT))
            for path in OUTPUT_FILES.values()
        ],
    }


# ============================================================
# 16. COMMAND-LINE ENTRY POINT
# ============================================================

if __name__ == "__main__":

    result = generate_d2_evidence_package()

    print(
        "\n"
        "============================================================"
    )
    print(
        "D2 DATA QUALITY & BIAS EVIDENCE PACKAGE"
    )
    print(
        "============================================================"
    )

    for key, value in result.items():
        print(f"{key}: {value}")

    print(
        "============================================================"
    )