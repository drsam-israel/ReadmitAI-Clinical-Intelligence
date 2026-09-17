# ============================================================
# D6 — FEATURE ENGINEERING EVIDENCE & REPORTING
# ============================================================
"""
Generate the governed D6 feature-engineering evidence package.

D6 evidence demonstrates that deterministic feature engineering:

1. consumes the frozen D5 patient split;
2. protects the locked test partition;
3. maintains D4 feature-governance lineage;
4. separates CANDIDATE from CONDITIONAL features;
5. prevents identifiers, outcomes, and blocked variables from
   entering the primary modeling matrix;
6. produces reproducible development artifacts.

No model fitting or preprocessing fitting occurs in D6.
"""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import hashlib

import pandas as pd
import yaml

from src.data.splitting import (
    GROUP_COLUMN,
    TARGET_COLUMN,
    TRAIN_LABEL,
    VALIDATION_LABEL,
    TEST_LABEL,
)

from src.features.engineering import (
    PROJECT_ROOT,
    D6_CANDIDATE,
    D6_CONDITIONAL,
    FEATURE_SPECIFICATIONS,
    EXPECTED_D5_ASSIGNMENT_SHA256,
    build_combined_d6_development_features,
    build_primary_candidate_development_matrix,
    get_governed_d6_feature_lists,
)


# ============================================================
# D6.R1 — EVIDENCE PATHS
# ============================================================

REPORT_TABLES_DIR = (
    PROJECT_ROOT
    / "reports"
    / "tables"
)

REPORT_GOVERNANCE_DIR = (
    PROJECT_ROOT
    / "reports"
    / "governance"
)

MANIFEST_DIR = (
    PROJECT_ROOT
    / "artifacts"
    / "manifests"
)

INTERIM_DATA_DIR = (
    PROJECT_ROOT
    / "data"
    / "interim"
)

FEATURE_REGISTRY_PATH = (
    REPORT_TABLES_DIR
    / "D6_feature_engineering_registry.csv"
)

FEATURE_LINEAGE_PATH = (
    REPORT_TABLES_DIR
    / "D6_feature_lineage_audit.csv"
)

FEATURE_SUMMARY_PATH = (
    REPORT_TABLES_DIR
    / "D6_feature_engineering_summary.csv"
)

CONTRACT_REPORT_PATH = (
    REPORT_GOVERNANCE_DIR
    / "D6_feature_engineering_contract.md"
)

GATE_DECISION_PATH = (
    REPORT_GOVERNANCE_DIR
    / "D6_feature_engineering_gate_decision.md"
)

MANIFEST_PATH = (
    MANIFEST_DIR
    / "D6_feature_engineering_manifest.yaml"
)

DEVELOPMENT_FEATURE_PATH = (
    INTERIM_DATA_DIR
    / "D6_development_engineered.parquet"
)


# ============================================================
# D6.R2 — SHA-256 UTILITY
# ============================================================

def calculate_sha256(
    path: Path,
) -> str:
    """
    Calculate an uppercase SHA-256 checksum for a persisted file.
    """

    sha256 = hashlib.sha256()

    with path.open("rb") as file_handle:
        for block in iter(
            lambda: file_handle.read(1024 * 1024),
            b"",
        ):
            sha256.update(block)

    return sha256.hexdigest().upper()


# ============================================================
# D6.R3 — DIRECTORY PREPARATION
# ============================================================

def prepare_d6_evidence_directories() -> None:
    """
    Ensure all D6 evidence directories exist.
    """

    for directory in (
        REPORT_TABLES_DIR,
        REPORT_GOVERNANCE_DIR,
        MANIFEST_DIR,
        INTERIM_DATA_DIR,
    ):
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )


# ============================================================
# D6.R4 — FEATURE ENGINEERING REGISTRY TABLE
# ============================================================

def build_feature_engineering_registry() -> pd.DataFrame:
    """
    Convert the authoritative D6 feature specification registry
    into a portfolio-ready evidence table.
    """

    records = []

    for specification in FEATURE_SPECIFICATIONS:
        records.append(
            {
                "feature_name":
                    specification.feature_name,

                "feature_class":
                    specification.feature_class,

                "source_columns":
                    "|".join(
                        specification.source_columns
                    ),

                "d6_disposition":
                    specification.disposition,

                "transformation":
                    specification.transformation,

                "prediction_time_rationale":
                    specification.prediction_time_rationale,

                "permitted_use":
                    specification.permitted_use,
            }
        )

    registry = pd.DataFrame(records)

    return registry


# ============================================================
# D6.R5 — FEATURE LINEAGE AUDIT
# ============================================================

def build_feature_lineage_audit() -> pd.DataFrame:
    """
    Produce feature-level lineage evidence showing whether each
    D6 feature originates from D4-approved or D4-conditional
    source information.
    """

    from src.features.engineering import (
        D4_APPROVED_SOURCE_FEATURES,
        D4_CONDITIONAL_SOURCE_FEATURES,
    )

    records = []

    for specification in FEATURE_SPECIFICATIONS:

        sources = set(
            specification.source_columns
        )

        approved_sources = sorted(
            sources
            & D4_APPROVED_SOURCE_FEATURES
        )

        conditional_sources = sorted(
            sources
            & D4_CONDITIONAL_SOURCE_FEATURES
        )

        if conditional_sources:
            source_governance = (
                "D4_CONDITIONAL"
            )

        elif approved_sources:
            source_governance = (
                "D4_APPROVED"
            )

        else:
            source_governance = (
                "UNRESOLVED"
            )

        candidate_lineage_violation = bool(
            specification.disposition
            == D6_CANDIDATE
            and conditional_sources
        )

        records.append(
            {
                "feature_name":
                    specification.feature_name,

                "feature_class":
                    specification.feature_class,

                "d6_disposition":
                    specification.disposition,

                "source_governance":
                    source_governance,

                "approved_source_columns":
                    "|".join(approved_sources),

                "conditional_source_columns":
                    "|".join(
                        conditional_sources
                    ),

                "candidate_lineage_violation":
                    candidate_lineage_violation,
            }
        )

    return pd.DataFrame(records)


# ============================================================
# D6.R6 — FEATURE ENGINEERING SUMMARY
# ============================================================

def build_feature_engineering_summary(
    combined_df: pd.DataFrame,
    audit: dict[str, Any],
) -> pd.DataFrame:
    """
    Build the lifecycle-level D6 summary table.
    """

    split_counts = (
        combined_df["split"]
        .value_counts()
        .to_dict()
    )

    patient_counts = (
        combined_df
        .groupby("split")[GROUP_COLUMN]
        .nunique()
        .to_dict()
    )

    rows = [
        {
            "metric":
                "development_encounters",
            "value":
                len(combined_df),
        },
        {
            "metric":
                "development_patients",
            "value":
                combined_df[
                    GROUP_COLUMN
                ].nunique(),
        },
        {
            "metric":
                "train_encounters",
            "value":
                split_counts.get(
                    TRAIN_LABEL,
                    0,
                ),
        },
        {
            "metric":
                "validation_encounters",
            "value":
                split_counts.get(
                    VALIDATION_LABEL,
                    0,
                ),
        },
        {
            "metric":
                "locked_test_encounters",
            "value":
                split_counts.get(
                    TEST_LABEL,
                    0,
                ),
        },
        {
            "metric":
                "train_patients",
            "value":
                patient_counts.get(
                    TRAIN_LABEL,
                    0,
                ),
        },
        {
            "metric":
                "validation_patients",
            "value":
                patient_counts.get(
                    VALIDATION_LABEL,
                    0,
                ),
        },
        {
            "metric":
                "registered_features",
            "value":
                audit[
                    "registered_feature_count"
                ],
        },
        {
            "metric":
                "candidate_features",
            "value":
                audit[
                    "candidate_feature_count"
                ],
        },
        {
            "metric":
                "conditional_features",
            "value":
                audit[
                    "conditional_feature_count"
                ],
        },
        {
            "metric":
                "candidate_conditional_overlap",
            "value":
                len(
                    audit[
                        "candidate_conditional_overlap"
                    ]
                ),
        },
        {
            "metric":
                "prohibited_model_features",
            "value":
                len(
                    audit[
                        "prohibited_model_features"
                    ]
                ),
        },
        {
            "metric":
                "candidate_conditional_lineage_violations",
            "value":
                len(
                    audit[
                        "candidate_features_with_conditional_lineage"
                    ]
                ),
        },
    ]

    return pd.DataFrame(rows)


# ============================================================
# D6.R7 — FEATURE ENGINEERING CONTRACT REPORT
# ============================================================

def build_feature_engineering_contract_report(
    combined_df: pd.DataFrame,
    audit: dict[str, Any],
) -> str:
    """
    Build the formal D6 feature-engineering governance contract.
    """

    feature_lists = (
        get_governed_d6_feature_lists()
    )

    candidate_lines = "\n".join(
        f"- `{feature}`"
        for feature
        in feature_lists[
            "candidate_features"
        ]
    )

    conditional_lines = "\n".join(
        f"- `{feature}`"
        for feature
        in feature_lists[
            "conditional_features"
        ]
    )

    return f"""# D6 Feature Engineering Contract

## Project

Diabetes Readmission Clinical AI

## Lifecycle Stage

D6 — Governed Feature Engineering

## Prediction Point

Before discharge, at the point when model output would support
discharge-planning decisions.

## Outcome

`{TARGET_COLUMN}` — 30-day hospital readmission.

## Development Boundary

Only the frozen D5 `{TRAIN_LABEL}` and `{VALIDATION_LABEL}`
partitions are permitted during D6.

The `{TEST_LABEL}` partition remains locked.

Development encounters: **{len(combined_df):,}**

## Frozen D5 Dependency

Authoritative patient split SHA-256:

`{EXPECTED_D5_ASSIGNMENT_SHA256}`

D6 does not generate a new patient split.

## Feature Engineering Boundary

D6 performs deterministic feature construction only.

D6 does not:

- fit imputers;
- fit encoders;
- perform scaling;
- train models;
- tune hyperparameters;
- calibrate models;
- select decision thresholds;
- evaluate the locked test partition.

## Primary Candidate Features

The primary downstream modeling pathway is authorized to consume
only the following {len(feature_lists["candidate_features"])}
D6-CANDIDATE features:

{candidate_lines}

## Conditional Features

The following {len(feature_lists["conditional_features"])}
features are retained for governed analysis but are not authorized
for primary model entry unless their D4 prediction-time uncertainty
is formally resolved:

{conditional_lines}

## Leakage Controls

Identifiers are governance-only.

Outcome variables are target-only.

D4 hard-blocked retrospective encounter variables are prohibited
from model entry.

A D6-CANDIDATE feature cannot depend on a D4-CONDITIONAL source.

## Validation

Registered features: **{audit["registered_feature_count"]}**

Candidate features: **{audit["candidate_feature_count"]}**

Conditional features: **{audit["conditional_feature_count"]}**

Candidate/conditional overlap:
**{len(audit["candidate_conditional_overlap"])}**

Prohibited model features:
**{len(audit["prohibited_model_features"])}**

Candidate features with conditional lineage:
**{len(audit["candidate_features_with_conditional_lineage"])}**

D6 validation status:

**{audit["validation_status"]}**
"""


# ============================================================
# D6.R8 — GATE DECISION
# ============================================================

def build_d6_gate_decision(
    audit: dict[str, Any],
) -> str:
    """
    Produce the formal D6 lifecycle gate decision.
    """

    passed = (
        audit["validation_status"] == "PASS"
        and audit["registered_feature_count"] == 40
        and audit["candidate_feature_count"] == 10
        and audit["conditional_feature_count"] == 30
        and not audit[
            "candidate_conditional_overlap"
        ]
        and not audit[
            "prohibited_model_features"
        ]
        and not audit[
            "candidate_features_with_conditional_lineage"
        ]
    )

    decision = (
        "PASS"
        if passed
        else "FAIL"
    )

    return f"""# D6 Feature Engineering Gate Decision

## Decision

**{decision}**

## Gate

D6 — Governed Feature Engineering

## Decision Basis

The D6 feature-engineering implementation was evaluated against
the approved D4 feature-governance contract and frozen D5
patient-level partition assignment.

The evidence confirms:

- 40 governed features are registered;
- 10 features are authorized as D6-CANDIDATE;
- 30 features remain D6-CONDITIONAL;
- candidate and conditional feature sets are disjoint;
- no prohibited raw variables enter the model feature set;
- no identifier or outcome variable enters the model feature set;
- no candidate feature depends on a D4-CONDITIONAL source;
- development data contains train and validation only;
- the locked test partition remains protected;
- the primary modeling matrix contains only the 10 authorized
  D6-CANDIDATE features.

## Downstream Authorization

If the gate decision is PASS, the 10-feature primary candidate
matrix may proceed to:

**D7 — Governed Preprocessing Pipeline**

D7 may fit preprocessing transformations using training data only.

The 30 D6-CONDITIONAL features remain excluded from the primary
modeling pathway unless a separate governance decision explicitly
changes their disposition.

The locked test partition remains unavailable for preprocessing
design, fitting, model selection, calibration, or threshold
selection.

## Final D6 Status

**{decision}**
"""


# ============================================================
# D6.R9 — MANIFEST BUILDER
# ============================================================

def build_d6_manifest(
    combined_df: pd.DataFrame,
    audit: dict[str, Any],
    development_checksum: str,
) -> dict[str, Any]:
    """
    Build the machine-readable D6 evidence manifest.
    """

    feature_lists = (
        get_governed_d6_feature_lists()
    )

    return {
        "lifecycle_stage":
            "D6_GOVERNED_FEATURE_ENGINEERING",

        "generated_at_utc":
            datetime.now(
                timezone.utc
            ).isoformat(),

        "source_dependencies": {
            "d3_governed_cohort":
                "D3_governed_modeling_cohort.parquet",

            "d5_split_assignment":
                "D5_patient_split_assignment.csv",

            "d5_split_assignment_sha256":
                EXPECTED_D5_ASSIGNMENT_SHA256,
        },

        "development_population": {
            "encounters":
                int(len(combined_df)),

            "patients":
                int(
                    combined_df[
                        GROUP_COLUMN
                    ].nunique()
                ),

            "permitted_partitions": [
                TRAIN_LABEL,
                VALIDATION_LABEL,
            ],

            "locked_partition":
                TEST_LABEL,

            "locked_test_present":
                bool(
                    TEST_LABEL
                    in set(
                        combined_df[
                            "split"
                        ].unique()
                    )
                ),
        },

        "feature_governance": {
            "registered_feature_count":
                int(
                    audit[
                        "registered_feature_count"
                    ]
                ),

            "candidate_feature_count":
                int(
                    audit[
                        "candidate_feature_count"
                    ]
                ),

            "conditional_feature_count":
                int(
                    audit[
                        "conditional_feature_count"
                    ]
                ),

            "candidate_features":
                feature_lists[
                    "candidate_features"
                ],

            "conditional_features":
                feature_lists[
                    "conditional_features"
                ],

            "candidate_conditional_overlap":
                audit[
                    "candidate_conditional_overlap"
                ],

            "prohibited_model_features":
                audit[
                    "prohibited_model_features"
                ],

            "candidate_features_with_conditional_lineage":
                audit[
                    "candidate_features_with_conditional_lineage"
                ],
        },

        "development_feature_artifact": {
            "path":
                str(
                    DEVELOPMENT_FEATURE_PATH.relative_to(
                        PROJECT_ROOT
                    )
                ),

            "sha256":
                development_checksum,

            "rows":
                int(len(combined_df)),

            "columns":
                int(combined_df.shape[1]),
        },

        "validation_status":
            audit["validation_status"],

        "downstream_authorization":
            "D7_GOVERNED_PREPROCESSING",
    }


# ============================================================
# D6.R10 — GENERATE COMPLETE EVIDENCE PACKAGE
# ============================================================

def generate_d6_evidence_package() -> dict[str, Any]:
    """
    Generate and persist the complete D6 evidence package.

    Returns an execution summary suitable for terminal validation.
    """

    prepare_d6_evidence_directories()

    combined_df, audit = (
        build_combined_d6_development_features()
    )

    X, y, primary_audit = (
        build_primary_candidate_development_matrix()
    )

    if audit["validation_status"] != "PASS":
        raise RuntimeError(
            "D6 evidence generation stopped because combined "
            "feature validation did not pass."
        )

    if (
        primary_audit[
            "primary_matrix_validation_status"
        ]
        != "PASS"
    ):
        raise RuntimeError(
            "D6 evidence generation stopped because the primary "
            "candidate matrix did not pass validation."
        )

    # --------------------------------------------------------
    # Registry
    # --------------------------------------------------------

    registry = (
        build_feature_engineering_registry()
    )

    registry.to_csv(
        FEATURE_REGISTRY_PATH,
        index=False,
    )

    # --------------------------------------------------------
    # Lineage audit
    # --------------------------------------------------------

    lineage = (
        build_feature_lineage_audit()
    )

    lineage.to_csv(
        FEATURE_LINEAGE_PATH,
        index=False,
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    summary = (
        build_feature_engineering_summary(
            combined_df,
            audit,
        )
    )

    summary.to_csv(
        FEATURE_SUMMARY_PATH,
        index=False,
    )

    # --------------------------------------------------------
    # Development engineered artifact
    # --------------------------------------------------------

    combined_df.to_parquet(
        DEVELOPMENT_FEATURE_PATH,
        index=False,
    )

    development_checksum = (
        calculate_sha256(
            DEVELOPMENT_FEATURE_PATH
        )
    )

    # --------------------------------------------------------
    # Governance contract
    # --------------------------------------------------------

    contract_report = (
        build_feature_engineering_contract_report(
            combined_df,
            audit,
        )
    )

    CONTRACT_REPORT_PATH.write_text(
        contract_report,
        encoding="utf-8",
    )

    # --------------------------------------------------------
    # Gate decision
    # --------------------------------------------------------

    gate_decision = (
        build_d6_gate_decision(
            audit
        )
    )

    GATE_DECISION_PATH.write_text(
        gate_decision,
        encoding="utf-8",
    )

    # --------------------------------------------------------
    # Manifest
    # --------------------------------------------------------

    manifest = (
        build_d6_manifest(
            combined_df,
            audit,
            development_checksum,
        )
    )

    with MANIFEST_PATH.open(
        "w",
        encoding="utf-8",
    ) as file_handle:
        yaml.safe_dump(
            manifest,
            file_handle,
            sort_keys=False,
        )

    # --------------------------------------------------------
    # Execution summary
    # --------------------------------------------------------

    return {
        "validation_status":
            audit["validation_status"],

        "development_encounters":
            int(len(combined_df)),

        "development_patients":
            int(
                combined_df[
                    GROUP_COLUMN
                ].nunique()
            ),

        "combined_columns":
            int(combined_df.shape[1]),

        "registered_features":
            int(
                audit[
                    "registered_feature_count"
                ]
            ),

        "candidate_features":
            int(
                audit[
                    "candidate_feature_count"
                ]
            ),

        "conditional_features":
            int(
                audit[
                    "conditional_feature_count"
                ]
            ),

        "primary_X_shape":
            tuple(X.shape),

        "target_rows":
            int(len(y)),

        "development_artifact_sha256":
            development_checksum,

        "registry_path":
            str(FEATURE_REGISTRY_PATH),

        "lineage_path":
            str(FEATURE_LINEAGE_PATH),

        "summary_path":
            str(FEATURE_SUMMARY_PATH),

        "contract_path":
            str(CONTRACT_REPORT_PATH),

        "gate_decision_path":
            str(GATE_DECISION_PATH),

        "manifest_path":
            str(MANIFEST_PATH),

        "development_artifact_path":
            str(DEVELOPMENT_FEATURE_PATH),
    }