# ============================================================
# D4 — LEAKAGE & FEATURE GOVERNANCE EVIDENCE REPORTING
# ============================================================
"""
Generate the persistent evidence package for D4.

The evidence package documents:
1. Prediction-time contract
2. Complete feature governance register
3. Leakage decision register
4. Feature disposition summary
5. Governance report
6. D4 gate decision
7. Machine-readable D4 manifest

No model training occurs in D4.
"""

# ============================================================
# D4.R1 — IMPORTS
# ============================================================

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from src.data.config import (
    TABLES_DIR,
    GOVERNANCE_REPORTS_DIR,
    MANIFESTS_DIR,
)
from src.data.feature_governance import (
    APPROVED,
    CONDITIONAL,
    BLOCKED,
    IDENTIFIER_ONLY,
    TARGET_ONLY,
    CLINICAL_DECISION_POINT,
    PREDICTION_TIME_CONTRACT,
    LEAKAGE_TAXONOMY,
    build_complete_feature_governance,
)


# ============================================================
# D4.R2 — OUTPUT PATHS
# ============================================================

FEATURE_REGISTER_PATH = (
    TABLES_DIR
    / "D4_feature_governance_register.csv"
)

LEAKAGE_REGISTER_PATH = (
    TABLES_DIR
    / "D4_leakage_decision_register.csv"
)

DISPOSITION_SUMMARY_PATH = (
    TABLES_DIR
    / "D4_feature_disposition_summary.csv"
)

PREDICTION_TIME_CONTRACT_PATH = (
    GOVERNANCE_REPORTS_DIR
    / "D4_prediction_time_contract.md"
)

GOVERNANCE_REPORT_PATH = (
    GOVERNANCE_REPORTS_DIR
    / "D4_leakage_feature_governance_report.md"
)

GATE_DECISION_PATH = (
    GOVERNANCE_REPORTS_DIR
    / "D4_feature_governance_gate_decision.md"
)

MANIFEST_PATH = (
    MANIFESTS_DIR
    / "D4_feature_governance_manifest.yaml"
)


# ============================================================
# D4.R3 — OUTPUT DIRECTORY VALIDATION
# ============================================================

def ensure_output_directories() -> None:
    """
    Ensure all D4 evidence output directories exist.
    """

    TABLES_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    GOVERNANCE_REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    MANIFESTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


# ============================================================
# D4.R4 — FEATURE DISPOSITION SUMMARY
# ============================================================

def build_feature_disposition_summary(
    inventory: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build auditable counts and percentages for each formal
    governance disposition.
    """

    ordered_dispositions = [
        APPROVED,
        CONDITIONAL,
        BLOCKED,
        IDENTIFIER_ONLY,
        TARGET_ONLY,
    ]

    records = []

    total = len(inventory)

    for disposition in ordered_dispositions:

        count = int(
            (
                inventory[
                    "governance_disposition"
                ]
                == disposition
            ).sum()
        )

        records.append(
            {
                "governance_disposition":
                    disposition,

                "feature_count":
                    count,

                "feature_pct":
                    round(
                        (count / total) * 100,
                        4,
                    ),
            }
        )

    return pd.DataFrame(records)


# ============================================================
# D4.R5 — LEAKAGE DECISION REGISTER
# ============================================================

def build_leakage_decision_register(
    inventory: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create a focused register of every field carrying explicit
    leakage, timing, identifier, target, or semantic risk.
    """

    risk_rows = inventory[
        inventory[
            "governance_disposition"
        ].isin(
            {
                CONDITIONAL,
                BLOCKED,
                IDENTIFIER_ONLY,
                TARGET_ONLY,
            }
        )
    ].copy()

    columns = [
        "source_position",
        "feature",
        "source_dtype",
        "governance_disposition",
        "feature_role",
        "prediction_time_status",
        "leakage_risk",
        "rationale",
        "permitted_use",
    ]

    return (
        risk_rows[
            columns
        ]
        .sort_values(
            "source_position"
        )
        .reset_index(drop=True)
    )


# ============================================================
# D4.R6 — PREDICTION-TIME CONTRACT DOCUMENT
# ============================================================

def build_prediction_time_contract_document() -> str:
    """
    Build the human-readable D4 prediction-time contract.
    """

    users = ", ".join(
        CLINICAL_DECISION_POINT.primary_users
    )

    contract_lines = []

    for key, value in (
        PREDICTION_TIME_CONTRACT.items()
    ):
        label = (
            key.replace("_", " ")
            .title()
        )

        contract_lines.append(
            f"### {label}\n\n{value}"
        )

    contract_body = "\n\n".join(
        contract_lines
    )

    return f"""# D4 Prediction-Time Contract

## Project

Diabetes Readmission Clinical AI

## Purpose

This document establishes the formal information boundary for
feature eligibility before model development.

A variable appearing in the retrospective source dataset is not
automatically eligible for modeling. Eligibility depends on whether
the information could legitimately have been available at or before
the defined prediction timestamp.

## Clinical Decision Point

**Population:** {CLINICAL_DECISION_POINT.population}

**Setting:** {CLINICAL_DECISION_POINT.setting}

**Primary users:** {users}

**Decision supported:** {CLINICAL_DECISION_POINT.decision}

**Prediction timestamp:** {CLINICAL_DECISION_POINT.prediction_timestamp}

**Prediction horizon:** {CLINICAL_DECISION_POINT.prediction_horizon}

**Outcome:** {CLINICAL_DECISION_POINT.outcome}

**Intended action:** {CLINICAL_DECISION_POINT.intended_action}

## Prediction-Time Governance Contract

{contract_body}

## Governance Principle

Feature availability must be established independently of model
performance. No feature may be approved because it improves
validation or test performance.

The locked test partition must not influence feature-governance
decisions.

## Status

Prediction-time contract established before model development.
"""


# ============================================================
# D4.R7 — GOVERNANCE REPORT
# ============================================================

def build_governance_report(
    inventory: pd.DataFrame,
    validation: dict[str, Any],
) -> str:
    """
    Build the formal D4 leakage and feature-governance report.
    """

    approved_features = inventory.loc[
        inventory[
            "governance_disposition"
        ] == APPROVED,
        "feature",
    ].tolist()

    conditional_features = inventory.loc[
        inventory[
            "governance_disposition"
        ] == CONDITIONAL,
        "feature",
    ].tolist()

    blocked_features = inventory.loc[
        inventory[
            "governance_disposition"
        ] == BLOCKED,
        "feature",
    ].tolist()

    approved_text = "\n".join(
        f"- `{feature}`"
        for feature in approved_features
    )

    conditional_text = "\n".join(
        f"- `{feature}`"
        for feature in conditional_features
    )

    blocked_text = "\n".join(
        f"- `{feature}`"
        for feature in blocked_features
    )

    taxonomy_text = "\n".join(
        (
            f"- **{risk}:** "
            f"{description}"
        )
        for risk, description
        in LEAKAGE_TAXONOMY.items()
    )

    return f"""# D4 Leakage & Feature Governance Report

## Project

Diabetes Readmission Clinical AI

## D4 Objective

D4 determines which source variables may legitimately participate
in model development at the defined clinical prediction time.

The purpose is to prevent target leakage, temporal leakage,
post-prediction leakage, aggregation leakage, identifier leakage,
proxy leakage, and unsupported assumptions about retrospective
variable availability.

## Prediction Context

**Prediction timestamp:** {CLINICAL_DECISION_POINT.prediction_timestamp}

**Prediction horizon:** {CLINICAL_DECISION_POINT.prediction_horizon}

**Decision:** {CLINICAL_DECISION_POINT.decision}

## Leakage Taxonomy

{taxonomy_text}

## Governance Results

- Total governed fields: {validation["total_fields"]}
- APPROVED: {validation["approved_features"]}
- CONDITIONAL: {validation["conditional_features"]}
- BLOCKED: {validation["blocked_features"]}
- IDENTIFIER/GOVERNANCE-ONLY: {validation["identifier_only_fields"]}
- TARGET/OUTCOME: {validation["target_only_fields"]}
- UNASSESSED: {validation["unassessed_features"]}
- Validation status: {validation["validation_status"]}

## Approved Source Features

These fields are eligible for governed preprocessing and feature
engineering. Approval does not require that the raw representation
be used directly.

{approved_text}

## Conditional Source Features

These variables are not authorized for direct model entry.
They require governed transformation, reconstruction, or explicit
prediction-time justification.

{conditional_text}

## Blocked Source Features

These fields are excluded from the primary model because their
final retrospective values are not proven safe at the defined
prediction time.

{blocked_text}

## Identifier Governance

`encounter_id` and `patient_nbr` are prohibited as predictive
features.

They remain available only for integrity checking, traceability,
audit, and patient-level data splitting.

## Outcome Governance

`readmitted` is the raw source outcome and `readmitted_30d` is the
formal binary prediction target.

Neither may enter the predictor matrix.

## Primary Safety Decision

No CONDITIONAL or BLOCKED field is authorized for direct primary
model entry at this stage.

Conditional fields may become eligible only after explicit
governed transformation or prediction-time justification.

Blocked fields may become eligible only if a timestamp-safe version
is reconstructed and independently governed.

## Locked-Test Protection

No feature-governance decision has been informed by locked-test
performance.

## D4 Validation

All source/governance fields received exactly one formal
disposition.

No unassessed fields remain.

D4 validation status: **{validation["validation_status"]}**

## Deployment Status

Clinical deployment is not approved by D4.

D4 authorizes progression to subsequent governed lifecycle stages;
it does not establish clinical effectiveness, calibration,
fairness, robustness, transportability, or deployment readiness.
"""


# ============================================================
# D4.R8 — GATE DECISION
# ============================================================

def build_gate_decision(
    validation: dict[str, Any],
) -> str:
    """
    Build the formal D4 lifecycle gate decision.
    """

    gate = (
        "PASS"
        if validation[
            "validation_status"
        ] == "PASS"
        else "FAIL"
    )

    return f"""# D4 Feature Governance Gate Decision

## Gate

**{gate}**

## Basis

The D4 leakage and feature-governance process has:

- established the clinical decision point;
- established the prediction-time contract;
- inventoried all {validation["total_fields"]} fields;
- classified every field under a formal governance disposition;
- prohibited identifiers from model input;
- prohibited source and engineered outcomes from model input;
- blocked retrospective/end-of-encounter fields that are not
  proven prediction-time safe;
- prevented conditional variables from direct model entry;
- preserved locked-test independence.

## Disposition Summary

- APPROVED: {validation["approved_features"]}
- CONDITIONAL: {validation["conditional_features"]}
- BLOCKED: {validation["blocked_features"]}
- IDENTIFIER/GOVERNANCE-ONLY: {validation["identifier_only_fields"]}
- TARGET/OUTCOME: {validation["target_only_fields"]}
- UNASSESSED: {validation["unassessed_features"]}

## Decision

D4 may close with a **{gate}** provided the generated evidence
package and automated tests remain valid.

Progression to D5 is authorized only under the D4 feature-governance
contract.

## Mandatory Downstream Controls

1. Patient-level disjoint splitting must be enforced.
2. Identifiers must not enter model predictors.
3. Source or engineered outcomes must not enter model predictors.
4. CONDITIONAL features must not enter the primary model without
   explicit governed transformation or approval.
5. BLOCKED features must remain excluded unless timestamp-safe
   reconstruction is separately governed.
6. Locked-test data must remain isolated from feature engineering,
   preprocessing, model selection, threshold selection, and
   calibration decisions.
7. Feature lineage must remain traceable through subsequent
   lifecycle stages.

## Clinical Deployment

**NOT APPROVED**

A D4 PASS is a feature-governance lifecycle decision, not evidence
of clinical deployment readiness.
"""


# ============================================================
# D4.R9 — MANIFEST
# ============================================================

def build_manifest(
    validation: dict[str, Any],
) -> dict[str, Any]:
    """
    Build the machine-readable D4 evidence manifest.
    """

    return {
        "stage":
            "D4",

        "name":
            "Leakage & Feature Governance",

        "project":
            "Diabetes Readmission Clinical AI",

        "generated_at_utc":
            datetime.now(
                timezone.utc
            ).isoformat(),

        "gate_decision":
            validation[
                "validation_status"
            ],

        "clinical_deployment_status":
            "NOT APPROVED",

        "prediction_context": {
            "timestamp":
                CLINICAL_DECISION_POINT
                .prediction_timestamp,

            "horizon":
                CLINICAL_DECISION_POINT
                .prediction_horizon,

            "outcome":
                CLINICAL_DECISION_POINT
                .outcome,
        },

        "field_counts": {
            "total":
                validation[
                    "total_fields"
                ],

            "approved":
                validation[
                    "approved_features"
                ],

            "conditional":
                validation[
                    "conditional_features"
                ],

            "blocked":
                validation[
                    "blocked_features"
                ],

            "identifier_governance_only":
                validation[
                    "identifier_only_fields"
                ],

            "target_outcome":
                validation[
                    "target_only_fields"
                ],

            "unassessed":
                validation[
                    "unassessed_features"
                ],
        },

        "mandatory_controls": {
            "patient_level_splitting_required":
                True,

            "identifiers_prohibited_as_predictors":
                True,

            "targets_prohibited_as_predictors":
                True,

            "conditional_features_require_governance":
                True,

            "blocked_features_prohibited":
                True,

            "locked_test_protection_required":
                True,
        },

        "generated_files": [
            str(
                FEATURE_REGISTER_PATH
                .relative_to(
                    FEATURE_REGISTER_PATH.parents[2]
                )
            ).replace("\\", "/"),

            str(
                LEAKAGE_REGISTER_PATH
                .relative_to(
                    LEAKAGE_REGISTER_PATH.parents[2]
                )
            ).replace("\\", "/"),

            str(
                DISPOSITION_SUMMARY_PATH
                .relative_to(
                    DISPOSITION_SUMMARY_PATH.parents[2]
                )
            ).replace("\\", "/"),

            str(
                PREDICTION_TIME_CONTRACT_PATH
                .relative_to(
                    PREDICTION_TIME_CONTRACT_PATH.parents[2]
                )
            ).replace("\\", "/"),

            str(
                GOVERNANCE_REPORT_PATH
                .relative_to(
                    GOVERNANCE_REPORT_PATH.parents[2]
                )
            ).replace("\\", "/"),

            str(
                GATE_DECISION_PATH
                .relative_to(
                    GATE_DECISION_PATH.parents[2]
                )
            ).replace("\\", "/"),
        ],
    }


# ============================================================
# D4.R10 — GENERATE COMPLETE EVIDENCE PACKAGE
# ============================================================

def generate_d4_evidence_package() -> dict[str, Any]:
    """
    Generate and persist the complete D4 evidence package.
    """

    ensure_output_directories()

    (
        governed_df,
        inventory,
        validation,
    ) = build_complete_feature_governance()

    if validation[
        "validation_status"
    ] != "PASS":
        raise RuntimeError(
            "D4 governance validation failed. "
            "Evidence package will not be finalized."
        )

    # --------------------------------------------------------
    # Feature governance register
    # --------------------------------------------------------

    inventory.to_csv(
        FEATURE_REGISTER_PATH,
        index=False,
    )

    # --------------------------------------------------------
    # Leakage decision register
    # --------------------------------------------------------

    leakage_register = (
        build_leakage_decision_register(
            inventory
        )
    )

    leakage_register.to_csv(
        LEAKAGE_REGISTER_PATH,
        index=False,
    )

    # --------------------------------------------------------
    # Disposition summary
    # --------------------------------------------------------

    disposition_summary = (
        build_feature_disposition_summary(
            inventory
        )
    )

    disposition_summary.to_csv(
        DISPOSITION_SUMMARY_PATH,
        index=False,
    )

    # --------------------------------------------------------
    # Prediction-time contract
    # --------------------------------------------------------

    PREDICTION_TIME_CONTRACT_PATH.write_text(
        build_prediction_time_contract_document(),
        encoding="utf-8",
    )

    # --------------------------------------------------------
    # Governance report
    # --------------------------------------------------------

    GOVERNANCE_REPORT_PATH.write_text(
        build_governance_report(
            inventory,
            validation,
        ),
        encoding="utf-8",
    )

    # --------------------------------------------------------
    # Gate decision
    # --------------------------------------------------------

    GATE_DECISION_PATH.write_text(
        build_gate_decision(
            validation
        ),
        encoding="utf-8",
    )

    # --------------------------------------------------------
    # Machine-readable manifest
    # --------------------------------------------------------

    manifest = build_manifest(
        validation
    )

    MANIFEST_PATH.write_text(
        yaml.safe_dump(
            manifest,
            sort_keys=False,
            allow_unicode=True,
        ),
        encoding="utf-8",
    )

    return {
        "status":
            "SUCCESS",

        "gate_decision":
            validation[
                "validation_status"
            ],

        "total_fields":
            validation[
                "total_fields"
            ],

        "approved":
            validation[
                "approved_features"
            ],

        "conditional":
            validation[
                "conditional_features"
            ],

        "blocked":
            validation[
                "blocked_features"
            ],

        "identifier_only":
            validation[
                "identifier_only_fields"
            ],

        "target_only":
            validation[
                "target_only_fields"
            ],

        "unassessed":
            validation[
                "unassessed_features"
            ],

        "generated_files": {
            "feature_register":
                str(FEATURE_REGISTER_PATH),

            "leakage_register":
                str(LEAKAGE_REGISTER_PATH),

            "disposition_summary":
                str(DISPOSITION_SUMMARY_PATH),

            "prediction_time_contract":
                str(PREDICTION_TIME_CONTRACT_PATH),

            "governance_report":
                str(GOVERNANCE_REPORT_PATH),

            "gate_decision":
                str(GATE_DECISION_PATH),

            "manifest":
                str(MANIFEST_PATH),
        },
    }


# ============================================================
# D4.R11 — COMMAND-LINE EXECUTION
# ============================================================

if __name__ == "__main__":

    result = generate_d4_evidence_package()

    print("=" * 70)
    print(
        "D4 — LEAKAGE & FEATURE GOVERNANCE EVIDENCE PACKAGE"
    )
    print("=" * 70)

    print(
        f"status: "
        f"{result['status']}"
    )

    print(
        f"gate_decision: "
        f"{result['gate_decision']}"
    )

    print(
        f"total_fields: "
        f"{result['total_fields']}"
    )

    print(
        f"approved: "
        f"{result['approved']}"
    )

    print(
        f"conditional: "
        f"{result['conditional']}"
    )

    print(
        f"blocked: "
        f"{result['blocked']}"
    )

    print(
        f"identifier_only: "
        f"{result['identifier_only']}"
    )

    print(
        f"target_only: "
        f"{result['target_only']}"
    )

    print(
        f"unassessed: "
        f"{result['unassessed']}"
    )

    print()
    print(
        "GENERATED FILES"
    )
    print("-" * 70)

    for name, path in (
        result[
            "generated_files"
        ].items()
    ):
        print(
            f"{name}: {path}"
        )

    print()
    print("=" * 70)
    print(
        "D4 evidence generation: SUCCESS"
    )
    print(
        "Clinical deployment: NOT APPROVED"
    )
    print("=" * 70)