# ============================================================
# D3 — COHORT & OUTCOME EVIDENCE GENERATOR
# ============================================================
"""
Generate the governed D3 cohort artifact and its supporting
evidence package.

Outputs:
    data/interim/D3_governed_modeling_cohort.parquet

    reports/tables/
        D3_cohort_flow.csv
        D3_discharge_disposition_assessment.csv
        D3_outcome_distribution.csv

    reports/governance/
        D3_cohort_exclusion_log.csv
        D3_cohort_outcome_definition.md
        D3_cohort_outcome_gate_decision.md

    artifacts/manifests/
        D3_cohort_outcome_manifest.yaml
"""

# ============================================================
# D3.R1 — IMPORTS
# ============================================================

from pathlib import Path
from typing import Any
import hashlib

import pandas as pd
import yaml

from src.data.config import (
    INTERIM_DATA_DIR,
    TABLES_DIR,
    GOVERNANCE_REPORTS_DIR,
    MANIFESTS_DIR,
)
from src.data.validation import load_raw_dataset
from src.data.cohort import (
    SOURCE_TARGET_COLUMN,
    DERIVED_TARGET_COLUMN,
    PATIENT_ID_COLUMN,
    ENCOUNTER_ID_COLUMN,
    DISCHARGE_COLUMN,
    EXPIRED_DISPOSITION_IDS,
    HOSPICE_DISPOSITION_IDS,
    assess_cohort_eligibility,
    build_disposition_semantic_evidence,
    build_governed_modeling_cohort,
)


# ============================================================
# D3.R2 — GOVERNED OUTPUT PATHS
# ============================================================

COHORT_ARTIFACT_PATH = (
    INTERIM_DATA_DIR
    / "D3_governed_modeling_cohort.parquet"
)

COHORT_FLOW_PATH = (
    TABLES_DIR
    / "D3_cohort_flow.csv"
)

DISPOSITION_ASSESSMENT_PATH = (
    TABLES_DIR
    / "D3_discharge_disposition_assessment.csv"
)

OUTCOME_DISTRIBUTION_PATH = (
    TABLES_DIR
    / "D3_outcome_distribution.csv"
)

EXCLUSION_LOG_PATH = (
    GOVERNANCE_REPORTS_DIR
    / "D3_cohort_exclusion_log.csv"
)

COHORT_DEFINITION_REPORT_PATH = (
    GOVERNANCE_REPORTS_DIR
    / "D3_cohort_outcome_definition.md"
)

GATE_DECISION_PATH = (
    GOVERNANCE_REPORTS_DIR
    / "D3_cohort_outcome_gate_decision.md"
)

MANIFEST_PATH = (
    MANIFESTS_DIR
    / "D3_cohort_outcome_manifest.yaml"
)


# ============================================================
# D3.R3 — FILE HASHING
# ============================================================

def calculate_sha256(
    file_path: Path,
) -> str:
    """
    Calculate an uppercase SHA-256 checksum for a persisted
    artifact.
    """

    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        for block in iter(
            lambda: file.read(1024 * 1024),
            b"",
        ):
            sha256.update(block)

    return sha256.hexdigest().upper()


# ============================================================
# D3.R4 — COHORT FLOW TABLE
# ============================================================

def build_cohort_flow_table(
    raw_df: pd.DataFrame,
    governed_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build the auditable source-to-modeling-cohort flow.
    """

    excluded = len(raw_df) - len(governed_df)

    rows = [
        {
            "stage": "Source dataset",
            "encounters": int(len(raw_df)),
            "patients": int(
                raw_df[
                    PATIENT_ID_COLUMN
                ].nunique()
            ),
            "excluded_at_stage": 0,
        },
        {
            "stage": (
                "Exclude death / expired "
                "discharge dispositions"
            ),
            "encounters": int(len(governed_df)),
            "patients": int(
                governed_df[
                    PATIENT_ID_COLUMN
                ].nunique()
            ),
            "excluded_at_stage": int(excluded),
        },
        {
            "stage": (
                "Final governed modeling cohort"
            ),
            "encounters": int(len(governed_df)),
            "patients": int(
                governed_df[
                    PATIENT_ID_COLUMN
                ].nunique()
            ),
            "excluded_at_stage": 0,
        },
    ]

    return pd.DataFrame(rows)


# ============================================================
# D3.R5 — EXCLUSION LOG
# ============================================================

def build_exclusion_log(
    raw_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build aggregate evidence for each governed expired
    disposition exclusion category.
    """

    semantic_evidence = (
        build_disposition_semantic_evidence(
            raw_df
        )
    )

    exclusion_log = (
        semantic_evidence.loc[
            semantic_evidence[
                DISCHARGE_COLUMN
            ].isin(
                EXPIRED_DISPOSITION_IDS
            )
        ]
        .copy()
        .sort_values(
            DISCHARGE_COLUMN
        )
        .reset_index(drop=True)
    )

    exclusion_log[
        "cohort_action"
    ] = "EXCLUDE"

    exclusion_log[
        "exclusion_rationale"
    ] = (
        "No meaningful post-discharge 30-day "
        "readmission opportunity after death/expiration"
    )

    return exclusion_log


# ============================================================
# D3.R6 — OUTCOME DISTRIBUTION TABLE
# ============================================================

def build_outcome_distribution(
    governed_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build the formal governed outcome distribution.
    """

    distribution = (
        governed_df[
            DERIVED_TARGET_COLUMN
        ]
        .value_counts()
        .sort_index()
        .rename_axis(
            DERIVED_TARGET_COLUMN
        )
        .reset_index(
            name="encounters"
        )
    )

    distribution[
        "outcome_label"
    ] = distribution[
        DERIVED_TARGET_COLUMN
    ].map(
        {
            0: "No 30-day readmission",
            1: "Readmitted within 30 days",
        }
    )

    distribution[
        "encounter_pct"
    ] = (
        distribution["encounters"]
        / len(governed_df)
        * 100
    ).round(4)

    return distribution[
        [
            DERIVED_TARGET_COLUMN,
            "outcome_label",
            "encounters",
            "encounter_pct",
        ]
    ]


# ============================================================
# D3.R7 — GOVERNANCE REPORT
# ============================================================

def build_governance_report(
    raw_df: pd.DataFrame,
    governed_df: pd.DataFrame,
    validation: dict[str, Any],
    cohort_hash: str,
) -> str:
    """
    Build the human-readable D3 cohort and outcome definition.
    """

    eligibility = (
        assess_cohort_eligibility(
            raw_df
        )
    )

    negative_count = int(
        (
            governed_df[
                DERIVED_TARGET_COLUMN
            ]
            == 0
        ).sum()
    )

    positive_count = int(
        (
            governed_df[
                DERIVED_TARGET_COLUMN
            ]
            == 1
        ).sum()
    )

    return f"""# D3 — Governed Cohort & Outcome Definition

## Lifecycle stage

D3 — Cohort & Outcome Engineering

## Purpose

Define the eligible modeling population and formal binary
30-day readmission outcome before patient-level splitting,
feature engineering, preprocessing, or model development.

## Source population

- Source encounters: {len(raw_df):,}
- Source unique patients: {raw_df[PATIENT_ID_COLUMN].nunique():,}
- Source target: `{SOURCE_TARGET_COLUMN}`

## Governed eligibility rule

The primary modeling cohort excludes encounters whose discharge
disposition indicates death or expiration.

Expired disposition IDs:

{sorted(EXPIRED_DISPOSITION_IDS)}

Hospice disposition IDs are retained in the primary cohort:

{sorted(HOSPICE_DISPOSITION_IDS)}

Hospice is not treated as equivalent to death. Hospice-related
sensitivity analysis is reserved for the later robustness and
transportability stage.

## Cohort flow

- Source encounters: {len(raw_df):,}
- Excluded encounters: {eligibility["excluded_encounters"]:,}
- Excluded percentage: {eligibility["excluded_encounter_pct"]:.4f}%
- Governed encounters: {len(governed_df):,}
- Governed unique patients: {governed_df[PATIENT_ID_COLUMN].nunique():,}
- Hospice encounters retained: {eligibility["hospice_encounters_retained"]:,}
- Positive outcomes among excluded encounters: {eligibility["excluded_positive_30d"]:,}

## Formal outcome definition

Derived target:

`{DERIVED_TARGET_COLUMN}`

Deterministic mapping:

- `<30` → 1
- `>30` → 0
- `NO` → 0

The original `{SOURCE_TARGET_COLUMN}` field is preserved for
auditability.

## Governed outcome distribution

- Negative encounters: {negative_count:,}
- Positive encounters: {positive_count:,}
- Positive prevalence: {validation["positive_30d_rate_pct"]:.4f}%

## Governance controls

- Raw source dataset remains immutable.
- Cohort construction does not mutate the source dataframe.
- Death/expired exclusions are applied before model splitting.
- Hospice encounters remain in the primary cohort.
- Encounter identifiers remain unique.
- Patient identifiers remain complete.
- The formal target contains no missing values.
- The formal target is strictly binary.
- Source target semantics are preserved.
- Outcome mapping is deterministic and validated.
- Patient and encounter identifiers are retained only for
  governance and later split construction; they are not approved
  modeling features.
- Locked-test evaluation has not occurred.

## Persisted cohort artifact

Path:

`data/interim/D3_governed_modeling_cohort.parquet`

SHA-256:

`{cohort_hash}`

## D3 validation result

**{validation["validation_status"]}**

The governed cohort and formal outcome are approved to proceed
to downstream leakage and feature governance. This approval does
not constitute approval for clinical deployment.
"""


# ============================================================
# D3.R8 — GATE DECISION
# ============================================================

def build_gate_decision(
    validation: dict[str, Any],
    cohort_hash: str,
) -> str:
    """
    Build the formal D3 lifecycle gate decision.
    """

    return f"""# D3 — Cohort & Outcome Gate Decision

## Decision

**PASS**

## Governed cohort

- Encounters: {validation["governed_encounters"]:,}
- Unique patients: {validation["unique_governed_patients"]:,}
- Positive 30-day outcomes: {validation["positive_30d_count"]:,}
- Positive prevalence: {validation["positive_30d_rate_pct"]:.4f}%

## Validation

All governed post-construction cohort and outcome invariants
passed.

## Artifact integrity

SHA-256:

`{cohort_hash}`

## Authorization

D3 is approved for progression to D4 — Leakage & Feature
Governance.

This gate does not authorize model training, locked-test
evaluation, or clinical deployment.
"""


# ============================================================
# D3.R9 — MANIFEST
# ============================================================

def build_manifest(
    raw_df: pd.DataFrame,
    governed_df: pd.DataFrame,
    validation: dict[str, Any],
    cohort_hash: str,
) -> dict[str, Any]:
    """
    Build the machine-readable D3 evidence manifest.
    """

    return {
        "artifact": {
            "name":
                "D3 Governed Cohort and Outcome",
            "lifecycle_stage":
                "D3 — Cohort & Outcome Engineering",
            "version":
                "1.0",
        },
        "cohort": {
            "source_encounters":
                int(len(raw_df)),
            "governed_encounters":
                int(len(governed_df)),
            "governed_unique_patients":
                int(
                    governed_df[
                        PATIENT_ID_COLUMN
                    ].nunique()
                ),
            "expired_disposition_ids_excluded":
                sorted(
                    EXPIRED_DISPOSITION_IDS
                ),
            "hospice_disposition_ids_retained":
                sorted(
                    HOSPICE_DISPOSITION_IDS
                ),
        },
        "outcome": {
            "source_column":
                SOURCE_TARGET_COLUMN,
            "derived_column":
                DERIVED_TARGET_COLUMN,
            "positive_definition":
                "<30",
            "negative_definitions":
                [">30", "NO"],
            "positive_count":
                int(
                    validation[
                        "positive_30d_count"
                    ]
                ),
            "positive_rate_pct":
                float(
                    validation[
                        "positive_30d_rate_pct"
                    ]
                ),
        },
        "persisted_cohort": {
            "path":
                "data/interim/"
                "D3_governed_modeling_cohort.parquet",
            "format":
                "parquet",
            "sha256":
                cohort_hash,
            "git_tracked":
                False,
        },
        "governance": {
            "raw_data_immutable":
                True,
            "patient_level_splitting_required":
                True,
            "identifiers_not_model_features":
                True,
            "hospice_sensitivity_analysis_required":
                True,
            "locked_test_evaluation_performed":
                False,
            "clinical_deployment_approved":
                False,
        },
        "validation": {
            "status":
                validation[
                    "validation_status"
                ],
            "checks": {
                key: bool(value)
                for key, value
                in validation[
                    "validation_checks"
                ].items()
            },
        },
        "gate": {
            "decision":
                "PASS",
            "next_stage":
                "D4 — Leakage & Feature Governance",
        },
    }


# ============================================================
# D3.R10 — GENERATE COMPLETE D3 EVIDENCE PACKAGE
# ============================================================

def generate_d3_evidence_package(
) -> dict[str, Any]:
    """
    Generate and persist the complete governed D3 evidence
    package.
    """

    for directory in (
        INTERIM_DATA_DIR,
        TABLES_DIR,
        GOVERNANCE_REPORTS_DIR,
        MANIFESTS_DIR,
    ):
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    raw_df = load_raw_dataset()

    governed_df, validation = (
        build_governed_modeling_cohort(
            raw_df
        )
    )

    if validation[
        "validation_status"
    ] != "PASS":
        raise RuntimeError(
            "D3 validation did not pass. "
            "Evidence generation aborted."
        )

    # --------------------------------------------------------
    # Persist governed cohort
    # --------------------------------------------------------

    governed_df.to_parquet(
        COHORT_ARTIFACT_PATH,
        index=False,
    )

    cohort_hash = calculate_sha256(
        COHORT_ARTIFACT_PATH
    )

    # --------------------------------------------------------
    # Build evidence tables
    # --------------------------------------------------------

    cohort_flow = (
        build_cohort_flow_table(
            raw_df,
            governed_df,
        )
    )

    disposition_assessment = (
        build_disposition_semantic_evidence(
            raw_df
        )
    )

    outcome_distribution = (
        build_outcome_distribution(
            governed_df
        )
    )

    exclusion_log = (
        build_exclusion_log(
            raw_df
        )
    )

    # --------------------------------------------------------
    # Persist evidence tables
    # --------------------------------------------------------

    cohort_flow.to_csv(
        COHORT_FLOW_PATH,
        index=False,
    )

    disposition_assessment.to_csv(
        DISPOSITION_ASSESSMENT_PATH,
        index=False,
    )

    outcome_distribution.to_csv(
        OUTCOME_DISTRIBUTION_PATH,
        index=False,
    )

    exclusion_log.to_csv(
        EXCLUSION_LOG_PATH,
        index=False,
    )

    # --------------------------------------------------------
    # Governance documentation
    # --------------------------------------------------------

    governance_report = (
        build_governance_report(
            raw_df,
            governed_df,
            validation,
            cohort_hash,
        )
    )

    COHORT_DEFINITION_REPORT_PATH.write_text(
        governance_report,
        encoding="utf-8",
    )

    gate_decision = (
        build_gate_decision(
            validation,
            cohort_hash,
        )
    )

    GATE_DECISION_PATH.write_text(
        gate_decision,
        encoding="utf-8",
    )

    # --------------------------------------------------------
    # Machine-readable manifest
    # --------------------------------------------------------

    manifest = build_manifest(
        raw_df,
        governed_df,
        validation,
        cohort_hash,
    )

    with MANIFEST_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:
        yaml.safe_dump(
            manifest,
            file,
            sort_keys=False,
            allow_unicode=True,
        )

    # --------------------------------------------------------
    # Final persistence validation
    # --------------------------------------------------------

    reloaded_df = pd.read_parquet(
        COHORT_ARTIFACT_PATH
    )

    if len(reloaded_df) != 100_114:
        raise RuntimeError(
            "Persisted D3 cohort row count "
            "validation failed."
        )

    if (
        reloaded_df[
            ENCOUNTER_ID_COLUMN
        ].duplicated().any()
    ):
        raise RuntimeError(
            "Persisted D3 cohort contains "
            "duplicate encounter IDs."
        )

    if (
        reloaded_df[
            DERIVED_TARGET_COLUMN
        ].sum()
        != 11_357
    ):
        raise RuntimeError(
            "Persisted D3 outcome count "
            "validation failed."
        )

    if calculate_sha256(
        COHORT_ARTIFACT_PATH
    ) != cohort_hash:
        raise RuntimeError(
            "Persisted cohort checksum "
            "validation failed."
        )

    return {
        "status": "SUCCESS",
        "gate_decision": "PASS",
        "governed_encounters":
            int(len(governed_df)),
        "governed_patients":
            int(
                governed_df[
                    PATIENT_ID_COLUMN
                ].nunique()
            ),
        "positive_30d":
            int(
                governed_df[
                    DERIVED_TARGET_COLUMN
                ].sum()
            ),
        "positive_30d_rate_pct":
            float(
                validation[
                    "positive_30d_rate_pct"
                ]
            ),
        "cohort_sha256":
            cohort_hash,
        "persisted_cohort":
            str(COHORT_ARTIFACT_PATH),
        "evidence_files": [
            str(COHORT_FLOW_PATH),
            str(
                DISPOSITION_ASSESSMENT_PATH
            ),
            str(
                OUTCOME_DISTRIBUTION_PATH
            ),
            str(EXCLUSION_LOG_PATH),
            str(
                COHORT_DEFINITION_REPORT_PATH
            ),
            str(GATE_DECISION_PATH),
            str(MANIFEST_PATH),
        ],
    }


# ============================================================
# D3.R11 — COMMAND-LINE EXECUTION
# ============================================================

if __name__ == "__main__":

    result = (
        generate_d3_evidence_package()
    )

    print("=" * 70)
    print(
        "D3 — COHORT & OUTCOME "
        "EVIDENCE PACKAGE"
    )
    print("=" * 70)

    for key, value in result.items():

        if key != "evidence_files":
            print(
                f"{key}: {value}"
            )

    print()
    print(
        "EVIDENCE FILES"
    )
    print("-" * 70)

    for file_path in result[
        "evidence_files"
    ]:
        print(file_path)

    print("=" * 70)